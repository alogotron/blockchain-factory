// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title ShutterZkTLSGateway
 * @author alogotron
 * @notice Front-run-proof, identity-gated transaction gateway combining:
 *         - Shutter Network threshold encryption (prevents front-running)
 *         - zkTLS identity claims (gates execution on verified offchain data)
 *
 * Flow:
 *   1. Submitter encrypts a zkTLS claim payload via Shutter API
 *   2. Calls `submitCommitment` with the encrypted bytes + claim hash + identity
 *   3. After `decryptionTimestamp` passes, Shutter Keypers release the decryption key
 *   4. Anyone calls `reveal` with the plaintext — contract verifies hash matches
 *   5. Emits `ClaimRevealed` — downstream verifiers can process the zkTLS claim
 *
 * The plaintext is a zkTLS attestation: ABI-encoded (claimType, claimData, signer)
 * This contract is agnostic to claim type — verification is delegated to IClaimVerifier.
 */
contract ShutterZkTLSGateway {

    // ==================== Types ====================

    enum CommitmentState { Empty, Pending, Revealed, Expired }

    struct Commitment {
        address submitter;          // Who submitted the encrypted commitment
        bytes32 claimHash;          // keccak256(plaintext) — commitment to the claim
        bytes   encryptedPayload;   // Shutter-encrypted ciphertext (stored for reference)
        bytes32 shutterIdentity;    // Shutter identity hash used for encryption
        uint64  decryptionTimestamp;// Unix timestamp after which Keypers release key
        uint64  submittedAt;        // Block timestamp of submission
        CommitmentState state;
        bytes   plaintext;          // Filled after reveal
    }

    // ==================== State ====================

    mapping(bytes32 => Commitment) public commitments;  // commitmentId => Commitment
    mapping(address => bytes32[]) public submitterCommitments;

    uint256 public totalCommitments;
    uint256 public totalRevealed;

    /// @notice Optional claim verifier — if set, reveal calls verifier.verify(plaintext)
    IClaimVerifier public claimVerifier;
    address public owner;

    // ==================== Events ====================

    event CommitmentSubmitted(
        bytes32 indexed commitmentId,
        address indexed submitter,
        bytes32 indexed shutterIdentity,
        bytes32 claimHash,
        uint64  decryptionTimestamp
    );

    event ClaimRevealed(
        bytes32 indexed commitmentId,
        address indexed revealer,
        bytes32 indexed shutterIdentity,
        bytes   plaintext
    );

    event ClaimVerified(
        bytes32 indexed commitmentId,
        bool    verified,
        bytes   verificationResult
    );

    event CommitmentExpired(bytes32 indexed commitmentId);

    // ==================== Errors ====================

    error CommitmentNotFound();
    error CommitmentAlreadyRevealed();
    error CommitmentNotPending();
    error DecryptionTimestampNotReached(uint64 timestamp, uint64 current);
    error ClaimHashMismatch(bytes32 expected, bytes32 actual);
    error EmptyPayload();
    error InvalidTimestamp();
    error Unauthorized();

    // ==================== Constructor ====================

    constructor(address _claimVerifier) {
        owner = msg.sender;
        if (_claimVerifier != address(0)) {
            claimVerifier = IClaimVerifier(_claimVerifier);
        }
    }

    // ==================== Core Functions ====================

    /**
     * @notice Submit a Shutter-encrypted zkTLS commitment.
     * @param shutterIdentity    The Shutter identity hash (32 bytes, from API response)
     * @param encryptedPayload   The Shutter-encrypted ciphertext (from shutter_crypto.py)
     * @param claimHash          keccak256 of the plaintext — commit to claim without revealing
     * @param decryptionTimestamp Unix timestamp after which decryption key is available
     * @return commitmentId      Unique ID for this commitment
     */
    function submitCommitment(
        bytes32 shutterIdentity,
        bytes calldata encryptedPayload,
        bytes32 claimHash,
        uint64 decryptionTimestamp
    ) external returns (bytes32 commitmentId) {
        if (encryptedPayload.length == 0) revert EmptyPayload();
        if (decryptionTimestamp <= block.timestamp) revert InvalidTimestamp();

        commitmentId = keccak256(abi.encodePacked(
            shutterIdentity,
            claimHash,
            msg.sender,
            block.timestamp
        ));

        commitments[commitmentId] = Commitment({
            submitter:           msg.sender,
            claimHash:           claimHash,
            encryptedPayload:    encryptedPayload,
            shutterIdentity:     shutterIdentity,
            decryptionTimestamp: decryptionTimestamp,
            submittedAt:         uint64(block.timestamp),
            state:               CommitmentState.Pending,
            plaintext:           new bytes(0)
        });

        submitterCommitments[msg.sender].push(commitmentId);
        totalCommitments++;

        emit CommitmentSubmitted(
            commitmentId,
            msg.sender,
            shutterIdentity,
            claimHash,
            decryptionTimestamp
        );
    }

    /**
     * @notice Reveal the plaintext after Shutter decryption.
     *         Anyone can call this — the claim hash proves authenticity.
     * @param commitmentId   The commitment to reveal
     * @param plaintext      The decrypted plaintext (must match claimHash)
     */
    function reveal(
        bytes32 commitmentId,
        bytes calldata plaintext
    ) external {
        Commitment storage c = commitments[commitmentId];
        if (c.submitter == address(0)) revert CommitmentNotFound();
        if (c.state != CommitmentState.Pending) revert CommitmentNotPending();
        if (block.timestamp < c.decryptionTimestamp) {
            revert DecryptionTimestampNotReached(c.decryptionTimestamp, uint64(block.timestamp));
        }

        bytes32 actualHash = keccak256(plaintext);
        if (actualHash != c.claimHash) {
            revert ClaimHashMismatch(c.claimHash, actualHash);
        }

        c.state = CommitmentState.Revealed;
        c.plaintext = plaintext;
        totalRevealed++;

        emit ClaimRevealed(commitmentId, msg.sender, c.shutterIdentity, plaintext);

        // Optional: call external claim verifier
        if (address(claimVerifier) != address(0)) {
            try claimVerifier.verify(commitmentId, plaintext) returns (bool ok, bytes memory result) {
                emit ClaimVerified(commitmentId, ok, result);
            } catch {
                // Verifier failure doesn't block reveal
            }
        }
    }

    /**
     * @notice Mark an expired commitment (past grace period without reveal).
     * @param commitmentId   The commitment to expire
     */
    function expireCommitment(bytes32 commitmentId) external {
        Commitment storage c = commitments[commitmentId];
        if (c.submitter == address(0)) revert CommitmentNotFound();
        if (c.state != CommitmentState.Pending) revert CommitmentNotPending();
        // Grace period: decryptionTimestamp + 7 days
        require(block.timestamp > c.decryptionTimestamp + 7 days, "Grace period not elapsed");
        c.state = CommitmentState.Expired;
        emit CommitmentExpired(commitmentId);
    }

    // ==================== View Functions ====================

    function getCommitment(bytes32 commitmentId) external view returns (Commitment memory) {
        return commitments[commitmentId];
    }

    function getSubmitterCommitments(address submitter) external view returns (bytes32[] memory) {
        return submitterCommitments[submitter];
    }

    function isRevealable(bytes32 commitmentId) external view returns (bool) {
        Commitment storage c = commitments[commitmentId];
        return c.state == CommitmentState.Pending &&
               block.timestamp >= c.decryptionTimestamp;
    }

    // ==================== Admin ====================

    function setClaimVerifier(address _verifier) external {
        if (msg.sender != owner) revert Unauthorized();
        claimVerifier = IClaimVerifier(_verifier);
    }

    function transferOwnership(address newOwner) external {
        if (msg.sender != owner) revert Unauthorized();
        owner = newOwner;
    }
}

/**
 * @title IClaimVerifier
 * @notice Interface for protocol-specific zkTLS claim verifiers.
 *         Implement this to add Aztec/Primus zkTLS proof verification.
 */
interface IClaimVerifier {
    function verify(
        bytes32 commitmentId,
        bytes calldata plaintext
    ) external returns (bool ok, bytes memory result);
}

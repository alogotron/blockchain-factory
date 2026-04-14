// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "forge-std/Test.sol";
import "../src/ShutterZkTLSGateway.sol";

contract ShutterZkTLSGatewayTest is Test {

    ShutterZkTLSGateway public gateway;

    address alice = address(0xA11ce);
    address bob   = address(0xB0b);

    bytes32 constant IDENTITY = bytes32(uint256(0xdeadbeef));
    bytes   constant PLAINTEXT = abi.encode("github:alogotron", uint256(42));
    bytes32 constant CLAIM_HASH = keccak256(abi.encode("github:alogotron", uint256(42)));
    bytes   constant ENCRYPTED = hex"03" // version byte + fake 192 bytes
        hex"0000000000000000000000000000000000000000000000000000000000000000"
        hex"0000000000000000000000000000000000000000000000000000000000000000"
        hex"0000000000000000000000000000000000000000000000000000000000000000"
        hex"0000000000000000000000000000000000000000000000000000000000000000"
        hex"0000000000000000000000000000000000000000000000000000000000000000"
        hex"0000000000000000000000000000000000000000000000000000000000000000";

    function setUp() public {
        gateway = new ShutterZkTLSGateway(address(0));
    }

    // ==================== submitCommitment ====================

    function test_SubmitCommitment_Success() public {
        uint64 decTs = uint64(block.timestamp + 100);

        vm.prank(alice);
        bytes32 id = gateway.submitCommitment(IDENTITY, ENCRYPTED, CLAIM_HASH, decTs);

        assertNotEq(id, bytes32(0));
        assertEq(gateway.totalCommitments(), 1);

        ShutterZkTLSGateway.Commitment memory c = gateway.getCommitment(id);
        assertEq(c.submitter, alice);
        assertEq(c.claimHash, CLAIM_HASH);
        assertEq(c.shutterIdentity, IDENTITY);
        assertEq(c.decryptionTimestamp, decTs);
        assertEq(uint8(c.state), uint8(ShutterZkTLSGateway.CommitmentState.Pending));
    }

    function test_SubmitCommitment_EmitsEvent() public {
        uint64 decTs = uint64(block.timestamp + 100);

        vm.prank(alice);
        vm.expectEmit(false, true, true, true);
        emit ShutterZkTLSGateway.CommitmentSubmitted(
            bytes32(0), // commitmentId — we don't know it yet
            alice,
            IDENTITY,
            CLAIM_HASH,
            decTs
        );
        gateway.submitCommitment(IDENTITY, ENCRYPTED, CLAIM_HASH, decTs);
    }

    function test_SubmitCommitment_RevertEmptyPayload() public {
        uint64 decTs = uint64(block.timestamp + 100);
        vm.prank(alice);
        vm.expectRevert(ShutterZkTLSGateway.EmptyPayload.selector);
        gateway.submitCommitment(IDENTITY, new bytes(0), CLAIM_HASH, decTs);
    }

    function test_SubmitCommitment_RevertPastTimestamp() public {
        vm.prank(alice);
        vm.expectRevert(ShutterZkTLSGateway.InvalidTimestamp.selector);
        gateway.submitCommitment(IDENTITY, ENCRYPTED, CLAIM_HASH, uint64(block.timestamp));
    }

    // ==================== reveal ====================

    function _submitAndAdvance() internal returns (bytes32 id, uint64 decTs) {
        decTs = uint64(block.timestamp + 100);
        vm.prank(alice);
        id = gateway.submitCommitment(IDENTITY, ENCRYPTED, CLAIM_HASH, decTs);
        vm.warp(decTs + 1);
    }

    function test_Reveal_Success() public {
        (bytes32 id,) = _submitAndAdvance();

        vm.prank(bob);
        gateway.reveal(id, PLAINTEXT);

        ShutterZkTLSGateway.Commitment memory c = gateway.getCommitment(id);
        assertEq(uint8(c.state), uint8(ShutterZkTLSGateway.CommitmentState.Revealed));
        assertEq(c.plaintext, PLAINTEXT);
        assertEq(gateway.totalRevealed(), 1);
    }

    function test_Reveal_EmitsEvent() public {
        (bytes32 id,) = _submitAndAdvance();

        vm.prank(bob);
        vm.expectEmit(true, true, true, true);
        emit ShutterZkTLSGateway.ClaimRevealed(id, bob, IDENTITY, PLAINTEXT);
        gateway.reveal(id, PLAINTEXT);
    }

    function test_Reveal_RevertNotFound() public {
        vm.expectRevert(ShutterZkTLSGateway.CommitmentNotFound.selector);
        gateway.reveal(bytes32(0), PLAINTEXT);
    }

    function test_Reveal_RevertTooEarly() public {
        uint64 decTs = uint64(block.timestamp + 100);
        vm.prank(alice);
        bytes32 id = gateway.submitCommitment(IDENTITY, ENCRYPTED, CLAIM_HASH, decTs);

        vm.expectRevert(
            abi.encodeWithSelector(
                ShutterZkTLSGateway.DecryptionTimestampNotReached.selector,
                decTs,
                uint64(block.timestamp)
            )
        );
        gateway.reveal(id, PLAINTEXT);
    }

    function test_Reveal_RevertHashMismatch() public {
        (bytes32 id,) = _submitAndAdvance();
        bytes memory wrongPlaintext = abi.encode("wrong");

        vm.expectRevert(
            abi.encodeWithSelector(
                ShutterZkTLSGateway.ClaimHashMismatch.selector,
                CLAIM_HASH,
                keccak256(wrongPlaintext)
            )
        );
        gateway.reveal(id, wrongPlaintext);
    }

    function test_Reveal_RevertDoubleReveal() public {
        (bytes32 id,) = _submitAndAdvance();
        gateway.reveal(id, PLAINTEXT);

        vm.expectRevert(ShutterZkTLSGateway.CommitmentNotPending.selector);
        gateway.reveal(id, PLAINTEXT);
    }

    // ==================== isRevealable ====================

    function test_IsRevealable_BeforeTimestamp() public {
        uint64 decTs = uint64(block.timestamp + 100);
        vm.prank(alice);
        bytes32 id = gateway.submitCommitment(IDENTITY, ENCRYPTED, CLAIM_HASH, decTs);
        assertFalse(gateway.isRevealable(id));
    }

    function test_IsRevealable_AfterTimestamp() public {
        (bytes32 id, uint64 decTs) = _submitAndAdvance();
        assertTrue(gateway.isRevealable(id));
    }

    function test_IsRevealable_AfterReveal() public {
        (bytes32 id,) = _submitAndAdvance();
        gateway.reveal(id, PLAINTEXT);
        assertFalse(gateway.isRevealable(id));
    }

    // ==================== getSubmitterCommitments ====================

    function test_GetSubmitterCommitments() public {
        uint64 decTs = uint64(block.timestamp + 100);
        vm.startPrank(alice);
        bytes32 id1 = gateway.submitCommitment(IDENTITY, ENCRYPTED, CLAIM_HASH, decTs);
        bytes32 id2 = gateway.submitCommitment(IDENTITY, ENCRYPTED, CLAIM_HASH, decTs + 1);
        vm.stopPrank();

        bytes32[] memory ids = gateway.getSubmitterCommitments(alice);
        assertEq(ids.length, 2);
        assertEq(ids[0], id1);
        assertEq(ids[1], id2);
    }

    // ==================== owner functions ====================

    function test_SetClaimVerifier_OnlyOwner() public {
        vm.prank(alice);
        vm.expectRevert(ShutterZkTLSGateway.Unauthorized.selector);
        gateway.setClaimVerifier(address(0x1));
    }

    function test_TransferOwnership() public {
        gateway.transferOwnership(alice);
        assertEq(gateway.owner(), alice);
    }

    // ==================== expireCommitment ====================

    function test_ExpireCommitment() public {
        uint64 decTs = uint64(block.timestamp + 100);
        vm.prank(alice);
        bytes32 id = gateway.submitCommitment(IDENTITY, ENCRYPTED, CLAIM_HASH, decTs);

        vm.warp(decTs + 7 days + 1);
        gateway.expireCommitment(id);

        ShutterZkTLSGateway.Commitment memory c = gateway.getCommitment(id);
        assertEq(uint8(c.state), uint8(ShutterZkTLSGateway.CommitmentState.Expired));
    }
}

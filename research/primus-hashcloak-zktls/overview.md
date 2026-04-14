# Primus Labs + HashCloak — zkTLS Verifier Toolkit on Aztec

**Research Date:** 2026-04-09  
**Status:** Active development, public repo, RC-grade maturity  
**Primary Repo:** https://github.com/primus-labs/zktls-verification-noir  
**Tutorial:** https://hashcloak.com/blog/primus-noir-zktls-tutorial  

---

## 1. Who Built It

### HashCloak
- **Description:** "A blockchain R&D lab focused on privacy and scalability"
- **GitHub:** https://github.com/hashcloak
- **Focus:** ZK tooling, privacy infrastructure, Aztec ecosystem
- **Notable repos:**
  - `flashbots-privacy` — 48 stars, privacy for Flashbots MEV
  - `aztec-semaphore` — Semaphore in Noir (Aztec)
  - `humanvoting` — private voting via Aztec Semaphore + zkPassport (updated Nov 23, 2025)
  - `noir_json_parser` — forked from noir-lang, adapted for vectors; v0.4.1-hc.5 (Feb 27, 2026)
- **Primary contributor on this project:** `@ewynx` (GitHub user ID: 22170967)
- **Organization:** No public members listed

### Primus Labs
- **Description:** "Data Verification and Computation with zkTLS and zkFHE"
- **GitHub:** https://github.com/primus-labs
- **Formerly:** PADO Labs
- **Core product:** Cryptographic infrastructure using MPC + FHE + ZKP to validate, encrypt, and process web data for data-driven dApps
- **Public members:** `@xiafubiao`, `@xiangxiecrypto`
- **Other repos:** `emp-rust` (24 stars, MPC toolkit), `primus-fhe`, `zktls-contracts` (EVM verifier)
- **Twitter:** @primus_labs

---

## 2. What is zkTLS

zkTLS enables cryptographically verified proofs about web2 data — proving that a piece of data came from a specific HTTPS endpoint without revealing private details.

### How it works (Primus DVC mode)

1. **TLS interception:** The Primus attestor acts as intermediary between client and target web server (proxy mode) or co-computes the TLS session (MPC mode)
2. **Data extraction:** JSON path selectors (`parsePath`) extract specific fields from the response
3. **Attestation generation:** The attestor signs the extracted data with a secp256k1 key, producing an attestation JSON with:
   - `publicKeyX/Y` — attestor's secp256k1 public key
   - `hash` — overall attestation hash
   - `signature` — secp256k1 signature over the hash
   - Per commitment/hash: either Pedersen commitments (Grumpkin curve) or SHA-256 hashes of plaintext
   - `requestUrls` — the actual URLs queried
   - `id` — unique attestation identifier
4. **On-chain verification:** The Noir circuit verifies the secp256k1 sig, URL allowlist matching, and data integrity

### Two Algorithm Modes

| Mode | Trust Model | Performance | Use Case |
|------|------------|-------------|----------|
| `proxytls` | Trust attestor as sole intermediary | Fast | Higher performance, simpler setup |
| `mpctls` | Attestor + client collaboratively compute | Slower | Stronger trust guarantees |

### Two Attestation Types

| Type | Mechanism | Noir Primitive | Use Case |
|------|-----------|----------------|----------|
| Hash-based | `SHA256(plaintext) == stored_hash` | `sha256_var` | Simple integrity proofs, cheaper |
| Commitment-based | Pedersen MSM on Grumpkin: `Σ(msg*G + rnd*H) == Σcom` | `multi_scalar_mul` | Hide-and-reveal, ZK computations on private data |

---

## 3. Repository Structure

```
primus-labs/zktls-verification-noir/
├── att_verifier_lib/          ← Noir library (core ZK logic)
│   ├── src/lib.nr             ← all verification functions
│   └── Nargo.toml             ← deps: poseidon v0.2.6, sha256 v0.2.1
├── att_verifier_parsing/      ← TypeScript JSON→circuit input parser
├── aztec-attestation-sdk/     ← TS SDK: Client, ContractHelpers, parseHashingData
├── contract_template/         ← Aztec Noir smart contract template
│   └── src/main.nr            ← full contract with storage, events, verify fns
└── example/
    ├── github_example/        ← Verify GitHub contributor status
    ├── okx_example/           ← Verify OKX trading pair liveness
    └── js_test/               ← E2E test scripts (TypeScript)
```

**Version:** Aztec `4.2.0-aztecnr-rc.2`  
**Language breakdown:** TypeScript 70.5%, Noir 29.5%  
**Commits:** 73 total on main  
**Stars:** 9 | **Forks:** 5 | **Issues:** 0 open  
**Last commit:** March 31, 2026  

---

## 4. Technical Deep Dive

### att_verifier_lib — Noir Library

**Dependencies:**
- `poseidon` v0.2.6 (github.com/noir-lang/poseidon)
- `sha256` v0.2.1 (github.com/noir-lang/sha256)
- `std::ecdsa_secp256k1` (Noir stdlib)
- `std::embedded_curve_ops` (Noir stdlib — Grumpkin)

**Public API:**

```noir
// Hash-based attestation verification
fn verify_attestation_hashing<
  let MAX_URL_LEN: u32,
  let N: u32,
  let MAX_CONTENT_LEN: u32
>(
  public_key_x: [u8; 32],
  public_key_y: [u8; 32],
  hash: [u8; 32],
  signature: [u8; 64],
  request_urls: [BoundedVec<u8, MAX_URL_LEN>; 2],
  allowed_urls: [BoundedVec<u8, MAX_URL_LEN>; 3],
  data_hashes: [[u8; 32]; N],
  contents: [BoundedVec<u8, MAX_CONTENT_LEN>; N]
) -> [Field; 2]

// Commitment-based attestation verification
fn verify_attestation_comm<
  let MAX_URL_LEN: u32,
  let NUM_REQUEST_URLS: u32,
  let NUM_ALLOWED_URLS: u32,
  let MAX_COMMS: u32,
  let NUM_RESPONSE_RESOLVE: u32
>(
  public_key_x: [u8; 32],
  public_key_y: [u8; 32],
  hash: [u8; 32],
  signature: [u8; 64],
  request_urls: [BoundedVec<u8, MAX_URL_LEN>; NUM_REQUEST_URLS],
  allowed_urls: [BoundedVec<u8, MAX_URL_LEN>; NUM_ALLOWED_URLS],
  coms_per_group: [BoundedVec<EmbeddedCurvePoint, MAX_COMMS>; NUM_RESPONSE_RESOLVE],
  rnds_per_group: [BoundedVec<Field, MAX_COMMS>; NUM_RESPONSE_RESOLVE],
  msgs_chunks_per_group: [BoundedVec<Field, MAX_COMMS>; NUM_RESPONSE_RESOLVE],
  H: EmbeddedCurvePoint
) -> [Field; NUM_REQUEST_URLS]
```

**Internal helpers:**
- `verify_sig_and_urls` — secp256k1 signature check + Poseidon2 hash of matched allowed URL
- `verify_commitment_group` — batched MSM Pedersen commitment check (cross-group swap attack prevention)
- `starts_with` — unconstrained BoundedVec prefix check
- `get_allowed_url_index` — unconstrained URL lookup

### contract_template — Aztec Smart Contract

**Storage:**
```noir
struct Storage<Context> {
  admin: PublicMutable<AztecAddress, Context>,
  allowed_url_hashes: PublicMutable<[Field; NUM_ALLOWED_URLS], Context>,
  H: PublicImmutable<EmbeddedCurvePoint>  // only for commitment-based
}
```

**Event:**
```noir
struct SuccessEvent {
  sender: AztecAddress,
  contract_address: AztecAddress,
  id: Field
}
```

**Public functions:** `constructor`, `update_allowed_url_hashes`, `set_admin`, `check_values_emit_event`, `check_urls_emit_event`  
**Private functions:** `verify_comm`, `verify_hash`  

**Verification flow:**  
1. Private function (`verify_hash` / `verify_comm`) runs ZK proof generation client-side  
2. Enqueues public call (`check_urls_emit_event` / `check_values_emit_event`)  
3. Public function validates URL hashes against storage, emits `SuccessEvent`  
4. Full verification confirmed when event is present in tx receipt  

### aztec-attestation-sdk — TypeScript SDK

```typescript
// Core client
const client = new Client({ nodeUrl: "http://localhost:8080" });
await client.initialize();
const account = await client.getAccount(0);

// Attestation (requires Primus DVC client)
const result = await client.doZKTLS(requests, responseResolves, {
  verifyVersion: '2',
  algorithmType: 'proxytls' | 'mpctls',
  runZkvm: boolean,
  noProxy: boolean,
});

// Parse attestation for circuit input
const parsed = parseHashingData(rawData, {
  maxResponseNum: number,
  allowedUrls: string[]
});
// Returns: { publicKeyX, publicKeyY, hash, signature, requestUrls,
//            allowedUrls, dataHashes, plainJsonResponses, id }

// Deploy verifier contract
const contract = await ContractHelpers.deployContract(ContractClass, client, {
  admin: AztecAddress,
  allowedUrls: string[],
  maxUrlLen: number,
  pointH: EmbeddedCurvePoint,  // commitment-based only
  from: AztecAddress,
  timeout: number,
});

// Query success events
const { events } = await getPublicEvents<SuccessEvent>(
  client.getNode(),
  Contract.events.SuccessEvent,
  { txHash, contractAddress }
);
```

### att_verifier_parsing — TypeScript Parsing Library

Converts raw Primus attestation JSON into the typed arrays expected by Noir circuits:
- Encodes URLs as `BoundedVec<u8, MAX_URL_LEN>`
- Extracts commitment groups or SHA256 hashes
- Handles padding and length alignment for fixed-size Noir arrays

---

## 5. Circuit Benchmarks

| Contract Method | Circuit Size (constraints) |
|----------------|---------------------------|
| GithubVerifier:verify_comm | 279,273 |
| GithubVerifier:verify_hash | 292,262 |
| OKXVerifier:verify_comm | 268,450 |
| OKXVerifier:verify_hash | 275,878 |

Note: ~270K-292K constraints is substantial — proof generation will take several seconds on consumer hardware without CHONK optimization.

---

## 6. Current State & Maturity

| Dimension | Status |
|-----------|--------|
| Repo visibility | Public |
| Aztec version | 4.2.0-aztecnr-rc.2 (RC, not stable) |
| Mainnet deployment | Not yet — local network only |
| Audit | None documented |
| npm packages | Not published to npm |
| Test coverage | E2E tests for github + OKX examples |
| Documentation | README + HashCloak tutorial |
| Contributors | 1 active (@ewynx) |
| Activity | Very active — 5 commits March 27-31, 2026 |
| Open issues | 0 |
| Supported APIs | GitHub API, OKX trading API |

---

## 7. Integration How-To (15-minute path)

**Prerequisites:**
- Aztec toolchain (`aztec` CLI, Aztec sandbox)
- Node.js + yarn
- Base Sepolia wallet with ETH (for DVC attestation)
- Primus DVC client from https://github.com/primus-labs/DVC-Demo

**Step 1: Generate attestation**
```typescript
// Configure which data to extract
const responseResolves = [[
  { keyName: 'field', parseType: 'json', parsePath: '$.path', op: 'SHA256_EX' },
]];
await client.doZKTLS(requests, responseResolves, { algorithmType: 'proxytls', ... });
```

**Step 2: Write verifier contract**
```noir
// Copy contract_template, add business logic
assert(contents[0].storage() == expected_value.storage());
```

**Step 3: Compile + deploy + verify**
```bash
aztec compile && aztec codegen -o ../bindings target
```
```typescript
const parsed = parseHashingData(attestationJson, { allowedUrls });
await contract.methods.verify_hash(...parsed).send();
```

---

## 8. Related Resources

- Primus DVC docs: https://docs.primuslabs.xyz/build/dvc
- Primus EVM contracts: https://github.com/primus-labs/zktls-contracts
- Primus Python SDK: https://pypi.org/project/zktls-py-sdk/
- HashCloak noir_json_parser: https://github.com/hashcloak/noir_json_parser (v0.4.1-hc.5, supports vectors)
- HashCloak aztec-semaphore: https://github.com/hashcloak/aztec-semaphore
- Aztec docs: https://docs.aztec.network/developers/getting_started_on_local_network

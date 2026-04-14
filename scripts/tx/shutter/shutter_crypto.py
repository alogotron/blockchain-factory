#!/usr/bin/env python3
"""
Shutter Network Encryption/Decryption — Pure Python Implementation
Using py_ecc optimized_bls12_381 for BLS12-381 operations.

Algorithm from: https://github.com/shutter-network/ShutterAPIHongbao/blob/main/encryptDataBlst.js

Encrypt:
  r = hash3(sigma || msg)
  c1 = G2 * r                        (96 bytes compressed)
  key = hash2(e(eonKey_G2, id_G1^r))  (32 bytes)
  c2 = sigma XOR key                  (32 bytes)
  c3 = PKCS7_blocks(msg) XOR block_keys(sigma)
  output = 0x03 || c1 || c2 || c3

Decrypt:
  key = hash2(e(c1_G2, dk_G1))
  sigma = c2 XOR key
  msg = unpad(c3_blocks XOR block_keys(sigma))
"""

import hashlib
import os
import struct
from typing import List

from py_ecc.optimized_bls12_381 import (
    G1, G2, multiply as bls_mul, pairing, FQ, FQ2
)
from py_ecc.bls.point_compression import compress_G2, decompress_G2, compress_G1, decompress_G1
from py_ecc.bls.g2_primitives import G1_to_pubkey
from py_ecc.bls.hash_to_curve import hash_to_G1
from eth_hash.auto import keccak

# BLS12-381 subgroup order
BLS_ORDER = 0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001

# Shutter DST for G1 hash-to-curve
SHUTTER_DST = b'SHUTTER_V01_BLS12381G1_XMD:SHA-256_SSWU_RO_'

# ==================== Serialization ====================

def g2_to_bytes(point) -> bytes:
    """Compress projective G2 point to 96 bytes."""
    z1, z2 = compress_G2(point)
    return z1.to_bytes(48, 'big') + z2.to_bytes(48, 'big')

def g2_from_bytes(data: bytes):
    """Decompress 96 bytes to projective G2 point."""
    z1 = int.from_bytes(data[:48], 'big')
    z2 = int.from_bytes(data[48:], 'big')
    return decompress_G2((z1, z2))  # returns projective 3-tuple

def g1_to_bytes(point) -> bytes:
    """Compress projective G1 point to 48 bytes."""
    return G1_to_pubkey(point)

def g1_from_bytes(data: bytes):
    """Decompress 48 bytes to projective G1 point."""
    z_int = int.from_bytes(data, 'big')
    affine = decompress_G1(z_int)  # returns (x, y) affine
    return (affine[0], affine[1], FQ(1))  # make projective

def fp12_to_bytes(gt) -> bytes:
    """Serialize FQ12 to 576 bytes (12 * 48, big-endian)."""
    return b''.join(int(c).to_bytes(48, 'big') for c in gt.coeffs)

# ==================== Hash functions ====================

def hash2(gt) -> bytes:
    """hash2: keccak256(0x02 || fp12_bytes)"""
    return keccak(bytes([0x02]) + fp12_to_bytes(gt))

def hash3(sigma_bytes: bytes, msg_bytes: bytes) -> int:
    """hash3: keccak256(0x03 || sigma || msg) mod BLS_ORDER"""
    h = keccak(bytes([0x03]) + sigma_bytes + msg_bytes)
    return int.from_bytes(h, 'big') % BLS_ORDER

def hash4(data: bytes) -> bytes:
    """hash4: keccak256(0x04 || data)"""
    return keccak(bytes([0x04]) + data)

# ==================== Block helpers ====================

def xor_blocks(a: bytes, b: bytes) -> bytes:
    assert len(a) == len(b), f'xor_blocks mismatch: {len(a)} vs {len(b)}'
    return bytes(x ^ y for x, y in zip(a, b))

def pad_and_split(data: bytes) -> List[bytes]:
    """PKCS7 pad to 32-byte boundary, split into 32-byte blocks."""
    pad_len = 32 - (len(data) % 32)
    padded = data + bytes([pad_len] * pad_len)
    return [padded[i:i+32] for i in range(0, len(padded), 32)]

def unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    if pad_len == 0 or pad_len > 32:
        raise ValueError(f'Invalid padding: {pad_len}')
    return data[:-pad_len]

def compute_block_keys(sigma: bytes, n: int) -> List[bytes]:
    keys = []
    for i in range(n):
        raw = struct.pack('>I', i).lstrip(b'\x00') or b'\x00'
        keys.append(hash4(sigma + raw))
    return keys

# ==================== G1 identity ====================

def compute_identity_g1(identity_prefix_bytes: bytes):
    """Hash-to-G1 with Shutter DST: H(0x01 || identity_prefix)"""
    preimage = bytes([0x01]) + identity_prefix_bytes
    return hash_to_G1(preimage, SHUTTER_DST, hashlib.sha256)

# ==================== Encrypt ====================

def encrypt_shutter(
    msg_bytes: bytes,
    eon_key_bytes: bytes,
    identity_prefix_bytes: bytes,
    sigma_bytes: bytes = None
) -> bytes:
    """
    Encrypt msg_bytes using Shutter threshold encryption.
    Returns raw ciphertext bytes: 0x03 || c1(96) || c2(32) || c3(N*32)
    """
    if sigma_bytes is None:
        sigma_bytes = os.urandom(32)

    # r = hash3(sigma || msg)
    r = hash3(sigma_bytes, msg_bytes)

    # c1 = G2 * r
    c1_point = bls_mul(G2, r)
    c1_bytes = g2_to_bytes(c1_point)

    # eonKey_G2 = decompress eon key
    eon_key_g2 = g2_from_bytes(eon_key_bytes)

    # identity_G1 = hash-to-G1(identity_prefix)
    id_g1 = compute_identity_g1(identity_prefix_bytes)

    # key = hash2(e(eon_key_G2, id_G1 * r))
    id_r = bls_mul(id_g1, r)
    gt = pairing(eon_key_g2, id_r)
    key = hash2(gt)

    # c2 = sigma XOR key
    c2_bytes = xor_blocks(sigma_bytes, key)

    # c3 = msg blocks XOR block_keys
    blocks = pad_and_split(msg_bytes)
    bkeys = compute_block_keys(sigma_bytes, len(blocks))
    c3_bytes = b''.join(xor_blocks(k, b) for k, b in zip(bkeys, blocks))

    return bytes([0x03]) + c1_bytes + c2_bytes + c3_bytes

# ==================== Decrypt ====================

def decrypt_shutter(ciphertext: bytes, decryption_key_bytes: bytes) -> bytes:
    """
    Decrypt Shutter ciphertext.
    decryption_key_bytes: 48-byte compressed G1 epoch secret key.
    Returns plaintext bytes.
    """
    if ciphertext[0] != 0x03:
        raise ValueError(f'Invalid version: {ciphertext[0]}')

    c1_bytes = ciphertext[1:97]
    c2_bytes = ciphertext[97:129]
    c3_bytes = ciphertext[129:]

    c1_g2 = g2_from_bytes(c1_bytes)
    dk_g1 = g1_from_bytes(decryption_key_bytes)

    # key = hash2(e(c1_G2, dk_G1))
    gt = pairing(c1_g2, dk_g1)
    key = hash2(gt)

    sigma = xor_blocks(c2_bytes, key)

    n_blocks = len(c3_bytes) // 32
    bkeys = compute_block_keys(sigma, n_blocks)
    decrypted = bytearray()
    for i in range(n_blocks):
        decrypted.extend(xor_blocks(c3_bytes[i*32:(i+1)*32], bkeys[i]))

    return unpad(bytes(decrypted))

# ==================== Self-test ====================

def self_test():
    """Verify encrypt/decrypt roundtrip without API."""
    print('[self_test] Running local roundtrip...')
    import time

    # Simulate: master_key=42 (eon private key), identity_prefix=random
    master = 42
    identity_prefix = os.urandom(32)

    # Public eon key = G2 * master
    eon_key_g2_proj = bls_mul(G2, master)
    eon_key_bytes = g2_to_bytes(eon_key_g2_proj)

    # Decryption key = identity_G1 * master  (this is what Keypers produce)
    id_g1 = compute_identity_g1(identity_prefix)
    dk_g1 = bls_mul(id_g1, master)
    dk_bytes = g1_to_bytes(dk_g1)

    msg = b'shutter-spike: identity-gated front-run-proof tx by alogotron'
    sigma = os.urandom(32)

    t0 = time.time()
    ciphertext = encrypt_shutter(msg, eon_key_bytes, identity_prefix, sigma)
    t1 = time.time()
    print(f'  Encrypted {len(msg)} bytes -> {len(ciphertext)} bytes in {t1-t0:.2f}s')

    t2 = time.time()
    plaintext = decrypt_shutter(ciphertext, dk_bytes)
    t3 = time.time()
    print(f'  Decrypted in {t3-t2:.2f}s')
    print(f'  Match: {plaintext == msg}')
    if plaintext != msg:
        print(f'  Expected: {msg}')
        print(f'  Got:      {plaintext}')
    assert plaintext == msg, 'ROUNDTRIP FAILED'
    print('[self_test] ✅ PASS')
    return True

# ==================== Main (API spike) ====================

if __name__ == '__main__':
    import json
    import time
    import urllib.parse
    import sys
    import requests as reqs

    API_BASE = 'https://shutter-api.chiado.staging.shutter.network/api'
    MESSAGE = b'shutter-spike: identity-gated front-run-proof tx by alogotron'

    def api_post(path, body):
        r = reqs.post(f'{API_BASE}{path}', json=body, timeout=30)
        r.raise_for_status()
        return r.json()

    def api_get(path):
        r = reqs.get(f'{API_BASE}{path}', timeout=30)
        r.raise_for_status()
        return r.json()

    # ---- Self-test first ----
    self_test()
    print()

    print('=== Shutter Python API Spike ===')
    print(f'Message: "{MESSAGE.decode()}"')

    # Step 1: Register identity
    identity_prefix = os.urandom(32)
    identity_prefix_hex = '0x' + identity_prefix.hex()
    decryption_ts = int(time.time()) + 90
    print(f'\n[Step 1] Register Identity')
    print(f'  prefix: {identity_prefix_hex}')

    reg = api_post('/register_identity', {
        'decryptionTimestamp': decryption_ts,
        'identityPrefix': identity_prefix_hex
    })
    reg_msg = reg.get('message', reg)
    print(f'  eon: {reg_msg["eon"]}')
    print(f'  identity: {reg_msg["identity"]}')
    print(f'  tx_hash: {reg_msg["tx_hash"]}')

    eon_key_hex = reg_msg['eon_key']
    computed_identity = reg_msg['identity']
    eon_key_bytes = bytes.fromhex(eon_key_hex.lstrip('0x'))

    # Step 2: Encrypt
    print(f'\n[Step 2] Encrypt')
    sigma = os.urandom(32)
    t0 = time.time()
    # Use computed identity hash (not raw prefix) as G1 preimage
    computed_identity_bytes = bytes.fromhex(computed_identity.lstrip('0x'))
    ciphertext = encrypt_shutter(MESSAGE, eon_key_bytes, computed_identity_bytes, sigma)
    print(f'  Done in {time.time()-t0:.2f}s, {len(ciphertext)} bytes')
    print(f'  Ciphertext: {ciphertext[:40].hex()}...')

    # Step 3: Wait
    wait_sec = max(decryption_ts - int(time.time()) + 5, 0)
    print(f'\n[Step 3] Waiting {wait_sec}s for decryption window...')
    for remaining in range(wait_sec, 0, -10):
        print(f'  {remaining}s...')
        time.sleep(min(10, remaining))

    # Step 4: Get decryption key
    print(f'\n[Step 4] Fetch Decryption Key')
    dk_hex = None
    for attempt in range(1, 7):
        try:
            r = api_get(f'/get_decryption_key?identity={urllib.parse.quote(computed_identity)}')
            dk_hex = (r.get('message') or r).get('decryption_key')
            if dk_hex:
                print(f'  Got key: {dk_hex[:40]}...')
                break
        except Exception as e:
            print(f'  Attempt {attempt}/6: {e}')
        if attempt < 6:
            time.sleep(10)

    if not dk_hex:
        print('FATAL: no decryption key')
        sys.exit(1)

    dk_bytes = bytes.fromhex(dk_hex.lstrip('0x'))

    # Step 5: Decrypt
    print(f'\n[Step 5] Decrypt')
    t0 = time.time()
    plaintext = decrypt_shutter(ciphertext, dk_bytes)
    print(f'  Done in {time.time()-t0:.2f}s')
    print(f'  Result: "{plaintext.decode()}"')

    success = plaintext == MESSAGE
    print('\n' + ('✅ SUCCESS! Full Shutter encrypt/decrypt via Chiado API works!' if success
                  else f'❌ MISMATCH: got {plaintext!r}'))

    # Save log
    log_dir = '/a0/usr/projects/blockchain-factory/logs/2026-04-14'
    os.makedirs(log_dir, exist_ok=True)
    summary = {
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'network': 'chiado-testnet',
        'message': MESSAGE.decode(),
        'identity_prefix': identity_prefix_hex,
        'computed_identity': computed_identity,
        'eon': reg_msg['eon'],
        'ciphertext_bytes': len(ciphertext),
        'decrypted': plaintext.decode() if success else repr(plaintext),
        'success': success
    }
    with open(f'{log_dir}/shutter-spike-result.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print(f'\nResult saved to {log_dir}/shutter-spike-result.json')

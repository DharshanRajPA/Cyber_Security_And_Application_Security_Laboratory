from __future__ import annotations

from typing import List, Tuple


BLOCK_SIZE_BYTES = 16


def _to_bytes(value: bytes | str) -> bytes:
    if isinstance(value, bytes):
        return value
    return value.encode("utf-8")


def _validate_key_length(key: bytes) -> Tuple[int, int]:
    key_len = len(key)
    if key_len not in (16, 24, 32):
        raise ValueError("AES key must be 16, 24, or 32 bytes long")
    nk = key_len // 4
    nr = {4: 10, 6: 12, 8: 14}[nk]
    return nk, nr


def _pkcs7_pad(data: bytes, block_size: int = BLOCK_SIZE_BYTES) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)


def _pkcs7_unpad(data: bytes, block_size: int = BLOCK_SIZE_BYTES) -> bytes:
    if not data or len(data) % block_size != 0:
        raise ValueError("Invalid PKCS#7 padding: data length is not a multiple of block size")
    pad_len = data[-1]
    if pad_len == 0 or pad_len > block_size:
        raise ValueError("Invalid PKCS#7 padding length")
    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Invalid PKCS#7 padding bytes")
    return data[:-pad_len]


# S-box and inverse S-box
S_BOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
]

INV_S_BOX = [0] * 256
for i, v in enumerate(S_BOX):
    INV_S_BOX[v] = i


RCON = [
    0x00000000,
    0x01000000, 0x02000000, 0x04000000, 0x08000000,
    0x10000000, 0x20000000, 0x40000000, 0x80000000,
    0x1b000000, 0x36000000,
    0x6c000000, 0xd8000000, 0xab000000, 0x4d000000, 0x9a000000,
]


def _rot_word(word: int) -> int:
    return ((word << 8) & 0xFFFFFFFF) | (word >> 24)


def _sub_word(word: int) -> int:
    return (
        (S_BOX[(word >> 24) & 0xFF] << 24)
        | (S_BOX[(word >> 16) & 0xFF] << 16)
        | (S_BOX[(word >> 8) & 0xFF] << 8)
        | (S_BOX[word & 0xFF])
    )


def _bytes_to_words(data: bytes) -> List[int]:
    assert len(data) % 4 == 0
    words = []
    for i in range(0, len(data), 4):
        words.append(
            (data[i] << 24) | (data[i + 1] << 16) | (data[i + 2] << 8) | data[i + 3]
        )
    return words


def _words_to_bytes(words: List[int]) -> bytes:
    out = bytearray()
    for w in words:
        out.extend([(w >> 24) & 0xFF, (w >> 16) & 0xFF, (w >> 8) & 0xFF, w & 0xFF])
    return bytes(out)


def _key_expansion(key: bytes) -> List[int]:
    nk, nr = _validate_key_length(key)
    nb = 4
    key_words = _bytes_to_words(key)
    w: List[int] = [0] * (nb * (nr + 1))

    for i in range(nk):
        w[i] = key_words[i]

    for i in range(nk, nb * (nr + 1)):
        temp = w[i - 1]
        if i % nk == 0:
            temp = _sub_word(_rot_word(temp)) ^ RCON[i // nk]
        elif nk > 6 and i % nk == 4:
            temp = _sub_word(temp)
        w[i] = w[i - nk] ^ temp
    return w


def _xtime(a: int) -> int:
    return ((a << 1) & 0xFF) ^ (0x1B if (a & 0x80) else 0x00)


def _gf_mul(a: int, b: int) -> int:
    res = 0
    for _ in range(8):
        if b & 1:
            res ^= a
        a = _xtime(a)
        b >>= 1
    return res & 0xFF


def _add_round_key(state: List[int], round_key_words: List[int]) -> None:
    rk = _words_to_bytes(round_key_words)
    for i in range(16):
        state[i] ^= rk[i]


def _sub_bytes(state: List[int]) -> None:
    for i in range(16):
        state[i] = S_BOX[state[i]]


def _inv_sub_bytes(state: List[int]) -> None:
    for i in range(16):
        state[i] = INV_S_BOX[state[i]]


def _shift_rows(state: List[int]) -> None:
    # state is 16 bytes: rows are [0,4,8,12], [1,5,9,13], [2,6,10,14], [3,7,11,15]
    state[1], state[5], state[9], state[13] = state[5], state[9], state[13], state[1]
    state[2], state[6], state[10], state[14] = state[10], state[14], state[2], state[6]
    state[3], state[7], state[11], state[15] = state[15], state[3], state[7], state[11]


def _inv_shift_rows(state: List[int]) -> None:
    state[1], state[5], state[9], state[13] = state[13], state[1], state[5], state[9]
    # Row 2 inverse shift is by 2 to the right (equivalently, left by 2)
    state[2], state[6], state[10], state[14] = state[10], state[14], state[2], state[6]
    state[3], state[7], state[11], state[15] = state[7], state[11], state[15], state[3]


def _mix_single_column(a0: int, a1: int, a2: int, a3: int) -> Tuple[int, int, int, int]:
    # MixColumns in GF(2^8)
    r0 = _gf_mul(a0, 2) ^ _gf_mul(a1, 3) ^ a2 ^ a3
    r1 = a0 ^ _gf_mul(a1, 2) ^ _gf_mul(a2, 3) ^ a3
    r2 = a0 ^ a1 ^ _gf_mul(a2, 2) ^ _gf_mul(a3, 3)
    r3 = _gf_mul(a0, 3) ^ a1 ^ a2 ^ _gf_mul(a3, 2)
    return r0 & 0xFF, r1 & 0xFF, r2 & 0xFF, r3 & 0xFF


def _inv_mix_single_column(a0: int, a1: int, a2: int, a3: int) -> Tuple[int, int, int, int]:
    r0 = _gf_mul(a0, 14) ^ _gf_mul(a1, 11) ^ _gf_mul(a2, 13) ^ _gf_mul(a3, 9)
    r1 = _gf_mul(a0, 9) ^ _gf_mul(a1, 14) ^ _gf_mul(a2, 11) ^ _gf_mul(a3, 13)
    r2 = _gf_mul(a0, 13) ^ _gf_mul(a1, 9) ^ _gf_mul(a2, 14) ^ _gf_mul(a3, 11)
    r3 = _gf_mul(a0, 11) ^ _gf_mul(a1, 13) ^ _gf_mul(a2, 9) ^ _gf_mul(a3, 14)
    return r0 & 0xFF, r1 & 0xFF, r2 & 0xFF, r3 & 0xFF


def _mix_columns(state: List[int]) -> None:
    for c in range(4):
        i = 4 * c
        a0, a1, a2, a3 = state[i], state[i + 1], state[i + 2], state[i + 3]
        r0, r1, r2, r3 = _mix_single_column(a0, a1, a2, a3)
        state[i], state[i + 1], state[i + 2], state[i + 3] = r0, r1, r2, r3


def _inv_mix_columns(state: List[int]) -> None:
    for c in range(4):
        i = 4 * c
        a0, a1, a2, a3 = state[i], state[i + 1], state[i + 2], state[i + 3]
        r0, r1, r2, r3 = _inv_mix_single_column(a0, a1, a2, a3)
        state[i], state[i + 1], state[i + 2], state[i + 3] = r0, r1, r2, r3


def _cipher_block(block: bytes, round_keys: List[int], nr: int) -> bytes:
    state = list(block)
    nb = 4
    _add_round_key(state, round_keys[0:nb])

    for r in range(1, nr):
        _sub_bytes(state)
        _shift_rows(state)
        _mix_columns(state)
        _add_round_key(state, round_keys[r * nb : (r + 1) * nb])

    _sub_bytes(state)
    _shift_rows(state)
    _add_round_key(state, round_keys[nr * nb : (nr + 1) * nb])
    return bytes(state)


def _inv_cipher_block(block: bytes, round_keys: List[int], nr: int) -> bytes:
    state = list(block)
    nb = 4
    _add_round_key(state, round_keys[nr * nb : (nr + 1) * nb])

    for r in range(nr - 1, 0, -1):
        _inv_shift_rows(state)
        _inv_sub_bytes(state)
        _add_round_key(state, round_keys[r * nb : (r + 1) * nb])
        _inv_mix_columns(state)

    _inv_shift_rows(state)
    _inv_sub_bytes(state)
    _add_round_key(state, round_keys[0:nb])
    return bytes(state)


def _expand_round_keys(key: bytes) -> Tuple[List[int], int]:
    nk, nr = _validate_key_length(key)
    del nk  # not used outside validation
    round_words = _key_expansion(key)
    return round_words, nr


def _encrypt_ecb(plaintext: bytes, key: bytes) -> bytes:
    padded = _pkcs7_pad(plaintext, BLOCK_SIZE_BYTES)
    round_words, nr = _expand_round_keys(key)
    out = bytearray()
    for i in range(0, len(padded), BLOCK_SIZE_BYTES):
        block = padded[i : i + BLOCK_SIZE_BYTES]
        out.extend(_cipher_block(block, round_words, nr))
    return bytes(out)


def _decrypt_ecb(ciphertext: bytes, key: bytes) -> bytes:
    if len(ciphertext) % BLOCK_SIZE_BYTES != 0:
        raise ValueError("Ciphertext length must be multiple of 16 bytes for ECB")
    round_words, nr = _expand_round_keys(key)
    out = bytearray()
    for i in range(0, len(ciphertext), BLOCK_SIZE_BYTES):
        block = ciphertext[i : i + BLOCK_SIZE_BYTES]
        out.extend(_inv_cipher_block(block, round_words, nr))
    return _pkcs7_unpad(bytes(out), BLOCK_SIZE_BYTES)


def _encrypt_cbc(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    if iv is None or len(iv) != BLOCK_SIZE_BYTES:
        raise ValueError("CBC mode requires a 16-byte IV")
    padded = _pkcs7_pad(plaintext, BLOCK_SIZE_BYTES)
    round_words, nr = _expand_round_keys(key)
    out = bytearray()
    prev = iv
    for i in range(0, len(padded), BLOCK_SIZE_BYTES):
        block = bytearray(padded[i : i + BLOCK_SIZE_BYTES])
        for j in range(BLOCK_SIZE_BYTES):
            block[j] ^= prev[j]
        enc = _cipher_block(bytes(block), round_words, nr)
        out.extend(enc)
        prev = enc
    return bytes(out)


def _decrypt_cbc(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    if iv is None or len(iv) != BLOCK_SIZE_BYTES:
        raise ValueError("CBC mode requires a 16-byte IV")
    if len(ciphertext) % BLOCK_SIZE_BYTES != 0:
        raise ValueError("Ciphertext length must be multiple of 16 bytes for CBC")
    round_words, nr = _expand_round_keys(key)
    out = bytearray()
    prev = iv
    for i in range(0, len(ciphertext), BLOCK_SIZE_BYTES):
        block = ciphertext[i : i + BLOCK_SIZE_BYTES]
        dec = bytearray(_inv_cipher_block(block, round_words, nr))
        for j in range(BLOCK_SIZE_BYTES):
            dec[j] ^= prev[j]
        out.extend(dec)
        prev = block
    return _pkcs7_unpad(bytes(out), BLOCK_SIZE_BYTES)


def encrypt_text(plaintext: str, key: bytes | str, mode: str = "ECB", iv: bytes | None = None) -> bytes:
    key_bytes = _to_bytes(key)
    _validate_key_length(key_bytes)
    data = _to_bytes(plaintext)
    mode_upper = mode.upper()
    if mode_upper == "ECB":
        return _encrypt_ecb(data, key_bytes)
    if mode_upper == "CBC":
        if iv is None:
            raise ValueError("CBC mode requires an IV")
        return _encrypt_cbc(data, key_bytes, iv)
    raise ValueError("Unsupported mode. Use 'ECB' or 'CBC'.")


def decrypt_text(ciphertext: bytes, key: bytes | str, mode: str = "ECB", iv: bytes | None = None) -> str:
    key_bytes = _to_bytes(key)
    _validate_key_length(key_bytes)
    mode_upper = mode.upper()
    if mode_upper == "ECB":
        pt = _decrypt_ecb(ciphertext, key_bytes)
        return pt.decode("utf-8")
    if mode_upper == "CBC":
        if iv is None:
            raise ValueError("CBC mode requires an IV")
        pt = _decrypt_cbc(ciphertext, key_bytes, iv)
        return pt.decode("utf-8")
    raise ValueError("Unsupported mode. Use 'ECB' or 'CBC'.")


def _self_check() -> None:
    # NIST SP 800-38A F.1.1 ECB-AES128 (first block check with padding emulation)
    key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
    pt = bytes.fromhex("6bc1bee22e409f96e93d7e117393172a")
    # Our API pads, so we use the core block functions to validate the round logic without padding
    round_words, nr = _expand_round_keys(key)
    ct_block = _cipher_block(pt, round_words, nr)
    expected_ct_block = bytes.fromhex("3ad77bb40d7a3660a89ecaf32466ef97")
    assert ct_block == expected_ct_block, "AES-128 ECB single-block KAT failed"

    # CBC example (first block) F.2.1
    iv = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    cbc_ct_first = _cipher_block(bytes([a ^ b for a, b in zip(pt, iv)]), round_words, nr)
    expected_cbc_first = bytes.fromhex("7649abac8119b246cee98e9b12e9197d")
    assert cbc_ct_first == expected_cbc_first, "AES-128 CBC first-block KAT failed"

    # End-to-end text API check with padding
    sample_text = "Hello AES!"
    e = encrypt_text(sample_text, key, mode="ECB")
    d = decrypt_text(e, key, mode="ECB")
    assert d == sample_text, "ECB encrypt/decrypt roundtrip failed"

    e2 = encrypt_text(sample_text, key, mode="CBC", iv=iv)
    d2 = decrypt_text(e2, key, mode="CBC", iv=iv)
    assert d2 == sample_text, "CBC encrypt/decrypt roundtrip failed"


def _parse_hex_bytes(h: str, allowed_lengths: Tuple[int, ...]) -> bytes | None:
    s = h.strip().lower().replace("0x", "")
    if len(s) not in allowed_lengths:
        return None
    try:
        return bytes.fromhex(s)
    except Exception:
        return None


def find_aes_algorithm() -> None:
    try:
        print("=== AES (ECB/CBC, PKCS#7) FINDER ===")
        mode = input("Enter mode (ECB/CBC): ").strip().upper()
        if mode not in ("ECB", "CBC"):
            print("Unsupported mode")
            return

        key_hex = input("Enter key as hex (16/24/32 bytes -> 32/48/64 hex chars): ")
        key = _parse_hex_bytes(key_hex, (32, 48, 64))
        if key is None:
            print("Invalid key format/length")
            return

        iv = None
        if mode == "CBC":
            iv_hex = input("Enter IV as 16-byte hex (32 hex chars): ")
            iv = _parse_hex_bytes(iv_hex, (32,))
            if iv is None:
                print("Invalid IV format/length")
                return

        plaintext = input("Enter plaintext: ").encode("utf-8")

        # Encrypt
        if mode == "ECB":
            cipher = _encrypt_ecb(plaintext, key)
        else:
            cipher = _encrypt_cbc(plaintext, key, iv)  # type: ignore[arg-type]

        print(f"Cipher (hex): {cipher.hex()}")

        # Decrypt back
        if mode == "ECB":
            recovered = _decrypt_ecb(cipher, key)
        else:
            recovered = _decrypt_cbc(cipher, key, iv)  # type: ignore[arg-type]

        print(f"Decrypted: {recovered.decode('utf-8', errors='ignore')}")
    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    find_aes_algorithm()



from __future__ import annotations

import hashlib
import hmac
import secrets
from dataclasses import dataclass
import importlib.util
import os
import binascii
from typing import Optional, Tuple, Dict, Any, Callable


Point = Optional[Tuple[int, int]]
CipherPackage = Dict[str, Any]


@dataclass(frozen=True)
class EllipticCurve:
    """Short Weierstrass form: y^2 = x^3 + a*x + b over prime field F_p."""

    p: int  # Field prime
    a: int  # Curve coefficient a
    b: int  # Curve coefficient b
    G: Tuple[int, int]  # Base point (generator)
    n: int  # Order of the base point
    h: int  # Cofactor


def _mod_inv(k: int, p: int) -> int:
    """Modular multiplicative inverse using Extended Euclidean Algorithm."""
    if k % p == 0:
        raise ZeroDivisionError("Inverse does not exist")
    # Python 3.8+: pow(k, -1, p) works; use EEA for clarity/compatibility
    t, new_t = 0, 1
    r, new_r = p, k % p
    while new_r != 0:
        q = r // new_r
        t, new_t = new_t, t - q * new_t
        r, new_r = new_r, r - q * new_r
    if r > 1:
        raise ZeroDivisionError("Inverse does not exist")
    if t < 0:
        t += p
    return t


def is_on_curve(curve: EllipticCurve, P: Point) -> bool:
    if P is None:
        return True
    x, y = P
    p = curve.p
    return (y * y - (x * x * x + curve.a * x + curve.b)) % p == 0


def _point_add(curve: EllipticCurve, P: Point, Q: Point) -> Point:
    """Add two points P and Q on the curve. Handles special cases."""
    if P is None:
        return Q
    if Q is None:
        return P

    p = curve.p
    (x1, y1), (x2, y2) = P, Q

    if x1 == x2 and (y1 + y2) % p == 0:
        return None  # P + (-P) = O

    if P == Q:
        # Point doubling
        if y1 % p == 0:
            return None
        m = (3 * x1 * x1 + curve.a) * _mod_inv(2 * y1, p) % p
    else:
        if (x2 - x1) % p == 0:
            return None
        m = (y2 - y1) * _mod_inv(x2 - x1, p) % p

    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    R = (x3, y3)
    return R


def scalar_multiply(curve: EllipticCurve, k: int, P: Point) -> Point:
    """Compute k*P using double-and-add. k may be any integer (reduce mod n)."""
    if P is None:
        return None
    if k % curve.n == 0:
        return None
    if k < 0:
        # k * P = (-k) * (-P)
        x, y = P
        return scalar_multiply(curve, -k, (x, (-y) % curve.p))

    result: Point = None
    addend: Point = P

    while k:
        if k & 1:
            result = _point_add(curve, result, addend)
        addend = _point_add(curve, addend, addend)
        k >>= 1

    return result


def generate_keypair(curve: EllipticCurve) -> Tuple[int, Point]:
    """Generate a private/public key pair: d in [1, n-1], Q = d*G."""
    while True:
        d = secrets.randbelow(curve.n)
        if 1 <= d < curve.n:
            Q = scalar_multiply(curve, d, curve.G)
            if Q is None:
                continue
            return d, Q


def _int_to_bytes(i: int, length: int) -> bytes:
    return i.to_bytes(length, byteorder="big")


def _bytes_needed(n: int) -> int:
    if n == 0:
        return 1
    return (n.bit_length() + 7) // 8


def _kdf_sha256(key_material: bytes, info: bytes, length: int) -> bytes:
    """Simple KDF using SHA-256 in counter mode to derive `length` bytes."""
    out = bytearray()
    counter = 1
    while len(out) < length:
        h = hashlib.sha256()
        h.update(key_material)
        h.update(info)
        h.update(counter.to_bytes(4, "big"))
        out.extend(h.digest())
        counter += 1
    return bytes(out[:length])


def ecdh_shared_secret(curve: EllipticCurve, private_key: int, peer_public: Point) -> bytes:
    """Derive a 32-byte shared secret via ECDH using x-coordinate of d*Q."""
    if peer_public is None or not is_on_curve(curve, peer_public):
        raise ValueError("Invalid peer public key")
    S = scalar_multiply(curve, private_key % curve.n, peer_public)
    if S is None:
        raise ValueError("Invalid shared point (infinity)")
    xS, _ = S
    x_len = _bytes_needed(curve.p - 1)
    return hashlib.sha256(_int_to_bytes(xS, x_len)).digest()


def _xor_stream(data: bytes, key_stream: Callable[[int], bytes]) -> bytes:
    result = bytearray(len(data))
    offset = 0
    block_size = 32
    while offset < len(data):
        block = key_stream(block_size)
        for i in range(min(block_size, len(data) - offset)):
            result[offset + i] = data[offset + i] ^ block[i]
        offset += block_size
    return bytes(result)


def encrypt(curve: EllipticCurve, recipient_public: Point, plaintext: bytes) -> CipherPackage:
    """Encrypt using ephemeral ECDH + XOR stream + HMAC-SHA256 integrity.

    Returns a dict with ephemeral_public, ciphertext, and tag.
    """
    if recipient_public is None or not is_on_curve(curve, recipient_public):
        raise ValueError("Invalid recipient public key")

    # Ephemeral key pair
    eph_priv, eph_pub = generate_keypair(curve)

    # Shared secret
    shared = ecdh_shared_secret(curve, eph_priv, recipient_public)

    # Derive encryption and authentication keys
    enc_key = _kdf_sha256(shared, b"enc", 32)
    mac_key = _kdf_sha256(shared, b"mac", 32)

    # Create keystream generator
    counter = 0

    def next_keystream(n: int) -> bytes:
        nonlocal counter
        out = bytearray()
        while len(out) < n:
            h = hashlib.sha256()
            h.update(enc_key)
            h.update(counter.to_bytes(8, "big"))
            out.extend(h.digest())
            counter += 1
        return bytes(out[:n])

    ciphertext = _xor_stream(plaintext, next_keystream)

    # Tag over associated data (ephemeral pub) + ciphertext
    x_e, y_e = eph_pub
    ad = _int_to_bytes(x_e, _bytes_needed(curve.p - 1)) + _int_to_bytes(
        y_e, _bytes_needed(curve.p - 1)
    )
    tag = hmac.new(mac_key, ad + ciphertext, hashlib.sha256).digest()

    return {
        "ephemeral_public": eph_pub,
        "ciphertext": ciphertext,
        "tag": tag,
    }


def decrypt(curve: EllipticCurve, recipient_private: int, package: CipherPackage) -> bytes:
    eph_pub = package.get("ephemeral_public")
    ciphertext = package.get("ciphertext")
    tag = package.get("tag")

    if not isinstance(ciphertext, (bytes, bytearray)) or not isinstance(tag, (bytes, bytearray)):
        raise ValueError("Invalid package fields")

    if eph_pub is None or not is_on_curve(curve, eph_pub):
        raise ValueError("Invalid ephemeral public key")

    shared = ecdh_shared_secret(curve, recipient_private, eph_pub)

    enc_key = _kdf_sha256(shared, b"enc", 32)
    mac_key = _kdf_sha256(shared, b"mac", 32)

    x_e, y_e = eph_pub
    ad = _int_to_bytes(x_e, _bytes_needed(curve.p - 1)) + _int_to_bytes(
        y_e, _bytes_needed(curve.p - 1)
    )
    expected_tag = hmac.new(mac_key, ad + bytes(ciphertext), hashlib.sha256).digest()
    if not hmac.compare_digest(expected_tag, bytes(tag)):
        raise ValueError("Authentication failed: tag mismatch")

    counter = 0

    def next_keystream(n: int) -> bytes:
        nonlocal counter
        out = bytearray()
        while len(out) < n:
            h = hashlib.sha256()
            h.update(enc_key)
            h.update(counter.to_bytes(8, "big"))
            out.extend(h.digest())
            counter += 1
        return bytes(out[:n])

    return _xor_stream(bytes(ciphertext), next_keystream)


# Default curve: secp256k1
secp256k1 = EllipticCurve(
    p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    a=0,
    b=7,
    G=(
        55066263022277343669578718895168534326250603453777594175500187360389116729240,
        32670510020758816978083085130507043184471273380659243275938904335757337482424,
    ),
    n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
    h=1,
)


__all__ = [
    "EllipticCurve",
    "Point",
    "CipherPackage",
    "is_on_curve",
    "scalar_multiply",
    "generate_keypair",
    "ecdh_shared_secret",
    "encrypt",
    "decrypt",
    "secp256k1",
]


def _load_aes_module():
    """Dynamically load AES implementation from 19_AES_Algorithm_Finder.py."""
    here = os.path.dirname(__file__)
    aes_path = os.path.join(here, "19_AES_Algorithm_Finder.py")
    spec = importlib.util.spec_from_file_location("aes_module", aes_path)
    if spec is None or spec.loader is None:
        raise ImportError("Failed to locate AES module file")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[attr-defined]
    return mod


def ecies_encrypt_aes_cbc(curve: EllipticCurve, recipient_public: Point, plaintext: bytes) -> Dict[str, Any]:
    """ECIES-style encryption using AES-CBC for payload and HMAC-SHA256 for integrity."""
    if recipient_public is None or not is_on_curve(curve, recipient_public):
        raise ValueError("Invalid recipient public key")

    aes = _load_aes_module()
    iv = secrets.token_bytes(16)

    eph_priv, eph_pub = generate_keypair(curve)
    shared = ecdh_shared_secret(curve, eph_priv, recipient_public)
    enc_key = _kdf_sha256(shared, b"enc", 32)
    mac_key = _kdf_sha256(shared, b"mac", 32)

    ciphertext = aes._encrypt_cbc(plaintext, enc_key, iv)  # type: ignore[attr-defined]

    x_e, y_e = eph_pub
    ad = (
        _int_to_bytes(x_e, _bytes_needed(curve.p - 1))
        + _int_to_bytes(y_e, _bytes_needed(curve.p - 1))
        + iv
    )
    tag = hmac.new(mac_key, ad + ciphertext, hashlib.sha256).digest()

    return {
        "ephemeral_public": eph_pub,
        "iv": iv,
        "ciphertext": ciphertext,
        "tag": tag,
    }


def ecies_decrypt_aes_cbc(curve: EllipticCurve, recipient_private: int, package: Dict[str, Any]) -> bytes:
    aes = _load_aes_module()
    eph_pub = package.get("ephemeral_public")
    iv = package.get("iv")
    ciphertext = package.get("ciphertext")
    tag = package.get("tag")

    if eph_pub is None or not is_on_curve(curve, eph_pub):
        raise ValueError("Invalid ephemeral public key")
    if not isinstance(iv, (bytes, bytearray)) or len(iv) != 16:
        raise ValueError("Invalid IV")
    if not isinstance(ciphertext, (bytes, bytearray)):
        raise ValueError("Invalid ciphertext")
    if not isinstance(tag, (bytes, bytearray)):
        raise ValueError("Invalid tag")

    shared = ecdh_shared_secret(curve, recipient_private, eph_pub)
    enc_key = _kdf_sha256(shared, b"enc", 32)
    mac_key = _kdf_sha256(shared, b"mac", 32)

    x_e, y_e = eph_pub
    ad = (
        _int_to_bytes(x_e, _bytes_needed(curve.p - 1))
        + _int_to_bytes(y_e, _bytes_needed(curve.p - 1))
        + bytes(iv)
    )
    expected_tag = hmac.new(mac_key, ad + bytes(ciphertext), hashlib.sha256).digest()
    if not hmac.compare_digest(expected_tag, bytes(tag)):
        raise ValueError("Authentication failed: tag mismatch")

    return aes._decrypt_cbc(bytes(ciphertext), enc_key, bytes(iv))  # type: ignore[attr-defined]


def _parse_hex_int(h: str) -> Optional[int]:
    s = h.strip().lower().replace("0x", "")
    if not s:
        return None
    try:
        return int(s, 16)
    except Exception:
        return None


def _point_to_hex(curve: EllipticCurve, P: Point) -> Tuple[str, str]:
    if P is None:
        return ("", "")
    x, y = P
    blen = _bytes_needed(curve.p - 1)
    return (
        _int_to_bytes(x, blen).hex(),
        _int_to_bytes(y, blen).hex(),
    )


def find_ecc_algorithm() -> None:
    try:
        print("=== ECC (ECIES over AES-CBC, HMAC-SHA256) FINDER ===")
        print("Curve: secp256k1")

        key_hex = input("Enter recipient private key as 32-byte hex (64 hex chars) or blank to generate: ").strip()
        if key_hex:
            d = _parse_hex_int(key_hex)
            if d is None:
                print("Invalid private key hex")
                return
            d = d % secp256k1.n
            if d == 0:
                print("Invalid private key value (zero)")
                return
            priv = d
            pub = scalar_multiply(secp256k1, priv, secp256k1.G)
            assert pub is not None
        else:
            priv, pub = generate_keypair(secp256k1)

        px_hex, py_hex = _point_to_hex(secp256k1, pub)
        print(f"Recipient public key X: {px_hex}")
        print(f"Recipient public key Y: {py_hex}")

        plaintext = input("Enter plaintext: ").encode("utf-8")

        package = ecies_encrypt_aes_cbc(secp256k1, pub, plaintext)

        ex_hex, ey_hex = _point_to_hex(secp256k1, package["ephemeral_public"])  # type: ignore[index]
        iv_hex = package["iv"].hex()  # type: ignore[index]
        ct_hex = package["ciphertext"].hex()  # type: ignore[index]
        tag_hex = package["tag"].hex()  # type: ignore[index]

        print(f"Ephemeral public X: {ex_hex}")
        print(f"Ephemeral public Y: {ey_hex}")
        print(f"IV (hex): {iv_hex}")
        print(f"Cipher (hex): {ct_hex}")
        print(f"Tag (hex): {tag_hex}")

        recovered = ecies_decrypt_aes_cbc(
            secp256k1,
            priv,
            {
                "ephemeral_public": package["ephemeral_public"],
                "iv": package["iv"],
                "ciphertext": package["ciphertext"],
                "tag": package["tag"],
            },
        )
        print(f"Decrypted: {recovered.decode('utf-8', errors='ignore')}")
    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    find_ecc_algorithm()

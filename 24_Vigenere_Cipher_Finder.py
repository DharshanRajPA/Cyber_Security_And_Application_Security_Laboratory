import re

def _sanitize_text(s):
    return re.sub(r"[^A-Za-z]", "", s).upper()


def _sanitize_key(key):
    key = _sanitize_text(key)
    return key


def _key_stream(key, length):
    key = _sanitize_key(key)
    if not key:
        return None
    return (key[i % len(key)] for i in range(length))


def vigenere_encrypt(plaintext, key):
    text = _sanitize_text(plaintext)
    key = _sanitize_key(key)
    if not key:
        return None
    stream = _key_stream(key, len(text))
    cipher = []
    for ch, k in zip(text, stream):
        p = ord(ch) - 65
        s = ord(k) - 65
        c = (p + s) % 26
        cipher.append(chr(c + 65))
    return "".join(cipher)


def vigenere_decrypt(ciphertext, key):
    text = _sanitize_text(ciphertext)
    key = _sanitize_key(key)
    if not key:
        return None
    stream = _key_stream(key, len(text))
    plain = []
    for ch, k in zip(text, stream):
        c = ord(ch) - 65
        s = ord(k) - 65
        p = (c - s) % 26
        plain.append(chr(p + 65))
    return "".join(plain)


def validate_vigenere_key(key):
    return len(_sanitize_key(key)) > 0


def find_vigenere_cipher():
    try:
        print("=== VIGENERE CIPHER FINDER ===")
        key = input("Enter key: ")
        if not validate_vigenere_key(key):
            print("Invalid key")
            return
        plaintext = input("Enter plaintext: ")
        ciphertext = vigenere_encrypt(plaintext, key)
        print(f"Ciphertext: {ciphertext}")
        recovered = vigenere_decrypt(ciphertext, key)
        print(f"Decrypted (raw): {recovered}")
    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    find_vigenere_cipher()

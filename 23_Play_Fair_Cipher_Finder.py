import re

def _sanitize_text(s):
    s = re.sub(r"[^A-Za-z]", "", s).upper()
    s = s.replace("J", "I")
    return s


def _prepare_key_matrix(key):
    key = _sanitize_text(key)
    seen = set()
    sequence = []
    for ch in key + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in seen:
            seen.add(ch)
            sequence.append(ch)
    matrix = [sequence[i:i + 5] for i in range(0, 25, 5)]
    positions = {matrix[r][c]: (r, c) for r in range(5) for c in range(5)}
    return matrix, positions


def _prepare_bigrams(text):
    text = _sanitize_text(text)
    if not text:
        return []
    bigrams = []
    i = 0
    while i < len(text):
        a = text[i]
        b = None
        if i + 1 < len(text):
            b = text[i + 1]
        if b is None:
            bigrams.append((a, "X"))
            i += 1
        elif a == b:
            filler = "X" if a != "X" else "Q"
            bigrams.append((a, filler))
            i += 1
        else:
            bigrams.append((a, b))
            i += 2
    if len(bigrams[-1]) == 2 and bigrams[-1][1] is None:
        bigrams[-1] = (bigrams[-1][0], "X")
    if len(bigrams[-1]) == 2 and bigrams[-1][1] == "":
        bigrams[-1] = (bigrams[-1][0], "X")
    if len(bigrams[-1]) == 2 and bigrams[-1][1] is None:
        bigrams[-1] = (bigrams[-1][0], "X")
    if len(bigrams[-1]) == 1:
        bigrams[-1] = (bigrams[-1][0], "X")
    return bigrams


def _encrypt_pair(a, b, matrix, pos):
    ra, ca = pos[a]
    rb, cb = pos[b]
    if ra == rb:
        return matrix[ra][(ca + 1) % 5] + matrix[rb][(cb + 1) % 5]
    if ca == cb:
        return matrix[(ra + 1) % 5][ca] + matrix[(rb + 1) % 5][cb]
    return matrix[ra][cb] + matrix[rb][ca]


def _decrypt_pair(a, b, matrix, pos):
    ra, ca = pos[a]
    rb, cb = pos[b]
    if ra == rb:
        return matrix[ra][(ca - 1) % 5] + matrix[rb][(cb - 1) % 5]
    if ca == cb:
        return matrix[(ra - 1) % 5][ca] + matrix[(rb - 1) % 5][cb]
    return matrix[ra][cb] + matrix[rb][ca]


def playfair_encrypt(plaintext, key):
    matrix, pos = _prepare_key_matrix(key)
    bigrams = _prepare_bigrams(plaintext)
    cipher = []
    for a, b in bigrams:
        cipher.append(_encrypt_pair(a, b, matrix, pos))
    return "".join(cipher)


def playfair_decrypt(ciphertext, key):
    matrix, pos = _prepare_key_matrix(key)
    text = _sanitize_text(ciphertext)
    if len(text) % 2 == 1:
        text += "X"
    plain = []
    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1]
        plain.append(_decrypt_pair(a, b, matrix, pos))
    return "".join(plain)


def validate_playfair_key(key):
    key = _sanitize_text(key)
    return len(key) > 0


def find_playfair_cipher():
    try:
        print("=== PLAYFAIR CIPHER FINDER ===")
        key = input("Enter key: ")
        if not validate_playfair_key(key):
            print("Invalid key")
            return
        plaintext = input("Enter plaintext: ")
        ciphertext = playfair_encrypt(plaintext, key)
        print(f"Ciphertext: {ciphertext}")
        recovered = playfair_decrypt(ciphertext, key)
        print(f"Decrypted (raw): {recovered}")
    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    find_playfair_cipher()

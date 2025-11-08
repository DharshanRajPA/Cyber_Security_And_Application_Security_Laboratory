import re

def _sanitize_text(s):
    return re.sub(r"[^A-Za-z]", "", s).upper()


def _char_to_num(ch):
    return ord(ch) - 65


def _num_to_char(n):
    return chr((n % 26) + 65)


def _chunk_text(text, size):
    chunks = []
    text = _sanitize_text(text)
    if not text:
        return []
    if len(text) % size != 0:
        text += "X" * (size - (len(text) % size))
    for i in range(0, len(text), size):
        chunks.append(text[i:i+size])
    return chunks


def _matrix_mod(M, mod):
    return [[elem % mod for elem in row] for row in M]


def _matrix_mul_vec(M, vec, mod):
    size = len(M)
    res = [0] * size
    for i in range(size):
        total = 0
        for j in range(size):
            total += M[i][j] * vec[j]
        res[i] = total % mod
    return res


def _determinant_2x2(M):
    return (M[0][0] * M[1][1] - M[0][1] * M[1][0])


def _determinant_3x3(M):
    a,b,c = M[0]
    d,e,f = M[1]
    g,h,i = M[2]
    return a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)


def _modinv(a, m):
    a %= m
    if a == 0:
        return None
    t, new_t = 0, 1
    r, new_r = m, a
    while new_r != 0:
        q = r // new_r
        t, new_t = new_t, t - q * new_t
        r, new_r = new_r, r - q * new_r
    if r != 1:
        return None
    return t % m


def _adjugate_2x2(M):
    return [[M[1][1], -M[0][1]],
            [-M[1][0], M[0][0]]]


def _cofactor_matrix_3x3(M):
    cof = [[0]*3 for _ in range(3)]
    for r in range(3):
        for c in range(3):
            sub = []
            for rr in range(3):
                if rr == r:
                    continue
                row = []
                for cc in range(3):
                    if cc == c:
                        continue
                    row.append(M[rr][cc])
                sub.append(row)
            minor = _determinant_2x2(sub)
            cof[r][c] = ((-1) ** (r + c)) * minor
    return cof


def _transpose(M):
    return [list(row) for row in zip(*M)]


def _inverse_mod_matrix(M, mod):
    n = len(M)
    if any(len(row) != n for row in M):
        return None
    if n == 2:
        det = _determinant_2x2(M) % mod
        inv_det = _modinv(det, mod)
        if inv_det is None:
            return None
        adj = _adjugate_2x2(M)
        inv = [[(adj[r][c] * inv_det) % mod for c in range(2)] for r in range(2)]
        return inv
    if n == 3:
        det = _determinant_3x3(M) % mod
        inv_det = _modinv(det, mod)
        if inv_det is None:
            return None
        cof = _cofactor_matrix_3x3(M)
        adj = _transpose(cof)
        inv = [[(adj[r][c] * inv_det) % mod for c in range(3)] for r in range(3)]
        return inv
    return None


def validate_hill_key_matrix(M):
    if not isinstance(M, list) or len(M) == 0:
        return False
    n = len(M)
    if any(not isinstance(row, list) or len(row) != n for row in M):
        return False
    if n not in (2, 3):
        return False
    try:
        mod = 26
        if n == 2:
            det = _determinant_2x2(M) % mod
        else:
            det = _determinant_3x3(M) % mod
        return _modinv(det, mod) is not None
    except Exception:
        return False


def hill_encrypt(plaintext, key_matrix):
    if not validate_hill_key_matrix(key_matrix):
        return None
    n = len(key_matrix)
    chunks = _chunk_text(plaintext, n)
    if not chunks:
        return ""
    cipher = []
    for chunk in chunks:
        vec = [_char_to_num(ch) for ch in chunk]
        res = _matrix_mul_vec(key_matrix, vec, 26)
        cipher.append("".join(_num_to_char(x) for x in res))
    return "".join(cipher)


def hill_decrypt(ciphertext, key_matrix):
    if not validate_hill_key_matrix(key_matrix):
        return None
    n = len(key_matrix)
    text = _sanitize_text(ciphertext)
    if len(text) % n != 0:
        return None
    invM = _inverse_mod_matrix(key_matrix, 26)
    if invM is None:
        return None
    plain = []
    for i in range(0, len(text), n):
        vec = [_char_to_num(ch) for ch in text[i:i+n]]
        res = _matrix_mul_vec(invM, vec, 26)
        plain.append("".join(_num_to_char(x) for x in res))
    return "".join(plain)


def _parse_matrix(s):
    rows = s.strip().split("/")
    M = []
    for row in rows:
        nums = row.strip().split()
        if not nums:
            return None
        M.append([int(x) % 26 for x in nums])
    return M


def find_hill_cipher():
    try:
        print("=== HILL CIPHER FINDER ===")
        key_str = input("Enter key matrix (rows separated by '/', entries by space). Example 2x2: '3 3/2 5': ")
        M = _parse_matrix(key_str)
        if not validate_hill_key_matrix(M):
            print("Invalid key matrix (must be 2x2 or 3x3, invertible mod 26)")
            return
        plaintext = input("Enter plaintext: ")
        ciphertext = hill_encrypt(plaintext, M)
        print(f"Ciphertext: {ciphertext}")
        recovered = hill_decrypt(ciphertext, M)
        print(f"Decrypted (raw): {recovered}")
    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    find_hill_cipher()

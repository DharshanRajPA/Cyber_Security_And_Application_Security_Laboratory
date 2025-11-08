import random

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def egcd(a, b):
    if b == 0:
        return (abs(a), 1 if a > 0 else -1, 0)
    g, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)


def modinv(a, m):
    a %= m
    g, x, _ = egcd(a, m)
    if g != 1:
        return None
    return x % m


def factorize(n):
    f = {}
    d = 2
    x = n
    while d * d <= x:
        while x % d == 0:
            f[d] = f.get(d, 0) + 1
            x //= d
        d = d + 1 if d == 2 else d + 2
    if x > 1:
        f[x] = f.get(x, 0) + 1
    return list(f.keys())


def primitive_root(p):
    if not is_prime(p):
        return None
    phi = p - 1
    factors = factorize(phi)
    for g in range(2, p):
        ok = True
        for q in factors:
            if pow(g, phi // q, p) == 1:
                ok = False
                break
        if ok:
            return g
    return None


def generate_keys(q):
    if not is_prime(q):
        return None, None, None, "q must be prime"
    g = primitive_root(q)
    if g is None:
        return None, None, None, "failed to find primitive root"
    x = random.randrange(1, q - 1)
    y = pow(g, x, q)
    return (g, q), (x, y), y, "OK"


def elgamal_encrypt(m, public_params, y):
    g, q = public_params
    if not (0 <= m < q):
        return None, None
    k = random.randrange(1, q - 1)
    c1 = pow(g, k, q)
    s = pow(y, k, q)
    c2 = (s * m) % q
    return c1, c2


def elgamal_decrypt(c1, c2, private_x, q):
    if not (0 <= c1 < q and 0 <= c2 < q):
        return None
    s = pow(c1, private_x, q)
    s_inv = modinv(s, q)
    if s_inv is None:
        return None
    m = (c2 * s_inv) % q
    return m


def find_elgamal_algorithm():
    try:
        print("=== ELGAMAL PUBLIC KEY ALGORITHM FINDER ===")
        q = int(input("Enter prime q: "))
        public_params, private_params, y, status = generate_keys(q)
        if status != "OK":
            print("Error:", status)
            return
        g, q = public_params
        x, y = private_params
        print(f"Public parameters (q, g, y): q={q}, g={g}, y={y}")
        print(f"Private key x: {x}")
        m = int(input(f"Enter message as integer (0 <= m < {q}): "))
        if not (0 <= m < q):
            print("Error: message must satisfy range 0 <= m < q")
            return
        c1, c2 = elgamal_encrypt(m, (g, q), y)
        print(f"Ciphertext: (C1={c1}, C2={c2})")
        recovered = elgamal_decrypt(c1, c2, x, q)
        print(f"Decrypted message: {recovered}")
    except ValueError:
        print("Please enter valid integers")


if __name__ == "__main__":
    find_elgamal_algorithm()



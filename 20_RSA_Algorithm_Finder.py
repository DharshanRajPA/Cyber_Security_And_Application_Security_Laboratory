import math

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


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


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


def choose_e(phi_n):
    e = 65537
    if e < phi_n and gcd(e, phi_n) == 1:
        return e
    for candidate in (3, 5, 17, 257, 65537):
        if candidate < phi_n and gcd(candidate, phi_n) == 1:
            return candidate
    for candidate in range(3, phi_n, 2):
        if gcd(candidate, phi_n) == 1:
            return candidate
    return None


def generate_keys(p, q):
    if not (is_prime(p) and is_prime(q)):
        return None, None, "p and q must be prime"
    if p == q:
        return None, None, "p and q must be distinct primes"
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = choose_e(phi_n)
    if e is None:
        return None, None, "Failed to choose public exponent e"
    d = modinv(e, phi_n)
    if d is None:
        return None, None, "Failed to compute modular inverse for d"
    return (e, n), (d, n), "OK"


def rsa_encrypt(m, e, n):
    if not (0 <= m < n):
        return None
    return pow(m, e, n)


def rsa_decrypt(c, d, n):
    if not (0 <= c < n):
        return None
    return pow(c, d, n)


def find_rsa_algorithm():
    try:
        print("=== RSA PUBLIC KEY ALGORITHM FINDER ===")
        p = int(input("Enter prime p: "))
        q = int(input("Enter prime q: "))
        public_key, private_key, status = generate_keys(p, q)
        if status != "OK":
            print("Error:", status)
            return
        e, n = public_key
        d, _ = private_key
        print(f"Public Key (e, n): ({e}, {n})")
        print(f"Private Key (d, n): ({d}, {n})")
        m = int(input("Enter message as integer (0 <= m < n): "))
        if not (0 <= m < n):
            print("Error: message must satisfy 0 <= m < n")
            return
        c = rsa_encrypt(m, e, n)
        print(f"Ciphertext: {c}")
        recovered = rsa_decrypt(c, d, n)
        print(f"Decrypted message: {recovered}")
    except ValueError:
        print("Please enter valid integers")


if __name__ == "__main__":
    find_rsa_algorithm()
    
    
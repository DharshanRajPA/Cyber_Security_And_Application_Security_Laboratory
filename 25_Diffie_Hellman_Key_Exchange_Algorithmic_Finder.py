import math


def is_prime(n: int) -> bool:
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


def _prime_factors(n: int) -> list:
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors.append(n)
    return factors


def is_primitive_root(g: int, p: int) -> bool:
    if not is_prime(p):
        return False
    if g <= 1 or g >= p:
        return False
    phi = p - 1
    for q in _prime_factors(phi):
        if pow(g, phi // q, p) == 1:
            return False
    return True


def validate_diffie_hellman_parameters(p: int, g: int) -> str:
    if not is_prime(p):
        return "p must be prime"
    if not (2 <= g <= p - 2):
        return "g must satisfy 2 <= g <= p-2"
    if not is_primitive_root(g, p):
        return "g must be a primitive root modulo p"
    return "OK"


def compute_public_key(p: int, g: int, private_key: int) -> int | None:
    if private_key is None or private_key <= 0 or private_key >= p - 1:
        return None
    return pow(g, private_key, p)


def compute_shared_key(p: int, public_key_other: int, private_key_self: int) -> int | None:
    if any(v is None for v in (p, public_key_other, private_key_self)):
        return None
    if not (1 < public_key_other < p):
        return None
    return pow(public_key_other, private_key_self, p)


def baby_step_giant_step_discrete_log(g: int, h: int, p: int) -> int | None:
    if not (is_prime(p) and is_primitive_root(g, p)):
        return None
    n = p - 1
    m = int(math.isqrt(n)) + 1

    table = {}
    e = 1
    for j in range(m):
        if e not in table:
            table[e] = j
        e = (e * g) % p

    factor = pow(g, (p - 1) - m, p)  # g^{-m} mod p
    gamma = h % p
    for i in range(m + 1):
        if gamma in table:
            return i * m + table[gamma]
        gamma = (gamma * factor) % p
    return None


def diffie_hellman_key_exchange(p: int, g: int, private_a: int, private_b: int):
    status = validate_diffie_hellman_parameters(p, g)
    if status != "OK":
        return None, None, None, None, status

    public_a = compute_public_key(p, g, private_a)
    public_b = compute_public_key(p, g, private_b)
    if public_a is None or public_b is None:
        return None, None, None, None, "invalid private keys"

    shared_a = compute_shared_key(p, public_b, private_a)
    shared_b = compute_shared_key(p, public_a, private_b)
    if shared_a is None or shared_b is None or shared_a != shared_b:
        return public_a, public_b, shared_a, shared_b, "shared key mismatch"

    return public_a, public_b, shared_a, shared_b, "OK"


if __name__ == "__main__":
    p_demo = 23
    g_demo = 5  
    a_demo = 6
    b_demo = 15

    #p_demo = 19
    #g_demo = 2   
    #a_demo = 5
    #b_demo = 12

    A, B, sA, sB, status = diffie_hellman_key_exchange(p_demo, g_demo, a_demo, b_demo)
    print("Status:", status)
    print(f"Public A: {A}")
    print(f"Public B: {B}")
    print(f"Shared A: {sA}")
    print(f"Shared B: {sB}")

    recovered_a = baby_step_giant_step_discrete_log(g_demo, A, p_demo)
    recovered_b = baby_step_giant_step_discrete_log(g_demo, B, p_demo)
    print(f"Recovered a (via dlog): {recovered_a}")
    print(f"Recovered b (via dlog): {recovered_b}")


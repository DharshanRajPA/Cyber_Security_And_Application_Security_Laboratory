def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def power_mod(base, exponent, modulus):
    if modulus == 1:
        return 0
    
    result = 1
    base = base % modulus
    
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    
    return result

def euler_totient(n):
    if n <= 0:
        return 0
    
    count = 0
    for i in range(1, n + 1):
        if gcd(i, n) == 1:
            count += 1
    
    return count

def get_prime_factors(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            if d not in factors:
                factors.append(d)
            n //= d
        d += 1
    if n > 1 and n not in factors:
        factors.append(n)
    return factors

def is_primitive_root(g, n):
    if gcd(g, n) != 1:
        return False
    
    phi_n = euler_totient(n)
    prime_factors = get_prime_factors(phi_n)
    
    for factor in prime_factors:
        if power_mod(g, phi_n // factor, n) == 1:
            return False
    
    return True

def find_primitive_roots(n):
    if n <= 1:
        return []
    
    phi_n = euler_totient(n)
    primitive_roots = []
    
    for g in range(1, n):
        if gcd(g, n) == 1 and is_primitive_root(g, n):
            primitive_roots.append(g)
    
    return primitive_roots

def find_primitive_root():
    try:
        n = int(input("Enter a positive integer n: "))
        
        if n <= 1:
            print("Primitive roots are not defined for n ≤ 1")
            return
        
        print(f"\n=== PRIMITIVE ROOT FINDER ===")
        print(f"Finding primitive roots modulo {n}")
        print(f"Euler's totient φ({n}) = {euler_totient(n)}")
        
        primitive_roots = find_primitive_roots(n)
        
        if primitive_roots:
            print(f"\nPrimitive roots modulo {n}: {primitive_roots}")
            print(f"Total primitive roots found: {len(primitive_roots)}")
            
            if len(primitive_roots) > 0:
                g = primitive_roots[0]
                print(f"\nExample: {g} is a primitive root")
                print(f"Powers of {g} modulo {n}:")
                for i in range(1, euler_totient(n) + 1):
                    power = power_mod(g, i, n)
                    print(f"  {g}^{i} ≡ {power} (mod {n})")
        else:
            print(f"\nNo primitive roots exist for {n}")
            
    except ValueError:
        print("Please enter a valid integer")

def test_primitive_root():
    try:
        n = int(input("Enter modulus n: "))
        g = int(input("Enter number g to test: "))
        
        if n <= 1:
            print("Modulus must be greater than 1")
            return
        
        if g <= 0 or g >= n:
            print("g must be between 1 and n-1")
            return
        
        print(f"\n=== PRIMITIVE ROOT TEST ===")
        print(f"Testing if {g} is a primitive root modulo {n}")
        
        if gcd(g, n) != 1:
            print(f"✗ {g} is not coprime to {n}")
            return
        
        if is_primitive_root(g, n):
            print(f"✓ {g} is a primitive root modulo {n}")
            
            phi_n = euler_totient(n)
            print(f"Order of {g} modulo {n} is {phi_n}")
            
            print(f"\nPowers of {g} modulo {n}:")
            for i in range(1, phi_n + 1):
                power = power_mod(g, i, n)
                print(f"  {g}^{i} ≡ {power} (mod {n})")
        else:
            print(f"✗ {g} is not a primitive root modulo {n}")
            
    except ValueError:
        print("Please enter valid integers")

if __name__ == "__main__":
    find_primitive_root()

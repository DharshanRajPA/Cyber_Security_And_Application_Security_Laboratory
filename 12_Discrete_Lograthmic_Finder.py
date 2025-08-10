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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd_val, x, y = extended_gcd(a, m)
    if gcd_val != 1:
        return None
    return (x % m + m) % m

def baby_step_giant_step(g, h, p):
    if gcd(g, p) != 1:
        return None
    
    m = int(p ** 0.5) + 1
    
    baby_steps = {}
    current = 1
    
    for j in range(m):
        baby_steps[current] = j
        current = (current * g) % p
    
    g_m = power_mod(g, m, p)
    g_m_inv = mod_inverse(g_m, p)
    
    if g_m_inv is None:
        return None
    
    current = h
    
    for i in range(m):
        if current in baby_steps:
            return i * m + baby_steps[current]
        current = (current * g_m_inv) % p
    
    return None

def brute_force_discrete_log(g, h, p):
    if gcd(g, p) != 1:
        return None
    
    current = 1
    for x in range(p):
        if current == h:
            return x
        current = (current * g) % p
    
    return None

def find_discrete_logarithm():
    try:
        print("Enter the base (generator) g:")
        g = int(input())
        
        print("Enter the target value h:")
        h = int(input())
        
        print("Enter the modulus p (prime):")
        p = int(input())
        
        if p <= 1:
            print("Modulus must be a prime number")
            return
        
        if g <= 0 or h < 0 or g >= p or h >= p:
            print("Values must be in range [0, p-1]")
            return
        
        print(f"\n=== DISCRETE LOGARITHM FINDER ===")
        print(f"Solving: {g}^x ≡ {h} (mod {p})")
        
        print(f"\nUsing Baby-Step Giant-Step Algorithm:")
        result_bsgs = baby_step_giant_step(g, h, p)
        
        if result_bsgs is not None:
            print(f"Solution: x = {result_bsgs}")
            verification = power_mod(g, result_bsgs, p)
            print(f"Verification: {g}^{result_bsgs} ≡ {verification} (mod {p})")
        else:
            print("No solution found using Baby-Step Giant-Step")
        
        if p < 1000:
            print(f"\nUsing Brute Force Method:")
            result_bf = brute_force_discrete_log(g, h, p)
            
            if result_bf is not None:
                print(f"Solution: x = {result_bf}")
                verification = power_mod(g, result_bf, p)
                print(f"Verification: {g}^{result_bf} ≡ {verification} (mod {p})")
            else:
                print("No solution found using Brute Force")
        else:
            print("\nBrute force skipped (modulus too large)")
            
    except ValueError:
        print("Please enter valid integers")

def test_discrete_log():
    try:
        print("Enter the base (generator) g:")
        g = int(input())
        
        print("Enter the exponent x:")
        x = int(input())
        
        print("Enter the modulus p:")
        p = int(input())
        
        if p <= 1:
            print("Modulus must be greater than 1")
            return
        
        if x < 0:
            print("Exponent must be non-negative")
            return
        
        print(f"\n=== DISCRETE LOGARITHM TEST ===")
        print(f"Calculating: {g}^{x} (mod {p})")
        
        result = power_mod(g, x, p)
        print(f"Result: {g}^{x} ≡ {result} (mod {p})")
        
        print(f"\nNow solving: {g}^x ≡ {result} (mod {p})")
        
        solution = baby_step_giant_step(g, result, p)
        if solution is not None:
            print(f"Solution found: x = {solution}")
            if solution == x:
                print("✓ Verification successful!")
            else:
                print("⚠ Multiple solutions may exist")
        else:
            print("No solution found")
            
    except ValueError:
        print("Please enter valid integers")

if __name__ == "__main__":
    find_discrete_logarithm()

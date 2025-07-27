def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y

def multiplicative_inverse_euclidean(a, m):
    gcd_val, x, y = extended_gcd(a, m)
    
    if gcd_val != 1:
        return None
    
    return (x % m + m) % m

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

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def multiplicative_inverse_fermat(a, p):
    if not is_prime(p):
        return None
    
    if a % p == 0:
        return None
    
    return power_mod(a, p-2, p)

def brute_force_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def find_multiplicative_inverse():
    try:
        print("Enter the number a:")
        a = int(input())
        
        print("Enter the modulus m:")
        m = int(input())
        
        if m <= 1:
            print("Modulus must be greater than 1")
            return
        
        if a <= 0:
            print("Number must be positive")
            return
        
        print(f"\n=== MULTIPLICATIVE INVERSE FINDER ===")
        print(f"Finding: {a}^(-1) (mod {m})")
        print(f"Solving: {a} × x ≡ 1 (mod {m})")
        
        print(f"\nUsing Extended Euclidean Algorithm:")
        result_euclidean = multiplicative_inverse_euclidean(a, m)
        
        if result_euclidean is not None:
            print(f"Solution: x = {result_euclidean}")
            verification = (a * result_euclidean) % m
            print(f"Verification: {a} × {result_euclidean} ≡ {verification} (mod {m})")
        else:
            print("No multiplicative inverse exists (gcd(a,m) ≠ 1)")
        
        if is_prime(m):
            print(f"\nUsing Fermat's Little Theorem (since {m} is prime):")
            result_fermat = multiplicative_inverse_fermat(a, m)
            
            if result_fermat is not None:
                print(f"Solution: x = {result_fermat}")
                verification = (a * result_fermat) % m
                print(f"Verification: {a} × {result_fermat} ≡ {verification} (mod {m})")
                print(f"Using: {a}^({m}-2) ≡ {result_fermat} (mod {m})")
            else:
                print("No multiplicative inverse exists")
        else:
            print(f"\nFermat's method not applicable ({m} is not prime)")
        
        if m < 1000:
            print(f"\nUsing Brute Force Method:")
            result_brute = brute_force_inverse(a, m)
            
            if result_brute is not None:
                print(f"Solution: x = {result_brute}")
                verification = (a * result_brute) % m
                print(f"Verification: {a} × {result_brute} ≡ {verification} (mod {m})")
            else:
                print("No multiplicative inverse found")
        else:
            print("\nBrute force skipped (modulus too large)")
            
    except ValueError:
        print("Please enter valid integers")

def test_inverse_calculation():
    try:
        print("Enter the number a:")
        a = int(input())
        
        print("Enter the modulus m:")
        m = int(input())
        
        print("Enter the inverse x:")
        x = int(input())
        
        if m <= 1:
            print("Modulus must be greater than 1")
            return
        
        if a <= 0 or x <= 0:
            print("Numbers must be positive")
            return
        
        print(f"\n=== MULTIPLICATIVE INVERSE TEST ===")
        print(f"Testing: {a} × {x} ≡ 1 (mod {m})")
        
        result = (a * x) % m
        print(f"Result: {a} × {x} ≡ {result} (mod {m})")
        
        if result == 1:
            print("✓ Correct! This is a valid multiplicative inverse")
            
            print(f"\nNow finding the inverse using algorithms:")
            inverse_euclidean = multiplicative_inverse_euclidean(a, m)
            if inverse_euclidean is not None:
                print(f"Extended Euclidean: {inverse_euclidean}")
                if inverse_euclidean == x:
                    print("✓ Matches the given inverse!")
                else:
                    print("⚠ Different inverse found (both are valid)")
        else:
            print("✗ Incorrect! This is not a valid multiplicative inverse")
            
    except ValueError:
        print("Please enter valid integers")

def main():
    while True:
        print("\n=== MULTIPLICATIVE INVERSE FINDER ===")
        print("1. Find multiplicative inverse")
        print("2. Test inverse calculation")
        print("3. Exit")
        
        choice = input("Enter choice (1, 2, or 3): ")
        
        if choice == '1':
            find_multiplicative_inverse()
        elif choice == '2':
            test_inverse_calculation()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()

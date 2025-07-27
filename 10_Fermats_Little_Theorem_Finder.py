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

def fermats_little_theorem_test(p, a):
    if not is_prime(p):
        return False, f"{p} is not prime"
    
    if a % p == 0:
        return False, f"{a} is divisible by {p}"
    
    result = power_mod(a, p-1, p)
    return result == 1, f"{a}^({p}-1) ≡ {result} (mod {p})"

def modular_inverse_fermat(a, p):
    if not is_prime(p):
        return None, f"{p} is not prime"
    
    if a % p == 0:
        return None, f"{a} is divisible by {p}"
    
    inverse = power_mod(a, p-2, p)
    return inverse, f"{a}^({p}-2) ≡ {inverse} (mod {p})"

def test_fermat():
    try:
        print("Enter a prime number p:")
        p = int(input())
        
        print("Enter a number a (not divisible by p):")
        a = int(input())
        
        if p <= 0 or a <= 0:
            print("Please enter positive numbers")
            return
        
        print(f"\n=== FERMAT'S LITTLE THEOREM TEST ===")
        print(f"Testing: {a}^({p}-1) ≡ 1 (mod {p})")
        
        is_valid, explanation = fermats_little_theorem_test(p, a)
        
        print(f"Result: {explanation}")
        if is_valid:
            print("✓ Fermat's Little Theorem holds!")
        else:
            print("✗ Fermat's Little Theorem does not hold")
            
    except ValueError:
        print("Please enter valid integers")

def find_modular_inverse():
    try:
        print("Enter a prime number p:")
        p = int(input())
        
        print("Enter a number a (not divisible by p):")
        a = int(input())
        
        if p <= 0 or a <= 0:
            print("Please enter positive numbers")
            return
        
        print(f"\n=== MODULAR INVERSE USING FERMAT ===")
        print(f"Finding: {a}^(-1) (mod {p})")
        print(f"Using: {a}^({p}-2) (mod {p})")
        
        inverse, explanation = modular_inverse_fermat(a, p)
        
        if inverse is not None:
            print(f"Result: {explanation}")
            print(f"Modular inverse: {inverse}")
            print(f"Verification: {a} × {inverse} ≡ {(a * inverse) % p} (mod {p})")
        else:
            print(f"Error: {explanation}")
            
    except ValueError:
        print("Please enter valid integers")

def main():
    while True:
        print("\n=== FERMAT'S LITTLE THEOREM ===")
        print("1. Test Fermat's Little Theorem")
        print("2. Find modular inverse using Fermat")
        print("3. Exit")
        
        choice = input("Enter choice (1, 2, or 3): ")
        
        if choice == '1':
            test_fermat()
        elif choice == '2':
            find_modular_inverse()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()

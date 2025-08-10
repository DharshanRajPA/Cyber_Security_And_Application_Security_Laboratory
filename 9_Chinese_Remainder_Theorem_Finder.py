def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None
    return (x % m + m) % m

def chinese_remainder_theorem(remainders, moduli):
    if len(remainders) != len(moduli):
        return None
    
    n = len(remainders)
    if n == 0:
        return None
    
    if n == 1:
        return remainders[0] % moduli[0]
    
    a1, a2 = remainders[0], remainders[1]
    n1, n2 = moduli[0], moduli[1]
    
    gcd, m1, m2 = extended_gcd(n1, n2)
    
    if gcd != 1:
        return None
    
    x = (a1 * m2 * n2 + a2 * m1 * n1) % (n1 * n2)
    
    for i in range(2, n):
        a1, n1 = x, n1 * n2
        a2, n2 = remainders[i], moduli[i]
        
        gcd, m1, m2 = extended_gcd(n1, n2)
        if gcd != 1:
            return None
        
        x = (a1 * m2 * n2 + a2 * m1 * n1) % (n1 * n2)
    
    return x

def solve_crt():
    try:
        print("Enter the number of congruences:")
        n = int(input())
        
        if n <= 0:
            print("Please enter a positive number")
            return
        
        remainders = []
        moduli = []
        
        print(f"\nEnter {n} congruences in the form: x ≡ a (mod m)")
        for i in range(n):
            print(f"\nCongruence {i+1}:")
            a = int(input("Enter remainder (a): "))
            m = int(input("Enter modulus (m): "))
            
            if m <= 0:
                print("Modulus must be positive")
                return
            
            remainders.append(a)
            moduli.append(m)
        
        result = chinese_remainder_theorem(remainders, moduli)
        
        if result is None:
            print("\nNo solution exists (moduli are not pairwise coprime)")
        else:
            print(f"\nSolution: x ≡ {result} (mod {moduli[0] * moduli[1]})")
            print(f"General solution: x = {result} + k × {moduli[0] * moduli[1]} for any integer k")
            
    except ValueError:
        print("Please enter valid integers")

if __name__ == "__main__":
    solve_crt()

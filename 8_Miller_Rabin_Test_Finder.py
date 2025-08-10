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

def miller_rabin_test(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    
    for _ in range(k):
        a = 2 + (_ % (n - 4))
        x = power_mod(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    
    return True

def test_miller_rabin():
    try:
        n = int(input("Enter a number to test: "))
        
        if n <= 1:
            print(f"{n} is not prime")
            return
            
        result = miller_rabin_test(n)
        
        if result:
            print(f"{n} is likely prime (Miller-Rabin test)")
        else:
            print(f"{n} is composite (Miller-Rabin test)")
            
    except ValueError:
        print("Please enter a valid integer")

if __name__ == "__main__":
    test_miller_rabin()

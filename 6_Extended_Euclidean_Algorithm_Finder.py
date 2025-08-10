def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y

def find_extended_gcd():
    try:
        a = int(input("Enter first number: "))
        b = int(input("Enter second number: "))
        
        if a == 0 and b == 0:
            print("Extended GCD of 0 and 0 is undefined")
            return
            
        gcd_val, x, y = extended_gcd(a, b)
        print(f"Extended GCD of {a} and {b}:")
        print(f"GCD = {gcd_val}")
        print(f"x = {x}")
        print(f"y = {y}")
        print(f"Verification: {a} × {x} + {b} × {y} = {a * x + b * y}")
        
    except ValueError:
        print("Please enter valid integers")

if __name__ == "__main__":
    find_extended_gcd()

def modular_division(a, b, m):
    if b == 0:
        return None, "Division by zero is not allowed"
    
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd_val, x, y = extended_gcd(b, m)
    if gcd_val != 1:
        return None, f"Multiplicative inverse does not exist (gcd({b}, {m}) = {gcd_val})"
    
    b_inverse = (x % m + m) % m
    result = (a * b_inverse) % m
    return result, f"({a} / {b}) mod {m} = ({a} × {b_inverse}) mod {m} = {result}"

def modular_multiplication(a, b, m):
    result = (a * b) % m
    return result, f"({a} × {b}) mod {m} = {result}"

def modular_addition(a, b, m):
    result = (a + b) % m
    return result, f"({a} + {b}) mod {m} = {result}"

def modular_subtraction(a, b, m):
    result = (a - b) % m
    return result, f"({a} - {b}) mod {m} = {result}"

def modular_exponentiation(base, exponent, modulus):
    if modulus == 1:
        return 0
    
    result = 1
    base = base % modulus
    
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    
    return result, f"({base}^{exponent}) mod {modulus} = {result}"

def find_modular_inverse(a, m):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd_val, x, y = extended_gcd(a, m)
    if gcd_val != 1:
        return None, f"Multiplicative inverse does not exist (gcd({a}, {m}) = {gcd_val})"
    
    inverse = (x % m + m) % m
    return inverse, f"{a}^(-1) mod {m} = {inverse}"

def validate_modular_operation(a, b, m, operation):
    if m <= 0:
        return False, "Modulus must be positive"
    
    if operation == "division" and b == 0:
        return False, "Division by zero is not allowed"
    
    if operation == "division":
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a
        
        if gcd(b, m) != 1:
            return False, f"Division not possible: gcd({b}, {m}) ≠ 1"
    
    return True, "Operation is valid"

def perform_modular_arithmetic():
    try:
        print("=== MODULAR ARITHMETIC FINDER ===")
        print("Enter the numbers for modular arithmetic:")
        
        a = int(input("Enter first number (a): "))
        b = int(input("Enter second number (b): "))
        m = int(input("Enter modulus (m): "))
        
        if m <= 0:
            print("Error: Modulus must be positive")
            return
        
        print(f"\n=== MODULAR ARITHMETIC RESULTS ===")
        print(f"Numbers: a = {a}, b = {b}, m = {m}")
        print("-" * 50)
        
        add_result, add_explanation = modular_addition(a, b, m)
        print(f"Addition: {add_explanation}")
        
        sub_result, sub_explanation = modular_subtraction(a, b, m)
        print(f"Subtraction: {sub_explanation}")
        
        mul_result, mul_explanation = modular_multiplication(a, b, m)
        print(f"Multiplication: {mul_explanation}")
        
        div_result, div_explanation = modular_division(a, b, m)
        if div_result is not None:
            print(f"Division: {div_explanation}")
        else:
            print(f"Division: {div_explanation}")
        
        exp_result, exp_explanation = modular_exponentiation(a, b, m)
        print(f"Exponentiation: {exp_explanation}")
        
        inv_result, inv_explanation = find_modular_inverse(a, m)
        if inv_result is not None:
            print(f"Inverse of {a}: {inv_explanation}")
        else:
            print(f"Inverse of {a}: {inv_explanation}")
        
        print("-" * 50)
        print("All operations completed using division method approach")
        
    except ValueError:
        print("Please enter valid integers")

def test_modular_properties():
    try:
        print("=== MODULAR ARITHMETIC PROPERTY TESTER ===")
        print("Enter numbers to test modular properties:")
        
        a = int(input("Enter number a: "))
        b = int(input("Enter number b: "))
        c = int(input("Enter number c: "))
        m = int(input("Enter modulus m: "))
        
        if m <= 0:
            print("Error: Modulus must be positive")
            return
        
        print(f"\n=== MODULAR PROPERTY VALIDATION ===")
        print(f"Testing with: a = {a}, b = {b}, c = {c}, m = {m}")
        print("-" * 60)
        
        left_assoc = ((a + b) % m + c) % m
        right_assoc = (a + (b + c) % m) % m
        print(f"Associative (Addition): ({a} + {b}) + {c} ≡ {a} + ({b} + {c}) (mod {m})")
        print(f"  Left: {left_assoc}, Right: {right_assoc}, Valid: {left_assoc == right_assoc}")
        
        left_comm = (a + b) % m
        right_comm = (b + a) % m
        print(f"Commutative (Addition): {a} + {b} ≡ {b} + {a} (mod {m})")
        print(f"  Left: {left_comm}, Right: {right_comm}, Valid: {left_comm == right_comm}")
        
        left_dist = (a * ((b + c) % m)) % m
        right_dist = ((a * b) % m + (a * c) % m) % m
        print(f"Distributive: {a} × ({b} + {c}) ≡ ({a} × {b}) + ({a} × {c}) (mod {m})")
        print(f"  Left: {left_dist}, Right: {right_dist}, Valid: {left_dist == right_dist}")
        
        inv_result, inv_explanation = find_modular_inverse(a, m)
        if inv_result is not None:
            verification = (a * inv_result) % m
            print(f"Inverse Property: {a} × {inv_result} ≡ {verification} (mod {m})")
            print(f"  Valid: {verification == 1}")
        else:
            print(f"Inverse Property: {inv_explanation}")
        
        print("-" * 60)
        print("All modular arithmetic properties tested successfully")
        
    except ValueError:
        print("Please enter valid integers")

def find_modular_remainders():
    try:
        print("=== MODULAR REMAINDER FINDER ===")
        print("Enter parameters for remainder analysis:")
        
        start = int(input("Enter start number: "))
        end = int(input("Enter end number: "))
        m = int(input("Enter modulus m: "))
        
        if m <= 0:
            print("Error: Modulus must be positive")
            return
        
        if start > end:
            print("Error: Start number must be less than or equal to end number")
            return
        
        print(f"\n=== MODULAR REMAINDERS ===")
        print(f"Numbers from {start} to {end} modulo {m}")
        print("-" * 40)
        
        remainders = {}
        for num in range(start, end + 1):
            remainder = num % m
            if remainder not in remainders:
                remainders[remainder] = []
            remainders[remainder].append(num)
        
        for remainder in sorted(remainders.keys()):
            numbers = remainders[remainder]
            print(f"Remainder {remainder}: {numbers}")
        
        print("-" * 40)
        print(f"Total unique remainders: {len(remainders)}")
        print(f"Remainder distribution: {[len(numbers) for numbers in remainders.values()]}")
        
    except ValueError:
        print("Please enter valid integers")

if __name__ == "__main__":
    perform_modular_arithmetic()

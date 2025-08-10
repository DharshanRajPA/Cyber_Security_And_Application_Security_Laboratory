def euclidean_algorithm(a, b):
    if a == 0 and b == 0:
        return None, "Both numbers cannot be zero"
    
    if a == 0:
        return abs(b), f"GCD({a}, {b}) = {abs(b)} (since {a} = 0)"
    
    if b == 0:
        return abs(a), f"GCD({a}, {b}) = {abs(a)} (since {b} = 0)"
    
    a, b = abs(a), abs(b)
    if a < b:
        a, b = b, a
    
    original_a, original_b = a, b
    steps = []
    
    while b != 0:
        quotient = a // b
        remainder = a % b
        steps.append({
            'a': a,
            'b': b,
            'quotient': quotient,
            'remainder': remainder,
            'equation': f"{a} = {b} × {quotient} + {remainder}"
        })
        a, b = b, remainder
    
    gcd = a
    return gcd, steps, f"GCD({original_a}, {original_b}) = {gcd}"

def extended_euclidean_algorithm(a, b):
    if a == 0 and b == 0:
        return None, "Both numbers cannot be zero"
    
    if a == 0:
        return (abs(b), 0, 1), f"Extended GCD({a}, {b}) = ({abs(b)}, 0, 1)"
    
    if b == 0:
        return (abs(a), 1, 0), f"Extended GCD({a}, {b}) = ({abs(a)}, 1, 0)"
    
    a, b = abs(a), abs(b)
    if a < b:
        a, b = b, a
    
    original_a, original_b = a, b
    steps = []
    
    r_prev, r_curr = a, b
    s_prev, s_curr = 1, 0
    t_prev, t_curr = 0, 1
    
    while r_curr != 0:
        quotient = r_prev // r_curr
        remainder = r_prev % r_curr
        
        steps.append({
            'r_prev': r_prev,
            'r_curr': r_curr,
            'quotient': quotient,
            'remainder': remainder,
            's_prev': s_prev,
            's_curr': s_curr,
            't_prev': t_prev,
            't_curr': t_curr,
            'equation': f"{r_prev} = {r_curr} × {quotient} + {remainder}"
        })
        
        r_next = remainder
        s_next = s_prev - quotient * s_curr
        t_next = t_prev - quotient * t_curr
        
        r_prev, r_curr = r_curr, r_next
        s_prev, s_curr = s_curr, s_next
        t_prev, t_curr = t_curr, t_next
    
    gcd = r_prev
    x, y = s_prev, t_prev
    
    return (gcd, x, y), steps, f"Extended GCD({original_a}, {original_b}) = ({gcd}, {x}, {y})"

def verify_gcd(a, b, gcd):
    if gcd is None:
        return False, "GCD is None"
    
    if a == 0 and b == 0:
        return gcd == 0, f"Both numbers are 0, GCD should be 0, got {gcd}"
    
    if a == 0:
        expected = abs(b)
        return gcd == expected, f"Expected GCD = {expected}, got {gcd}"
    
    if b == 0:
        expected = abs(a)
        return gcd == expected, f"Expected GCD = {expected}, got {gcd}"
    
    if a % gcd != 0 or b % gcd != 0:
        return False, f"{gcd} does not divide both {a} and {b}"
    
    for i in range(gcd + 1, min(abs(a), abs(b)) + 1):
        if a % i == 0 and b % i == 0:
            return False, f"{i} is a larger common divisor than {gcd}"
    
    return True, f"GCD({a}, {b}) = {gcd} is verified correctly"

def test_euclidean_properties(a, b):
    if a == 0 and b == 0:
        return "Cannot test properties with both numbers zero"
    
    a, b = abs(a), abs(b)
    gcd, steps, explanation = euclidean_algorithm(a, b)
    
    if gcd is None:
        return "Cannot test properties with invalid GCD"
    
    properties = []
    
    if a % gcd == 0 and b % gcd == 0:
        properties.append(f"✓ {gcd} divides both {a} and {b}")
    else:
        properties.append(f"✗ {gcd} does not divide both numbers")
    
    if a == 0 or b == 0:
        properties.append("✓ One number is zero, GCD is the other number")
    else:
        co_prime = gcd == 1
        properties.append(f"{'✓' if co_prime else '✗'} Numbers are {'coprime' if co_prime else 'not coprime'}")
    
    if a != 0 and b != 0:
        lcm = (a * b) // gcd
        properties.append(f"✓ LCM({a}, {b}) = {lcm}")
        properties.append(f"✓ GCD × LCM = {gcd} × {lcm} = {gcd * lcm}")
        properties.append(f"✓ Product of numbers = {a} × {b} = {a * b}")
        properties.append(f"✓ GCD × LCM = Product: {gcd * lcm == a * b}")
    
    return properties

def find_euclidean_algorithm():
    try:
        print("=== EUCLIDEAN ALGORITHM FINDER ===")
        print("Finding GCD using division method approach")
        print("-" * 50)
        
        a = int(input("Enter first number (a): "))
        b = int(input("Enter second number (b): "))
        
        print(f"\n=== EUCLIDEAN ALGORITHM RESULTS ===")
        print(f"Numbers: a = {a}, b = {b}")
        print("-" * 50)
        
        gcd, steps, explanation = euclidean_algorithm(a, b)
        
        if gcd is None:
            print(f"Error: {explanation}")
            return
        
        print(f"GCD({a}, {b}) = {gcd}")
        print(f"Explanation: {explanation}")
        
        if isinstance(steps, list) and len(steps) > 0:
            print(f"\n=== DIVISION METHOD STEPS ===")
            for i, step in enumerate(steps, 1):
                print(f"Step {i}: {step['equation']}")
                print(f"  Quotient: {step['quotient']}, Remainder: {step['remainder']}")
            
            print(f"\nTotal steps: {len(steps)}")
        
        print(f"\n=== VERIFICATION ===")
        is_valid, verification_msg = verify_gcd(a, b, gcd)
        print(f"Verification: {verification_msg}")
        
        print(f"\n=== PROPERTY TESTING ===")
        properties = test_euclidean_properties(a, b)
        for prop in properties:
            print(f"  {prop}")
        
        print("-" * 50)
        print("Euclidean Algorithm completed using division method approach")
        
    except ValueError:
        print("Please enter valid integers")

def test_extended_euclidean():
    try:
        print("=== EXTENDED EUCLIDEAN ALGORITHM TESTER ===")
        print("Finding extended GCD (gcd, x, y) where ax + by = gcd")
        print("-" * 60)
        
        a = int(input("Enter first number (a): "))
        b = int(input("Enter second number (b): "))
        
        print(f"\n=== EXTENDED EUCLIDEAN RESULTS ===")
        print(f"Numbers: a = {a}, b = {b}")
        print("-" * 60)
        
        result, steps, explanation = extended_euclidean_algorithm(a, b)
        
        if result is None:
            print(f"Error: {explanation}")
            return
        
        gcd, x, y = result
        print(f"Extended GCD({a}, {b}) = ({gcd}, {x}, {y})")
        print(f"Explanation: {explanation}")
        
        verification = a * x + b * y
        print(f"\n=== VERIFICATION ===")
        print(f"Verifying: {a} × {x} + {b} × {y} = {verification}")
        print(f"Expected: {gcd}, Got: {verification}")
        print(f"Verification: {'✓ PASS' if verification == gcd else '✗ FAIL'}")
        
        if isinstance(steps, list) and len(steps) > 0:
            print(f"\n=== EXTENDED ALGORITHM STEPS ===")
            for i, step in enumerate(steps, 1):
                print(f"Step {i}: {step['equation']}")
                print(f"  r_prev={step['r_prev']}, r_curr={step['r_curr']}")
                print(f"  s_prev={step['s_prev']}, s_curr={step['s_curr']}")
                print(f"  t_prev={step['t_prev']}, t_curr={step['t_curr']}")
        
        print("-" * 60)
        print("Extended Euclidean Algorithm completed successfully")
        
    except ValueError:
        print("Please enter valid integers")

def analyze_euclidean_complexity():
    try:
        print("=== EUCLIDEAN ALGORITHM COMPLEXITY ANALYZER ===")
        print("Analyzing time complexity and efficiency")
        print("-" * 60)
        
        a = int(input("Enter first number (a): "))
        b = int(input("Enter second number (b): "))
        
        if a == 0 and b == 0:
            print("Cannot analyze complexity with both numbers zero")
            return
        
        a, b = abs(a), abs(b)
        if a < b:
            a, b = b, a
        
        print(f"\n=== COMPLEXITY ANALYSIS ===")
        print(f"Numbers: a = {a}, b = {b}")
        print("-" * 60)
        
        gcd, steps, explanation = euclidean_algorithm(a, b)
        
        if gcd is None:
            print(f"Error: {explanation}")
            return
        
        num_steps = len(steps) if isinstance(steps, list) else 0
        
        print(f"GCD: {gcd}")
        print(f"Number of division steps: {num_steps}")
        print(f"Largest number: {max(a, b)}")
        print(f"Smallest number: {min(a, b)}")
        
        if num_steps > 0:
            print(f"\n=== COMPLEXITY ESTIMATES ===")
            print(f"Worst case: O(log(min(a,b)))")
            print(f"Average case: O(log(min(a,b)))")
            print(f"Best case: O(1) when one number divides the other")
            
            if b != 0:
                ratio = a / b
                print(f"Ratio a/b: {ratio:.2f}")
                if ratio > 10:
                    print("High ratio indicates potential for many steps")
                elif ratio < 2:
                    print("Low ratio suggests efficient convergence")
        
        print(f"\n=== EFFICIENCY METRICS ===")
        if num_steps > 0:
            efficiency = f"{num_steps} steps for numbers of size {len(str(max(a, b)))} digits"
            print(f"Efficiency: {efficiency}")
            
            if num_steps <= 5:
                print("✓ Very efficient execution")
            elif num_steps <= 10:
                print("✓ Moderately efficient execution")
            else:
                print("⚠ Many steps required (consider using larger numbers)")
        
        print("-" * 60)
        print("Complexity analysis completed")
        
    except ValueError:
        print("Please enter valid integers")

if __name__ == "__main__":
    find_euclidean_algorithm()

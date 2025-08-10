def get_factors(number):
    factors = []
    for i in range(1, abs(number) + 1):
        if abs(number) % i == 0:
            factors.append(i)
    return factors

def gcd_tabulation_method(num1, num2):
    if num1 == 0 and num2 == 0:
        return None
    
    factors1 = get_factors(num1)
    factors2 = get_factors(num2)
    
    common_factors = []
    for factor in factors1:
        if factor in factors2:
            common_factors.append(factor)
    
    if not common_factors:
        return 1
    
    return max(common_factors)

def find_gcd_tabulation():
    try:
        num1 = int(input("Enter first number: "))
        num2 = int(input("Enter second number: "))
        
        if num1 == 0 and num2 == 0:
            print("GCD of 0 and 0 is undefined")
            return
            
        result = gcd_tabulation_method(num1, num2)
        print(f"GCD of {num1} and {num2} is: {result}")
        
    except ValueError:
        print("Please enter valid integers")

if __name__ == "__main__":
    find_gcd_tabulation()

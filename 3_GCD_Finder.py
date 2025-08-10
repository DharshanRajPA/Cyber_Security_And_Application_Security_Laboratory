def gcd_division_method(a, b):
    while b:
        a, b = b, a % b
    return a

def find_gcd():
    try:
        num1 = int(input("Enter first number: "))
        num2 = int(input("Enter second number: "))
        
        if num1 == 0 and num2 == 0:
            print("GCD of 0 and 0 is undefined")
            return
            
        result = gcd_division_method(abs(num1), abs(num2))
        print(f"GCD of {num1} and {num2} is: {result}")
        
    except ValueError:
        print("Please enter valid integers")

if __name__ == "__main__":
    find_gcd()

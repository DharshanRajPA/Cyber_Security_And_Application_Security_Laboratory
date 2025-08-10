def calculate_modulus(dividend, divisor):
    if divisor == 0:
        return None
    return dividend % divisor

def find_modulus():
    try:
        dividend = int(input("Enter dividend: "))
        divisor = int(input("Enter divisor: "))
        
        if divisor == 0:
            print("Error: Division by zero is not allowed")
            return
            
        result = calculate_modulus(dividend, divisor)
        print(f"{dividend} % {divisor} = {result}")
        
    except ValueError:
        print("Please enter valid integers")

if __name__ == "__main__":
    find_modulus()

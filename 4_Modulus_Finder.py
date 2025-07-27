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

def main():
    while True:
        print("\n=== MODULUS CALCULATOR ===")
        print("1. Calculate modulus of two numbers")
        print("2. Exit")
        
        choice = input("Enter choice (1 or 2): ")
        
        if choice == '1':
            find_modulus()
        elif choice == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()

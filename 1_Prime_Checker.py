def is_prime(number):
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    
    for i in range(3, int(number ** 0.5) + 1, 2):
        if number % i == 0:
            return False
    return True

def check_prime():
    try:
        num = int(input("Enter a number: "))
        if is_prime(num):
            print(f"{num} is prime")
        else:
            print(f"{num} is not prime")
    except ValueError:
        print("Please enter a valid number")

def main():
    while True:
        print("\n=== PRIME NUMBER CHECKER ===")
        print("1. Check if number is prime")
        print("2. Exit")
        
        choice = input("Enter choice (1 or 2): ")
        
        if choice == '1':
            check_prime()
        elif choice == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()

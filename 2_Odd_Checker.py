def is_odd(number):
    return number % 2 != 0

def check_odd():
    try:
        num = int(input("Enter a number: "))
        if is_odd(num):
            print(f"{num} is odd")
        else:
            print(f"{num} is even")
    except ValueError:
        print("Please enter a valid number")

def main():
    while True:
        print("\n=== ODD NUMBER CHECKER ===")
        print("1. Check if number is odd")
        print("2. Exit")
        
        choice = input("Enter choice (1 or 2): ")
        
        if choice == '1':
            check_odd()
        elif choice == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()

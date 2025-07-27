def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def is_coprime(a, b):
    return gcd(a, b) == 1

def euler_totient_function(n):
    if n <= 0:
        return 0
    
    count = 0
    for i in range(1, n + 1):
        if is_coprime(i, n):
            count += 1
    
    return count

def find_euler_totient():
    try:
        n = int(input("Enter a positive integer: "))
        
        if n <= 0:
            print("Please enter a positive integer")
            return
            
        result = euler_totient_function(n)
        print(f"\nEuler's Totient Function φ({n}) = {result}")
        
        coprime_numbers = []
        for i in range(1, n + 1):
            if is_coprime(i, n):
                coprime_numbers.append(i)
        
        print(f"Numbers coprime to {n}: {coprime_numbers}")
        print(f"Total count: {len(coprime_numbers)}")
        
    except ValueError:
        print("Please enter a valid integer")

def main():
    while True:
        print("\n=== EULER'S TOTIENT FUNCTION (ETH) ===")
        print("1. Calculate Euler's Totient Function")
        print("2. Exit")
        
        choice = input("Enter choice (1 or 2): ")
        
        if choice == '1':
            find_euler_totient()
        elif choice == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main() 
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

if __name__ == "__main__":
    check_prime()

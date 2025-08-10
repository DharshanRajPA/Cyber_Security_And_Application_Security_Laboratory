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

if __name__ == "__main__":
    check_odd()

def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - ascii_offset + shift) % 26
            result += chr(shifted + ascii_offset)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def caesar_brute_force(text):
    results = []
    for shift in range(26):
        decrypted = caesar_decrypt(text, shift)
        results.append((shift, decrypted))
    return results

def encrypt_message():
    try:
        message = input("Enter the message to encrypt: ")
        shift = int(input("Enter the shift value (0-25): "))
        
        if shift < 0 or shift > 25:
            print("Shift value must be between 0 and 25")
            return
        
        encrypted = caesar_encrypt(message, shift)
        
        print(f"\n=== CAESAR CIPHER ENCRYPTION ===")
        print(f"Original message: {message}")
        print(f"Shift value: {shift}")
        print(f"Encrypted message: {encrypted}")
        
    except ValueError:
        print("Please enter a valid shift value")

def decrypt_message():
    try:
        message = input("Enter the message to decrypt: ")
        shift = int(input("Enter the shift value (0-25): "))
        
        if shift < 0 or shift > 25:
            print("Shift value must be between 0 and 25")
            return
        
        decrypted = caesar_decrypt(message, shift)
        
        print(f"\n=== CAESAR CIPHER DECRYPTION ===")
        print(f"Encrypted message: {message}")
        print(f"Shift value: {shift}")
        print(f"Decrypted message: {decrypted}")
        
    except ValueError:
        print("Please enter a valid shift value")

def brute_force_decrypt():
    try:
        message = input("Enter the encrypted message: ")
        
        print(f"\n=== BRUTE FORCE DECRYPTION ===")
        print(f"Encrypted message: {message}")
        print(f"\nAll possible decryptions:")
        print("-" * 50)
        
        results = caesar_brute_force(message)
        
        for shift, decrypted in results:
            print(f"Shift {shift:2d}: {decrypted}")
        
        print("-" * 50)
        print(f"Total possibilities: {len(results)}")
        
    except Exception as e:
        print(f"Error: {e}")

def frequency_analysis():
    try:
        message = input("Enter the encrypted message: ")
        
        print(f"\n=== FREQUENCY ANALYSIS ===")
        print(f"Encrypted message: {message}")
        
        letter_count = {}
        total_letters = 0
        
        for char in message.upper():
            if char.isalpha():
                letter_count[char] = letter_count.get(char, 0) + 1
                total_letters += 1
        
        if total_letters == 0:
            print("No letters found in the message")
            return
        
        print(f"\nLetter frequencies:")
        print("-" * 30)
        
        for letter in sorted(letter_count.keys()):
            count = letter_count[letter]
            percentage = (count / total_letters) * 100
            print(f"{letter}: {count:2d} ({percentage:5.1f}%)")
        
        print("-" * 30)
        print(f"Total letters: {total_letters}")
        
        print(f"\nMost common letters in English: E, T, A, O, I, N, S, H, R, D")
        print("Compare with the frequencies above to guess the shift")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    encrypt_message()

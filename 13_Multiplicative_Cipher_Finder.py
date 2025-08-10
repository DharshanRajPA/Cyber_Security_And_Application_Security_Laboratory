def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y

def multiplicative_inverse(a, m):
    gcd_val, x, y = extended_gcd(a, m)
    
    if gcd_val != 1:
        return None
    
    return (x % m + m) % m

def multiplicative_encrypt(text, key):
    """
    Encrypt text using multiplicative cipher
    Formula: E(x) = (x * key) mod 26
    """
    if multiplicative_inverse(key, 26) is None:
        return None, f"Key {key} is not valid (must be coprime with 26)"
    
    encrypted = ""
    for char in text:
        if char.isalpha():
            # Convert to 0-25 range
            if char.isupper():
                x = ord(char) - ord('A')
            else:
                x = ord(char) - ord('a')
            
            # Apply multiplicative cipher
            encrypted_char = (x * key) % 26
            
            # Convert back to character
            if char.isupper():
                encrypted += chr(encrypted_char + ord('A'))
            else:
                encrypted += chr(encrypted_char + ord('a'))
        else:
            encrypted += char
    
    return encrypted, None

def multiplicative_decrypt(text, key):
    """
    Decrypt text using multiplicative cipher
    Formula: D(x) = (x * key^(-1)) mod 26
    """
    key_inverse = multiplicative_inverse(key, 26)
    if key_inverse is None:
        return None, f"Key {key} is not valid (must be coprime with 26)"
    
    decrypted = ""
    for char in text:
        if char.isalpha():
            # Convert to 0-25 range
            if char.isupper():
                x = ord(char) - ord('A')
            else:
                x = ord(char) - ord('a')
            
            # Apply multiplicative cipher decryption
            decrypted_char = (x * key_inverse) % 26
            
            # Convert back to character
            if char.isupper():
                decrypted += chr(decrypted_char + ord('A'))
            else:
                decrypted += chr(decrypted_char + ord('a'))
        else:
            decrypted += char
    
    return decrypted, None

def get_valid_keys():
    """
    Get all valid keys for multiplicative cipher (coprime with 26)
    """
    valid_keys = []
    for key in range(1, 26):
        if multiplicative_inverse(key, 26) is not None:
            valid_keys.append(key)
    return valid_keys

def multiplicative_brute_force(text):
    """
    Try all valid keys to decrypt the text
    """
    valid_keys = get_valid_keys()
    results = []
    
    for key in valid_keys:
        decrypted, error = multiplicative_decrypt(text, key)
        if error is None:
            results.append((key, decrypted))
    
    return results

def encrypt_message():
    try:
        message = input("Enter the message to encrypt: ")
        key = int(input("Enter the multiplicative key (1-25, must be coprime with 26): "))
        
        if key < 1 or key > 25:
            print("Key must be between 1 and 25")
            return
        
        encrypted, error = multiplicative_encrypt(message, key)
        
        if error:
            print(f"Error: {error}")
            print("Valid keys are:", get_valid_keys())
            return
        
        print(f"\n=== MULTIPLICATIVE CIPHER ENCRYPTION ===")
        print(f"Original message: {message}")
        print(f"Multiplicative key: {key}")
        print(f"Encrypted message: {encrypted}")
        
        # Show the mathematical process
        print(f"\nMathematical process:")
        print(f"E(x) = (x × {key}) mod 26")
        
    except ValueError:
        print("Please enter a valid key")

def decrypt_message():
    try:
        message = input("Enter the message to decrypt: ")
        key = int(input("Enter the multiplicative key (1-25, must be coprime with 26): "))
        
        if key < 1 or key > 25:
            print("Key must be between 1 and 25")
            return
        
        decrypted, error = multiplicative_decrypt(message, key)
        
        if error:
            print(f"Error: {error}")
            print("Valid keys are:", get_valid_keys())
            return
        
        print(f"\n=== MULTIPLICATIVE CIPHER DECRYPTION ===")
        print(f"Encrypted message: {message}")
        print(f"Multiplicative key: {key}")
        print(f"Decrypted message: {decrypted}")
        
        # Show the mathematical process
        key_inverse = multiplicative_inverse(key, 26)
        print(f"\nMathematical process:")
        print(f"D(x) = (x × {key_inverse}) mod 26")
        print(f"Where {key_inverse} is the multiplicative inverse of {key} modulo 26")
        
    except ValueError:
        print("Please enter a valid key")

def brute_force_decrypt():
    try:
        message = input("Enter the encrypted message: ")
        
        print(f"\n=== BRUTE FORCE DECRYPTION ===")
        print(f"Encrypted message: {message}")
        print(f"\nTrying all valid keys:")
        print("-" * 60)
        
        results = multiplicative_brute_force(message)
        
        for key, decrypted in results:
            print(f"Key {key:2d}: {decrypted}")
        
        print("-" * 60)
        print(f"Total valid keys tried: {len(results)}")
        print(f"Valid keys: {get_valid_keys()}")
        
    except Exception as e:
        print(f"Error: {e}")

def analyze_cipher():
    try:
        print("=== MULTIPLICATIVE CIPHER ANALYSIS ===")
        print(f"Valid keys (coprime with 26): {get_valid_keys()}")
        print(f"Total valid keys: {len(get_valid_keys())}")
        
        print(f"\nKey properties:")
        for key in get_valid_keys():
            inverse = multiplicative_inverse(key, 26)
            print(f"Key {key:2d}: Inverse = {inverse:2d}, Verification: {key} × {inverse} ≡ {(key * inverse) % 26} (mod 26)")
        
        print(f"\nMathematical properties:")
        print("- Multiplicative cipher: E(x) = (x × key) mod 26")
        print("- Decryption: D(x) = (x × key^(-1)) mod 26")
        print("- Only keys coprime with 26 are valid")
        print("- Valid keys: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=== MULTIPLICATIVE CIPHER CRYPTOGRAPHY ===")
    print("1. Encrypt a message")
    print("2. Decrypt a message")
    print("3. Brute force decryption")
    print("4. Analyze cipher properties")
    choice = input("Enter choice (1-4): ")
    
    if choice == '1':
        encrypt_message()
    elif choice == '2':
        decrypt_message()
    elif choice == '3':
        brute_force_decrypt()
    elif choice == '4':
        analyze_cipher()
    else:
        print("Invalid choice. Running encryption by default.")
        encrypt_message()

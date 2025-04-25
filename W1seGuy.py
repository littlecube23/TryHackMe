def hex_to_bytes(hex_str):
    """Converts a hex string to bytes."""
    return bytes.fromhex(hex_str)

def recover_key(encoded_text, plaintext_start, plaintext_end):
    """Recovers parts of the key by XORing known parts of the plaintext with the encrypted text."""
    
    # Convert the encoded hex string into a byte array
    encrypted_bytes = hex_to_bytes(encoded_text)
    
    # Convert the known start and end of the plaintext into byte arrays
    start_bytes = plaintext_start.encode()
    end_bytes = plaintext_end.encode()

    # Initialize an empty list to store key bytes
    key_bytes = []
    
    # Recover key bytes from the beginning of the plaintext
    for i in range(len(start_bytes)):
        # XOR each encrypted byte with the corresponding plaintext byte
        key_byte = encrypted_bytes[i] ^ start_bytes[i]
        key_bytes.append(key_byte)

    # Recover key bytes from the end of the plaintext
    for i in range(len(end_bytes)):
        # Calculate position from the end
        enc_index = -(len(end_bytes) - i)
        plain_index = -(len(end_bytes) - i)
        
        # XOR the end of the encrypted text with the end of the known plaintext
        key_byte = encrypted_bytes[enc_index] ^ end_bytes[plain_index]
        key_bytes.append(key_byte)

    # Return raw key bytes
    return bytes(key_bytes)

# Prompt the user to enter the XOR-encoded hex string
encoded_text = input("Please enter the XOR encoded text: ")

# Define the known start of the plaintext (e.g. beginning of the flag)
plaintext_start = "THM{"

# Define the known end of the plaintext (e.g. closing brace of the flag)
plaintext_end = "}"

# Recover the key bytes by XORing known plaintext with the encrypted text
key_bytes = recover_key(encoded_text, plaintext_start, plaintext_end)

# Convert and print the key in hexadecimal format
key_hex = ''.join(f'{b:02x}' for b in key_bytes)
print("Recovered Key (Hex):", key_hex)

# Convert and print the ASCII representation (show dot for non-printable characters)
key_ascii = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in key_bytes)
print("Recovered Key (ASCII):", key_ascii)

import logging
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os
import sys

logging.basicConfig(level=logging.DEBUG)

def encrypt_file(file_path, encryption_key):
    try:
        iv = get_random_bytes(AES.block_size)  
        cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
        with open(file_path, 'rb') as f:
            plaintext = f.read()
        padded_plaintext = pad(plaintext, AES.block_size)
        ciphertext = cipher.encrypt(padded_plaintext)
        encrypted_file_path = file_path + '.enc'  
        with open(encrypted_file_path, 'wb') as f:
            f.write(iv + ciphertext)
        os.remove(file_path)
        logging.info(f"File '{file_path}' encrypted successfully.")
    except Exception as e:
        logging.error(f"Error encrypting '{file_path}': {e}")

def decrypt_file(file_path, encryption_key):
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
        iv = file_content[:AES.block_size]
        ciphertext = file_content[AES.block_size:]
        cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext = unpad(padded_plaintext, AES.block_size)
        original_file_path = file_path[:-4]  
        with open(original_file_path, 'wb') as f:
            f.write(plaintext)
        os.remove(file_path)
        logging.info(f"File '{file_path}' decrypted successfully.")
    except Exception as e:
        logging.error(f"Error decrypting '{file_path}': {e}")

def encrypt_directory(directory, encryption_key):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            encrypt_file(file_path, encryption_key)

def decrypt_directory(directory, encryption_key):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.enc'):  
                file_path = os.path.join(root, file_name)
                decrypt_file(file_path, encryption_key)

def main():
    
    action = 'encrypt'
    directory = './critical'
    key='qwerty1234!@#$%^'
    
    if len(key) != 16:
        print("Key must be 16 bytes long.")
        return

    if action in ['encrypt', 'decrypt']:
        if action == 'encrypt':
            encrypt_directory(directory, key.encode())
        else:
            decrypt_directory(directory, key.encode())
    else:
        print("Invalid action. Please choose either 'encrypt' or 'decrypt'.")

if __name__ == "__main__":
    main()

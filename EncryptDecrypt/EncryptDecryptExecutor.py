import sys
from Encrypt import encrypt
from Decrypt import decrypt

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python EncryptDecryptExecutor.py <Encrypt|Decrypt> <input>")
    
    command = sys.argv[1]
    input_data = sys.argv[2] if len(sys.argv) > 2 else ""
    
    if command == "Encrypt":
        encrypt(input_data)
    elif command == "Decrypt":
        decrypt(input_data)
    else:
        # do nothing
        pass

from EncryptAndDecryptUtil import EncryptAndDecryptUtil

def decrypt(encrypted_data_text):
    try:
        # print(f"Decrypting data: {encrypted_data_text}")  # Debugging step
        decrypted_text = EncryptAndDecryptUtil.decrypt(encrypted_data_text)
        print(f"Encrypted Message : {encrypted_data_text}")
        print(f"Decrypted Message : {decrypted_text}")
    except Exception as e:
        print(f"Error during decryption: {e}")



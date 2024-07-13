from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64

class EncryptAndDecryptUtil:
    SECRET_KEY = b'4{2Laj*!<X^3$]0K|pvth`.8w;nyD[Ug'

    @staticmethod
    def encrypt(plain_text):
        key = EncryptAndDecryptUtil.SECRET_KEY
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plain_text.encode()) + padder.finalize()
        # print(f"Padded data: {padded_data}")  # Debugging step

        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        encoded_data = base64.b64encode(encrypted_data).decode('utf-8')
        # print(f"Encrypted data (base64): {encoded_data}")  # Debugging step
        return encoded_data

    @staticmethod
    def decrypt(encrypted_data):
        key = EncryptAndDecryptUtil.SECRET_KEY
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()

        encrypted_data_bytes = base64.b64decode(encrypted_data)
        # print(f"Encrypted data bytes: {encrypted_data_bytes}")  # Debugging step
        decrypted_data = decryptor.update(encrypted_data_bytes) + decryptor.finalize()
        # print(f"Decrypted data (before unpadding): {decrypted_data}")  # Debugging step

        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
        # print(f"Unpadded data: {unpadded_data}")  # Debugging step

        return unpadded_data.decode('utf-8')

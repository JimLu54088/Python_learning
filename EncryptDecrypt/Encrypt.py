import base64
from EncryptAndDecryptUtil import EncryptAndDecryptUtil  # 假设 EncryptAndDecryptUtil.py 包含了加密函数

def encrypt(plain_text):
    try:
        # 调用加密函数
        encrypted_data = EncryptAndDecryptUtil.encrypt(plain_text)

        # 输出原始消息和加密后的消息
        print(f"Original Message : {plain_text}")
        print(f"Encrypted Message : {encrypted_data}")

    except Exception as e:
        print(f"Error during encryption: {e}")

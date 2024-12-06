import base64
import zlib

from security import cipher_suite

def encrypt_text(text: str):
    if text:
        return cipher_suite.encrypt(text.encode())
    else:
        return None

def decrypt_text(encrypted_text: bytes):
    decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
    if decrypted_text == 'None':
        return None
    else:
        return decrypted_text


def encrypt_data_64(data: str):
    compressed_data = zlib.compress(data.encode())
    encrypted_data = cipher_suite.encrypt(compressed_data)
    encrypted_base64 = base64.urlsafe_b64encode(encrypted_data).decode()
    return encrypted_base64[:54]

def decrypt_data_64(data: str):
    encrypt_data = base64.urlsafe_b64decode(data)
    decrypted_data = cipher_suite.decrypt(encrypt_data)
    decompressed_data = zlib.decompress(decrypted_data).decode()
    return decompressed_data

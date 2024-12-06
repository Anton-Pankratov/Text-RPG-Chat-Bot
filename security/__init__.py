from cryptography.fernet import Fernet

from src.properties import CIPHER_KEY_FILE_NAME

with open(CIPHER_KEY_FILE_NAME, "rb") as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)
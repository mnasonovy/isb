from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

def encrypt_data(settings):
    with open(settings['initial_file'], 'rb') as f:
        data = f.read()

    with open(settings['symmetric_key'], 'rb') as key_file:
        symmetric_key = key_file.read()

    padder = padding.ANSIX923(algorithms.Blowfish.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    iv = os.urandom(algorithms.Blowfish.block_size // 8)
    cipher = Cipher(algorithms.Blowfish(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    with open(settings['encrypted_file'], 'wb') as f:
        f.write(iv + encrypted_data)

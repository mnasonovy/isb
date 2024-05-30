import os

from typing import Dict
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def encrypt_data(initial_file: str, symmetric_key_file: str, encrypted_file: str) -> None:
    """
    Encrypts a file using the Blowfish algorithm in CBC mode.

    Args:
        initial_file (str): Path to the file containing the data to be encrypted.
        symmetric_key_file (str): Path to the file containing the symmetric key.
        encrypted_file (str): Path where the encrypted data will be saved.

    Raises:
        FileNotFoundError: If any of the files specified do not exist.
        ValueError: If the encryption process encounters an error (e.g., invalid key).
    """
    try:
        with open(initial_file, 'rb') as f:
            data = f.read()

        with open(symmetric_key_file, 'rb') as key_file:
            symmetric_key = key_file.read()

        padder = padding.ANSIX923(algorithms.Blowfish.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()

        iv = os.urandom(algorithms.Blowfish.block_size // 8)
        cipher = Cipher(algorithms.Blowfish(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        with open(encrypted_file, 'wb') as f:
            f.write(iv + encrypted_data)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {str(e)}")
    except Exception as e:
        raise ValueError(f"Encryption error: {str(e)}")

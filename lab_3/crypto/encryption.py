import os


from typing import Dict
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def encrypt_data(settings: Dict[str, str]) -> None:
    """
    Encrypts a file using the Blowfish algorithm in CBC mode.

    Args:
        settings (Dict[str, str]): A dictionary containing the paths for the 
                                   initial file, symmetric key file, and 
                                   the output file for encrypted data.
            - 'initial_file': Path to the file containing the data to be encrypted.
            - 'symmetric_key': Path to the file containing the symmetric key.
            - 'encrypted_file': Path where the encrypted data will be saved.

    Raises:
        FileNotFoundError: If any of the files specified in the settings do not exist.
        ValueError: If the encryption process encounters an error (e.g., invalid key).
    """
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

from typing import Dict
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def decrypt_data(settings: Dict[str, str]) -> None:
    """
    Decrypts a file encrypted with Blowfish algorithm in CBC mode.

    Args:
        settings (Dict[str, str]): A dictionary containing the paths for the 
                                   encrypted file, symmetric key file, and 
                                   the output file for decrypted data.
            - 'encrypted_file': Path to the file containing encrypted data.
            - 'symmetric_key': Path to the file containing the symmetric key.
            - 'decrypted_file': Path where the decrypted data will be saved.

    Raises:
        FileNotFoundError: If any of the files specified in the settings do not exist.
        ValueError: If the decryption process encounters an error (e.g., wrong key or corrupted data).
    """
    with open(settings['encrypted_file'], 'rb') as f:
        iv = f.read(algorithms.Blowfish.block_size // 8)
        encrypted_data = f.read()

    with open(settings['symmetric_key'], 'rb') as key_file:
        symmetric_key = key_file.read()

    cipher = Cipher(algorithms.Blowfish(symmetric_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.ANSIX923(algorithms.Blowfish.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    with open(settings['decrypted_file'], 'wb') as f:
        f.write(data)

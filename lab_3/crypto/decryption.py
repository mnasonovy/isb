from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def decrypt_data(settings):
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

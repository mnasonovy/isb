import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def generate_keys(settings):
    key_length = settings['key_length']
    if key_length < 32 or key_length > 448 or key_length % 8 != 0:
        raise ValueError("Key length must be between 32 and 448 bits, in multiples of 8.")
    symmetric_key = os.urandom(key_length // 8)
    with open(settings['symmetric_key'], 'wb') as key_file:
        key_file.write(symmetric_key)

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    with open(settings['public_key'], 'wb') as public_out:
        public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                  format=serialization.PublicFormat.SubjectPublicKeyInfo))

    with open(settings['private_key'], 'wb') as private_out:
        private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                    encryption_algorithm=serialization.NoEncryption()))

    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    with open(settings['symmetric_key_encrypted'], 'wb') as key_file:
        key_file.write(encrypted_symmetric_key)

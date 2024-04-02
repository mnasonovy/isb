import json
import os


def generate_cipher_key(shift, filename):
    alphabet = list('абвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
    shifted_alphabet = alphabet[shift % len(alphabet):] + alphabet[:shift % len(alphabet)]
    cipher_key = dict(zip(alphabet, shifted_alphabet))
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(cipher_key, file, ensure_ascii=False)
    return {'original_alphabet': alphabet, 'shifted_alphabet': shifted_alphabet}

def encrypt_text(input_file, output_file, cipher_key_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    with open(cipher_key_file, 'r', encoding='utf-8') as file:
        cipher_key = json.load(file)
    encrypted_text = ''
    for char in text:
        encrypted_text += cipher_key.get(char, char)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(encrypted_text)
        
with open(os.path.join('First task', 'settings.json'), 'r') as settings:
        settings = json.load(settings)
cipher_key = generate_cipher_key(settings['shift'], settings['random_key'])
encrypt_text(settings['sourse_text'], settings['encrypted text'], settings['random_key'])

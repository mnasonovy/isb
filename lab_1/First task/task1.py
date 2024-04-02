import json
import os


def generate_cipher_key(shift, filename):
    # Генерация ключа шифрования для алфавита с учетом сдвига
    alphabet = list('абвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
    shifted_alphabet = alphabet[shift % len(alphabet):] + alphabet[:shift % len(alphabet)]
    cipher_key = dict(zip(alphabet, shifted_alphabet))
    
    # Сохранение ключа в JSON файл
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(cipher_key, file, ensure_ascii=False)
    
    # Возвращаем ключ
    return {'original_alphabet': alphabet, 'shifted_alphabet': shifted_alphabet}

with open(os.path.join('First task', 'settings.json'), 'r') as settings:
        settings = json.load(settings)
cipher_key = generate_cipher_key(settings['shift'], settings['random_key'])


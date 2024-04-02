import json
import os

def generate_cipher_key(shift, filename):
    alphabet = list(settings['alphabet'])
    shifted_alphabet = alphabet[shift % len(alphabet):] + alphabet[:shift % len(alphabet)]
    cipher_key = dict(zip(alphabet, shifted_alphabet))
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(cipher_key, file, ensure_ascii=False)
    return {'original_alphabet': alphabet, 'shifted_alphabet': shifted_alphabet}

def process_text(input_file, output_file, cipher_key_file, mode):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    with open(cipher_key_file, 'r', encoding='utf-8') as file:
        cipher_key = json.load(file)

    match mode:
        case "encrypt":
            processed_text = ''.join(cipher_key.get(char, char) for char in text)
        case "decrypt":
            reversed_cipher_key = {v: k for k, v in cipher_key.items()} # Создаем обратный шифр
            processed_text = ''.join(reversed_cipher_key.get(char, char) for char in text)
        case _:
            raise ValueError("Invalid mode. Choose either 'encrypt' or 'decrypt'.")

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(processed_text)
        
with open(os.path.join('First task', 'settings.json'), 'r', encoding='utf-8') as settings:
        settings = json.load(settings)
        
cipher_key = generate_cipher_key(settings['shift'], settings['random_key'])
process_text(settings['sourse_text'], settings['encrypted text'], settings['random_key'],settings['mode'],)

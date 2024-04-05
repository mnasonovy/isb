import json
import os

from typing import Any, Dict, Union

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def generate_cipher_key(shift: int, filename: str) -> Dict[str, Any]:
    """
    Generate a cipher key and save it to a file.

    Args:
        shift (int): The shift value for the cipher.
        filename (str): The filename to save the cipher key.

    Returns:
        dict: A dictionary containing the original and shifted alphabets.
    """
    shifted_alphabet = ALPHABET[shift % len(ALPHABET):] + ALPHABET[:shift % len(ALPHABET)]
    cipher_key = dict(zip(ALPHABET, shifted_alphabet))
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(cipher_key, file, ensure_ascii=False)
    return {'original_alphabet': ALPHABET, 'shifted_alphabet': shifted_alphabet}


def process_text(input_file: str, output_file: str, cipher_key_file: str, mode: str) -> None:
    """
    Process the text based on the provided mode using the cipher key.

    Args:
        input_file (str): The input text file.
        output_file (str): The output text file.
        cipher_key_file (str): The file containing the cipher key.
        mode (str): The mode of operation: 'encrypt' or 'decrypt'.

    Raises:
        ValueError: If an invalid mode is provided.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    with open(cipher_key_file, 'r', encoding='utf-8') as file:
        cipher_key = json.load(file)

    match mode:
        case "encrypt":
            processed_text = ''.join(cipher_key.get(char, char) for char in text)
        case "decrypt":
            reversed_cipher_key = {v: k for k, v in cipher_key.items()}  
            processed_text = ''.join(reversed_cipher_key.get(char, char) for char in text)
        case _:
            raise ValueError("Invalid mode. Choose either 'encrypt' or 'decrypt'.")

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(processed_text)


def main():
    # Assuming settings is defined somewhere
    with open(os.path.join('settings.json'), 'r', encoding='utf-8') as settings_file:
        settings = json.load(settings_file)

    cipher_key = generate_cipher_key(settings['shift'], settings['cipher_key_1'])
    process_text(settings['source_text_1'], settings['encrypted_text_1'], settings['cipher_key_1'], settings['mode_1'])
    process_text(settings['source_text_2'], settings['encrypted_text_2'], settings['cipher_key_2'], settings['mode_2'])


if __name__ == "__main__":
    main()
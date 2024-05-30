import hashlib
import multiprocessing

def check_card_number(hash_value, card_number):
    hashed_card_number = hashlib.sha384(card_number.encode()).hexdigest()
    return hash_value == hashed_card_number


def find_card_number(hash_value, last_four_digits, bin_prefix, num_processes):
    possible_card_numbers = (bin_prefix + str(x).zfill(9) + last_four_digits for x in range(10000))
    
    def check_card_numbers(card_numbers):
        for card_number in card_numbers:
            if check_card_number(hash_value, card_number):
                return card_number
        return None
    
    chunk_size = 1000
    chunks = [possible_card_numbers[i:i+chunk_size] for i in range(0, 10000, chunk_size)]
    
    with multiprocessing.Pool(processes=num_processes) as pool:
        result = pool.map(check_card_numbers, chunks)
    
    valid_card_numbers = [card_number for card_number in result if card_number is not None]
    
    if valid_card_numbers:
        return valid_card_numbers[0]
    else:
        return None


hash_value = "50c6b2ca7a569f006d23b3be8007dd775652c1028c2c44bbb3847008956e179e4f8cc315d8076cf97483279e44075424"
last_four_digits = "1512"
bin_prefix = "510510"


num_processes = multiprocessing.cpu_count()
card_number = find_card_number(hash_value, last_four_digits, bin_prefix, num_processes)

if card_number:
    with open("card_number.txt", "w") as file:
        file.write(card_number)
        print("Найден номер карты:", card_number)
else:
    print("Номер карты не найден.")

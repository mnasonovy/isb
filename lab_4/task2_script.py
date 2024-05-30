def luhn_algorithm(card_number):
    card_number = [int(x) for x in card_number.replace(" ", "")]  
    checksum = 0
    
    for i in range(len(card_number) - 1, -1, -1):
        digit = card_number[i]
        
        if (len(card_number) - i) % 2 == 0:
            digit *= 2
            if digit > 9:
                digit -= 9
        
        checksum += digit
    
    return checksum % 10 == 0

card_number = "4539 1488 0343 6467"

if luhn_algorithm(card_number):
    print("Номер карты корректен.")
else:
    print("Номер карты некорректен.")

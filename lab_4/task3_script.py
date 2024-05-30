import hashlib
import multiprocessing
import itertools
import time
import matplotlib.pyplot as plt

def find_collision(hash_value, last_four_digits, bin_prefix, num_processes):
    possible_card_numbers = (bin_prefix + str(x).zfill(9) + last_four_digits for x in range(10000))
    
    def check_card_number(card_number):
        hashed_card_number = hashlib.sha384(card_number.encode()).hexdigest()
        return hash_value == hashed_card_number

    start_time = time.time()
    for card_number in possible_card_numbers:
        if check_card_number(card_number):
            end_time = time.time()
            return card_number, end_time - start_time

    return None, time.time() - start_time


hash_value = "50c6b2ca7a569f006d23b3be8007dd775652c1028c2c44bbb3847008956e179e4f8cc315d8076cf97483279e44075424"
last_four_digits = "1512"
bin_prefix = "510510"


num_processes_list = list(range(1, multiprocessing.cpu_count() + int(0.5 * multiprocessing.cpu_count()) + 1))

execution_times = []
num_processes_used = []

for num_processes in num_processes_list:
    card_number, execution_time = find_collision(hash_value, last_four_digits, bin_prefix, num_processes)
    execution_times.append(execution_time)
    num_processes_used.append(num_processes)

plt.plot(num_processes_used, execution_times, marker='o')
plt.title('Зависимость времени поиска коллизии от числа процессов')
plt.xlabel('Число процессов')
plt.ylabel('Время выполнения (сек)')
plt.grid(True)
plt.show()


min_index = execution_times.index(min(execution_times))
optimal_num_processes = num_processes_used[min_index]
optimal_execution_time = execution_times[min_index]
print(f"Точка глобального минимума: {optimal_num_processes} процессов, время выполнения: {optimal_execution_time:.2f} сек")

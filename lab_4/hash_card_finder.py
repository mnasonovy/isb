import time
import multiprocessing as mp
from typing import Optional, Tuple, List
from hashlib import sha3_256
import json
import matplotlib.pyplot as plt
from utility import read_json_file, write_json_file


class Card:
    def __init__(self, last_num: str, hash_value: str, bin_list: List[str]) -> None:
        """Initialize Card object.

        Args:
            last_num (str): Last numbers of the card.
            hash_value (str): Hash value of the card.
            bin_list (List[str]): List of BINs (Bank Identification Numbers).
        """
        self.last_num = last_num
        self.hash_value = hash_value
        self.bin_list = bin_list

    def verify_card(self, bin: str, middle_number: str) -> Optional[str]:
        """Verify a card number using the provided BIN and middle number.

        Args:
            bin (str): BIN (Bank Identification Number) of the card.
            middle_number (str): Middle number to be verified.

        Returns:
            Optional[str]: Valid card number if verification is successful, else None.
        """
        middle_number = int(middle_number.zfill(6))
        card_number = f"{bin}{middle_number}{self.last_num}"
        if sha3_256(card_number.encode()).hexdigest() == self.hash_value:
            return card_number
        else:
            return None

    def bruteforce_card_number(self, cores: int) -> Tuple[Optional[str], float]:
        """Bruteforce card number using multiple processes.

        Args:
            cores (int): Number of CPU cores to utilize.

        Returns:
            Tuple[Optional[str], float]: Tuple containing found card number and time taken.
        """
        start = time.time()
        with mp.Pool(processes=cores) as pool:
            card_numbers = pool.starmap(
                self.verify_card,
                [(bin, str(mid)) for bin in self.bin_list for mid in range(1000000)],
            )
            for card_number in card_numbers:
                if card_number is not None:
                    return card_number, time.time() - start
        return None, time.time() - start

    def performance_test(self) -> Tuple[List[int], List[float], Tuple[int, float]]:
        """Test performance of the bruteforce algorithm with varying number of cores.

        Returns:
            Tuple[List[int], List[float], Tuple[int, float]]: Tuple containing core counts, results,
            and minimum cores time.
        """
        results = []
        core_counts = list(range(1, int(mp.cpu_count() * 1.5) + 1))
        for cores in core_counts:
            _, time_taken = self.bruteforce_card_number(cores)
            results.append(time_taken)
        min_time = min(results)
        min_cores = core_counts[results.index(min_time)]
        return core_counts, results, (min_cores, min_time)


def luhn_algorithm(card_num: str) -> bool:
    """Perform Luhn Algorithm check on a card number.

    Args:
        card_num (str): Card number to be checked.

    Returns:
        bool: True if card number is valid, False otherwise.
    """
    last_digit = int(card_num[-1])
    card_num_list = [int(i) for i in card_num]
    for i in range(0, len(card_num_list) - 1, 2):
        card_num_list[i] *= 2
        if card_num_list[i] > 9:
            card_num_list[i] = sum(map(int, str(card_num_list[i])))
    res_sum = sum(card_num_list[-2::-1])
    check_digit = (10 - (res_sum % 10)) % 10
    return last_digit == check_digit


def find_card_data(bin_list: List[str], hash_value: str, last_numbers: str, file_path: str) -> Optional[str]:
    """Find card data using bruteforce method.

    Args:
        bin_list (List[str]): List of BINs (Bank Identification Numbers).
        hash_value (str): Hash value of the card.
        last_numbers (str): Last numbers of the card.
        file_path (str): File path to save the card number.

    Returns:
        Optional[str]: Found card number if successful, else None.
    """
    card = Card(last_numbers, hash_value, bin_list)
    result, _ = card.bruteforce_card_number(mp.cpu_count())
    if result:
        with open(file_path, 'w') as file:
            json.dump({"card_number": result}, file)
        return result
    return None


def visualize_performance(core_counts: List[int], results: List[float], min_cores_time: Tuple[int, float]):
    """Visualize performance results.

    Args:
        core_counts (List[int]): List of core counts used.
        results (List[float]): List of time taken for each core count.
        min_cores_time (Tuple[int, float]): Tuple containing minimum cores and time.
    """
    plt.plot(core_counts, results, marker='o', linestyle='-')
    plt.xlabel('Number of Processes')
    plt.ylabel('Time (seconds)')
    plt.title('Performance vs Number of Processes')
    plt.grid(True)
    plt.scatter(min_cores_time[0], min_cores_time[1], color='red', label=f'Minimum Time: {min_cores_time[1]:.2f}s (Cores: {min_cores_time[0]})')
    plt.legend()
    plt.show()


def main(settings_path: str):
    """Main function to execute the program.

    Args:
        settings_path (str): Path to the settings file.
    """
    settings = read_json_file(settings_path)
    if settings:
        bin_list = [str(bin) for bin in settings.get('bins', [])]
        hash_value = settings.get('hash', '')
        last_numbers = settings.get('last_numbers', '')
        file_path = settings.get('card_number_path', 'card_number.json')

        card = Card(last_numbers, hash_value, bin_list)
        core_counts, results, min_cores_time = card.performance_test()
        visualize_performance(core_counts, results, min_cores_time)
        result, _ = card.bruteforce_card_number(min_cores_time[0])
        if result:
            write_json_file(file_path, {"card_number": result})
            print(f"Card number found: {result}")
        else:
            print("Card number not found.")
    else:
        print("Failed to read settings file.")


if __name__ == "__main__":
    settings_path = "settings.json"
    main(settings_path)

import time
import multiprocessing as mp
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional
from utility import read_json_file
from hash_card_finder import Card


class CardTester:
    def __init__(self, card, path_test):
        self.card = card
        self.path_test = path_test

    def start_test(self) -> None:
        if self.card.bin_list and self.card.hash_value and self.card.last_num:
            x, y = self.time_test()
            plt.plot(x, y, marker="o")
            plt.title("Dependency of Time on Number of Processes")
            plt.ylabel("Time (seconds)")
            plt.xlabel("Number of Processes")
            plt.show()  # Изменение здесь, чтобы график выводился на экран


    def time_test(self) -> Tuple[List[int], List[float]]:
        """Function to test number of cores in multiprocessing

        Returns:
            Tuple[List[int], List[float]]: Number of cores and time
        """
        results = []
        core_counts = list(range(1, int(mp.cpu_count() * 1.5)))
        for cores in core_counts:
            results.append(self.num_bruteforce(cores)[1])
        return core_counts, results

    def num_bruteforce(self, cores: int) -> Tuple[Optional[str], float]:
        """Function to perform brute-force card number search using multiprocessing

        Args:
            cores (int): Number of CPU cores to use

        Returns:
            Tuple[Optional[str], float]: Card number found (if any) and time taken
        """
        return self.card.bruteforce_card_number(cores)

def main(settings_path: str):
    settings = read_json_file(settings_path)
    if settings:
        bin_list = [str(bin) for bin in settings.get('bins', [])]
        hash_value = settings.get('hash', '')
        last_numbers = settings.get('last_numbers', '')
        file_path = settings.get('card_number_path', 'card_number.json')
        test_path = settings.get('test_path', 'test_result.png')

        card_tester = CardTester(Card(last_numbers, hash_value, bin_list), test_path)
        card_tester.start_test()

if __name__ == "__main__":
    settings_path = "settings.json"
    main(settings_path)

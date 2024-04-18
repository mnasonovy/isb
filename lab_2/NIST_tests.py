def read_sequence_from_file(filename: str) -> str:

    with open(filename, 'r') as file:
        sequence = file.read().strip()
    return sequence

def write_results_to_file(filename: str, results: dict):
    with open(filename, 'w') as file:
        for test, result in results.items():
            file.write(f"{test}: {result}\n")



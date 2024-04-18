import math

def read_sequence_from_file(filename: str) -> str:

    with open(filename, 'r') as file:
        sequence = file.read().strip()
    return sequence

def write_results_to_file(filename: str, results: dict):
    with open(filename, 'w') as file:
        for test, result in results.items():
            file.write(f"{test}: {result}\n")
            
def frequency_bitwise_test(sequence: str) -> float:
    """
    Calculate the P value for the frequency bitwise test of a sequence.

    Parameters:
        sequence (str): Sequence of bytes.

    Returns:
        float: The P value.
    """
    N = len(sequence)
    sum_bits = sum(1 if bit == '1' else -1 for bit in sequence)
    P = sum_bits / math.sqrt(N)
    P = math.erfc(P / math.sqrt(2))
    return P


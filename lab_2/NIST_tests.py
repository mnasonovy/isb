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

def same_bits_test(sequence: str) -> float:
    """
    Calculate the P value for the test of same consecutive bits in a sequence.

    Parameters:
        sequence (str): Sequence of bits.

    Returns:
        float: The P value.
    """
    N = len(sequence)
    sum_bits = sum(int(bit) for bit in sequence)
    sigma = sum_bits / N
    if not abs(sigma - 0.5) < (2 / math.sqrt(N)):
        return 0 
    Vn = sum(1 for i in range(len(sequence) - 1) if sequence[i] != sequence[i + 1])
    P = math.erfc(abs(Vn - 2 * N * sigma * (1 - sigma)) / (2 * math.sqrt(2 * N) * sigma * (1 - sigma)))
    return P
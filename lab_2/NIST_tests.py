import math
from scipy.special import gammainc

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

def longest_ones_sequence_test(sequence: str) -> float:
    """
    Calculate the P value for the test of the longest sequence of ones in a block.

    Parameters:
        sequence (str): Sequence of bits.

    Returns:
        float: The P value.
    """
    block_length = 8
    v = [0, 0, 0, 0]
    hi_2 = 0
    for block in range(0, len(sequence) // block_length):
        max_len = 0
        curr_len = 0
        for i in range(block * block_length, block * block_length + block_length):
            if sequence[i] == '1':
                curr_len += 1
                max_len = max(max_len, curr_len)
            else:
                curr_len = 0
        if max_len <= 1:
            v[0] += 1
        elif max_len == 2:
            v[1] += 1
        elif max_len == 3:
            v[2] += 1
        else:
            v[3] += 1
    consts_PI = [0.2148, 0.3672, 0.2305, 0.1875]  
    for i in range(len(v)):
        hi_2 += ((v[i] - 16 * consts_PI[i]) ** 2) / (16 * consts_PI[i])
    P = gammainc(3 / 2, hi_2 / 2)  
    return P

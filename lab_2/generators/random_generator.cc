#include <iostream>
#include <fstream>
#include <random>

void generateRandomSequence(const std::string& filename) {
    std::random_device rd;
    std::mt19937_64 generator(rd()); 
    std::ofstream outFile(filename, std::ios::binary);
    if (!outFile) {
        std::cerr << "Не удалось открыть файл для записи\n";
        return;
    }
    for (int i = 0; i < 128 / 8; ++i) { 
        uint64_t randomValue = generator(); 
        outFile.write(reinterpret_cast<const char*>(&randomValue), sizeof(randomValue));
    }
    outFile.close();
    std::cout << "Псевдослучайная последовательность успешно записана в файл " << filename << "\n";
}

int main() {
    generateRandomSequence("random_sequence.bin");
    return 0;
}

#include "analysis.h"
#include "cipher.h"
#include "cryptanalysis.h"
#include "utils.h"

#include <iostream>
#include <limits>
#include <string>

static void encryptFromPlaintextFile() {
    std::string plaintext = readTextFile("plaintext.txt");
    if (plaintext.empty()) {
        std::cout << "Could not read plaintext.txt, or the file is empty.\n";
        std::cout << "Put your assigned Katz-Lindell page text into plaintext.txt first.\n";
        return;
    }

    SubstitutionKey key = generateRandomKey();
    std::string ciphertext = encryptText(plaintext, key);

    writeTextFile("ciphertext.txt", ciphertext);
    writeTextFile("key.txt", keyToString(key) + "\n");

    std::cout << "\nEncryption completed.\n";
    printEncryptionKey(key);
    std::cout << "\nSaved ciphertext to ciphertext.txt\n";
    std::cout << "Saved the original encryption key to key.txt for instructor-side verification.\n";
    std::cout << "Do NOT use key.txt during cryptanalysis.\n";
}

static void encryptWithUserKey() {
    std::string plaintext = readTextFile("plaintext.txt");
    if (plaintext.empty()) {
        std::cout << "Could not read plaintext.txt, or the file is empty.\n";
        return;
    }

    std::string keyString;
    std::cout << "Enter a 26-letter substitution alphabet.\n";
    std::cout << "Example format: QWERTYUIOPASDFGHJKLZXCVBNM\n";
    std::cout << "Key: ";
    std::cin >> keyString;

    SubstitutionKey key{};
    if (!keyFromString(keyString, key)) {
        std::cout << "Invalid key. It must contain every letter A-Z exactly once.\n";
        return;
    }

    std::string ciphertext = encryptText(plaintext, key);
    writeTextFile("ciphertext.txt", ciphertext);
    writeTextFile("key.txt", keyToString(key) + "\n");

    std::cout << "Ciphertext written to ciphertext.txt\n";
    printEncryptionKey(key);
}

static std::string loadCiphertext() {
    std::string ciphertext = readTextFile("ciphertext.txt");
    if (ciphertext.empty()) {
        std::cout << "Could not read ciphertext.txt, or it is empty.\n";
    }
    return ciphertext;
}

int main() {
    while (true) {
        std::cout << "\n=====================================================\n";
        std::cout << " Monoalphabetic Substitution Cipher + Cryptanalysis\n";
        std::cout << "=====================================================\n";
        std::cout << "1. Encrypt plaintext.txt using a random substitution key\n";
        std::cout << "2. Encrypt plaintext.txt using a user-supplied key\n";
        std::cout << "3. Run letter-frequency analysis on ciphertext.txt\n";
        std::cout << "4. Run word-frequency analysis on ciphertext.txt\n";
        std::cout << "5. Run word-pattern/repeated-word analysis\n";
        std::cout << "6. Start interactive cryptanalysis\n";
        std::cout << "7. Verify using key.txt (final cross-check only)\n";
        std::cout << "0. Exit\n";
        std::cout << "Choice: ";

        int choice;
        if (!(std::cin >> choice)) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "Invalid input.\n";
            continue;
        }

        if (choice == 0) {
            break;
        }

        if (choice == 1) {
            encryptFromPlaintextFile();
        } else if (choice == 2) {
            encryptWithUserKey();
        } else if (choice == 3) {
            std::string ciphertext = loadCiphertext();
            if (!ciphertext.empty()) {
                frequency_analysis(ciphertext);
            }
        } else if (choice == 4) {
            std::string ciphertext = loadCiphertext();
            if (!ciphertext.empty()) {
                word_frequency_analysis(ciphertext);
            }
        } else if (choice == 5) {
            std::string ciphertext = loadCiphertext();
            if (!ciphertext.empty()) {
                pattern_analysis(ciphertext);
            }
        } else if (choice == 6) {
            std::string ciphertext = loadCiphertext();
            if (!ciphertext.empty()) {
                runInteractiveCryptanalysis(ciphertext);
            }
        } else if (choice == 7) {
            std::string plaintext = readTextFile("plaintext.txt");
            std::string ciphertext = readTextFile("ciphertext.txt");
            std::string keyString = readTextFile("key.txt");

            if (plaintext.empty() || ciphertext.empty() || keyString.empty()) {
                std::cout << "plaintext.txt, ciphertext.txt and key.txt are all required.\n";
                continue;
            }

            SubstitutionKey key{};
            if (!keyFromString(keyString, key)) {
                std::cout << "key.txt does not contain a valid substitution key.\n";
                continue;
            }

            bool success = verify_solution(plaintext, ciphertext, key);
            std::cout << "Verification result: "
                      << (success ? "SUCCESS" : "FAILED") << "\n";
        } else {
            std::cout << "Unknown choice.\n";
        }
    }

    return 0;
}

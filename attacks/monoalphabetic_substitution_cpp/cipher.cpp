#include "cipher.h"
#include "utils.h"

#include <algorithm>
#include <cctype>
#include <iostream>
#include <numeric>
#include <random>

SubstitutionKey generateRandomKey() {
    SubstitutionKey key{};
    for (int i = 0; i < 26; ++i) {
        key[i] = static_cast<char>('A' + i);
    }

    std::random_device rd;
    std::mt19937 generator(rd());
    std::shuffle(key.begin(), key.end(), generator);
    return key;
}

bool keyIsValid(const SubstitutionKey& key) {
    std::array<bool, 26> seen{};
    seen.fill(false);

    for (char c : key) {
        if (c < 'A' || c > 'Z') {
            return false;
        }
        int index = c - 'A';
        if (seen[index]) {
            return false;
        }
        seen[index] = true;
    }
    return true;
}

std::string encryptText(const std::string& plaintext, const SubstitutionKey& key) {
    std::string result;
    result.reserve(plaintext.size());

    for (char c : plaintext) {
        if (!isEnglishLetter(c)) {
            result += c;
            continue;
        }

        bool lower = std::islower(static_cast<unsigned char>(c));
        char p = upperChar(c);
        char encrypted = key[p - 'A'];
        result += lower
            ? static_cast<char>(std::tolower(static_cast<unsigned char>(encrypted)))
            : encrypted;
    }

    return result;
}

std::string decryptText(const std::string& ciphertext, const SubstitutionKey& key) {
    SubstitutionKey inverse{};
    for (int plainIndex = 0; plainIndex < 26; ++plainIndex) {
        char cipherLetter = key[plainIndex];
        inverse[cipherLetter - 'A'] = static_cast<char>('A' + plainIndex);
    }

    std::string result;
    result.reserve(ciphertext.size());

    for (char c : ciphertext) {
        if (!isEnglishLetter(c)) {
            result += c;
            continue;
        }

        bool lower = std::islower(static_cast<unsigned char>(c));
        char encrypted = upperChar(c);
        char decrypted = inverse[encrypted - 'A'];
        result += lower
            ? static_cast<char>(std::tolower(static_cast<unsigned char>(decrypted)))
            : decrypted;
    }

    return result;
}

void printEncryptionKey(const SubstitutionKey& key) {
    std::cout << "Plain : ABCDEFGHIJKLMNOPQRSTUVWXYZ\n";
    std::cout << "Cipher: ";
    for (char c : key) {
        std::cout << c;
    }
    std::cout << '\n';
}

std::string keyToString(const SubstitutionKey& key) {
    return std::string(key.begin(), key.end());
}

bool keyFromString(const std::string& keyString, SubstitutionKey& key) {
    std::string cleaned;
    for (char c : keyString) {
        if (isEnglishLetter(c)) {
            cleaned += upperChar(c);
        }
    }

    if (cleaned.size() != 26) {
        return false;
    }

    for (int i = 0; i < 26; ++i) {
        key[i] = cleaned[i];
    }
    return keyIsValid(key);
}

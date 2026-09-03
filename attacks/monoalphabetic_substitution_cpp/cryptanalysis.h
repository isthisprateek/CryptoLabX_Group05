#ifndef CRYPTANALYSIS_H
#define CRYPTANALYSIS_H

#include "cipher.h"

#include <array>
#include <string>

class CryptanalysisSession {
private:
    std::array<char, 26> cipherToPlain;
    std::array<char, 26> plainToCipher;

public:
    CryptanalysisSession();

    bool apply_substitution(char cipherLetter, char plainLetter, std::string& message);
    bool remove_substitution(char cipherLetter, std::string& message);
    void clear_substitutions();

    std::string display_partial_plaintext(const std::string& ciphertext) const;
    void printCurrentMappings() const;
    bool isComplete() const;

    bool buildRecoveredEncryptionKey(SubstitutionKey& recoveredKey) const;
};

bool verify_solution(const std::string& recoveredPlaintext,
                     const std::string& originalCiphertext,
                     const SubstitutionKey& recoveredEncryptionKey);

void runInteractiveCryptanalysis(const std::string& ciphertext);

#endif

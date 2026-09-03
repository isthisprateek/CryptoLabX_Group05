#include "cryptanalysis.h"
#include "analysis.h"
#include "utils.h"

#include <cctype>
#include <iostream>
#include <limits>

CryptanalysisSession::CryptanalysisSession() {
    clear_substitutions();
}

void CryptanalysisSession::clear_substitutions() {
    cipherToPlain.fill('?');
    plainToCipher.fill('?');
}

bool CryptanalysisSession::apply_substitution(char cipherLetter,
                                              char plainLetter,
                                              std::string& message) {
    if (!isEnglishLetter(cipherLetter) || !isEnglishLetter(plainLetter)) {
        message = "Both symbols must be letters A-Z.";
        return false;
    }

    cipherLetter = upperChar(cipherLetter);
    plainLetter = upperChar(plainLetter);

    int c = cipherLetter - 'A';
    int p = plainLetter - 'A';

    if (cipherToPlain[c] != '?' && cipherToPlain[c] != plainLetter) {
        message = std::string("Cipher letter ") + cipherLetter +
                  " is already mapped to " + cipherToPlain[c] + ".";
        return false;
    }

    if (plainToCipher[p] != '?' && plainToCipher[p] != cipherLetter) {
        message = std::string("Plain letter ") + plainLetter +
                  " is already used by cipher letter " + plainToCipher[p] + ".";
        return false;
    }

    cipherToPlain[c] = plainLetter;
    plainToCipher[p] = cipherLetter;
    message = std::string("Accepted: ") + cipherLetter + " -> " + plainLetter;
    return true;
}

bool CryptanalysisSession::remove_substitution(char cipherLetter, std::string& message) {
    if (!isEnglishLetter(cipherLetter)) {
        message = "Cipher symbol must be a letter A-Z.";
        return false;
    }

    cipherLetter = upperChar(cipherLetter);
    int c = cipherLetter - 'A';
    char oldPlain = cipherToPlain[c];

    if (oldPlain == '?') {
        message = std::string("No mapping exists for ") + cipherLetter + ".";
        return false;
    }

    cipherToPlain[c] = '?';
    plainToCipher[oldPlain - 'A'] = '?';
    message = std::string("Removed: ") + cipherLetter + " -> " + oldPlain;
    return true;
}

std::string CryptanalysisSession::display_partial_plaintext(const std::string& ciphertext) const {
    std::string result;
    result.reserve(ciphertext.size());

    for (char c : ciphertext) {
        if (!isEnglishLetter(c)) {
            result += c;
            continue;
        }

        char cipherUpper = upperChar(c);
        char plain = cipherToPlain[cipherUpper - 'A'];
        if (plain == '?') {
            result += '?';
        } else if (std::islower(static_cast<unsigned char>(c))) {
            result += static_cast<char>(std::tolower(static_cast<unsigned char>(plain)));
        } else {
            result += plain;
        }
    }

    return result;
}

void CryptanalysisSession::printCurrentMappings() const {
    std::cout << "\nCurrent cipher -> plain mappings:\n";
    bool any = false;
    for (int i = 0; i < 26; ++i) {
        if (cipherToPlain[i] != '?') {
            std::cout << static_cast<char>('A' + i) << " -> " << cipherToPlain[i] << "    ";
            any = true;
        }
    }
    if (!any) {
        std::cout << "(none)";
    }
    std::cout << "\n";
}

bool CryptanalysisSession::isComplete() const {
    for (char c : cipherToPlain) {
        if (c == '?') {
            return false;
        }
    }
    return true;
}

bool CryptanalysisSession::buildRecoveredEncryptionKey(SubstitutionKey& recoveredKey) const {
    if (!isComplete()) {
        return false;
    }

    // Encryption key is indexed by plaintext letter and stores ciphertext letter.
    for (int p = 0; p < 26; ++p) {
        recoveredKey[p] = plainToCipher[p];
    }

    return keyIsValid(recoveredKey);
}

bool verify_solution(const std::string& recoveredPlaintext,
                     const std::string& originalCiphertext,
                     const SubstitutionKey& recoveredEncryptionKey) {
    std::string reEncrypted = encryptText(recoveredPlaintext, recoveredEncryptionKey);
    return reEncrypted == originalCiphertext;
}

void runInteractiveCryptanalysis(const std::string& ciphertext) {
    CryptanalysisSession session;

    while (true) {
        std::cout << "\n========== INTERACTIVE CRYPTANALYSIS ==========\n";
        std::cout << "1. Show letter frequency analysis\n";
        std::cout << "2. Show word frequency analysis\n";
        std::cout << "3. Show word/pattern analysis\n";
        std::cout << "4. Propose/apply substitution (cipher -> plain)\n";
        std::cout << "5. Remove a substitution\n";
        std::cout << "6. Display partial plaintext\n";
        std::cout << "7. Show current mappings\n";
        std::cout << "8. Clear all substitutions\n";
        std::cout << "9. Attempt final verification\n";
        std::cout << "0. Return to main menu\n";
        std::cout << "Choice: ";

        int choice;
        if (!(std::cin >> choice)) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "Invalid input.\n";
            continue;
        }

        if (choice == 0) {
            return;
        }

        if (choice == 1) {
            frequency_analysis(ciphertext);
        } else if (choice == 2) {
            word_frequency_analysis(ciphertext);
        } else if (choice == 3) {
            pattern_analysis(ciphertext);
        } else if (choice == 4) {
            char cipherLetter, plainLetter;
            std::cout << "Ciphertext letter: ";
            std::cin >> cipherLetter;
            std::cout << "Possible plaintext letter: ";
            std::cin >> plainLetter;

            std::string message;
            bool ok = session.apply_substitution(cipherLetter, plainLetter, message);
            std::cout << message << '\n';
            if (ok) {
                std::cout << "\nPartial plaintext:\n"
                          << session.display_partial_plaintext(ciphertext) << "\n";
            }
        } else if (choice == 5) {
            char cipherLetter;
            std::cout << "Ciphertext letter whose mapping should be removed: ";
            std::cin >> cipherLetter;

            std::string message;
            session.remove_substitution(cipherLetter, message);
            std::cout << message << '\n';
        } else if (choice == 6) {
            std::cout << "\nPartial plaintext:\n"
                      << session.display_partial_plaintext(ciphertext) << "\n";
        } else if (choice == 7) {
            session.printCurrentMappings();
        } else if (choice == 8) {
            session.clear_substitutions();
            std::cout << "All candidate substitutions cleared.\n";
        } else if (choice == 9) {
            SubstitutionKey recoveredKey{};
            if (!session.buildRecoveredEncryptionKey(recoveredKey)) {
                std::cout << "The mapping is not complete yet. Every A-Z cipher letter must be mapped.\n";
                continue;
            }

            std::string recoveredPlaintext = session.display_partial_plaintext(ciphertext);
            bool verified = verify_solution(recoveredPlaintext, ciphertext, recoveredKey);

            std::cout << "\nRecovered encryption key:\n";
            printEncryptionKey(recoveredKey);
            std::cout << "\nRecovered plaintext:\n" << recoveredPlaintext << "\n";
            std::cout << "\nVerification by re-encryption: "
                      << (verified ? "SUCCESS" : "FAILED") << "\n";
        } else {
            std::cout << "Unknown choice.\n";
        }
    }
}

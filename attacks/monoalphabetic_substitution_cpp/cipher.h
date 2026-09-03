#ifndef CIPHER_H
#define CIPHER_H

#include <array>
#include <string>

using SubstitutionKey = std::array<char, 26>;

SubstitutionKey generateRandomKey();
bool keyIsValid(const SubstitutionKey& key);
std::string encryptText(const std::string& plaintext, const SubstitutionKey& key);
std::string decryptText(const std::string& ciphertext, const SubstitutionKey& key);
void printEncryptionKey(const SubstitutionKey& key);
std::string keyToString(const SubstitutionKey& key);
bool keyFromString(const std::string& keyString, SubstitutionKey& key);

#endif

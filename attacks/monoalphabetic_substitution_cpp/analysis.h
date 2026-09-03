#ifndef ANALYSIS_H
#define ANALYSIS_H

#include <array>
#include <map>
#include <string>
#include <vector>

struct LetterFrequency {
    char letter;
    long long count;
    double percentage;
};

std::vector<LetterFrequency> frequency_analysis(const std::string& ciphertext);
std::map<std::string, int> word_frequency_analysis(const std::string& ciphertext);
std::string getWordPattern(const std::string& word);
void pattern_analysis(const std::string& ciphertext);
void printWordsByLength(const std::string& ciphertext, int length);
void printRepeatedWords(const std::string& ciphertext);
void printRepeatedLetterPatterns(const std::string& ciphertext);

#endif

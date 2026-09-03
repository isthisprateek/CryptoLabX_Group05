#include "analysis.h"
#include "utils.h"

#include <algorithm>
#include <array>
#include <iomanip>
#include <iostream>
#include <map>
#include <set>
#include <sstream>

std::vector<LetterFrequency> frequency_analysis(const std::string& ciphertext) {
    std::array<long long, 26> counts{};
    counts.fill(0);

    long long total = 0;
    for (char c : ciphertext) {
        if (isEnglishLetter(c)) {
            ++counts[upperChar(c) - 'A'];
            ++total;
        }
    }

    std::vector<LetterFrequency> result;
    for (int i = 0; i < 26; ++i) {
        double percent = total == 0 ? 0.0 : (100.0 * counts[i] / total);
        result.push_back({static_cast<char>('A' + i), counts[i], percent});
    }

    std::sort(result.begin(), result.end(), [](const LetterFrequency& a, const LetterFrequency& b) {
        if (a.count != b.count) {
            return a.count > b.count;
        }
        return a.letter < b.letter;
    });

    std::cout << "\n========== LETTER FREQUENCY ANALYSIS ==========\n";
    std::cout << std::left << std::setw(10) << "Letter"
              << std::setw(12) << "Count"
              << "Percentage\n";
    std::cout << "-----------------------------------------------\n";

    for (const auto& item : result) {
        std::cout << std::left << std::setw(10) << item.letter
                  << std::setw(12) << item.count
                  << std::fixed << std::setprecision(2)
                  << item.percentage << "%\n";
    }

    std::cout << "\nDescending order: ";
    for (const auto& item : result) {
        std::cout << item.letter << ' ';
    }
    std::cout << "\n";

    if (!result.empty()) {
        std::cout << "Most frequent ciphertext letters: ";
        int shown = 0;
        for (const auto& item : result) {
            if (item.count == 0 || shown == 5) {
                break;
            }
            std::cout << item.letter << "(" << item.count << ") ";
            ++shown;
        }
        std::cout << "\n";
    }

    return result;
}

std::map<std::string, int> word_frequency_analysis(const std::string& ciphertext) {
    std::map<std::string, int> frequencies;
    for (const std::string& word : extractWords(ciphertext)) {
        ++frequencies[word];
    }

    std::vector<std::pair<std::string, int>> sorted(frequencies.begin(), frequencies.end());
    std::sort(sorted.begin(), sorted.end(), [](const auto& a, const auto& b) {
        if (a.second != b.second) {
            return a.second > b.second;
        }
        return a.first < b.first;
    });

    std::cout << "\n========== WORD FREQUENCY ANALYSIS ==========\n";
    std::cout << std::left << std::setw(24) << "Word" << "Count\n";
    std::cout << "---------------------------------------------\n";
    for (const auto& [word, count] : sorted) {
        std::cout << std::left << std::setw(24) << word << count << '\n';
    }

    return frequencies;
}

std::string getWordPattern(const std::string& word) {
    std::map<char, int> firstSeen;
    int nextId = 0;
    std::ostringstream out;

    for (std::size_t i = 0; i < word.size(); ++i) {
        char c = upperChar(word[i]);
        if (firstSeen.find(c) == firstSeen.end()) {
            firstSeen[c] = nextId++;
        }
        if (i > 0) {
            out << '.';
        }
        out << firstSeen[c];
    }

    return out.str();
}

void printWordsByLength(const std::string& ciphertext, int length) {
    std::map<std::string, int> counts;
    for (const std::string& word : extractWords(ciphertext)) {
        if (static_cast<int>(word.size()) == length) {
            ++counts[word];
        }
    }

    std::vector<std::pair<std::string, int>> sorted(counts.begin(), counts.end());
    std::sort(sorted.begin(), sorted.end(), [](const auto& a, const auto& b) {
        if (a.second != b.second) {
            return a.second > b.second;
        }
        return a.first < b.first;
    });

    std::cout << "\n" << length << "-letter words:\n";
    if (sorted.empty()) {
        std::cout << "  None\n";
        return;
    }

    for (const auto& [word, count] : sorted) {
        std::cout << "  " << std::setw(12) << std::left << word
                  << " count=" << count
                  << " pattern=" << getWordPattern(word) << '\n';
    }
}

void printRepeatedWords(const std::string& ciphertext) {
    std::map<std::string, int> counts;
    for (const std::string& word : extractWords(ciphertext)) {
        ++counts[word];
    }

    std::cout << "\nRepeated words:\n";
    bool found = false;
    for (const auto& [word, count] : counts) {
        if (count > 1) {
            std::cout << "  " << std::setw(18) << std::left << word
                      << " count=" << count
                      << " pattern=" << getWordPattern(word) << '\n';
            found = true;
        }
    }
    if (!found) {
        std::cout << "  None\n";
    }
}

void printRepeatedLetterPatterns(const std::string& ciphertext) {
    std::map<std::string, std::set<std::string>> patternToWords;

    for (const std::string& word : extractWords(ciphertext)) {
        bool repeatedLetter = false;
        std::array<int, 26> seen{};
        seen.fill(0);
        for (char c : word) {
            int idx = c - 'A';
            ++seen[idx];
            if (seen[idx] > 1) {
                repeatedLetter = true;
            }
        }
        if (repeatedLetter) {
            patternToWords[getWordPattern(word)].insert(word);
        }
    }

    std::cout << "\nWords containing repeated-letter patterns:\n";
    if (patternToWords.empty()) {
        std::cout << "  None\n";
        return;
    }

    for (const auto& [pattern, words] : patternToWords) {
        std::cout << "  Pattern " << std::setw(14) << std::left << pattern << ": ";
        for (const auto& word : words) {
            std::cout << word << ' ';
        }
        std::cout << '\n';
    }
}

void pattern_analysis(const std::string& ciphertext) {
    std::cout << "\n========== WORD/PATTERN ANALYSIS ==========\n";
    printWordsByLength(ciphertext, 1);
    printWordsByLength(ciphertext, 2);
    printWordsByLength(ciphertext, 3);
    printRepeatedWords(ciphertext);
    printRepeatedLetterPatterns(ciphertext);
}

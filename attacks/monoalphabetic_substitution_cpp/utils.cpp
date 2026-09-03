#include "utils.h"

#include <cctype>
#include <fstream>
#include <sstream>

std::string readTextFile(const std::string& filename) {
    std::ifstream file(filename);
    if (!file) {
        return "";
    }

    std::ostringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

bool writeTextFile(const std::string& filename, const std::string& data) {
    std::ofstream file(filename);
    if (!file) {
        return false;
    }
    file << data;
    return true;
}

char upperChar(char c) {
    return static_cast<char>(std::toupper(static_cast<unsigned char>(c)));
}

bool isEnglishLetter(char c) {
    char u = upperChar(c);
    return u >= 'A' && u <= 'Z';
}

std::string toUpperCopy(const std::string& text) {
    std::string result = text;
    for (char& c : result) {
        if (isEnglishLetter(c)) {
            c = upperChar(c);
        }
    }
    return result;
}

std::vector<std::string> extractWords(const std::string& text) {
    std::vector<std::string> words;
    std::string current;

    for (char c : text) {
        if (isEnglishLetter(c)) {
            current += upperChar(c);
        } else if (!current.empty()) {
            words.push_back(current);
            current.clear();
        }
    }

    if (!current.empty()) {
        words.push_back(current);
    }

    return words;
}

#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <vector>

std::string readTextFile(const std::string& filename);
bool writeTextFile(const std::string& filename, const std::string& data);
std::string toUpperCopy(const std::string& text);
std::vector<std::string> extractWords(const std::string& text);
bool isEnglishLetter(char c);
char upperChar(char c);

#endif

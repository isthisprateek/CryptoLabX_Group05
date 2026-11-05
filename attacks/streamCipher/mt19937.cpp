#include <iostream>
#include <random>
#include <string>
#include <vector>
#include <cstdint>
#include <iomanip>
#include <sstream>
#include <chrono>
#include <algorithm>

using namespace std;

// --------------------------------------------------
// COMMON FUNCTION: Convert bytes to hexadecimal
// --------------------------------------------------

string toHex(const string& data) {
    stringstream ss;

    for (unsigned char c : data) {
        ss << hex << setw(2) << setfill('0')
           << static_cast<int>(c);
    }

    return ss.str();
}

// --------------------------------------------------
// PART A: MT19937 STREAM CIPHER
// --------------------------------------------------

// Same function is used for encryption and decryption.

string streamCipher(const string& input, uint32_t seed) {

    // Initialize MT19937 with the given seed.
    mt19937 generator(seed);

    string output;

    // Generate one keystream byte per input byte.
    for (unsigned char c : input) {

        // Generate a 32-bit random number.
        uint32_t randomNumber = generator();

        // Extract the lowest 8 bits.
        uint8_t keyByte = randomNumber & 0xFF;

        // XOR plaintext/ciphertext with keystream.
        uint8_t result = c ^ keyByte;

        output.push_back(static_cast<char>(result));
    }

    return output;
}

// --------------------------------------------------
// Generate random printable prefix (5-20 characters)
// --------------------------------------------------

string generatePrefix() {

    random_device rd;

    uniform_int_distribution<int> lengthDist(5, 20);
    uniform_int_distribution<int> charDist(32, 126);

    int length = lengthDist(rd);

    string prefix;

    for (int i = 0; i < length; i++) {
        prefix.push_back(static_cast<char>(charDist(rd)));
    }

    return prefix;
}

// --------------------------------------------------
// Generate a random 16-bit seed for Part A
// --------------------------------------------------

uint32_t generateSeed() {

    random_device rd;

    uniform_int_distribution<uint32_t> dist(0, 65535);

    return dist(rd);
}

// --------------------------------------------------
// PART A: Brute-force all 65536 seeds
// --------------------------------------------------

void recoverSeed(const string& ciphertext) {

    cout << "\n--- PART A: SEED RECOVERY ---\n";

    string knownPattern(14, 'A');

    bool found = false;

    for (uint32_t seed = 0; seed <= 65535; seed++) {

        // Attempt decryption with candidate seed.
        string decrypted = streamCipher(ciphertext, seed);

        // Check for 14 consecutive A characters.
        if (decrypted.find(knownPattern) != string::npos) {

            cout << "\nMatching seed found!\n";

            cout << "Recovered seed: " << seed << '\n';

            cout << "Recovered plaintext: "
                 << decrypted << '\n';

            // Verify complete decryption.
            string verification = streamCipher(decrypted, seed);

            if (verification == ciphertext) {
                cout << "Full ciphertext verification: SUCCESS\n";
            } else {
                cout << "Full ciphertext verification: FAILED\n";
            }

            found = true;
            break;
        }
    }

    if (!found) {
        cout << "No matching seed found.\n";
    }
}

// --------------------------------------------------
// PART B: Generate a 16-byte token using timestamp
// --------------------------------------------------

long long getUnixTimestamp() {

    return chrono::duration_cast<chrono::seconds>(
        chrono::system_clock::now().time_since_epoch()
    ).count();
}

// Generate 16 bytes from MT19937.

string generateToken(uint32_t seed) {

    mt19937 generator(seed);

    string token;

    for (int i = 0; i < 16; i++) {

        uint32_t randomNumber = generator();

        uint8_t byteValue = randomNumber & 0xFF;

        token.push_back(static_cast<char>(byteValue));
    }

    return token;
}

// --------------------------------------------------
// PART B: Brute-force possible timestamp seeds
// --------------------------------------------------

void predictToken(const string& observedToken,
                  long long actualTimestamp) {

    cout << "\n--- PART B: TOKEN PREDICTION ---\n";

    int window = 300;

    long long startTime = actualTimestamp - window;
    long long endTime = actualTimestamp + window;

    int tested = 0;

    bool found = false;

    cout << "Searching timestamps from "
         << startTime << " to " << endTime << '\n';

    for (long long candidate = startTime;
         candidate <= endTime;
         candidate++) {

        tested++;

        // Generate a candidate token.
        string candidateToken =
            generateToken(static_cast<uint32_t>(candidate));

        // Compare candidate token with observed token.
        if (candidateToken == observedToken) {

            cout << "\nMatching timestamp found!\n";

            cout << "Recovered timestamp: "
                 << candidate << '\n';

            cout << "Candidate tokens tested: "
                 << tested << '\n';

            cout << "Recovered token: "
                 << toHex(generateToken(
                        static_cast<uint32_t>(candidate)
                    )) << '\n';

            cout << "Observed token: "
                 << toHex(observedToken) << '\n';

            cout << "Token verification: "
                 << (generateToken(static_cast<uint32_t>(candidate))
                     == observedToken ? "SUCCESS" : "FAILED")
                 << '\n';

            found = true;
            break;
        }
    }

    if (!found) {
        cout << "No matching timestamp found in the search window.\n";
        cout << "Timestamps tested: " << tested << '\n';
    }
}

// --------------------------------------------------
// MAIN FUNCTION
// --------------------------------------------------

int main() {

    // ==============================================
    // PART A
    // ==============================================

    cout << "====================================\n";
    cout << " PART A: MT19937 STREAM CIPHER\n";
    cout << "====================================\n";

    // Task 1 and 2: Test encryption/decryption.

    string testMessage = "Cryptography Lab Assignment";

    uint32_t testSeed = 12345;

    string encrypted =
        streamCipher(testMessage, testSeed);

    string decrypted =
        streamCipher(encrypted, testSeed);

    cout << "\nOriginal message: " << testMessage << '\n';

    cout << "Encrypted (hex): " << toHex(encrypted) << '\n';

    cout << "Decrypted message: " << decrypted << '\n';

    cout << "Encryption/Decryption: "
         << (testMessage == decrypted ? "SUCCESS" : "FAILED")
         << '\n';


    // Task 3: Generate plaintext.

    uint32_t secretSeed = generateSeed();

    string prefix = generatePrefix();

    string plaintext = prefix + string(14, 'A');

    cout << "\nGenerated plaintext: " << plaintext << '\n';

    cout << "Secret 16-bit seed: " << secretSeed << '\n';

    // Encrypt using randomly selected seed.

    string ciphertext =
        streamCipher(plaintext, secretSeed);

    cout << "Ciphertext (hex): " << toHex(ciphertext) << '\n';

    // Task 4 and 5: Recover the seed.

    recoverSeed(ciphertext);


    // ==============================================
    // PART B
    // ==============================================

    cout << "\n====================================\n";
    cout << " PART B: PREDICTABLE RESET TOKENS\n";
    cout << "====================================\n";

    // Task 6: Record timestamp.

    long long timestamp = getUnixTimestamp();

    cout << "\nGeneration timestamp: "
         << timestamp << '\n';

    // Task 7: Generate a 16-byte token.

    string token =
        generateToken(static_cast<uint32_t>(timestamp));

    // Task 8: Display token in hexadecimal.

    cout << "Generated 16-byte token: "
         << toHex(token) << '\n';

    cout << "Token size: " << token.size() << " bytes\n";

    // Task 9, 10 and 11:
    // Simulate attacker recovering timestamp.

    predictToken(token, timestamp);

    cout << "\n====================================\n";
    cout << " ASSIGNMENT COMPLETED\n";
    cout << "====================================\n";

    return 0;
}

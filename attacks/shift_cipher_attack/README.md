# Shift Cipher Cryptanalysis

## Objective

The objective of this experiment is to perform cryptanalysis of a Shift Cipher using:

1. Brute-force attack with dictionary scoring
2. Chi-Square statistical analysis

The experiment compares the key predicted by both techniques with the actual encryption key.

---

## Shift Cipher

A Shift Cipher replaces each alphabetic character with another character obtained by shifting its position in the alphabet.

For encryption:

C = (P + K) mod 26

For decryption:

P = (C - K) mod 26

where K is the encryption key.

---

## Attack 1: Brute Force with Dictionary Scoring

Since a Shift Cipher has only 26 possible keys, all possible keys can be tested.

For every key:

1. Decrypt the ciphertext.
2. Split the plaintext into words.
3. Compare the words against an English dictionary.
4. Calculate a dictionary score.
5. Select the key with the highest score.

---

## Attack 2: Chi-Square Analysis

Chi-Square analysis compares the frequency distribution of letters in the decrypted text with the expected frequency distribution of English.

For every possible key:

1. Decrypt the ciphertext.
2. Count the frequency of each alphabetic character.
3. Calculate the Chi-Square statistic.
4. Select the key with the lowest Chi-Square value.

A lower Chi-Square value indicates a closer match to the expected English distribution.

---

## Project Structure

```text
shift_cipher_attack/
├── src/
│   ├── shift_cipher.py
│   ├── brute_force_dictionary.py
│   ├── chi_square_attack.py
│   └── main.py
│
├── dictionary/
│   └── english_words.txt
│
├── testcases/
├── outputs/
├── screenshots/
├── reports/
└── README.md

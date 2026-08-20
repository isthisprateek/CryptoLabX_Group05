import re
from shift_cipher import decrypt


def load_dictionary(filename):
    words = set()

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            word = line.strip().lower()

            if word:
                words.add(word)

    return words


def dictionary_score(text, dictionary):
    words = re.findall(r"[a-zA-Z]+", text.lower())

    if not words:
        return 0

    score = 0

    for word in words:
        if word in dictionary:
            score += 1

    return score


def brute_force_dictionary(ciphertext, dictionary):
    best_key = 0
    best_plaintext = ""
    best_score = -1

    results = []

    for key in range(26):
        plaintext = decrypt(ciphertext, key)
        score = dictionary_score(plaintext, dictionary)

        results.append((key, plaintext, score))

        if score > best_score:
            best_score = score
            best_key = key
            best_plaintext = plaintext

        print(
            "Current Attempt ! -> ",
            plaintext,
            " key -> ",
            key,
            "score -> ",
            score
        )

    return best_key, best_plaintext, best_score, results

from shift_cipher import encrypt
from brute_force_dict import (
    load_dictionary,
    brute_force_dictionary
)
from chi_square_attack import chi_square_attack


DICTIONARY_FILE = "../dictionary/english_words.txt"


def display_results(results):
    print("\n" + "=" * 80)
    print("ALL POSSIBLE KEYS")
    print("=" * 80)

    for key, plaintext, score in results:
        print(f"Key {key:2d} | Score: {score:8.3f} | {plaintext}")


def main():
    print("=" * 60)
    print("       SHIFT CIPHER CRYPTANALYSIS")
    print("=" * 60)

    plaintext = input("\nEnter plaintext: ")
    key = int(input("Enter encryption key (0-25): "))

    ciphertext = encrypt(plaintext, key)

    print("\nCiphertext:")
    print(ciphertext)

    dictionary = load_dictionary(DICTIONARY_FILE)

    # Dictionary attack
    (
        dictionary_key,
        dictionary_plaintext,
        dictionary_score_value,
        dictionary_results
    ) = brute_force_dictionary(ciphertext, dictionary)

    print("\n" + "=" * 60)
    print("DICTIONARY SCORING ATTACK")
    print("=" * 60)

    print(f"Predicted Key       : {dictionary_key}")
    print(f"Predicted Plaintext : {dictionary_plaintext}")
    print(f"Dictionary Score    : {dictionary_score_value}")

    # Chi-square attack
    (
        chi_key,
        chi_plaintext,
        chi_score,
        chi_results
    ) = chi_square_attack(ciphertext)

    print("\n" + "=" * 60)
    print("CHI-SQUARE ATTACK")
    print("=" * 60)

    print(f"Predicted Key       : {chi_key}")
    print(f"Predicted Plaintext : {chi_plaintext}")
    print(f"Chi-Square Score    : {chi_score:.3f}")

    # Comparison
    print("\n" + "=" * 60)
    print("COMPARISON")
    print("=" * 60)

    print(f"Actual Key          : {key}")
    print(f"Dictionary Key      : {dictionary_key}")
    print(f"Chi-Square Key      : {chi_key}")

    print(
        f"Dictionary Correct? : "
        f"{'YES' if dictionary_key == key else 'NO'}"
    )

    print(
        f"Chi-Square Correct? : "
        f"{'YES' if chi_key == key else 'NO'}"
    )


if __name__ == "__main__":
    main()

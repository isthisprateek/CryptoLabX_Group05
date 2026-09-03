import re
from collections import Counter

from analysis import (
    frequency_analysis,
    word_frequency_analysis,
    pattern_analysis,
    extract_words,
    word_pattern,
)


def build_partial_decryption(ciphertext, cipher_to_plain):
    """
    Apply a partial ciphertext -> plaintext mapping.

    Unknown ciphertext letters are displayed as '?'.
    Non-alphabetic characters are preserved.
    """
    result = []

    for ch in ciphertext:
        upper = ch.upper()

        if "A" <= upper <= "Z":
            if upper in cipher_to_plain:
                p = cipher_to_plain[upper]
                result.append(p.lower() if ch.islower() else p)
            else:
                result.append("?")
        else:
            result.append(ch)

    return "".join(result)


def display_partial_plaintext(ciphertext, cipher_to_plain):
    print("\n" + "=" * 70)
    print("CURRENT PARTIAL PLAINTEXT")
    print("=" * 70)
    print(build_partial_decryption(ciphertext, cipher_to_plain))


def mapping_is_valid(cipher_letter, plain_letter,
                     cipher_to_plain, plain_to_cipher):
    cipher_letter = cipher_letter.upper()
    plain_letter = plain_letter.upper()

    if not ("A" <= cipher_letter <= "Z"):
        return False

    if not ("A" <= plain_letter <= "Z"):
        return False

    # Same ciphertext letter already mapped to another plaintext letter.
    if cipher_letter in cipher_to_plain:
        if cipher_to_plain[cipher_letter] != plain_letter:
            return False

    # Same plaintext letter already used by another ciphertext letter.
    if plain_letter in plain_to_cipher:
        if plain_to_cipher[plain_letter] != cipher_letter:
            return False

    return True


def add_mapping(cipher_letter, plain_letter,
                cipher_to_plain, plain_to_cipher):
    cipher_letter = cipher_letter.upper()
    plain_letter = plain_letter.upper()

    if not mapping_is_valid(
        cipher_letter,
        plain_letter,
        cipher_to_plain,
        plain_to_cipher
    ):
        return False

    cipher_to_plain[cipher_letter] = plain_letter
    plain_to_cipher[plain_letter] = cipher_letter
    return True


def remove_mapping(cipher_letter, cipher_to_plain, plain_to_cipher):
    cipher_letter = cipher_letter.upper()

    if cipher_letter not in cipher_to_plain:
        return False

    plain_letter = cipher_to_plain[cipher_letter]

    del cipher_to_plain[cipher_letter]

    if plain_letter in plain_to_cipher:
        del plain_to_cipher[plain_letter]

    return True


def show_current_key(cipher_to_plain):
    print("\nCurrent substitutions:")
    if not cipher_to_plain:
        print("No substitutions have been added.")
        return

    for cipher in sorted(cipher_to_plain):
        print(f"{cipher} -> {cipher_to_plain[cipher]}")


def suggest_frequency_substitutions(ciphertext):
    counts = frequency_analysis_silent(ciphertext)

    ordered_cipher = sorted(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        key=lambda x: (-counts[x], x)
    )

    english_order = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

    print("\nFrequency-based candidate mappings:")
    print(f"{'Cipher':<10}{'Candidate plaintext':<25}")

    for i in range(min(15, 26)):
        print(f"{ordered_cipher[i]:<10}{english_order[i]:<25}")


def frequency_analysis_silent(ciphertext):
    counts = Counter()

    for ch in ciphertext.upper():
        if "A" <= ch <= "Z":
            counts[ch] += 1

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if letter not in counts:
            counts[letter] = 0

    return counts


def show_word_candidates(ciphertext, cipher_to_plain):
    """
    Display words and their partially decrypted forms.
    Repeated words are grouped together.
    """
    words = extract_words(ciphertext)
    counts = Counter(words)

    print("\n" + "=" * 70)
    print("WORD/PATTERN CLUES")
    print("=" * 70)

    shown = set()

    for word in words:
        if word in shown:
            continue

        shown.add(word)

        partial = []
        for ch in word:
            partial.append(cipher_to_plain.get(ch, "?"))

        print(
            f"{word:<15}"
            f"pattern={word_pattern(word):<10}"
            f"count={counts[word]:<4}"
            f"partial={''.join(partial)}"
        )

        if len(shown) >= 50:
            break


def candidate_words_for_pattern(cipher_word, dictionary):
    target_pattern = word_pattern(cipher_word)

    result = []

    for word in dictionary:
        if len(word) == len(cipher_word):
            if word_pattern(word) == target_pattern:
                result.append(word)

    return result


def interactive_cryptanalysis(ciphertext):
    """
    Human-guided iterative cryptanalysis.

    The assignment explicitly asks for:
      - candidate substitutions
      - replacing suspected letters
      - examining partial plaintext
      - rejecting incorrect hypotheses
      - continuing until meaningful plaintext is obtained

    This interface therefore deliberately leaves the final hypotheses
    under the student's control rather than using an automatic cipher
    solver.
    """
    cipher_to_plain = {}
    plain_to_cipher = {}

    while True:
        print("\n" + "=" * 70)
        print("INTERACTIVE CRYPTANALYSIS")
        print("=" * 70)

        print("1. Frequency suggestions")
        print("2. Word/pattern clues")
        print("3. Display partial plaintext")
        print("4. Add/test substitution")
        print("5. Remove/reject substitution")
        print("6. Show current key")
        print("7. Show all analysis")
        print("8. Finish and save recovered solution")
        print("9. Cancel")

        choice = input("Choice: ").strip()

        if choice == "1":
            suggest_frequency_substitutions(ciphertext)

        elif choice == "2":
            show_word_candidates(ciphertext, cipher_to_plain)

        elif choice == "3":
            display_partial_plaintext(ciphertext, cipher_to_plain)

        elif choice == "4":
            cipher_letter = input("Ciphertext letter: ").strip().upper()
            plain_letter = input("Proposed plaintext letter: ").strip().upper()

            if len(cipher_letter) != 1 or len(plain_letter) != 1:
                print("Enter exactly one letter for each.")
                continue

            if add_mapping(
                cipher_letter,
                plain_letter,
                cipher_to_plain,
                plain_to_cipher
            ):
                print(f"Accepted hypothesis: {cipher_letter} -> {plain_letter}")
                display_partial_plaintext(ciphertext, cipher_to_plain)
            else:
                print("Rejected: this would violate the one-to-one substitution rule.")

        elif choice == "5":
            cipher_letter = input(
                "Ciphertext letter whose hypothesis should be rejected: "
            ).strip().upper()

            if remove_mapping(
                cipher_letter,
                cipher_to_plain,
                plain_to_cipher
            ):
                print(f"Removed hypothesis for {cipher_letter}.")
            else:
                print("No mapping exists for that letter.")

        elif choice == "6":
            show_current_key(cipher_to_plain)

        elif choice == "7":
            frequency_analysis(ciphertext)
            word_frequency_analysis(ciphertext)
            pattern_analysis(ciphertext)
            show_word_candidates(ciphertext, cipher_to_plain)
            display_partial_plaintext(ciphertext, cipher_to_plain)

        elif choice == "8":
            if len(cipher_to_plain) != 26:
                print(
                    f"\nOnly {len(cipher_to_plain)}/26 mappings are known."
                )
                print("A complete key is required for verification.")

                answer = input(
                    "Return to analysis? [Y/n]: "
                ).strip().lower()

                if answer != "n":
                    continue

            completed = complete_key_interactively(
                cipher_to_plain,
                plain_to_cipher
            )

            if completed is None:
                print("Could not construct a complete valid key.")
                continue

            print("\nRecovered substitution key:")
            for c in sorted(completed):
                print(f"{c} -> {completed[c]}")

            return maps_to_key_format(completed)

        elif choice == "9":
            return None

        else:
            print("Invalid choice.")


def complete_key_interactively(cipher_to_plain, plain_to_cipher):
    """
    If all mappings have not been recovered, ask the student to fill the
    remaining mappings. This prevents silently guessing the final key.
    """
    c2p = dict(cipher_to_plain)
    p2c = dict(plain_to_cipher)

    remaining_cipher = [
        c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if c not in c2p
    ]

    remaining_plain = [
        p for p in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if p not in p2c
    ]

    if not remaining_cipher:
        return c2p

    print("\nRemaining ciphertext letters:")
    print(" ".join(remaining_cipher))

    print("Remaining plaintext letters:")
    print(" ".join(remaining_plain))

    print(
        "\nYou may enter the remaining mappings manually."
    )
    print(
        "Example: Q E means ciphertext Q -> plaintext E."
    )

    while remaining_cipher:
        pair = input(
            f"Map {remaining_cipher[0]} (or 'cancel'): "
        ).strip().upper()

        if pair == "CANCEL":
            return None

        parts = pair.split()

        if len(parts) == 1 and len(parts[0]) == 2:
            cipher_letter = parts[0][0]
            plain_letter = parts[0][1]
        elif len(parts) == 2:
            cipher_letter = parts[0]
            plain_letter = parts[1]
        else:
            print("Use format: Q E")
            continue

        if len(cipher_letter) != 1 or len(plain_letter) != 1:
            print("Use single letters.")
            continue

        if add_mapping(
            cipher_letter,
            plain_letter,
            c2p,
            p2c
        ):
            print(f"Accepted: {cipher_letter} -> {plain_letter}")
            remaining_cipher = [
                c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                if c not in c2p
            ]
        else:
            print("Invalid mapping: plaintext letter may already be used.")

    return c2p


def maps_to_key_format(cipher_to_plain):
    """
    Convert recovered ciphertext->plaintext mapping into the same
    key format used by cipher.py.
    """
    # Encryption requires plaintext -> ciphertext.
    plain_to_cipher = {}

    for cipher, plain in cipher_to_plain.items():
        plain_to_cipher[plain] = cipher

    return {
        "plain": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        "cipher": [
            plain_to_cipher[p]
            for p in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ]
    }

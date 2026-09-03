import re
from collections import Counter


ENGLISH_FREQUENCY_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"


def only_letters(text):
    result = []

    for ch in text.upper():
        if "A" <= ch <= "Z":
            result.append(ch)

    return "".join(result)


def frequency_analysis(ciphertext):
    letters = only_letters(ciphertext)
    total = len(letters)

    counts = Counter(letters)

    print("\n" + "=" * 70)
    print("LETTER FREQUENCY ANALYSIS")
    print("=" * 70)

    print(f"Total alphabetic characters: {total}\n")
    print(f"{'Letter':<10}{'Count':<10}{'Percentage':<15}")
    print("-" * 35)

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        count = counts[letter]
        percentage = (count / total * 100) if total else 0
        print(f"{letter:<10}{count:<10}{percentage:>8.2f}%")

    ordered = sorted(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        key=lambda x: (-counts[x], x)
    )

    print("\nLetters in descending frequency:")
    print(" ".join(ordered))

    print("\nMost frequent letters:")
    if total:
        highest = counts[ordered[0]]
        most = [x for x in ordered if counts[x] == highest]
        print(" ".join(most))
    else:
        print("No alphabetic characters.")

    print("\nEnglish reference order:")
    print(ENGLISH_FREQUENCY_ORDER)

    return counts


def extract_words(text):
    return re.findall(r"[A-Za-z]+", text.upper())


def word_frequency_analysis(ciphertext):
    words = extract_words(ciphertext)
    counts = Counter(words)

    print("\n" + "=" * 70)
    print("WORD FREQUENCY ANALYSIS")
    print("=" * 70)

    print(f"Total words: {len(words)}")
    print(f"Unique words: {len(counts)}")

    print("\nOne-letter words:")
    print_counter_for_length(words, counts, 1)

    print("\nTwo-letter words:")
    print_counter_for_length(words, counts, 2)

    print("\nThree-letter words:")
    print_counter_for_length(words, counts, 3)

    print("\nRepeated words:")
    repeated = [(word, count) for word, count in counts.items() if count > 1]
    repeated.sort(key=lambda x: (-x[1], x[0]))

    if repeated:
        for word, count in repeated:
            print(f"{word:<20} {count}")
    else:
        print("No repeated words.")

    print("\nMost frequent words:")
    for word, count in counts.most_common(20):
        print(f"{word:<20} {count}")

    return counts


def print_counter_for_length(words, counts, length):
    selected = [
        (word, count)
        for word, count in counts.items()
        if len(word) == length
    ]
    selected.sort(key=lambda x: (-x[1], x[0]))

    if not selected:
        print("None")
        return

    for word, count in selected:
        print(f"{word:<20} {count}")


def word_pattern(word):
    """
    Convert a word to a normalized repeated-letter pattern.

    Example:
        THAT -> 0120
        TOO  -> 011
        HELLO -> 01223
    """
    mapping = {}
    next_number = 0
    pattern = []

    for ch in word.upper():
        if ch not in mapping:
            mapping[ch] = str(next_number)
            next_number += 1

        pattern.append(mapping[ch])

    return "".join(pattern)


def pattern_analysis(ciphertext):
    words = extract_words(ciphertext)

    print("\n" + "=" * 70)
    print("WORD PATTERN ANALYSIS")
    print("=" * 70)

    pattern_groups = {}

    for word in words:
        pattern = word_pattern(word)

        if pattern not in pattern_groups:
            pattern_groups[pattern] = []

        if word not in pattern_groups[pattern]:
            pattern_groups[pattern].append(word)

    print(f"{'Pattern':<12}{'Words'}")
    print("-" * 60)

    for pattern in sorted(pattern_groups):
        words_for_pattern = pattern_groups[pattern]
        print(f"{pattern:<12}{', '.join(words_for_pattern[:15])}")

    print("\nExamples of common patterns:")
    for word in sorted(set(words))[:30]:
        print(f"{word:<15} -> {word_pattern(word)}")

    return pattern_groups

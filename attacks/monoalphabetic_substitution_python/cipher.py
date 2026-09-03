import random
import string


ALPHABET = string.ascii_uppercase


def generate_key():
    """
    Generate a random one-to-one monoalphabetic substitution key.

    key["plain"][i] is the plaintext alphabet.
    key["cipher"][i] is the corresponding ciphertext alphabet.
    """
    shuffled = list(ALPHABET)
    random.shuffle(shuffled)

    return {
        "plain": list(ALPHABET),
        "cipher": shuffled
    }


def validate_key(key):
    if len(key["plain"]) != 26 or len(key["cipher"]) != 26:
        return False

    if set(key["plain"]) != set(ALPHABET):
        return False

    if set(key["cipher"]) != set(ALPHABET):
        return False

    if len(set(key["cipher"])) != 26:
        return False

    return True


def key_to_maps(key):
    """
    Create both directions:
        plaintext -> ciphertext
        ciphertext -> plaintext
    """
    if not validate_key(key):
        raise ValueError("Invalid substitution key.")

    enc = {}
    dec = {}

    for i in range(26):
        enc[key["plain"][i]] = key["cipher"][i]
        dec[key["cipher"][i]] = key["plain"][i]

    return enc, dec


def encrypt(text, key):
    enc, _ = key_to_maps(key)

    result = []

    for ch in text:
        upper = ch.upper()

        if upper in enc:
            converted = enc[upper]

            if ch.islower():
                result.append(converted.lower())
            else:
                result.append(converted)
        else:
            result.append(ch)

    return "".join(result)


def decrypt(text, key):
    _, dec = key_to_maps(key)

    result = []

    for ch in text:
        upper = ch.upper()

        if upper in dec:
            converted = dec[upper]

            if ch.islower():
                result.append(converted.lower())
            else:
                result.append(converted)
        else:
            result.append(ch)

    return "".join(result)


def save_key(filename, key):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("".join(key["plain"]) + "\n")
        f.write("".join(key["cipher"]) + "\n")


def load_key(filename):
    with open(filename, "r", encoding="utf-8") as f:
        plain = f.readline().strip().upper()
        cipher = f.readline().strip().upper()

    key = {
        "plain": list(plain),
        "cipher": list(cipher)
    }

    if not validate_key(key):
        raise ValueError("Invalid key file.")

    return key

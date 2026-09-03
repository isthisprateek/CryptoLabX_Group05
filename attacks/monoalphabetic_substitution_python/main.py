from cipher import generate_key, encrypt, decrypt, save_key, load_key
from analysis import frequency_analysis, word_frequency_analysis, pattern_analysis
from cryptanalysis import interactive_cryptanalysis
from utils import read_text_file, write_text_file


def print_menu():
    print("\n" + "=" * 70)
    print(" MONOALPHABETIC SUBSTITUTION CIPHER")
    print("=" * 70)
    print("1. Encrypt plaintext")
    print("2. Decrypt using a key")
    print("3. Letter-frequency analysis")
    print("4. Word-frequency analysis")
    print("5. Pattern analysis")
    print("6. Interactive cryptanalysis")
    print("7. Verify recovered solution")
    print("8. Exit")
    print("=" * 70)


def main():
    plaintext_file = "plaintext.txt"
    ciphertext_file = "ciphertext.txt"
    key_file = "key.txt"
    recovered_key_file = "recovered_key.txt"

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            try:
                plaintext = read_text_file(plaintext_file)
            except FileNotFoundError:
                print(f"Create {plaintext_file} and put the required Katz & Lindell text in it.")
                continue

            key = generate_key()
            ciphertext = encrypt(plaintext, key)

            write_text_file(ciphertext_file, ciphertext)
            save_key(key_file, key)

            print("\nEncryption completed.")
            print(f"Ciphertext saved to: {ciphertext_file}")
            print(f"Secret key saved to: {key_file}")
            print("\nKey:")
            print_key(key)

        elif choice == "2":
            try:
                ciphertext = read_text_file(ciphertext_file)
                key = load_key(key_file)
            except FileNotFoundError:
                print("Run option 1 first.")
                continue

            plaintext = decrypt(ciphertext, key)
            write_text_file("decrypted.txt", plaintext)

            print("\nDecrypted text saved to decrypted.txt")
            print(plaintext[:1000])

        elif choice == "3":
            try:
                ciphertext = read_text_file(ciphertext_file)
            except FileNotFoundError:
                print("Run option 1 first.")
                continue

            frequency_analysis(ciphertext)

        elif choice == "4":
            try:
                ciphertext = read_text_file(ciphertext_file)
            except FileNotFoundError:
                print("Run option 1 first.")
                continue

            word_frequency_analysis(ciphertext)

        elif choice == "5":
            try:
                ciphertext = read_text_file(ciphertext_file)
            except FileNotFoundError:
                print("Run option 1 first.")
                continue

            pattern_analysis(ciphertext)

        elif choice == "6":
            try:
                ciphertext = read_text_file(ciphertext_file)
            except FileNotFoundError:
                print("Run option 1 first.")
                continue

            recovered_key = interactive_cryptanalysis(ciphertext)

            if recovered_key:
                save_key(recovered_key_file, recovered_key)
                recovered_plaintext = decrypt(ciphertext, recovered_key)
                write_text_file("recovered_plaintext.txt", recovered_plaintext)

                print("\nRecovered key saved to recovered_key.txt")
                print("Recovered plaintext saved to recovered_plaintext.txt")

        elif choice == "7":
            try:
                ciphertext = read_text_file(ciphertext_file)
                plaintext = read_text_file("recovered_plaintext.txt")
                recovered_key = load_key(recovered_key_file)
            except FileNotFoundError:
                print("Run interactive cryptanalysis first.")
                continue

            generated = encrypt(plaintext, recovered_key)

            if generated == ciphertext:
                print("\nSUCCESS: Re-encryption exactly matches the ciphertext.")
            else:
                print("\nFAILED: Re-encryption does not match the ciphertext.")

                # Helpful diagnostic.
                mismatch = 0
                for a, b in zip(generated, ciphertext):
                    if a != b:
                        mismatch += 1
                mismatch += abs(len(generated) - len(ciphertext))
                print(f"Number of mismatching characters: {mismatch}")

        elif choice == "8":
            print("Exiting.")
            break

        else:
            print("Invalid choice.")


def print_key(key):
    print("Plain : " + " ".join(key["plain"]))
    print("Cipher: " + " ".join(key["cipher"]))


if __name__ == "__main__":
    main()

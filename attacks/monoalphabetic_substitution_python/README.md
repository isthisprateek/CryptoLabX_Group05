# Monoalphabetic Substitution Cipher and Cryptanalysis

This project implements the assignment:

**Monoalphabetic Substitution Cipher and its Cryptanalysis Using Frequency and Pattern Analysis**

## Files

- `main.py` - main menu and program control
- `cipher.py` - key generation, encryption, decryption and key handling
- `analysis.py` - letter, word and pattern frequency analysis
- `cryptanalysis.py` - interactive cryptanalysis and partial plaintext recovery
- `utils.py` - text-file utilities
- `plaintext.txt` - put the assigned Katz & Lindell plaintext here

## Run

Python 3 is required.

```bash
python3 main.py
```

On Windows:

```bash
python main.py
```

## Assignment workflow

### 1. Put plaintext in plaintext.txt

Use the required page from *Modern Cryptography* by Katz and Lindell.

### 2. Encrypt

Choose:

```text
1. Encrypt plaintext
```

The program generates a random monoalphabetic substitution key and creates:

```text
ciphertext.txt
key.txt
```

Do not use `key.txt` while doing cryptanalysis.

### 3. Perform analyses

Use:

```text
3. Letter-frequency analysis
4. Word-frequency analysis
5. Pattern analysis
```

These provide the observations required for the notebook table.

### 4. Cryptanalysis

Choose:

```text
6. Interactive cryptanalysis
```

The program allows you to:

- inspect frequency-based candidate substitutions
- inspect repeated words
- inspect word patterns
- add suspected mappings
- reject/remove mappings
- display partial plaintext
- complete the key manually

Example:

```text
Ciphertext letter: Q
Proposed plaintext letter: E
```

The program checks that the substitution remains one-to-one.

### 5. Verification

When the recovered key is complete, the program saves:

```text
recovered_key.txt
recovered_plaintext.txt
```

Then choose:

```text
7. Verify recovered solution
```

The recovered plaintext is encrypted again using the recovered key.

If the generated ciphertext is exactly equal to the original ciphertext, the solution is verified.

## Important cryptanalysis principle

Frequency analysis provides clues, not guaranteed answers.

For example, if `Q` is the most frequent ciphertext character, `Q -> E` is a reasonable hypothesis, but it should be tested against words and patterns.

The intended process is:

```text
frequency
    ↓
candidate substitution
    ↓
partial plaintext
    ↓
word/pattern check
    ↓
accept/reject hypothesis
    ↓
repeat
```

No external cryptography library is used.

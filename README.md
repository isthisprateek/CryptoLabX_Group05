# CryptoLabX

CryptoLabX is a modular, semester-long cryptanalysis toolkit built as part of
our coursework. It is being developed incrementally: each assignment adds a
new capability (classical ciphers, attack techniques, modern cryptography,
and statistical analysis tools) on top of a shared, reusable codebase.

This repository corresponds to **Assignment 1 (Week 1): Project Foundation**.
No cryptographic algorithms are implemented yet — this stage focuses on
project setup, version control, a working CLI shell, file handling, and
logging.

## Team Members

| Name | Roll No. | 
|------|----------|------|
| Prateek Kumar | 2024UCP1751| 
| Ajay Yadav | 2024UCP1533 |  


## Project Structure

```
CryptoLabX/
├── classical/     # Classical ciphers (Caesar, Vigenere, Playfair, ...) - future
├── attacks/       # Cryptanalysis / attack techniques 
├── math/          # Number theory & math helpers (modular arithmetic, GCD, etc.) - future
├── modern/         # Modern cryptography (AES, RSA, etc.) - future
├── analysis/       # Statistical / cryptanalytic analysis tools - future
├── datasets/       # Sample text files used for testing and analysis
├── outputs/        # Generated logs, reports, and other run-time output
├── docs/           # Project documentation
├── tests/          # Unit tests
├── utils/          # Shared helper modules (file analysis, logging, etc.)
├── main.py         # CLI entry point
├── README.md       # This file
└── requirements.txt
```

## Features Implemented in Week 1

- **Menu-driven CLI** (`main.py`) with options: Encrypt, Decrypt, Attack,
  Analyze, Exit. Encrypt/Decrypt/Attack currently display "Coming Soon"
  placeholders, since those modules will be built in later assignments.
- **Text file analysis** (`utils/file_analysis.py`): reads a `.txt` file
  from `datasets/` and reports character count, word count, line count,
  unique character count, and A-Z letter frequency (with percentages).
- **Session logging** (`utils/logger.py`): every menu selection is appended
  to `outputs/cryptolabx.log` with the date and time.
- **Sample datasets**: five `.txt` files in `datasets/`, covering plain
  English text, a crypto-history passage, a short single-line message, a
  repetitive/frequency-skewed text, and a longer mixed-case paragraph with
  punctuation and numbers — chosen to be broadly reusable for classical
  cipher and frequency-analysis assignments later in the semester.

## How to Run

```bash
python main.py
```

Then follow the on-screen menu. Choosing **Analyze** lets you pick any
`.txt` file from `datasets/` and view its statistics. Every selection you
make is recorded in `outputs/cryptolabx.log`.

## Requirements

This assignment uses only the Python standard library — see
`requirements.txt`. No external packages are required yet; it is included
as a placeholder for future assignments (e.g. numeric/crypto libraries).

## Future Modules (Planned)

- **classical/** — Caesar, Vigenère, Playfair, Hill, Rail Fence, and other
  classical ciphers with encrypt/decrypt functions.
- **attacks/** — Brute-force, frequency analysis, Kasiski examination, and
  other cryptanalytic attacks against classical ciphers.
- **modern/** — Modern primitives such as AES and RSA.
- **math/** — Supporting number theory utilities (modular inverse, GCD,
  primality testing, etc.) used by classical and modern modules.
- **analysis/** — Deeper statistical analysis tools (index of coincidence,
  chi-squared scoring, n-gram analysis) to support automated attacks.
- **tests/** — Unit tests covering each module as it is implemented.

## Version Control

This project uses Git. The initial commit establishes the folder structure
and Week 1 deliverables; subsequent assignments will be added as new
commits/branches as the toolkit grows.

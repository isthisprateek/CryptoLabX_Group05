#!/usr/bin/env python3
"""
Generate a probable 512-bit prime with Miller-Rabin and verify it independently.

Run:
    python3 miller_rabin_prime.py
Optional:
    python3 miller_rabin_prime.py --rounds 40
"""

import argparse
import secrets
import time


def miller_rabin(n: int, rounds: int = 40) -> bool:
    """Return True if n passes the Miller-Rabin probable-prime test."""
    if n < 2:
        return False

    # Handle small primes and reject their multiples early.
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False

    # Write n - 1 as d * 2**s, where d is odd.
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # Test independently chosen random bases in [2, n - 2].
    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def random_odd_candidate(bits: int) -> int:
    """Generate an odd integer with exactly `bits` bits."""
    return secrets.randbits(bits) | (1 << (bits - 1)) | 1


def independent_verification(n: int) -> tuple[bool, str]:
    """Verify using SymPy if installed; otherwise report that it is unavailable."""
    try:
        from sympy import isprime
        return bool(isprime(n)), "sympy.isprime"
    except ImportError:
        return False, "unavailable (install sympy with: python3 -m pip install sympy)"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bits", type=int, default=512)
    parser.add_argument("--rounds", type=int, default=40)
    args = parser.parse_args()

    if args.bits < 2 or args.rounds < 1:
        parser.error("--bits must be >= 2 and --rounds must be >= 1")

    started = time.perf_counter()
    candidates_tested = 0

    while True:
        candidate = random_odd_candidate(args.bits)
        candidates_tested += 1
        if miller_rabin(candidate, args.rounds):
            prime = candidate
            break

    elapsed = time.perf_counter() - started
    independent_ok, verifier = independent_verification(prime)

    print("=== Miller-Rabin Prime Generation ===")
    print(f"Assigned bit length: {args.bits}")
    print(f"Generated probable prime: {prime}")
    print(f"Hexadecimal: 0x{prime:x}")
    print(f"Actual bit length: {prime.bit_length()}")
    print(f"Number of candidates tested: {candidates_tested}")
    print(f"Miller-Rabin rounds per candidate: {args.rounds}")
    print(f"Total execution time (seconds): {elapsed:.6f}")
    print(f"Odd: {prime % 2 == 1}")
    print(f"Top bit set: {bool(prime & (1 << (args.bits - 1)))}")
    print(f"Independent verifier: {verifier}")
    if verifier != "unavailable (install sympy with: python3 -m pip install sympy)":
        print(f"Independent verification passed: {independent_ok}")
    else:
        print("Independent verification passed: NOT CHECKED")
    print(f"Final Miller-Rabin recheck: {miller_rabin(prime, args.rounds)}")


if __name__ == "__main__":
    main()
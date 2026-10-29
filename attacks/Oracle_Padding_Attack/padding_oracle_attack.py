"""
Padding Oracle Attack on AES-CBC
--------------------------------

Educational/lab implementation for demonstrating how a CBC padding oracle
can recover plaintext without giving the attack code access to the AES key.

Requirements:
    pip install cryptography

Run:
    python padding_oracle_attack.py

The program:
1. Generates a random AES-128 key.
2. Encrypts a sample plaintext using AES-CBC + PKCS#7.
3. Exposes only a padding-oracle function to the attacker.
4. Recovers the plaintext from right to left, block by block.
5. Reports the number of oracle queries.
6. Verifies that the recovered plaintext equals the original plaintext.

IMPORTANT:
The AES key is kept inside the oracle/server side. The attack function
receives only IV + ciphertext and the oracle callable.
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os


BLOCK_SIZE = 16


# ---------------------------
# PKCS#7 padding
# ---------------------------

def pkcs7_pad(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    padder = padding.PKCS7(block_size * 8).padder()
    return padder.update(data) + padder.finalize()


def pkcs7_unpad(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    try:
        unpadder = padding.PKCS7(block_size * 8).unpadder()
        return unpadder.update(data) + unpadder.finalize()
    except ValueError as exc:
        raise ValueError("Invalid padding") from exc


# ---------------------------
# Server-side encryption
# ---------------------------

class CBCServer:
    """
    Simulates the vulnerable server.

    The AES key is stored here and is never passed to the attacker.
    """

    def __init__(self, key: bytes):
        self._key = key

    def encrypt(self, plaintext: bytes):
        iv = os.urandom(BLOCK_SIZE)
        padded = pkcs7_pad(plaintext)

        encryptor = Cipher(
            algorithms.AES(self._key),
            modes.CBC(iv)
        ).encryptor()

        ciphertext = encryptor.update(padded) + encryptor.finalize()

        return iv, ciphertext

    def padding_oracle(self, iv: bytes, ciphertext: bytes) -> bool:
        """
        The vulnerable oracle.

        Returns only whether the decrypted data has valid PKCS#7 padding.
        It deliberately does NOT return the plaintext.
        """

        if len(iv) != BLOCK_SIZE:
            return False

        if not ciphertext or len(ciphertext) % BLOCK_SIZE != 0:
            return False

        try:
            decryptor = Cipher(
                algorithms.AES(self._key),
                modes.CBC(iv)
            ).decryptor()

            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            pkcs7_unpad(plaintext)
            return True
        except ValueError:
            return False


# ---------------------------
# Padding Oracle wrapper
# ---------------------------

class CountingOracle:
    """
    Wraps the server oracle so we can count how many queries are made.
    """

    def __init__(self, server: CBCServer):
        self.server = server
        self.queries = 0

    def query(self, iv: bytes, ciphertext: bytes) -> bool:
        self.queries += 1
        return self.server.padding_oracle(iv, ciphertext)


# ---------------------------
# Attack
# ---------------------------

def recover_block(previous_block: bytes,
                  target_block: bytes,
                  oracle: CountingOracle) -> bytes:
    """
    Recover one plaintext block using the padding oracle.

    CBC decryption:
        P = D_K(C) XOR previous_block

    Let:
        I = D_K(C)

    Then:
        P = I XOR previous_block

    We recover I one byte at a time from right to left.
    """

    if len(previous_block) != BLOCK_SIZE:
        raise ValueError("previous_block must be 16 bytes")

    if len(target_block) != BLOCK_SIZE:
        raise ValueError("target_block must be 16 bytes")

    intermediate = bytearray(BLOCK_SIZE)
    recovered = bytearray(BLOCK_SIZE)

    # Work from the last byte toward the first byte.
    for pad in range(1, BLOCK_SIZE + 1):
        index = BLOCK_SIZE - pad

        # Start with a copy of the previous ciphertext block.
        forged = bytearray(previous_block)

        # Force already-recovered bytes to become the new padding value.
        for j in range(BLOCK_SIZE - 1, index, -1):
            forged[j] = intermediate[j] ^ pad

        found = False

        for guess in range(256):
            forged[index] = guess

            if not oracle.query(bytes(forged), target_block):
                continue

            # For pad == 1, a valid response can occasionally be caused by
            # the target already having valid padding. Verify the candidate
            # by perturbing the byte immediately before the padding.
            if pad == 1:
                check = bytearray(forged)
                check[index - 1] ^= 1

                if not oracle.query(bytes(check), target_block):
                    # The candidate probably produced the original padding
                    # length rather than a genuine 0x01 padding.
                    continue

            # If:
            #   D_K(C)[index] XOR forged[index] == pad
            #
            # then:
            #   D_K(C)[index] = forged[index] XOR pad
            intermediate[index] = guess ^ pad

            # Original plaintext:
            #   P[index] = D_K(C)[index] XOR previous_block[index]
            recovered[index] = intermediate[index] ^ previous_block[index]

            found = True
            break

        if not found:
            raise RuntimeError(
                f"Could not recover byte at position {index}. "
                "The oracle may not behave as expected."
            )

    return bytes(recovered)


def padding_oracle_attack(iv: bytes,
                          ciphertext: bytes,
                          oracle: CountingOracle) -> bytes:
    """
    Recover the complete padded plaintext.

    Notice what is NOT passed here:
        - AES key
        - AES cipher object
        - original plaintext

    The attack has only:
        - IV
        - ciphertext
        - a yes/no padding oracle
    """

    if len(iv) != BLOCK_SIZE:
        raise ValueError("Invalid IV length")

    if not ciphertext or len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Ciphertext must contain complete AES blocks")

    blocks = [
        ciphertext[i:i + BLOCK_SIZE]
        for i in range(0, len(ciphertext), BLOCK_SIZE)
    ]

    recovered = bytearray()

    for i, target_block in enumerate(blocks):
        previous_block = iv if i == 0 else blocks[i - 1]

        block_plaintext = recover_block(
            previous_block,
            target_block,
            oracle
        )

        recovered.extend(block_plaintext)

        print(
            f"Recovered block {i + 1}/{len(blocks)}: "
            f"{block_plaintext!r}"
        )

    return pkcs7_unpad(bytes(recovered))


# ---------------------------
# Main demonstration
# ---------------------------

def main():
    print("=" * 70)
    print("AES-CBC Padding Oracle Attack Demonstration")
    print("=" * 70)

    # Server-side secret.
    key = os.urandom(16)

    # This plaintext is known only to the server for the attack.
    original_plaintext = (
        b"Padding oracle attacks show why confidentiality alone is not "
        b"enough for secure CBC encryption."
    )

    server = CBCServer(key)
    iv, ciphertext = server.encrypt(original_plaintext)

    oracle = CountingOracle(server)

    print("\n[+] Ciphertext information given to attacker:")
    print(f"    IV         : {iv.hex()}")
    print(f"    Ciphertext : {ciphertext.hex()}")
    print(f"    Blocks     : {len(ciphertext) // BLOCK_SIZE}")

    print("\n[+] Starting attack...")
    print("    AES key is NOT passed to the attack.")
    print("    Original plaintext is NOT passed to the attack.")
    print("    Only a valid/invalid padding response is available.\n")

    recovered = padding_oracle_attack(
        iv,
        ciphertext,
        oracle
    )

    print("\n" + "=" * 70)
    print("RESULT")
    print("=" * 70)

    print(f"Original plaintext : {original_plaintext!r}")
    print(f"Recovered plaintext: {recovered!r}")
    print(f"Oracle queries     : {oracle.queries}")

    if recovered == original_plaintext:
        print("\nSUCCESS: plaintext recovered without using the AES key.")
    else:
        print("\nFAILURE: recovered plaintext does not match.")

    print("\nSecurity lesson:")
    print("AES-CBC itself was not broken.")
    print("The vulnerability was the server leaking whether padding was valid.")
    print("Use authenticated encryption such as AES-GCM, or authenticate")
    print("ciphertext before attempting CBC decryption.")


if __name__ == "__main__":
    main()

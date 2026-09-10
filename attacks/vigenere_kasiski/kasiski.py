import collections
import string

# Ciphertext 1 for Group 05 (Odd)
CIPHERTEXT = """
DAZFI SFSPA VQLSN PXYSZ WXALC DAFGQ UISMT PHZGA 
MKTTF TCCFX 
KFCRG GLPFE TZMMM ZOZDE ADWVZ WMWKV GQSOH QSVHP 
WFKLS LEASE 
PWHMJ EGKPU RVSXJ XVBWV POSDE TEQTX OBZIK WCXLW 
NUOVJ MJCLL 
OEOFA ZENVM JILOW ZEKAZ EJAQD ILSWW ESGUG KTZGQ 
ZVRMN WTQSE 
OTKTK PBSTA MQVER MJEGL JQRTL GFJYG SPTZP GTACM 
OECBX SESCI 
YGUFP KVILL TWDKS ZODFW FWEAA PQTFS TQIRG MPMEL 
RYELH QSVWB 
AWMOS DELHM UZGPG YEKZU KWTAM ZJMLS EVJQT GLAWV 
OVVXH KWQIL 
IEUYS ZWXAH HUSZO GMUZQ CIMVZ UVWIF JJHPW VXFSE 
TZEDF
"""

# Standard English Letter Frequencies
ENGLISH_FREQ = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}

def clean_ciphertext(text):
    """Remove spaces/special characters and normalize the ciphertext."""
    return ''.join([c.upper() for c in text if c.isalpha()])

def find_repeated_patterns(text, min_length=3):
    """Identify repeated sequences in the ciphertext."""
    patterns = collections.defaultdict(list)
    for length in range(min_length, len(text) // 2):
        for i in range(len(text) - length + 1):
            pattern = text[i:i+length]
            if len(patterns[pattern]) == 0:  # Only search if not already found
                pos = text.find(pattern)
                while pos != -1:
                    patterns[pattern].append(pos)
                    pos = text.find(pattern, pos + 1)
    
    # Keep only those that repeat
    return {p: positions for p, positions in patterns.items() if len(positions) > 1}

def calculate_distances(patterns):
    """Find distances between repeated occurrences."""
    distances = []
    for pattern, positions in patterns.items():
        for i in range(len(positions) - 1):
            distances.append(positions[i+1] - positions[i])
    return distances

def find_factors(distances):
    """Find factors of the distances obtained from repeated patterns."""
    factors = []
    for d in distances:
        for i in range(2, min(d + 1, 21)): # Limit to reasonable key lengths up to 20
            if d % i == 0:
                factors.append(i)
    return collections.Counter(factors)

def calculate_ic(text):
    """Calculate Index of Coincidence."""
    if not text:
        return 0
    counts = collections.Counter(text)
    n = len(text)
    if n <= 1:
        return 0
    ic = sum(f * (f - 1) for f in counts.values()) / (n * (n - 1))
    return ic

def kasiski_analysis(text):
    """Use repeated patterns/distances to suggest candidate key lengths."""
    patterns = find_repeated_patterns(text)
    distances = calculate_distances(patterns)
    factors = find_factors(distances)
    
    if not factors:
        return 1 # Fallback
        
    # Get top 5 most common factors as candidates
    candidates = [factor for factor, count in factors.most_common(5)]
    
    # We evaluate these candidates using IC
    best_length = candidates[0]
    best_ic_diff = float('inf')
    
    ic_scores = {}
    for length in candidates:
        groups = split_into_groups(text, length)
        avg_ic = sum(calculate_ic(g) for g in groups) / length
        ic_scores[length] = avg_ic
        
        # Standard English IC is ~0.066
        diff = abs(avg_ic - 0.066)
        if diff < best_ic_diff:
            best_ic_diff = diff
            best_length = length
            
    return best_length, ic_scores

def split_into_groups(text, key_length):
    """Divide ciphertext according to a candidate key length."""
    groups = [""] * key_length
    for i, char in enumerate(text):
        groups[i % key_length] += char
    return groups

def frequency_analysis(group):
    """Calculate A-Z frequency for each group."""
    counts = collections.Counter(group)
    total = len(group)
    # Return a normalized dictionary A-Z
    freq_dict = {chr(i + 65): counts.get(chr(i + 65), 0) / total for i in range(26)}
    return freq_dict

def find_shift(group):
    """Estimate the Caesar shift for a group."""
    freq_dict = frequency_analysis(group)
    
    best_shift = 0
    best_score = float('inf')
    
    # Test all 26 possible shifts
    for shift in range(26):
        score = 0
        for i in range(26):
            c_char = chr(i + 65) # Character in ciphertext group
            # If shift is k, plaintext p = (c - k) mod 26
            p_char = chr(((i - shift) % 26) + 65) 
            
            observed_freq = freq_dict.get(c_char, 0)
            expected_freq = ENGLISH_FREQ.get(p_char, 0)
            
            # Chi-squared statistic: sum( (O-E)^2 / E )
            if expected_freq > 0:
                score += ((observed_freq - expected_freq) ** 2) / expected_freq
                
        if score < best_score:
            best_score = score
            best_shift = shift
            
    return best_shift

def find_key(groups):
    """Combine shifts to obtain the probable Vigenere key."""
    key = ""
    for group in groups:
        shift = find_shift(group)
        key += chr(shift + 65)
    return key

def vigenere_decrypt(text, key):
    """Decrypt ciphertext using the recovered key."""
    decrypted = ""
    key_len = len(key)
    for i, char in enumerate(text):
        shift = ord(key[i % key_len]) - 65
        p = chr(((ord(char) - 65 - shift) % 26) + 65)
        decrypted += p
    return decrypted

def vigenere_encrypt(text, key):
    """Re-encrypt plaintext for verification."""
    encrypted = ""
    key_len = len(key)
    for i, char in enumerate(text):
        shift = ord(key[i % key_len]) - 65
        c = chr(((ord(char) - 65 + shift) % 26) + 65)
        encrypted += c
    return encrypted

def verify(plaintext, key, original_ciphertext):
    """Check whether re-encryption produces the original ciphertext."""
    re_encrypted = vigenere_encrypt(plaintext, key)
    return re_encrypted == original_ciphertext

def format_freq_table(freq_dict):
    """Helper function to format frequency dictionaries nicely."""
    sorted_freq = sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)
    return ", ".join([f"{k}: {v:.3f}" for k, v in sorted_freq[:5]]) + " ..."

if __name__ == "__main__":
    print("-" * 50)
    print("Vigenère Cryptanalysis: Kasiski & Frequency Attack")
    print("-" * 50)

    # 1. Preprocess
    cleaned_ct = clean_ciphertext(CIPHERTEXT)
    print(f"[*] Cleaned Ciphertext Length: {len(cleaned_ct)}")

    # 2. Estimate Key Length
    est_key_len, ic_scores = kasiski_analysis(cleaned_ct)
    print("\n[*] Kasiski Analysis Candidate ICs:")
    for length, ic in ic_scores.items():
        print(f"    - Length {length}: IC = {ic:.4f}")
    
    print(f"\n=> Estimated Key Length: {est_key_len}")

    # 3. Divide into groups
    groups = split_into_groups(cleaned_ct, est_key_len)

    # 4. Perform Frequency Analysis
    print("\n[*] Frequency Tables (Top 5 for each group):")
    for i, group in enumerate(groups):
        freq = frequency_analysis(group)
        print(f"    - Group {i+1}: {format_freq_table(freq)}")

    # 5. Determine the probable key
    recovered_key = find_key(groups)
    print(f"\n=> Recovered Key: {recovered_key}")

    # 6. Decrypt the ciphertext
    recovered_plaintext = vigenere_decrypt(cleaned_ct, recovered_key)
    print(f"\n=> Recovered Plaintext (First 100 chars):")
    print(recovered_plaintext[:100] + "...")

    # 7 & 8. Verify
    print("\n[*] Verifying Recovery...")
    is_valid = verify(recovered_plaintext, recovered_key, cleaned_ct)
    if is_valid:
        print("[SUCCESS] Re-encryption matches original ciphertext.")
    else:
        print("[FAILED] Re-encryption does not match.")
    print("-" * 50)
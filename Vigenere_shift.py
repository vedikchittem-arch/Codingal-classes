
import string
from collections import Counter

ABC = string.ascii_uppercase
FREQ = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0,
        0.15, 0.77, 4.0, 2.4, 6.7, 7.5, 1.9, 0.095,
        6.0, 6.3, 9.1, 2.8, 1.0, 2.4, 0.15, 2.0, 0.074]

COMMON = [
    "THE", "AND", "ING", "ION", "ENT", "TH", "HE", "IN",
    "ER", "AN", "RE", "ON", "AT", "EN", "ND", "TO", "OF",
    "ED", "IS", "IT", "FOR", "HER", "HAT", "ERE", "YOU",
    "THAT", "THIS", "WITH", "TION", "HAVE", "MENT"
]

WORDS = set("""
THE BE AND OF TO IN IS YOU THAT IT HE WAS FOR ON ARE AS
WITH HIS THEY I AT THIS HAVE FROM OR ONE HAD BY WORD BUT
NOT WHAT ALL WERE WE WHEN YOUR CAN THERE USE EACH WHICH
SHE HOW THEIR IF WILL UP OTHER ABOUT OUT MANY THEN THEM
SOME WOULD MAKE LIKE HIM INTO TIME HAS LOOK TWO MORE
WRITE GO SEE NUMBER NO WAY COULD PEOPLE MY THAN FIRST
BEEN CALL WHO ITS NOW FIND LONG DOWN DAY DID GET COME
MADE MAY PART OVER NEW TAKE ONLY WORK KNOW PLACE YEAR
LIVE BACK GIVE MOST VERY AFTER THING OUR JUST NAME GOOD
THINK SAY GREAT WHERE HELP MUCH BEFORE RIGHT TOO MEAN
ANY SAME TELL FOLLOW WANT SHOW ALSO FORM SMALL END HERE
KING QUEEN SECRET MESSAGE ATTACK CODE KEY
""".split())

def clean(text):
    return ''.join(c for c in text.upper() if c in ABC)

def decrypt(text, key):
    result = []
    j = 0
    for c in text.upper():
        if c in ABC:
            shift = ABC.index(key[j % len(key)])
            result.append(ABC[(ABC.index(c) - shift) % 26])
            j += 1
        else:
            result.append(c)
    return ''.join(result)

def caesar_shift(column):
    best_shift, best_score = 0, float("inf")
    for shift in range(26):
        counts = Counter((ABC.index(c) - shift) % 26
                         for c in column)
        n = len(column)
        score = sum(
            (counts[i] - n * FREQ[i] / 100) ** 2 /
            max(n * FREQ[i] / 100, 0.01)
            for i in range(26)
        )
        if score < best_score:
            best_shift, best_score = shift, score
    return ABC[best_shift]

def english_score(text):
    letters = clean(text)
    score = 0

    for pattern in COMMON:
        score += letters.count(pattern) * len(pattern)

    for word in text.split():
        if clean(word) in WORDS:
            score += len(word) * 12

    return score

def solve(ciphertext):
    letters = clean(ciphertext)
    if len(letters) < 8:
        return "Use a longer ciphertext for a better guess."

    candidates = []
    max_len = min(20, len(letters) // 3)

    # Estimate likely key lengths using Index of Coincidence
    for length in range(1, max_len + 1):
        ics = []
        for i in range(length):
            col = letters[i::length]
            n = len(col)
            if n > 1:
                counts = Counter(col)
                ic = sum(v * (v - 1) for v in counts.values()) / (
                    n * (n - 1)
                )
                ics.append(ic)
        if ics:
            candidates.append((sum(ics) / len(ics), length))

    # Test the most promising key lengths
    candidates.sort(reverse=True)
    best_key, best_text, best_score = "", "", float("-inf")

    for _, length in candidates[:10]:
        key = ''.join(
            caesar_shift(letters[i::length])
            for i in range(length)
        )
        text = decrypt(ciphertext, key)
        score = english_score(text) - length * 0.5

        if score > best_score:
            best_key, best_text, best_score = key, text, score

    print("Likely key:", best_key)
    return best_text

ciphertext = input("Enter the Vigenere ciphertext: ")
print("\nBest decryption:")
print(solve(ciphertext))

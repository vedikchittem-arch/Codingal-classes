
import random
import string
import math
import re
from collections import Counter

ABC = string.ascii_uppercase

# Common English letter combinations
QUADS = {
    "TION": 12, "NTHE": 11, "THER": 11, "THAT": 10,
    "OFTH": 10, "FTHE": 10, "WITH": 10, "ATIO": 9,
    "MENT": 9, "IONS": 9, "THIS": 9, "HERE": 8,
    "OULD": 8, "IGHT": 8, "HAVE": 8, "ENCE": 8,
    "EDTH": 7, "THEM": 7, "TING": 7, "EVER": 7,
    "FROM": 7, "THEI": 7, "ETHE": 7, "ANDT": 7,
    "THES": 7, "INTH": 7, "THIN": 7, "ATIO": 7,
    "ERES": 6, "ANCE": 6, "ALLY": 6, "EING": 6,
    "WERE": 6, "RETH": 6, "NING": 6, "ABLE": 6
}

COMMON_WORDS = set("""
THE BE TO OF AND A IN THAT HAVE I IT FOR NOT ON WITH HE
AS YOU DO AT THIS BUT HIS BY FROM THEY WE SAY HER SHE OR
AN WILL MY ONE ALL WOULD THERE THEIR WHAT SO UP OUT IF
ABOUT WHO GET WHICH GO ME WHEN MAKE CAN LIKE TIME NO JUST
HIM KNOW TAKE PEOPLE INTO YEAR YOUR GOOD SOME COULD THEM
SEE OTHER THAN THEN NOW LOOK ONLY COME ITS OVER THINK ALSO
BACK AFTER USE TWO HOW OUR WORK FIRST WELL WAY EVEN NEW
WANT BECAUSE ANY THESE GIVE DAY MOST US IS WAS ARE WERE
BEEN HAS HAD DID SAID EACH MANY MUCH WHERE THROUGH BEFORE
RIGHT SHOULD WORLD STILL OWN LAST NEVER HERE WHILE THING
LIFE PLACE LONG GREAT SMALL EVERY FOUND UNDER STATE THREE
HOUSE NIGHT LIGHT KING QUEEN SECRET MESSAGE ATTACK ENEMY
LETTER CODE KEY MEET AT DAWN MEET THE KING
""".split())

def clean(text):
    return ''.join(c for c in text.upper() if c in ABC)

def decrypt(ciphertext, key):
    """Plaintext-autokey decryption."""
    result = []
    j = 0

    for char in ciphertext.upper():
        if char in ABC:
            i = ABC.index(char)

            if j < len(key):
                shift = ABC.index(key[j])
            else:
                shift = result[j - len(key)]

            result.append((i - shift) % 26)
            j += 1
        else:
            result.append(char)

    return ''.join(ABC[x] if x >= 0 else x for x in result)

def score(text):
    letters = clean(text)

    if len(letters) < 4:
        return -999999

    points = 0

    # Score common four-letter combinations
    for quad, weight in QUADS.items():
        points += letters.count(quad) * weight

    # Score common words, favouring longer matches
    for word in re.findall(r"[A-Z]+", text.upper()):
        if word in COMMON_WORDS:
            points += len(word) ** 1.5 * 4

    # Reward realistic English letter frequencies
    expected = "ETAOINSHRDLU"
    counts = Counter(letters)
    ranked = ''.join(c for c, _ in counts.most_common())

    for i, char in enumerate(expected):
        if i < len(ranked) and ranked[i] == char:
            points += 1

    # Penalise unusual letter combinations
    for bad in ("JQ", "QJ", "QZ", "ZX", "VVV", "JJ"):
        points -= letters.count(bad) * 4

    return points

def solve(ciphertext, max_key_length=20,
          restarts=12, iterations=2500):

    letters = clean(ciphertext)

    if len(letters) < 12:
        return None, "Use at least 12 letters for a better chance."

    best_key = ""
    best_plain = ""
    best_score = float("-inf")

    max_len = min(max_key_length, len(letters) // 3)

    for length in range(1, max_len + 1):
        for restart in range(restarts):

            key = [random.randrange(26) for _ in range(length)]
            key_text = ''.join(ABC[x] for x in key)
            plain = decrypt(ciphertext, key_text)
            current_score = score(plain)

            for step in range(iterations):
                pos = random.randrange(length)
                old = key[pos]

                # Try a different letter in the keyword
                new = random.randrange(26)
                while new == old:
                    new = random.randrange(26)

                key[pos] = new
                candidate_key = ''.join(ABC[x] for x in key)
                candidate = decrypt(ciphertext, candidate_key)
                candidate_score = score(candidate)

                temperature = max(
                    0.15, 6 * (1 - step / iterations)
                )

                accept = (
                    candidate_score > current_score or
                    random.random() < math.exp(
                        max(-100, min(0,
                            (candidate_score - current_score)
                            / temperature
                        ))
                    )
                )

                if accept:
                    plain = candidate
                    current_score = candidate_score
                else:
                    key[pos] = old

                if current_score > best_score:
                    best_score = current_score
                    best_key = ''.join(ABC[x] for x in key)
                    best_plain = plain

    return best_key, best_plain

ciphertext = input("Enter Autokey ciphertext: ")

print("\nSearching for the key...")
key, plaintext = solve(ciphertext)

if key is None:
    print(plaintext)
else:
    print("\nBest estimated keyword:", key)
    print("Best estimated plaintext:")
    print(plaintext)
    print("\nNote: this is the best candidate found,")
    print("not a guarantee that the decryption is correct.")

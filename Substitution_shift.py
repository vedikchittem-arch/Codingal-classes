
import random
import string
import math

ALPHABET = string.ascii_uppercase

COMMON = [
    "THE", "AND", "ING", "ION", "ENT", "HER", "FOR", "THA",
    "NTH", "INT", "ERE", "TIO", "TER", "EST", "ERS", "ATI",
    "HAT", "ATE", "ALL", "ETH", "HES", "VER", "HIS", "OFT",
    "TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN",
    "ND", "TI", "ES", "OR", "TE", "OF", "ED", "IS", "IT",
    "AL", "AR", "ST", "TO", "NT", "NG", "SE", "HA", "AS",
    "OU", "IO", "LE", "VE", "CO", "ME", "DE", "HI", "RI"
]

WORDS = set("""
THE BE AND OF TO IN IS YOU THAT IT HE WAS FOR ON ARE AS WITH
HIS THEY I AT BE THIS HAVE FROM OR ONE HAD BY WORD BUT NOT WHAT
ALL WERE WE WHEN YOUR CAN SAID THERE USE EACH WHICH SHE HOW
THEIR IF WILL UP OTHER ABOUT OUT MANY THEN THEM THESE SO SOME
HER WOULD MAKE LIKE HIM INTO TIME HAS LOOK TWO MORE WRITE GO
SEE NUMBER NO WAY COULD PEOPLE MY THAN FIRST WATER BEEN CALL
WHO OIL ITS NOW FIND LONG DOWN DAY DID GET COME MADE MAY
PART OVER NEW SOUND TAKE ONLY LITTLE WORK KNOW PLACE YEAR
LIVE ME BACK GIVE MOST VERY AFTER THING OUR JUST NAME GOOD
MAN THINK SAY GREAT WHERE HELP THROUGH MUCH BEFORE LINE RIGHT
TOO MEAN OLD ANY SAME TELL BOY FOLLOW CAME WANT SHOW ALSO
AROUND FORM THREE SMALL SET PUT END DOES ANOTHER WELL LARGE
MUST BIG EVEN SUCH BECAUSE TURN HERE WHY ASK WENT MEN READ
NEED LAND DIFFERENT HOME US MOVE TRY KIND HAND PICTURE AGAIN
CHANGE OFF PLAY SPELL AIR AWAY ANIMAL HOUSE POINT PAGE LETTER
MOTHER FATHER KING QUEEN WAR NIGHT DARK DAY LIGHT DEATH LIFE
""".split())

def clean(text):
    return ''.join(c for c in text.upper() if c in ALPHABET)

def decrypt(text, key):
    return ''.join(
        key[ALPHABET.index(c)] if c in ALPHABET else c
        for c in text.upper()
    )

def score(text):
    letters = clean(text)
    if not letters:
        return -999999

    points = 0

    for pattern in COMMON:
        points += letters.count(pattern) * len(pattern)

    for word in text.split():
        word = clean(word)
        if word in WORDS:
            points += len(word) * 10

    expected = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
    counts = {c: letters.count(c) for c in ALPHABET}
    actual = sorted(ALPHABET, key=lambda c: counts[c], reverse=True)
    points += sum(
        1 for a, b in zip(actual, expected) if a == b
    ) * 2

    return points

def solve(ciphertext, restarts=20, iterations=4000):
    best_text = ""
    best_score = float("-inf")

    cipher_letters = clean(ciphertext)
    if not cipher_letters:
        return "Please enter some ciphertext containing letters."

    for _ in range(restarts):
        key = list(ALPHABET)
        random.shuffle(key)

        current = decrypt(ciphertext, key)
        current_score = score(current)

        for step in range(iterations):
    
            a, b = random.sample(range(26), 2)
            key[a], key[b] = key[b], key[a]

            candidate = decrypt(ciphertext, key)
            candidate_score = score(candidate)

            temperature = max(0.1, 8 * (1 - step / iterations))

            if (candidate_score > current_score or
                random.random() < math.exp(
                    (candidate_score - current_score) / temperature
                )):
                current = candidate
                current_score = candidate_score
            else:
                key[a], key[b] = key[b], key[a]

            if current_score > best_score:
                best_score = current_score
                best_text = current

    return best_text

ciphertext = input("Enter the substitution cipher: ")

print("\nBest automatic decryption:")
print(solve(ciphertext))



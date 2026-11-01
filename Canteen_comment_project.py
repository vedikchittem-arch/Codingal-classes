
# CANTEEN COMMENT BOX
# ---------- SETUP (given to you) ----------
LEXICON = {
    "delicious": 3, "great": 3, "tasty": 2, "kind": 2, "fresh": 2, "good": 2,
    "cold": -1, "slow": -1, "bad": -2, "rude": -2, "burnt": -2, "awful": -3,
}
NEGATIONS = {"not", "never", "no"}
PUNCTUATION = ".,!?:;\"'()"

TEST_COMMENTS = [
    ("The pasta was delicious and the staff were kind", "HAPPY"),
    ("The queue was slow and the juice was awful", "UNHAPPY"),
    ("Not good, the rice was cold", "UNHAPPY"),
    ("Not bad at all, I will come again", "HAPPY"),
    ("Lunch is at 1 pm on Fridays", "OK"),
    ("Great, they ran out of food again", "UNHAPPY"),
]

# ---------- PART 1: clean the words ----------
def clean_words(comment):
    words = comment.split()
    cleaned = []

    for word in words:
        word = word.lower()
        word = word.strip(PUNCTUATION)
        cleaned.append(word)

    return cleaned


print("PART 1: Clean words")
print(clean_words("Not GOOD, the rice was cold!"))


# ---------- PART 2: score the comment ----------
def comment_score(comment):
    score = 0
    flip = False

    for word in clean_words(comment):
        if word in NEGATIONS:
            flip = True

        elif word in LEXICON:
            points = LEXICON[word]

            if flip:
                points = -points
                flip = False

            score += points

    return score


print("\nPART 2: Score")
print(comment_score("Not good, the rice was cold"))


# ---------- PART 3: decide the mood ----------
def mood(comment):
    score = comment_score(comment)

    if score >= 1:
        return "HAPPY"

    elif score <= -1:
        return "UNHAPPY"

    else:
        return "OK"


print("\nPART 3: Mood")
print(mood("The pasta was delicious and the staff were kind"))


# ---------- PART 4: check every test comment ----------
print("\nPART 4: Test all comments")

mistakes = 0

for comment, expected in TEST_COMMENTS:
    result = mood(comment)
    score = comment_score(comment)

    if result != expected:
        mistakes += 1

    print(result, score, "-", comment)

print("Mistakes:", mistakes, "out of", len(TEST_COMMENTS))


# BAKERY HELP DESK SORTER
# ---------- SETUP (given to you) ----------
URGENT_WORDS = {
    "refund": 3, "broken": 3, "late": 2, "missing": 2, "wrong": 2,
    "cancel": 2, "never": 2, "again": 1, "now": 1,
}
THRESHOLD = 4
PUNCTUATION = ".,!?:;\"'()"

TEST_MESSAGES = [
    ("My cake arrived broken and I want a refund now!", "URGENT"),
    ("The delivery is late again, and my order is missing", "URGENT"),
    ("Thank you, the cupcakes were delicious", "NORMAL"),
    ("Do you sell gluten free bread?", "NORMAL"),
    ("Can I cancel my order? I ordered the wrong size", "URGENT"),
    ("I never had a late delivery before, great service!", "NORMAL"),
]

# ---------- PART 1: clean the words ----------
def tokenize(message):
    words = message.split()
    cleaned = []

    for word in words:
        word = word.lower().strip(PUNCTUATION)

        if word != "":
            cleaned.append(word)

    return cleaned


print("PART 1: Clean words")
print(tokenize("Where is my REFUND?!"))


# ---------- PART 2: score the message ----------
def urgency_score(message):
    score = 0

    for word in tokenize(message):
        score += URGENT_WORDS.get(word, 0)

    return score


print("\nPART 2: Score")
print(urgency_score("My cake arrived broken and I want a refund now!"))


# ---------- PART 3: label the message ----------
def label(message):
    if urgency_score(message) >= THRESHOLD:
        return "URGENT"
    else:
        return "NORMAL"


print("\nPART 3: Label")
print(label("Thank you, the cupcakes were delicious"))


# ---------- PART 4: check every test message ----------
print("\nPART 4: Test all messages")
mistakes = 0

for message, expected in TEST_MESSAGES:
    result = label(message)
    score = urgency_score(message)

    if result != expected:
        mistakes += 1

    print(result, score, message)

print("Mistakes:", mistakes, "out of", len(TEST_MESSAGES))


# Common English words
COMMON_WORDS = {
    "THE", "BE", "TO", "OF", "AND", "A", "IN", "THAT",
    "HAVE", "I", "IT", "FOR", "NOT", "ON", "WITH",
    "HE", "AS", "YOU", "DO", "AT", "THIS", "BUT",
    "HELLO", "WORLD", "CODE", "CIPHER", "SECRET",
    "KEY", "IS", "MY", "NAME", "TEST", "GOOD",
    "YES", "NO", "CAT", "DOG", "MEET", "ATTACK"
}


def caesar(text, shift):
    result = ""

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char

    return result


def solve_caesar(text):
    candidates = []

    for shift in range(26):
        decrypted = caesar(text, -shift)

        words = decrypted.upper().split()
        score = sum(word in COMMON_WORDS for word in words)

        candidates.append((score, shift, decrypted))

    candidates.sort(reverse=True)

    best_score, best_shift, best_result = candidates[0]

    print("\n--- AUTOMATIC SOLUTION ---")
    print("Best guess:", best_result)
    print("Shift:", best_shift)
    print("Word matches:", best_score)

    print("\nOther possibilities:")
    for score, shift, result in candidates[:5]:
        print(f"Shift {shift:2}: {result}")


# Run the program
message = input("Enter encrypted message: ")
solve_caesar(message)
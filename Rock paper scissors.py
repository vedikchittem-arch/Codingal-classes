import random

# Possible moves
moves = ["ROCK", "PAPER", "SCISSORS"]

# Scores
player_score = 0
ai_score = 0

def get_player_move():
    while True:
        move = input("Enter Rock, Paper, or Scissors: ").upper()
        if move in moves:
            return move
        print("Invalid input. Please enter Rock, Paper, or Scissors.")

def get_ai_move():
    return random.choice(moves)

def check_win(player, ai):
    if player == ai:
        return "Tie"
    elif (
        (player == "ROCK" and ai == "SCISSORS") or
        (player == "PAPER" and ai == "ROCK") or
        (player == "SCISSORS" and ai == "PAPER")
    ):
        return "Player"
    else:
        return "AI"

while True:
    player_move = get_player_move()
    ai_move = get_ai_move()

    print(f"\nYou chose: {player_move}")
    print(f"AI chose: {ai_move}")

    result = check_win(player_move, ai_move)

    if result == "Tie":
        print("It's a tie!")
    elif result == "Player":
        print("You win this round!")
        player_score += 1
    else:
        print("AI wins this round!")
        ai_score += 1

    print(f"Player: {player_score}")
    print(f"AI: {ai_score}")

    play_again = input("\nPlay another round? (yes/no): ").strip().lower()
    if play_again != "yes":
        print(f"Player: {player_score}")
        print(f"AI: {ai_score}")
        print("Thanks for playing!")
        break
    else:
        True
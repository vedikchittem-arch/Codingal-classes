import pandas as pd
from textblob import TextBlob
from colorama import init, Fore

init(autoreset=True)

try:
    df = pd.read_csv("Movies.csv")
except FileNotFoundError:
    print(Fore.RED + "Error: CSV file not found!")
    exit()

print(Fore.CYAN + "\n🎬 MOVIE AI RECOMMENDER 🎬")
print(Fore.WHITE + "---------------------------")


genres = sorted(df["Genre"].dropna().unique())

print(Fore.YELLOW + "\nAvailable genres:")
for genre in genres:
    print(Fore.WHITE + "- " + genre)

genre = input(Fore.GREEN + "\nWhat genre do you want? ").strip()


matches = df[df["Genre"].str.lower() == genre.lower()].copy()

if matches.empty:
    print(Fore.RED + "\nThat genre wasn't found.")
    exit()


while True:
    try:
        rating = float(input(
            Fore.CYAN + "Minimum IMDb rating (7.6-10): "
        ))

        if 7.6 <= rating <= 10:
            break

        print(Fore.RED + "Please enter a rating between 7.6 and 10.")

    except ValueError:
        print(Fore.RED + "Please enter a number.")

print(Fore.YELLOW + "\nTell me what you want from the movie.")
print(Fore.WHITE + "(Example: exciting, funny, emotional, dark, relaxing...)")

request = input(Fore.GREEN + "You: ")

sentiment = TextBlob(request).sentiment.polarity

if sentiment > 0.3:
    mood = "positive"
    print(Fore.GREEN + "\nAI: You sound like you're in a good mood! 😃")

elif sentiment < -0.3:
    mood = "negative"
    print(Fore.BLUE + "\nAI: You seem to want something more serious. 😔")

else:
    mood = "neutral"
    print(Fore.YELLOW + "\nAI: I'll find something balanced for you. 😐")

movies = matches[matches["IMDb Rating"] >= rating].copy()

if movies.empty:
    print(Fore.RED + "\nNo movies match your genre and rating.")
    exit()

def recommendation_score(movie):
    score = movie["IMDb Rating"]

    # Sentiment-based bonus
    if mood == "positive":
        if movie["Genre"] in ["Comedy", "Animation", "Adventure"]:
            score += 0.5

    elif mood == "negative":
        if movie["Genre"] in ["Drama", "Romance", "Thriller"]:
            score += 0.5

    return score

movies["Score"] = movies.apply(recommendation_score, axis=1)

shown = set()

while True:

    available = movies[~movies["Movie"].isin(shown)]

    if available.empty:
        print(Fore.RED + "\nI've run out of movies matching your choices!")
        break

    recommendations = available.sort_values(
        "Score", ascending=False
    ).head(5)

    print(Fore.CYAN + "\n🍿 RECOMMENDATIONS 🍿")
    print(Fore.WHITE + "-------------------------")

    for _, movie in recommendations.iterrows():
        print(
            Fore.GREEN + movie["Movie"] +
            Fore.YELLOW + " ⭐ " +
            str(movie["IMDb Rating"]) +
            Fore.WHITE + " | " +
            movie["Genre"]
        )


    for movie in recommendations["Movie"]:
        shown.add(movie)

    choice = input(
        Fore.GREEN +
        "\nDo you like these movies? (yes/no): "
    ).lower()

    if choice in ["yes", "y"]:
        print(Fore.GREEN + "\nAI: Great! Enjoy your movie! 🎬")
        break

    elif choice in ["no", "n"]:
        print(
            Fore.YELLOW +
            "\nAI: No problem! Here's another 5... 🔎"
        )

    else:
        print(
            Fore.YELLOW +
            "\nAI: I'll give you another 5 recommendations."
        )

print(Fore.CYAN + "\nThanks for using Movie AI! 🎥")
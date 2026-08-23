import re, random
from datetime import datetime
from zoneinfo import ZoneInfo
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


destinations = {
    "beaches": ["Bali", "Maldives", "Phuket"],
    "mountains": ["Swiss Alps", "Rocky Mountains", "Himalayas"],
    "cities": ["Tokyo", "Paris", "New York"]
}

jokes = [
    "Why don't programmers like nature? Too many bugs!",
    "Why did the computer go to the doctor? Because it had a virus!",
    "Why do travelers always feel warm? Because of all their hot spots!"
]

weather = {
    "london": "Cloudy, 18°C",
    "paris": "Sunny, 22°C",
    "tokyo": "Partly cloudy, 26°C",
    "new york": "Sunny, 24°C",
    "dubai": "Sunny, 35°C",
    "sydney": "Clear, 20°C"
}

news = [
    "Scientists have announced a new breakthrough in space exploration.",
    "A new technology exhibition has opened in London.",
    "Several countries are investing in greener forms of transport.",
    "A major international travel festival is taking place this week."
]

time_zones = {
    "london": "Europe/London",
    "paris": "Europe/Paris",
    "tokyo": "Asia/Tokyo",
    "new york": "America/New_York",
    "dubai": "Asia/Dubai",
    "sydney": "Australia/Sydney"
}

conversation_history = []



# Normalize input by removing extra spaces and making it lowercase
def normalize_input(text):
    return re.sub(r"\s+", " ", text.strip().lower())


# Save a message to memory
def remember(message):
    conversation_history.append(message)


# Save conversation history to a file
def save_history():
    with open("travelbot_history.txt", "w") as file:
        for message in conversation_history:
            file.write(message + "\n")



# Provide travel recommendations
def recommend():
    print(Fore.CYAN + "TravelBot: Beaches, mountains, or cities?")
    preference = normalize_input(input(Fore.YELLOW + "You: "))
    remember("Preference: " + preference)

    if preference in destinations:
        suggestion = random.choice(destinations[preference])

        print(Fore.GREEN + f"TravelBot: How about {suggestion}?")
        print(Fore.CYAN + "TravelBot: Do you like it? (yes/no)")

        answer = normalize_input(input(Fore.YELLOW + "You: "))

        if re.search(r"\b(yes|yeah|yep|sure)\b", answer):
            print(Fore.GREEN + f"TravelBot: Awesome! Enjoy {suggestion}!")

        elif re.search(r"\b(no|nope|nah)\b", answer):
            print(Fore.RED + "TravelBot: Let's try another.")
            recommend()

        else:
            print(Fore.RED + "TravelBot: I'll suggest again.")
            recommend()

    else:
        print(Fore.RED + "TravelBot: Sorry, I don't have that type of destination.")
        recommend()



def packing_tips():
    print(Fore.CYAN + "TravelBot: Where to?")
    location = normalize_input(input(Fore.YELLOW + "You: "))

    print(Fore.CYAN + "TravelBot: How many days?")
    days = input(Fore.YELLOW + "You: ")

    remember("Packing trip: " + location + " for " + days + " days")

    print(Fore.GREEN + f"TravelBot: Packing tips for {days} days in {location}:")
    print(Fore.GREEN + "- Pack versatile clothes.")
    print(Fore.GREEN + "- Bring chargers/adapters.")
    print(Fore.GREEN + "- Check the weather forecast.")
    print(Fore.GREEN + "- Keep important documents somewhere safe.")


# Tell a random joke
def tell_joke():
    print(Fore.YELLOW + f"TravelBot: {random.choice(jokes)}")



def weather_info():
    print(Fore.CYAN + "TravelBot: Which city would you like the weather for?")

    city = normalize_input(input(Fore.YELLOW + "You: "))

    if city in weather:
        print(Fore.GREEN + f"TravelBot: Weather in {city.title()}: {weather[city]}")
    else:
        print(Fore.RED + "TravelBot: I don't have simulated weather for that city.")
        print(Fore.MAGENTA + "Available cities:", ", ".join(weather.keys()))


def news_update():
    print(Fore.CYAN + "TravelBot: Here are some simulated news updates:")

    selected_news = random.sample(news, min(3, len(news)))

    for story in selected_news:
        print(Fore.GREEN + "• " + story)



def local_time():
    print(Fore.CYAN + "TravelBot: Which city do you want the time for?")

    city = normalize_input(input(Fore.YELLOW + "You: "))

    if city in time_zones:
        current_time = datetime.now(ZoneInfo(time_zones[city]))
        formatted_time = current_time.strftime("%H:%M:%S")

        print(
            Fore.GREEN +
            f"TravelBot: The current time in {city.title()} is {formatted_time}."
        )

    else:
        print(Fore.RED + "TravelBot: I don't know that city's time zone.")
        print(Fore.MAGENTA + "Available cities:", ", ".join(time_zones.keys()))



def show_memory(name):
    print(Fore.MAGENTA + "\nTravelBot Memory:")

    print(Fore.GREEN + f"- Your name is {name}")

    if len(conversation_history) > 0:
        print(Fore.GREEN + f"- I remember {len(conversation_history)} previous inputs.")
    else:
        print(Fore.GREEN + "- No previous inputs stored yet.")



def show_help():
    print(Fore.MAGENTA + "\n========== TravelBot Help ==========")

    print(Fore.GREEN + "Travel:")
    print("- Say 'recommendation' for travel suggestions")
    print("- Say 'packing' for packing tips")

    print(Fore.GREEN + "\nEntertainment:")
    print("- Say 'joke' for a joke")

    print(Fore.GREEN + "\nInformation:")
    print("- Say 'weather' for simulated weather")
    print("- Say 'news' for simulated news")
    print("- Say 'time' for the time in another city")

    print(Fore.GREEN + "\nMemory:")
    print("- Say 'memory' to see what I remember")

    print(Fore.CYAN + "\nType 'exit' or 'bye' to end.")
    print(Fore.MAGENTA + "====================================\n")


def chat():

    print(Fore.CYAN + Style.BRIGHT + "Hello! I'm TravelBot.")

    name = input(Fore.YELLOW + "Your name? ")
    name = normalize_input(name)

    print(Fore.GREEN + f"Nice to meet you, {name.title()}!")

    show_help()

    while True:

        user_input = input(Fore.YELLOW + f"{name.title()}: ")
        user_input = normalize_input(user_input)

        # Save input to memory
        remember(user_input)


        if re.search(r"\b(recommend|recommendation|suggest|suggestion)\b", user_input):
            recommend()

        elif re.search(r"\b(pack|packing)\b", user_input):
            packing_tips()

        elif re.search(r"\b(joke|funny)\b", user_input):
            tell_joke()

        elif re.search(r"\b(weather|temperature|forecast)\b", user_input):
            weather_info()

        elif re.search(r"\b(news|headlines|updates)\b", user_input):
            news_update()

        elif re.search(r"\b(time|clock)\b", user_input):
            local_time()

        elif re.search(r"\b(memory|remember)\b", user_input):
            show_memory(name)

        elif re.search(r"\b(help|commands)\b", user_input):
            show_help()

        elif re.search(r"\b(exit|bye|quit|goodbye)\b", user_input):
            save_history()

            print(Fore.CYAN + "TravelBot: Safe travels! Goodbye!")
            print(Fore.MAGENTA + "Conversation history saved.")
            break

        else:
            print(
                Fore.RED +
                "TravelBot: I don't understand that yet. "
                "Try saying 'help' to see what I can do."
            )



if __name__ == "__main__":
    chat()
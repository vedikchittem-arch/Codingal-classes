
import requests
import time
import json
from datetime import datetime

# ==========================================
# REALITY SCANNER
# Internet Intelligence Dashboard
# ==========================================

session = requests.Session()
session.headers.update({
    "User-Agent": "RealityScanner/1.0"
})

BASE_URL = "https://api.open-notify.org"


def line():
    print("=" * 55)


def get_data(url, params=None):
    """Request data from an API and return JSON."""
    try:
        response = session.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        print(f"\n[ERROR] Could not contact server: {error}")
        return None

    except ValueError:
        print("\n[ERROR] The server returned invalid JSON.")
        return None


def earth_watch():
    """Retrieve recent earthquake information."""
    line()
    print("🌍 EARTH WATCH")
    line()

    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    params = {
        "format": "geojson",
        "limit": 10,
        "orderby": "time",
        "minmagnitude": 4.5
    }

    data = get_data(url, params)

    if not data:
        return

    earthquakes = data.get("features", [])

    if not earthquakes:
        print("No matching earthquakes were returned.")
        return

    print("Recent earthquakes of magnitude 4.5 or greater:\n")

    for number, quake in enumerate(earthquakes, 1):
        details = quake["properties"]

        magnitude = details.get("mag")
        location = details.get("place", "Unknown location")
        timestamp = details.get("time")

        if timestamp:
            date = datetime.fromtimestamp(
                timestamp / 1000
            ).strftime("%d %b %Y, %H:%M UTC")
        else:
            date = "Unknown time"

        print(f"{number}. Magnitude: {magnitude}")
        print(f"   Location: {location}")
        print(f"   Time: {date}\n")


def space_tracker():
    """Find the current position of the ISS."""
    line()
    print("🚀 SPACE TRACKER")
    line()

    url = "https://api.wheretheiss.at/v1/satellites/25544"

    data = get_data(url)

    if not data:
        return

    print(f"Latitude:  {data['latitude']:.4f}°")
    print(f"Longitude: {data['longitude']:.4f}°")
    print(f"Altitude:  {data['altitude']:.2f} km")
    print(f"Velocity:  {data['velocity']:.2f} km/h")

    print("\nLive map:")
    print(
        "https://www.google.com/maps/search/?api=1&query="
        f"{data['latitude']},{data['longitude']}"
    )


def news_scanner():
    """Retrieve recent headlines using a public news feed."""
    line()
    print("📰 NEWS SCANNER")
    line()

    url = "https://feeds.bbci.co.uk/news/world/rss.xml"

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()

        import xml.etree.ElementTree as ET

        root = ET.fromstring(response.content)
        articles = root.findall("./channel/item")

        if not articles:
            print("No articles were found.")
            return

        for number, article in enumerate(articles[:10], 1):
            title = article.findtext("title", "Untitled")
            link = article.findtext("link", "")

            print(f"\n{number}. {title}")
            print(f"   {link}")

    except (requests.RequestException, ET.ParseError) as error:
        print(f"Could not retrieve news: {error}")


def website_inspector():
    """Check whether a website responds."""
    line()
    print("🌐 WEBSITE INSPECTOR")
    line()

    website = input("Enter a website (e.g. https://example.com): ").strip()

    if not website.startswith(("https://", "http://")):
        website = "https://" + website

    print("\nScanning website...")

    try:
        start = time.perf_counter()

        response = session.get(
            website,
            timeout=10,
            allow_redirects=True
        )

        elapsed = time.perf_counter() - start

        print(f"\nStatus code: {response.status_code}")
        print(f"Response time: {elapsed * 1000:.2f} ms")
        print(f"Final URL: {response.url}")

        if response.ok:
            print("Result: Website responded successfully.")
        else:
            print("Result: Website responded with an HTTP error.")

    except requests.RequestException as error:
        print(f"\nWebsite could not be reached: {error}")


def ip_intelligence():
    """Retrieve approximate public IP information."""
    line()
    print("🔎 IP INTELLIGENCE")
    line()

    ip = input(
        "Enter an IP address, or press Enter for your public IP: "
    ).strip()

    if ip:
        url = f"https://ipwho.is/{ip}"
    else:
        url = "https://ipwho.is/"

    data = get_data(url)

    if not data:
        return

    if not data.get("success", False):
        print("Lookup failed:", data.get("message", "Unknown error"))
        return

    connection = data.get("connection") or {}

    print("\nIP INFORMATION")
    print(f"IP address: {data.get('ip', 'Unknown')}")
    print(f"Country: {data.get('country', 'Unknown')}")
    print(f"Region: {data.get('region', 'Unknown')}")
    print(f"City: {data.get('city', 'Unknown')}")
    print(f"Latitude: {data.get('latitude', 'Unknown')}")
    print(f"Longitude: {data.get('longitude', 'Unknown')}")
    print(f"Internet provider: {connection.get('isp', 'Unknown')}")

    print("\nNote: Location estimates are approximate.")
    print("This does not reveal someone's exact home address.")


def random_discovery():
    """Discover a random fact from a public API."""
    line()
    print("🎲 RANDOM DISCOVERY")
    line()

    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"

    data = get_data(url, {"language": "en"})

    if data:
        print("\nYour random fact:\n")
        print(data.get("text", "No fact returned."))


def main():
    while True:
        line()
        print("       REALITY SCANNER v1.0")
        print("       INTERNET INTELLIGENCE")
        line()

        print("1. Earth Watch")
        print("2. Space Tracker")
        print("3. News Scanner")
        print("4. Website Inspector")
        print("5. IP Intelligence")
        print("6. Random Discovery")
        print("7. Exit")

        line()

        choice = input("Select a module: ").strip()

        if choice == "1":
            earth_watch()
        elif choice == "2":
            space_tracker()
        elif choice == "3":
            news_scanner()
        elif choice == "4":
            website_inspector()
        elif choice == "5":
            ip_intelligence()
        elif choice == "6":
            random_discovery()
        elif choice == "7":
            print("\nReality Scanner shutting down...")
            break
        else:
            print("\nInvalid option. Choose 1–7.")

        input("\nPress Enter to return to the dashboard...")


if __name__ == "__main__":
    main()

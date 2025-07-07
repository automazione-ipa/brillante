"""Concrete implementations of TravelForge GPT-callable functions."""

def read_file(path: str) -> str:
    """Reads the contents of a file and returns it as a string."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(path: str, content: str) -> str:
    """Writes the given content to a file and returns a confirmation."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return f"File scritto correttamente in: {path}"


def generate_schema(city_country: str, duration_days: int, season_or_dates: dict) -> dict:
    """Generates a basic itinerary schema. Placeholder version."""
    itinerary = []
    for i in range(duration_days):
        itinerary.append({
            "day": i + 1,
            "activity": f"Esplora attrazione locale {i+1} a {city_country}"
        })
    return {"city": city_country, "itinerary": itinerary}


def search_images(keywords: list[str]) -> dict:
    """Returns fake image URLs for the given keywords."""
    return {kw: [f"https://fakeimg.pl/600x400/?text={kw.replace(' ', '+')}"] for kw in keywords}


def fetch_prices(itinerary: list[dict], dates: dict) -> dict:
    """Returns mock prices for each activity in the itinerary."""
    return {
        step["activity"]: {
            "price": 25.0 + i * 5,
            "currency": "EUR"
        }
        for i, step in enumerate(itinerary)
    }


def build_report(city: str, dates: dict, itinerary: list[dict], images: dict, prices: dict) -> str:
    """Generates a markdown report from the itinerary."""
    report = [f"# Viaggio a {city}\n", f"## Date: {dates}\n", "## Itinerario:\n"]
    for step in itinerary:
        day = step["day"]
        activity = step["activity"]
        image = images.get(activity, [""])[0]
        price_info = prices.get(activity, {})
        report.append(f"### Giorno {day}: {activity}")
        if image:
            report.append(f"![{activity}]({image})")
        if price_info:
            report.append(f"**Prezzo stimato**: {price_info['price']} {price_info['currency']}")
        report.append("")  # spacing
    return "\n".join(report)

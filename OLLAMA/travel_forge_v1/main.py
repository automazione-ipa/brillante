from interactive_agent import ItineraryAgent


def main():
    print("Benvenuto in TravelForge CLI ✈️")

    city_country = input("📍 Destinazione (es: Kyoto, Japan): ")
    duration_days = int(input("📆 Durata in giorni: "))
    season = input("🗓️  Stagione o periodo (es: Primavera, o '2025-04-10 to 2025-04-20'): ")

    season_or_dates = {"label": season}  # semplice dict compatibile

    agent = ItineraryAgent()
    markdown = agent.run(city_country, duration_days, season_or_dates)

    output_path = f"report_{city_country.replace(',', '').replace(' ', '_')}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"\n✅ Report generato: {output_path}")


if __name__ == "__main__":
    main()

"""Module where some functions are defined."""


def get_weather_api(location: str) -> dict:
    """
    Logica per chiamare la nostra API di meteo.
    """
    # MOCK di esempio
    return {
        "location": location,
        "temperature": 18.5,
        "unit": "Celsius",
        "condition": "Parzialmente nuvoloso"
    }


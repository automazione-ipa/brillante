"""GPT functions module."""
dct_fn_read_file = {
    "name": "read_file",
    "description": "Legge il contenuto di un file.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string",
                     "description": "Percorso del file da leggere."}
        },
        "required": ["path"]
    }
}

dct_fn_write_file = {
    "name": "write_file",
    "description": "Scrive contenuto su file.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string",
                     "description": "Percorso di destinazione."},
            "content": {"type": "string",
                        "description": "Contenuto da scrivere nel file."}
        },
        "required": ["path", "content"]
    }
}

# TravelForge specific functions

dct_fn_generate_schema = {
    "name": "generate_itinerary_schema",
    "description": "Produce un JSON con tappe e attività giorno-per-giorno.",
    "parameters": {
        "type": "object",
        "properties": {
            "city_country": {"type": "string"},
            "duration_days": {"type": "integer"},
            "season_or_dates": {"type": "object"}
        },
        "required": ["city_country", "duration_days", "season_or_dates"]
    }
}

dct_fn_search_images = {
    "name": "search_images",
    "description": "Restituisce immagini per un elenco di keywords.",
    "parameters": {
        "type": "object",
        "properties": {
            "keywords": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["keywords"]
    }
}

dct_fn_fetch_prices = {
    "name": "fetch_prices",
    "description": "Recupera prezzi stimati per un elenco di attività e date.",
    "parameters": {
        "type": "object",
        "properties": {
            "itinerary": {
                "type": "array",
                "items": {"type": "object"}
            },
            "dates": {"type": "object"}
        },
        "required": ["itinerary", "dates"]
    }
}

dct_fn_build_report = {
    "name": "build_report",
    "description": "Genera un report in Markdown basato su city, dates, itinerary, images e prices.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string"},
            "dates": {"type": "object"},
            "itinerary": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "day": {"type": "integer"},
                        "activity": {"type": "string"},
                        "location": {"type": "string"}
                    },
                    "required": ["day", "activity", "location"]
                }
            },
            "images": {"type": "object"},
            "prices": {"type": "object"}
        },
        "required": ["city", "dates", "itinerary", "images", "prices"]
    }
}


FUNCTIONS = [
    dct_fn_read_file,
    dct_fn_write_file,
    dct_fn_generate_schema,
    dct_fn_search_images,
    dct_fn_fetch_prices,
    dct_fn_build_report
]

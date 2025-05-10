"""Module for functions."""

dct_fn_read_file = {
    "name": "read_file",
    "description": "Legge un file e restituisce una stringa.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Il percorso del file da leggere."
            }
        },
        "required": ["file_path"]
    }
}

dct_fn_get_weather = {
    "name": "get_weather",
    "description": "Get current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City and country e.g. Bogotá, Colombia"
            }
        },
        "required": ["location"],
        "additionalProperties": False
    }
}

# Definizione del JSON Schema relativo alla funzione di calcolo
dct_calculate = {
    "name": "calculate",
    "description": "Esegue un'espressione matematica e restituisce il risultato.",
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Espressione matematica da valutare, ad es. '2+2*3'"
            }
        },
        "required": ["expression"]
    }
}

# Definizione del JSON Schema relativo alla funzione di riassunto Wikipedia
dct_wiki_summary = {
    "name": "wikipedia_summary",
    "description": "Restituisce un breve riassunto di una voce Wikipedia per una query fornita.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Termine di ricerca per Wikipedia, es. 'Leonardo da Vinci'"
            }
        },
        "required": ["query"]
    }
}


FUNCTIONS = [dct_fn_get_weather, dct_fn_read_file]

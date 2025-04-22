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

FUNCTIONS = [dct_fn_get_weather, dct_fn_read_file]

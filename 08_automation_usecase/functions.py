"""Module for functions."""

dct_fn_read_file = {
    "name": "read_file",
    "description": "Legge il contenuto di un file.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Percorso del file da leggere."
            }
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
            "path": {
                "type": "string",
                "description": "Percorso di destinazione."
            },
            "content": {
                "type": "string",
                "description": "Contenuto da scrivere nel file."
            }
        },
        "required": ["path", "content"]
    }
}

FUNCTIONS = [dct_fn_read_file, dct_fn_write_file]

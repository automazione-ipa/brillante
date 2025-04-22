"""Module where some functions are defined."""


def read_file(file_path):
    """Legge il contenuto di un file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"Errore: File non trovato: {file_path}"
    except Exception as e:
        return f"Errore durante la lettura del file: {e}"

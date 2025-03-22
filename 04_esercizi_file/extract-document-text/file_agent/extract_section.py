import re


def divide_sections(text):
    """Divide il testo in sezioni basandosi sui titoli in maiuscolo"""
    return re.split(r"(\n[A-ZÀ-Ú][A-ZÀ-Ú\s]+\n)", text)


def get_section_dict(sections: list) -> dict:
    section_dict = {}
    current_title = None

    for part in sections:
        part = part.strip()
        if re.match(r"^[A-ZÀ-Ú][A-ZÀ-Ú\s]+$", part):  # Se è un titolo
            current_title = part
            section_dict[current_title] = ""
        elif current_title:
            section_dict[current_title] += part + " "

    return section_dict


def get_content(section_dict, section_name):
    """Recupera il testo della sezione richiesta"""
    return section_dict.get(section_name.upper(), "Sezione non trovata")


def extract_section(text, section_name):
    """Estrae il testo della sezione richiesta fino al prossimo titolo."""

    sections = divide_sections(text)
    # Dizionario { "titolo_paragrafo": "contenuto paragrafo" }
    section_dict = get_section_dict(sections)
    return get_content(section_dict, section_name)


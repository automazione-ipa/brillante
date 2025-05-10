import logging
import wikipedia

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def wikipedia_summary(query: str) -> dict:
    """
    Cerca una voce su Wikipedia e restituisce un breve riassunto.
    """
    logging.info(f"Avvio ricerca Wikipedia per query: '{query}'")
    try:
        wikipedia.set_lang("it")
        summary = wikipedia.summary(query, sentences=2)
        logging.info(f"Riassunto ottenuto con successo per '{query}'")
    except wikipedia.DisambiguationError as e:
        logging.warning(f"Query ambigua per '{query}': {e.options[:5]}")
        return {"error": f"Query ambigua, possibili voci: {e.options[:5]}"}
    except wikipedia.PageError:
        logging.error(f"Pagina non trovata su Wikipedia per '{query}'")
        return {"error": "Pagina non trovata su Wikipedia"}
    except Exception as e:
        logging.exception(f"Errore imprevisto durante il recupero di '{query}'")
        return {"error": str(e)}

    return {"summary": summary}

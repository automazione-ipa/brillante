import json
from gpt_wrap.gpt_wrap import chat_functions


def extract_ner(chunk: str, system_msg: str = None) -> dict:
    """
    Estrae entità e relazioni dal testo, restituendo un dizionario con due chiavi:
    - 'entities': lista di entità trovate
    - 'relations': lista di tuple (entità1, relazione, entità2)
    """
    prompt = (
        "Estrai le entità nominate e le loro relazioni dal testo seguente.\n"
        "Rispondi in formato JSON con due campi: 'entities' e 'relations'.\n\n"
        f"{chunk}"
    )
    resp = chat_functions(
        user_message=prompt,
        system_message=system_msg or "Sei un modello esperto in Named Entity Recognition e relazione tra entità.",
        temperature=0.0
    )

    try:
        return json.loads(resp['choices'][0]['message']['content'])
    except json.JSONDecodeError:
        # se non è JSON valido, restituisci raw string
        return {"error": resp['choices'][0]['message']['content']}

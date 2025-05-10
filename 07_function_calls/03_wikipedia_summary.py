import json
import logging
from functions import dct_wiki_summary
from gpt_wrap import (
    chat_functions,
    gpt_choice_message,
    gpt_choice_content
)
from wikipedia_api.wiki_api import wikipedia_summary


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

FUNCTIONS = [dct_wiki_summary]


def main():
    # Esempio di richiesta all'assistente per cultura generale
    user_query = "Chi era Galileo Galilei?"
    logging.info(f"Utente: {user_query}")

    # Invio della richiesta al modello
    resp = chat_functions(
        user_message=user_query,
        functions=FUNCTIONS,
        function_call="auto"
    )
    logging.info("Risposta iniziale ricevuta dal modello")

    message = gpt_choice_message(response_json=resp)

    # Verifica della chiamata di funzione richiesta
    if message.get("function_call") and message["function_call"]["name"] == "wikipedia_summary":
        logging.info("Il modello ha richiesto wikipedia_summary")
        args = json.loads(message["function_call"]["arguments"])
        logging.info(f"Parametri passati a wikipedia_summary: {args}")

        # Chiamata della funzione wikipedia_summary
        wiki_result = wikipedia_summary(args.get("query"))

        # Preparazione del messaggio di risposta della funzione
        function_response = {
            "role": "function",
            "name": "wikipedia_summary",
            "content": json.dumps(wiki_result, ensure_ascii=False)
        }
        logging.info(f"Risposta della funzione pronta: {wiki_result}")

        # Invio del messaggio di funzione al modello per completare la risposta
        final_resp = chat_functions(
            assistant_message=message,
            function_message=function_response,
            model="gpt-4o-mini",
            temperature=0.0
        )
        logging.info("Risposta finale ricevuta dal modello dopo call di funzione")
        print(gpt_choice_content(final_resp))
    else:
        logging.info("Nessuna chiamata di funzione: stampa contenuto semplice")
        print(message.get("content"))


if __name__ == "__main__":
    main()

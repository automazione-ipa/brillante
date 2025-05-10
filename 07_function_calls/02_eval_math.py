import json

from functions import dct_calculate
from gpt_wrap import (
    chat_functions,
    gpt_choice_message,
    gpt_choice_content
)
from math_api.evaluate_api import calculate

FUNCTIONS = [dct_calculate]


def main():
    # Chiediamo al modello di eseguire un calcolo
    user_query = "Quanto fa 2+2*3?"
    resp = chat_functions(
        user_message=user_query,
        functions=FUNCTIONS,
        function_call="auto"
    )

    message = gpt_choice_message(response_json=resp)

    # Controlliamo se il modello vuole chiamare calculate
    if message.get("function_call") and message["function_call"]["name"] == "calculate":
        args = json.loads(message["function_call"]["arguments"])
        # Eseguiamo il calcolo
        calc_result = calculate(args.get("expression"))

        # Prepariamo il messaggio di risposta della funzione
        function_response = {
            "role": "function",
            "name": "calculate",
            "content": json.dumps(calc_result)
        }

        # Richiamiamo il modello per ottenere la risposta finale
        final_resp = chat_functions(
            assistant_message=message,
            function_message=function_response,
            model="gpt-4o-mini",
            temperature=0.0
        )
        print(gpt_choice_content(final_resp))
    else:
        # Se nessuna chiamata di funzione, stampiamo direttamente il contenuto
        print(message.get("content"))

if __name__ == "__main__":
    main()



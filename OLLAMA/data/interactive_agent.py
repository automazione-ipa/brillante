"""Interactive function call agent"""
import logging
import json
from gpt_wrap import chat_functions, gpt_choice_message
from functions import FUNCTIONS
from agent_functions import parse_pom_file, write_file, read_file, load_json
from config import POM_FILE

logger = logging.getLogger(__name__)

FUNCTION_DISPATCHER = {
    "parse_pom_file": parse_pom_file,
    "write_file": write_file,
    "read_file": read_file,
    "load_json": load_json
}


def run_pom_agent():
    initial_prompt = f"""
Sei un assistente tecnico. Il tuo compito è leggere un file pom.xml da percorso '{POM_FILE}', estrarre le informazioni e salvarle in un file JSON chiamato 'pom_info.json'.

Dopo l'elaborazione, l'utente potrà farti domande su:
- dipendenze del progetto
- struttura XML
- tecnologie e versioni usate
"""

    logger.info("🤖 Avvio del POM Agent...")

    response = chat_functions(
        user_message=initial_prompt,
        functions=FUNCTIONS,
        function_call="auto"
    )

    message = gpt_choice_message(response)
    while True:
        if message.get("function_call"):
            fname = message["function_call"]["name"]
            args = json.loads(message["function_call"]["arguments"])

            if fname in FUNCTION_DISPATCHER:
                logger.info(f"⚙️  Eseguo funzione: {fname} con args: {args}")
                result = FUNCTION_DISPATCHER[fname](**args)

                message = chat_functions(
                    function_message={
                        "role": "function",
                        "name": fname,
                        "content": json.dumps(result)
                    },
                    functions=FUNCTIONS,
                    function_call="auto"
                )["choices"][0]["message"]
            else:
                logger.warning(f"❌ Funzione non gestita: {fname}")
                break
        else:
            logger.info(f"🗨️ {message.get('content')}")
            break

    # Ora avvia la chat interattiva
    while True:
        user_input = input("\n❓ Fai una domanda sul pom.xml (oppure digita 'exit'): ")
        if user_input.lower() == "exit":
            break

        chat_response = chat_functions(
            user_message=user_input,
            functions=FUNCTIONS,
            function_call="auto"
        )

        message = gpt_choice_message(chat_response)

        if message.get("function_call"):
            fname = message["function_call"]["name"]
            args = json.loads(message["function_call"]["arguments"])

            if fname in FUNCTION_DISPATCHER:
                result = FUNCTION_DISPATCHER[fname](**args)

                message = chat_functions(
                    function_message={
                        "role": "function",
                        "name": fname,
                        "content": json.dumps(result)
                    },
                    functions=FUNCTIONS,
                    function_call="auto"
                )["choices"][0]["message"]
                logger.info("🗨️ %s", message["content"])
            else:
                logger.warning(f"⚠️ Funzione non riconosciuta: {fname}")
        else:
            logger.info("🗨️ %s", message.get("content"))

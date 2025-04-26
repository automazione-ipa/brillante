from gpt_wrap import chat_functions, gpt_choice_message
from functions import FUNCTIONS

import json
import os


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def remap_from_proto():
    input_file = "shard_info.py"
    output_file = "results/shard_info_remap.py"

    file_content = read_file(input_file)

    user_prompt = f"""
    Sei uno sviluppatore Python.
    
    Dato il seguente contenuto di un file:
    ---
    {file_content}
    ---
    1. Converti le classi in modelli Pydantic BaseModel.
    2. Aggiungi gli import corretti di typing e pydantic.
    3. Scrivi il risultato chiamando la funzione `write_file`, salvando il file in "{output_file}".
    """

    resp = chat_functions(
        user_message=user_prompt,
        functions=FUNCTIONS,
        function_call="auto"
    )

    message = gpt_choice_message(response_json=resp)

    if message.get("function_call"):
        fname = message["function_call"]["name"]
        args = json.loads(message["function_call"]["arguments"])

        if fname == "write_file":
            write_file(**args)
            print(f"✅ File scritto correttamente in {args['path']}")
        else:
            print("⚠️ Funzione non gestita:", fname)
    else:
        print(message.get("content"))


if __name__ == "__main__":
    remap_from_proto()

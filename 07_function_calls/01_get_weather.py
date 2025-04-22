from functions import FUNCTIONS
from gpt_wrap import (
    chat_functions,
    gpt_choice_message,
    gpt_choice_content
)

from weather_api.get_weather import get_weather_api

import json


def main():
    # 1. Chiedo al modello di usare get_weather
    resp = chat_functions(
        user_message="What is the weather like in Paris today?",
        functions=FUNCTIONS,
        function_call="auto"  # lascia che sia il modello a decidere
    )

    message = gpt_choice_message(response_json=resp)

    # 2. Verifico se c'è una function_call del modello
    if message.get("function_call"):
        fname = message["function_call"]["name"]
        args = json.loads(message["function_call"]["arguments"])

        if fname == "get_weather":
            weather_info = get_weather_api(**args)

            dct_assistant = {
                    "role": "assistant",
                    "content": None,
                    "function_call": message["function_call"]
            }

            dct_function = {
                    "role": "function",
                    "name": fname,
                    "content": json.dumps(weather_info)

            }
            followup = chat_functions(
                user_message=None,
                system_message=None,
                assistant_message=dct_assistant,
                function_message=dct_function,
                model="gpt-4o-mini",
                temperature=0.0,
            )

            last_resp = gpt_choice_content(followup)
            print(last_resp)
        else:
            print("Funzione non gestita:", fname)
    else:
        print(message.get("content"))


if __name__ == "__main__":
    main()

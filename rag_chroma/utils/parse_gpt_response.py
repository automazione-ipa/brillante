import json

def parse_response(resp):
    """Parsing JSON dalla stringa di risposta."""
    try:
        return json.loads(resp['choices'][0]['message']['content'])
    except json.JSONDecodeError:
        # se non è JSON valido, restituisci raw string
        return {"error": resp['choices'][0]['message']['content']}


def gpt_choice_message(response_json):
    return response_json['choices'][0]['message']


def gpt_choice_content(response_json):
    return response_json['choices'][0]['message']['content']

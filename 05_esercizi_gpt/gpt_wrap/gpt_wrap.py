import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# TODO : funzione generica per request POST e specializzazione


def chat_with_openai(
    user_message,
    system_message=None,
    model='gpt-4o-mini',
    temperature=0.7,
    **kwargs
):
    """
    Sends a chat message to the OpenAI API and returns the assistant's reply.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    messages = []
    if system_message:
        messages.append({'role': 'system', 'content': system_message})
    messages.append({'role': 'user', 'content': user_message})

    data = {
        'model': model,
        'messages': messages,
        'temperature': temperature,
        **kwargs
    }

    response = requests.post(
        url='https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        response_json = response.json()
        reply = response_json['choices'][0]['message']['content']
        return reply
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")


def get_embedding(text, model='text-embedding-ada-002'):
    """Funzione per ottenere l'embedding di un testo."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY non trovato nelle variabili d'ambiente.")

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'model': model,
        'input': text
    }

    response = requests.post(
        url='https://api.openai.com/v1/embeddings',
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        response_json = response.json()
        embedding = response_json['data'][0]['embedding']
        return embedding
    else:
        raise Exception(f"Richiesta fallita con codice di stato {response.status_code}: {response.text}")

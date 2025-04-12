import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from gpt_wrap import chat_with_openai, get_embedding
from db_core import load_index


def generate_embedding(text):
    """Funzione per generare l'embedding di un testo."""
    embedding = get_embedding(text)
    return np.array(embedding).reshape(1, -1)


def retrieve_relevant_chunk(query, index, chunks, top_k=1):
    """Recupera i chunk rilevanti."""
    query_embedding = generate_embedding(query)
    similarities = cosine_similarity(query_embedding, index)
    relevant_indices = similarities.argsort()[0][-top_k:][::-1]
    return [chunks[i] for i in relevant_indices]


def generate_answer_from_chunk(chunk, query, system_message):
    """Funzione per generare la risposta con OpenAI."""
    return chat_with_openai(
        user_message=f"Domanda: {query}\nContesto: {chunk}",
        system_message=system_message,
        model="gpt-4o-mini",
        temperature=0.1
    )


def main(query):
    index = load_index()
    index = np.array(index)
    if index.ndim == 3:
        index = index.reshape(index.shape[0], -1)
    # Assumiamo che l'indice contenga direttamente i chunk
    chunks = [chunk for chunk in index]
    relevant_chunks = retrieve_relevant_chunk(query, index, chunks)
    answer = generate_answer_from_chunk(
        relevant_chunks[0],
        query,
        system_message="Sei un assistente esperto."
    )
    print("Risposta:", answer)


if __name__ == "__main__":
    query = "Qual è il tema principale del documento?"  # Sostituisci con la tua domanda
    main(query)

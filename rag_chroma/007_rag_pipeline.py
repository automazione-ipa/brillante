from db_core import query_documents
from gpt_wrap import chat_with_openai


def rag_pipeline(query_text: str, n_results: int = 1) -> str:
    """
    Esegue la pipeline RAG: retrieval + generazione.

    Args:
        query_text: domanda dell'utente
        n_results: numero di documenti da recuperare

    Returns:
        Risposta generata da OpenAI GPT
    """
    try:
        retrieved_docs, metadata = query_documents(query_text, n_results=n_results)
        context = " ".join(retrieved_docs[0]) if retrieved_docs else "No relevant documents found."

        augmented_prompt = f"Context: {context}\n\nQuestion: {query_text}\nAnswer:"
        print("######## Augmented Prompt ########")
        print(augmented_prompt)

        system_msg = "You are a helpful assistant. Answer the question using the provided context."
        response = chat_with_openai(
            user_message=augmented_prompt,
            system_message=system_msg,
            model="gpt-4o-mini"
        )
        return response

    except Exception as e:
        return f"Errore durante l'esecuzione della pipeline: {e}"


if __name__ == "__main__":
    query = "What is artificial intelligence?"
    response = rag_pipeline(query, n_results=2)
    print("######## Response from GPT ########\n", response)

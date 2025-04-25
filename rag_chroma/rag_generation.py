import os
import uuid
import json
from gpt_wrap.gpt_wrap import chat_functions, get_embedding
from functions.job_summary import summarize_text
from functions.job_ner import extract_ner

from rag_chroma.file_agent.text_extraction_agent import PdfReadAgent
import chromadb

# Inizializzazione del client Chroma
client = chromadb.PersistentClient(path="./chroma_db")
collection_name = "all-my-documents"

# Creazione o recupero della collezione
collection = client.get_or_create_collection(name=collection_name)

def ingest_document(doc_text: str, doc_id: str, source: str):
    """
    Ingesta un documento nella collezione ChromaDB.
    """
    reader = PdfReadAgent()

    chunks = reader.chunk_text(doc_text, max_length=500)
    for i, chunk in enumerate(chunks):
        chunk_id = f"{doc_id}_chunk_{i}"
        # Verifica se il chunk esiste già
        existing = collection.get(ids=[chunk_id])
        if existing['ids']:
            print(f"🔁 Chunk {chunk_id} già presente, salto.")
            continue
        print(f"➕ Aggiunta del chunk {chunk_id}...")
        summary = summarize_text(chunk)
        ner = extract_ner(chunk)
        embedding = get_embedding(chunk)
        metadata = {
            "doc_id": doc_id,
            "chunk_index": i,
            "summary": summary,
            "ner": ner,
            "source": source
        }
        collection.add(
            ids=[chunk_id],
            documents=[chunk],
            metadatas=[metadata],
            embeddings=[embedding]
        )
    print(f"✅ Documento {doc_id} indicizzato con successo.")


def generate_answer(query: str, top_k: int = 3):
    """
    Genera una risposta alla query utilizzando i chunk più rilevanti.
    """
    print(f"🔍 Ricerca dei top {top_k} chunk per la query: '{query}'...")
    results = collection.query(query_texts=[query], n_results=top_k)
    retrieved_chunks = results["documents"][0]
    context = "\n\n".join(retrieved_chunks)
    prompt = (
        f"Rispondi alla seguente domanda utilizzando le informazioni fornite:\n\n"
        f"Domanda: {query}\n\n"
        f"Contesto:\n{context}"
    )
    response = chat_functions(
        user_message=prompt,
        system_message="Sei un assistente esperto che fornisce risposte accurate basate sul contesto fornito.",
        temperature=0.5
    )
    answer = response['choices'][0]['message']['content']
    print("🧠 Risposta generata:")
    print(answer)
    return answer


if __name__ == "__main__":
    
    pdf_text = PdfReadAgent.text_from_pdf("esempio.pdf")
    if pdf_text:
        print(pdf_text)
        doc_id = str(uuid.uuid4())
        source = "esempio"

        # Ingestione del documento
        # ingest_document(pdf_text, doc_id, source)

        # Generazione della risposta
        # query = "Chi ha fondato OpenAI?"
        # generate_answer(query)

    else:
        print("Nessun testo estratto o errore nella lettura del PDF.")

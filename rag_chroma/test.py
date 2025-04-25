import os
import uuid
import json
from gpt_wrap.gpt_wrap import chat_functions, get_embedding
from functions.job_summary import summarize_text
from functions.job_ner import extract_ner

from file_agent.text_extraction_agent import PdfReadAgent
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

    chunks = reader.chunk_text(
        text=doc_text,
        max_length=500
    )
    # Visualizziamo i risultati
    # for i, chunk in enumerate(chunks):
    #     print(chunk)
    #     print("###############")


    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i} ({len(chunk)} caratteri):\n{chunk}\n{'-'*40}")



if __name__ == "__main__":
    
    pdf_text = PdfReadAgent.text_from_pdf("esempio.pdf")
    if pdf_text:
        print(pdf_text)
        doc_id = str(uuid.uuid4())
        source = "esempio"

        # Ingestione del documento
        ingest_document(pdf_text, doc_id, source)

        # Generazione della risposta
        # query = "Chi ha fondato OpenAI?"
        # generate_answer(query)

    else:
        print("Nessun testo estratto o errore nella lettura del PDF.")

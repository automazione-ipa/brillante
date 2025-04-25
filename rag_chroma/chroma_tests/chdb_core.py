import os
import chromadb
from chromadb import Documents, Embeddings

from rag_chroma.gpt_wrap.gpt_wrap import get_embedding
from chromadb.utils.embedding_functions import EmbeddingFunction


# ---------- ChromaDB setup ----------
chroma_client = chromadb.PersistentClient(
    path=os.path.join(os.getcwd(), "chroma_db")
)


class ChromaDBEmbeddingFunction(EmbeddingFunction[Documents]):
    def __call__(self, input: Documents) -> Embeddings:
        if isinstance(input, str):
            input = [input]

        results = []
        for text in input:
            embedding = get_embedding(text)
            if not isinstance(embedding, list):
                raise ValueError("Embedding must be a list")
            if not all(isinstance(x, float) for x in embedding):
                raise ValueError("All embedding values must be floats")
            results.append(embedding)

        return results


# Istanza della funzione di embedding
embedding_fn = ChromaDBEmbeddingFunction()

# Creazione / recupero della collection
collection = chroma_client.get_or_create_collection(
    name="rag_collection_demo_1",
    metadata={"description": "A collection for RAG with OpenAI GPT"},
    embedding_function=embedding_fn
)


# ---------- Funzioni DB ----------
def add_documents(documents, ids):
    print("[DEBUG] Preparing to add documents...")

    for i, doc in enumerate(documents):
        print(f"[DEBUG] Generating embedding for doc{i + 1}...")

    collection.add(
        documents=documents,
        ids=ids
    )

    print("[DEBUG] Documents added to ChromaDB.")


def query_documents(query_text, n_results=1):
    """
    Interroga la collection per documenti rilevanti.
    Restituisce tuple (documents, metadatas)
    """
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results["documents"], results["metadatas"]

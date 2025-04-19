from db_core import add_documents
import time

documents = [
    "Artificial intelligence is the simulation of human intelligence processes by machines.",
    "Python is a programming language that lets you work quickly and integrate systems more effectively.",
    "ChromaDB is a vector database designed for AI applications."
]
doc_ids = ["doc1", "doc2", "doc3"]

print("Start inserting documents...")
time.sleep(1)

try:
    add_documents(documents, doc_ids)
    print("Documents added successfully.")
except Exception as e:
    print("Errore durante l'inserimento dei documenti:", e)

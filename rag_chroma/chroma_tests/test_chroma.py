import chromadb

print("▶️ Inizializzazione del client Chroma in memoria...")
client = chromadb.Client()

print("📂 Creazione della collezione 'all-my-documents'...")
collection = client.create_collection("all-my-documents")

print("📝 Aggiunta di documenti alla collezione...")
collection.add(
    documents=["This is document1", "This is document2"],
    metadatas=[{"source": "notion"}, {"source": "google-docs"}],
    ids=["doc1", "doc2"],
)
print("✅ Documenti aggiunti con successo!")

print("🔍 Esecuzione della query...")
results = collection.query(
    query_texts=["This is a query document"],
    n_results=2,
)
print("✅ Query completata!")

print("📊 Risultati della query:")
print(results)

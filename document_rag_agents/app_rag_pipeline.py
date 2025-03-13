import os
from document_rag_agents.complex_agents.rag_pipeline import RAGPipeline

rag_pipeline = RAGPipeline(api_key=os.getenv("OPENAI_API_KEY"))

# RAG Process for the document:
# - extract text, create chunks, generate questions, build vector store
text_chunks, vector_store = (
    rag_pipeline.process_document(
        pdf_path="data/AI_information.pdf",
        chunk_size=1000,
        chunk_overlap=200,
        questions_per_chunk=3
    )
)

# Print vector_store size
print(f"Vector store contains {len(vector_store.texts)} items")

# Print the number of text chunks created
print("Number of text chunks:", len(text_chunks))

# Print the first text chunk
print("\nFirst text chunk:")
print(text_chunks[0])


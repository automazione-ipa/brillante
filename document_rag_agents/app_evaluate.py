import os
from document_rag_agents.pipelines.generate_augmented_response import RAGSearchVector


rag_search_vector = RAGSearchVector(api_key=os.getenv("OPENAI_API_KEY"))

# Path del dato
value_path = "data/val.json"
query = rag_search_vector.generate_augmented_response(
    value_path=value_path,
    evaluate=True
)

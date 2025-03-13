from document_rag_agents.db.query_data import QueryData
from document_rag_agents.complex_agents.semantic_search_agent import (
    SemanticSearchAgent
)

from document_rag_agents.complex_agents.rag_pipeline import RAGPipeline


class RAGSearchVector:
    def __init__(self, api_key):
        self.rag_pipeline = RAGPipeline(api_key)
        self.query_data_agent = QueryData()
        self.semantic_search_agent = SemanticSearchAgent(
            embedding_agent=self.rag_pipeline.embedding_agent
        )

    @staticmethod
    def print_response_info(query, top_chunks):
        # Print the query
        print("\nQuery:", query)
        # Print the top 2 most relevant text chunks
        for i, chunk in enumerate(top_chunks):
            print(
                f"Context {i + 1}:\n{chunk}\n=====================================")

    def query_on_extracted_chunks(self, value_path):
        query = self.query_data_agent.get_query_data(value_path)

        # RAG Process for the document:
        # - extract text, create chunks, generate questions, build vector store
        text_chunks, vector_store = (
            self.rag_pipeline.process_document(
                pdf_path="data/AI_information.pdf",
                chunk_size=1000,
                chunk_overlap=200,
                questions_per_chunk=3
            )
        )

        # Create embeddings for the text chunks
        response = self.rag_pipeline.embedding_agent.create_embeddings(
            text_chunks)

        top_chunks = self.semantic_search_agent.semantic_search_v2(
            query, text_chunks=text_chunks, embeddings=response.data, k=2
        )

        self.print_response_info(query, top_chunks)

        return top_chunks

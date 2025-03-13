from document_rag_agents.db.simple_vector_store import SimpleVectorStore
from document_rag_agents.base_agents.embedding_agent import EmbeddingAgent
from document_rag_agents.complex_agents.semantic_search_agent import SemanticSearchAgent


class VectorSearchAgent:
    def __init__(self, api_key):
        self.embedding_agent = EmbeddingAgent(api_key)
        self.semantic_search_agent = SemanticSearchAgent(self.embedding_agent)
        self.vector_store = SimpleVectorStore()

    @staticmethod
    def print_chunk_results(chunk_results):
        print("\nRelevant Document Chunks:")
        for i, result in enumerate(chunk_results):
            print(f"Context {i + 1} (similarity: {result['similarity']:.4f}):")
            print(result["text"][:300] + "...")
            print("=====================================")

    @staticmethod
    def print_question_matches(question_results):
        print("\nMatched Questions:")
        for i, result in enumerate(question_results):
            print(f"Question {i + 1} (similarity: {result['similarity']:.4f}):")
            print(result["text"])
            chunk_idx = result["metadata"]["chunk_index"]
            print(f"From chunk {chunk_idx}")
            print("=====================================")

    @staticmethod
    def organize_results_by_type(query, search_results):
        """Organizes results in two different datasets."""
        print("Query:", query)
        print("\nSearch Results:")

        chunk_results = []
        question_results = []

        for result in search_results:
            if result["metadata"]["type"] == "chunk":
                chunk_results.append(result)
            else:
                question_results.append(result)

        return chunk_results, question_results

    @staticmethod
    def prepare_context(search_results):
        """
        Prepares a unified context from search results for response generation.

        Args:
        search_results (List[Dict]): Results from semantic search.

        Returns:
        str: Combined context string.
        """
        # Extract unique chunks referenced in the results
        chunk_indices = set()
        context_chunks = []

        # First add direct chunk matches
        for result in search_results:
            if result["metadata"]["type"] == "chunk":
                chunk_indices.add(result["metadata"]["index"])
                context_chunks.append(
                    f"Chunk {result['metadata']['index']}:\n{result['text']}")

        # Then add chunks referenced by questions
        for result in search_results:
            if result["metadata"]["type"] == "question":
                chunk_idx = result["metadata"]["chunk_index"]
                if chunk_idx not in chunk_indices:
                    chunk_indices.add(chunk_idx)
                    context_chunks.append(
                        f"Chunk {chunk_idx} (referenced by question '{result['text']}'):\n{result['metadata']['original_chunk']}")

        # Combine all context chunks
        full_context = "\n\n".join(context_chunks)
        return full_context

    def vector_db_semantic_search(self, query):
        """
        Performs the semantic search to find relevant content on the vector db.
        Prints some important data too.
        """
        search_res = self.semantic_search_agent.semantic_search(
            query, vector_store=self.vector_store, k=5
        )

        chunk_results, question_results = self.organize_results_by_type(
            query=query, search_results=search_res
        )

        self.print_chunk_results(chunk_results)
        self.print_question_matches(question_results)

        return search_res

import numpy as np

from document_rag_agents.base_agents.embedding_agent import EmbeddingAgent
from document_rag_agents.base_agents.math_agent import MathAgent


class SemanticSearchAgent:
    def __init__(self, embedding_agent: EmbeddingAgent):
        self.processor = embedding_agent
        self.math_agent = MathAgent()

    def get_embeddings(self, query):
        query_embedding_res = self.processor.create_embeddings(query)
        return query_embedding_res.data[0].embedding

    def semantic_search(self, query, vector_store, k=5):
        """
        Performs semantic search using the query and vector store.

        Args:
        query (str): The search query.
        vector_store (SimpleVectorStore): The vector store to search in.
        k (int): Number of results to return.

        Returns:
        List[Dict]: Top k most relevant items.
        """
        query_embedding = self.get_embeddings(query)
        results = vector_store.similarity_search(query_embedding, k=k)

        return results

    def semantic_search_v2(self, query, text_chunks, embeddings, k=5):
        """
        Performs semantic search on the text chunks using the given query and embeddings.

        Args:
        query (str): The query for the semantic search.
        text_chunks (List[str]): A list of text chunks to search through.
        embeddings (List[dict]): A list of embeddings for the text chunks.
        k (int): The number of top relevant text chunks to return. Default is 5.

        Returns:
        List[str]: A list of the top k most relevant text chunks based on the query.
        """
        query_embedding = self.get_embeddings()
        similarity_scores = []

        # Calculate similarity scores between the query embedding and each text chunk embedding
        for i, chunk_embedding in enumerate(embeddings):
            similarity_score = self.math_agent.cosine_similarity(
                np.array(query_embedding), np.array(chunk_embedding.embedding)
            )
            # Append the index and similarity score
            similarity_scores.append((i, similarity_score))

        # Sort the similarity scores in descending order
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        # Get the indices of the top k most similar text chunks
        top_indices = [index for index, _ in similarity_scores[:k]]

        return [text_chunks[index] for index in top_indices]

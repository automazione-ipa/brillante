from document_rag_agents.db.query_data import QueryData
from document_rag_agents.base_agents.chat_agent import ChatAgent
from document_rag_agents.complex_agents.vector_search_agent import VectorSearchAgent


class RAGSearchVector:
    def __init__(self, api_key):
        self.query_data_agent = QueryData()
        self.vector_search_agent = VectorSearchAgent(api_key)
        self.chat_agent = ChatAgent(api_key)

    @staticmethod
    def print_response_info(query, response_text):
        print("\nQuery:", query)
        print(f"\nResponse: {response_text}")

    @staticmethod
    def print_evaluation(evaluation):
        print(f"\nEvaluation:{evaluation}")

    def generate_augmented_response(self, value_path, evaluate: bool = False):
        query = self.query_data_agent.get_query_data(value_path)

        search_results = self.vector_search_agent.vector_db_semantic_search(
            query=query
        )
        context = self.vector_search_agent.prepare_context(
            search_results=search_results
        )
        response_text = self.chat_agent.generate_response(
            query=query, context=context
        )

        self.print_response_info(query, response_text)

        if evaluate:
            reference_answer = self.query_data_agent.get_reference_answer(value_path)

            evaluation = self.chat_agent.evaluate_response(
                query=query, response=response_text, reference_answer=reference_answer
            )

            self.print_evaluation(evaluation)

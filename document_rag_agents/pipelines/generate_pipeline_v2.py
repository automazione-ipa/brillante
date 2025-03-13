from document_rag_agents.db.query_data import QueryData
from document_rag_agents.base_agents.chat_agent import ChatAgent


class GenerationPipelineV2:
    def __init__(self, api_key):
        self.system_prompt = "You are an AI assistant that strictly answers based on the given context. If the answer cannot be derived directly from the provided context, respond with: 'I do not have enough information to answer that.'"
        self.query_data_agent = QueryData()
        self.chat_agent = ChatAgent(api_key)

    def generate_response_pipeline_v2(self, value_path, top_chunks):
        """Generates an ai response based on chunks and returns it."""
        query = self.query_data_agent.get_query_data(value_path)

        # Create the user prompt based on the top chunks
        user_prompt = "\n".join(
            [
                f"Context {i + 1}:\n{chunk}\n=====================================\n"
                for i, chunk in enumerate(top_chunks)
            ]
        )
        user_prompt = f"{user_prompt}\nQuestion: {query}"

        return self.chat_agent.generate(self.system_prompt, user_prompt)

    def evaluate_pipeline_v2(self, value_path, ai_response, data):
        """Generates an evaluation response from LLM."""
        query = self.query_data_agent.get_query_data(value_path)

        evaluate_system_prompt = "You are an intelligent evaluation system tasked with assessing the AI assistant's responses. If the AI assistant's response is very close to the true response, assign a score of 1. If the response is incorrect or unsatisfactory in relation to the true response, assign a score of 0. If the response is partially aligned with the true response, assign a score of 0.5."

        # Create the evaluation prompt by combining the user query, AI response, true response, and evaluation system prompt
        evaluation_prompt = f"User Query: {query}\nAI Response:\n{ai_response.choices[0].message.content}\nTrue Response: {data[0]['ideal_answer']}\n{evaluate_system_prompt}"

        # Generate the evaluation response using the evaluation system prompt and evaluation prompt
        evaluation_response = self.chat_agent.generate(
            system_prompt=evaluate_system_prompt,
            user_message=evaluation_prompt
        )

        # Print the evaluation response
        print(evaluation_response.choices[0].message.content)
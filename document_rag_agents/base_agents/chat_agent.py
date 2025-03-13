from typing import Optional
import re

from openai import OpenAI


class ChatAgent:
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(
            self,
            system_prompt,
            user_message,
            temperature=0.0,
            model="meta-llama/Llama-3.2-3B-Instruct"
    ):
        """
        Generates a response from the AI model based on the system prompt and user message.

        Args:
        system_prompt (str): The system prompt to guide the AI's behavior.
        user_message (str): The user's message or query.
        model (str): The model to be used for generating the response. Default is "meta-llama/Llama-2-7B-chat-hf".

        Returns:
        dict: The response from the AI model.
        """
        response = self.client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return response

    def generate_questions(self, text_chunk, num_questions=5, model="meta-llama/Llama-3.2-3B-Instruct"):
        """
        Generates relevant questions that can be answered from the given text chunk.

        Args:
        text_chunk (str): The text chunk to generate questions from.
        num_questions (int): Number of questions to generate.
        model (str): The model to use for question generation.

        Returns:
        List[str]: List of generated questions.
        """
        response = self.generate(
            system_prompt="You are an expert at generating relevant questions from text.",
            user_message=f"Generate {num_questions} questions from the following text:\n{text_chunk}",
            temperature=0.7,
            model=model
        )

        questions_text = response.choices[0].message.content.strip()
        questions = [
            re.sub(r'^\d+\.\s*', '', line.strip())
            for line in questions_text.split('\n') if line.endswith('?')
        ]

        return questions

    def generate_response(self, query, context, model="meta-llama/Llama-3.2-3B-Instruct"):
        """
        Generates a response based on the query and context.

        Args:
        query (str): User's question.
        context (str): Context information retrieved from the vector store.
        model (str): Model to use for response generation.

        Returns:
        str: Generated response.
        """
        response = self.generate(
            system_prompt= "You are an AI assistant that strictly answers based on the given context. If the answer cannot be derived directly from the provided context, respond with: 'I do not have enough information to answer that.'",
            user_message=f"""
                Context:
                {context}
    
                Question: {query}
    
                Please answer the question based only on the context provided above. Be concise and accurate.
            """,
            temperature=0.0,
            model=model
        )

        return response.choices[0].message.content

    def evaluate_response(self, query, response, reference_answer,
                          model="meta-llama/Llama-3.2-3B-Instruct"):
        """
        Evaluates the AI response against a reference answer.

        Args:
        query (str): The user's question.
        response (str): The AI-generated response.
        reference_answer (str): The reference/ideal answer.
        model (str): Model to use for evaluation.

        Returns:
        str: Evaluation feedback.
        """
        evaluate_system_prompt = """You are an intelligent evaluation system tasked with assessing AI responses.

            Compare the AI assistant's response to the true/reference answer, and evaluate based on:
            1. Factual correctness - Does the response contain accurate information?
            2. Completeness - Does it cover all important aspects from the reference?
            3. Relevance - Does it directly address the question?

            Assign a score from 0 to 1:
            - 1.0: Perfect match in content and meaning
            - 0.8: Very good, with minor omissions/differences
            - 0.6: Good, covers main points but misses some details
            - 0.4: Partial answer with significant omissions
            - 0.2: Minimal relevant information
            - 0.0: Incorrect or irrelevant

            Provide your score with justification.
        """

        evaluation_prompt = f"""
            User Query: {query}

            AI Response:
            {response}

            Reference Answer:
            {reference_answer}

            Please evaluate the AI response against the reference answer.
        """

        eval_response = self.generate(
            system_prompt=evaluate_system_prompt,
            user_message=evaluation_prompt,
            temperature=0.0,
            model=model

        )

        return eval_response.choices[0].message.content

from typing import Optional

from openai import OpenAI

from logic.entities import Message


class ChatAgent:
    def __init__(self, api_key: str, model: str):
        """
        Initialize the ChatAgent with an API key and a model (engine).

        :param api_key: The OpenAI API key.
        :param model: The model to use (e.g., "gpt-3.5-turbo", "gpt-4o").
        """
        self.api_key = api_key
        self.model = model

        self.client = OpenAI(api_key=self.api_key)

    def generate_receipt(
            self, user_prompt: str, system_prompt: Optional[str] = None
    ) -> Message:
        """
        Generates a tweet based on a given prompt using the Chat Completion API
        and returns a structured Tweet response.

        :param user_prompt: The prompt to generate the receipt.
        :param system_prompt: The system prompt to generate the receipt.

        :return: A Message object containing the generated receipt and metadata.
        """
        messages = [
            {"role": "user", "content": user_prompt}
        ]

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )

        result = response.choices[0].message.content.strip()

        return Message(testo=result)

from openai import OpenAI

from logic.entities import Tweet


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

    def generate_tweet(self, prompt: str) -> Tweet:
        """
        Generates a tweet based on a given prompt using the Chat Completion API
        and returns a structured Tweet response.

        :param prompt: The prompt to generate the tweet.
        :return: A Tweet object containing the generated tweet and metadata.
        """
        messages = [{"role": "user", "content": prompt}]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=150,
            temperature=0.7,
        )

        tweet_text = response.choices[0].message.content.strip()

        return Tweet(testo=tweet_text)

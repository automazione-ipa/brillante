from openai import OpenAI


class EmbeddingAgent:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def create_embeddings(self, text, model="BAAI/bge-en-icl"):
        """
        Creates embeddings for the given text using the specified OpenAI model.

        Args:
        text (str): The input text for which embeddings are to be created.
        model (str): The model to be used for creating embeddings.

        Returns:
        dict: The response from the OpenAI API containing the embeddings.
        """
        response = self.client.embeddings.create(
            model=model, input=text
        )

        return response

import numpy as np


class MathAgent:

    @staticmethod
    def cosine_similarity(vec1, vec2):
        """
        Calculates the cosine similarity between two vectors.
        Compute the dot product of the two vectors and divide by the product of their norms.

        Args:
        vec1 (np.ndarray): The first vector.
        vec2 (np.ndarray): The second vector.

        Returns:
        float: The cosine similarity between the two vectors.
        """
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

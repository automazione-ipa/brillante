class TextChunker:
    @staticmethod
    def chunk_text(text, n, overlap):
        """
        Chunks the given text into segments of n characters with overlap.

        Args:
        text (str): The text to be chunked.
        n (int): The number of characters in each chunk.
        overlap (int): The number of overlapping characters between chunks.

        Returns:
        List[str]: A list of text chunks.
        """
        # Initialize an empty list to store the chunks
        chunks = []
        # Loop through the text with a step size of (n - overlap)
        for i in range(0, len(text), n - overlap):
            # Append a chunk of text from index i to i + n to the chunks list
            chunks.append(text[i:i + n])

        return chunks
from tqdm import tqdm

from document_rag_agents.base_agents.docai_agent import DocaiAgent
from document_rag_agents.base_agents.text_chunker import TextChunker
from document_rag_agents.base_agents.chat_agent import ChatAgent
from document_rag_agents.base_agents.embedding_agent import EmbeddingAgent
from document_rag_agents.db.simple_vector_store import SimpleVectorStore


class RAGPipeline:
    def __init__(self, api_key):
        self.extractor = DocaiAgent()
        self.chunker = TextChunker()
        self.chat_agent = ChatAgent(api_key)
        self.embedding_agent = EmbeddingAgent(api_key)
        self.vector_store = SimpleVectorStore()

    def process_document(
            self,
            pdf_path,
            chunk_size=1000,
            chunk_overlap=200,
            questions_per_chunk=5
    ):
        """
        Process a document with question augmentation.

        Args:
        pdf_path (str): Path to the PDF file.
        chunk_size (int): Size of each text chunk in characters.
        chunk_overlap (int): Overlap between chunks in characters.
        questions_per_chunk (int): Number of questions to generate per chunk.

        Returns:
        Tuple[List[str], SimpleVectorStore]: Text chunks and vector store.
        """
        print("Extracting text from PDF...")
        extracted_text = self.extractor.extract_text_from_pdf(pdf_path)

        print("Chunking text...")
        text_chunks = self.chunker.chunk_text(
            extracted_text, chunk_size, chunk_overlap
        )
        print(f"Created {len(text_chunks)} chunks")

        print("Processing chunks and generating questions...")
        for i, chunk in enumerate(tqdm(text_chunks, desc="Processing Chunks")):
            # Create embedding for the chunk itself
            chunk_embedding_res = self.embedding_agent.create_embeddings(chunk)
            chunk_embedding = chunk_embedding_res.data[0].embedding
            # Add the chunk to the vector store
            self.vector_store.add_item(
                text=chunk,
                embedding=chunk_embedding,
                metadata={"type": "chunk", "index": i}
            )
            # Generate questions for this chunk
            questions = self.chat_agent.generate_questions(
                text_chunk=chunk,
                num_questions=questions_per_chunk,
                model="meta-llama/Llama-3.2-3B-Instruct"
            )
            # Create embeddings for each question and add to vector store
            for j, question in enumerate(questions):
                question_embedding_response = self.embedding_agent.create_embeddings(question)
                question_embedding = question_embedding_response.data[0].embedding

                # Add the question to the vector store
                self.vector_store.add_item(
                    text=question,
                    embedding=question_embedding,
                    metadata={
                        "type": "question",
                        "chunk_index": i,
                        "original_chunk": chunk
                    }
                )

        return text_chunks, self.vector_store

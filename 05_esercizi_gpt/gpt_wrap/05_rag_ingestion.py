import PyPDF2
import pickle
import numpy as np
from gpt_wrap import get_embedding


def extract_text_from_pdf(pdf_path):
    """Funzione per estrarre il testo da un PDF."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text


def split_text_into_chunks(text, chunk_size=1000):
    """Funzione per suddividere il testo in chunk."""
    words = text.split()
    chunks = []
    while len(words) > chunk_size:
        chunk = ' '.join(words[:chunk_size])
        chunks.append(chunk)
        words = words[chunk_size:]
    if words:
        chunks.append(' '.join(words))
    return chunks


def generate_embedding(text):
    """Funzione per generare l'embedding di un testo."""
    embedding = get_embedding(text)
    return np.array(embedding).reshape(1, -1)


def build_index(chunks):
    """Funzione per costruire l'indice dei chunk"""
    embeddings = []
    for chunk in chunks:
        embeddings.append(generate_embedding(chunk))
    return embeddings


def save_index(index, filename='index.pkl'):
    """Funzione per salvare l'indice su disco."""
    with open(filename, 'wb') as f:
        pickle.dump(index, f)


def main(pdf_path):
    """Funzione principale."""
    text = extract_text_from_pdf(pdf_path)
    chunks = split_text_into_chunks(text)
    index = build_index(chunks)
    save_index(index)
    print(f"Indice creato e salvato da '{pdf_path}'.")


if __name__ == "__main__":
    pdf_path = 'resources/mws.pdf'
    main(pdf_path)

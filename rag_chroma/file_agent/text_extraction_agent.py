import PyPDF2
import os


class PdfReadAgent:
    RESOURCES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                  "resources")

    @staticmethod
    def text_from_pdf(pdf_name):
        """Legge il pdf dalla cartella resources e restituisce un testo"""
        pdf_path = os.path.join(PdfReadAgent.RESOURCES_PATH, pdf_name)

        if not os.path.exists(pdf_path):
            print(f"Il file {pdf_name} non esiste nella cartella resources.")
            return None

        try:
            with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = "\n".join(page.extract_text() for page in reader.pages if
                                 page.extract_text())
                return text
        except Exception as e:
            print(f"Errore nella lettura del PDF: {str(e)}")
            return None
        
    @staticmethod
    def chunk_text(text: str, max_length: int):
        return [
            text[i:i+max_length] for i in range(0, len(text), max_length)
        ]


    @staticmethod
    def smart_paragraph_chunking(text: str, max_length: int):
        """
        Divide un testo lungo in chunk di massimo `max_length` caratteri, 
        evitando di spezzare a metà le parole quando possibile.

        Logica:
        - Il testo viene prima diviso sui paragrafi (doppio a capo '\n\n').
        - Se un paragrafo è più lungo di `max_length`:
            - Viene tagliato trovando il più vicino spazio prima del limite.
            - Se non ci sono spazi, si taglia comunque esattamente a `max_length`.
        - I paragrafi più corti vengono concatenati insieme,
          finché la lunghezza totale non supera `max_length`.
        - Quando un chunk raggiunge la dimensione massima, viene salvato e si riparte.

        Args:
            text (str): Il testo completo da suddividere.
            max_length (int): La lunghezza massima consentita per ogni chunk.

        Returns:
            List[str]: Una lista di chunk di testo, ognuno lungo al massimo `max_length` caratteri.
        """
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ''

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            while len(para) > max_length:
                # Trova l'ultimo spazio prima del limite max_length
                split_pos = para.rfind(' ', 0, max_length)
                if split_pos == -1:
                    # Se non trova spazi, taglia brutalmente a max_length
                    split_pos = max_length
                chunk = para[:split_pos].strip()
                chunks.append(chunk)
                para = para[split_pos:].strip()  # Il resto da processare

            # Ora il paragrafo è più corto di max_length
            if not current_chunk:
                current_chunk = para
            elif len(current_chunk) + len(para) + 2 <= max_length:
                current_chunk += '\n\n' + para
            else:
                chunks.append(current_chunk.strip())
                current_chunk = para

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

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

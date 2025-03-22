from file_agent.text_extraction_agent import PdfReadAgent
from file_agent.extract_section import (
    extract_section,
    clean_extracted_text
)

if __name__ == "__main__":
    pdf_text = PdfReadAgent.text_from_pdf("esempio.pdf")
    if pdf_text:
        pdf_text = clean_extracted_text(pdf_text)
        print(pdf_text)

        # Ricerca della sezione corretta
        section_name = input("INSERISCI IL NOME DELLA SEZIONE DA CERCARE: ")
        result = extract_section(pdf_text, "CORSI E VOLONTARIATO")

        print("Trovata la sezione corrispondente!")
        print(result)
    else:
        print("Nessun testo estratto o errore nella lettura del PDF.")

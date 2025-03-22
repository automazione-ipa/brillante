from file_agent.text_extraction_agent import PdfReadAgent


if __name__ == "__main__":
    pdf_text = PdfReadAgent.text_from_pdf("esempio.pdf")
    if pdf_text:
        print(pdf_text)
    else:
        print("Nessun testo estratto o errore nella lettura del PDF.")

import os
from PyPDF2 import PdfReader

from gpt_wrap import chat_with_openai


def get_pdf_text(pdf_path):
    """Estrae il testo da tutte le pagine di un PDF."""
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + ' '
    return text.strip()


def main():
    """Funzione principale del programma interattivo."""
    dir_path = os.path.dirname(os.path.abspath(__file__))
    pdf_filename = "Temi d'esame Algoritmi e Programmazione (1).pdf"
    pdf_path = os.path.join(dir_path, "docs", pdf_filename)

    print("Estrazione del testo dal PDF...")
    context_text = get_pdf_text(pdf_path)

    print("Pronto! Fai una domanda sul documento (INVIO per uscire).")

    while True:
        user_question = input("\nDomanda: ")
        if not user_question:
            print("Fine della sessione. Alla prossima!")
            break

        try:
            risposta = chat_with_openai(
                user_message=context_text + ' ' + user_question,
                system_message="Sei un assistente utile.",
                model='gpt-4o-mini',
                temperature=0.7
            )
            print("\nRisposta:\n", risposta)
        except Exception as e:
            print("Errore durante la richiesta:", e)


if __name__ == "__main__":
    main()

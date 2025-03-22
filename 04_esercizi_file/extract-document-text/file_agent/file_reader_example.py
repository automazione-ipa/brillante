from PyPDF2 import PdfReader

reader = PdfReader("documento.pdf")

num_pag = len(reader.pages)

print(f"Numero di pagine: {num_pag}")

for page in reader.pages:
    print(page.extract_text())

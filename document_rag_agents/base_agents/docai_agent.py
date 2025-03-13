import fitz


class DocaiAgent:

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        """
        Extracts text from a PDF file and prints the first `num_chars` characters.

        Args:
        pdf_path (str): Path to the PDF file.

        Returns:
        str: Extracted text from the PDF.
        """
        mypdf = fitz.open(pdf_path)  # Open the PDF file
        all_text = ""  # Initialize an empty string to store the extracted text

        for page_num in range(mypdf.page_count):  # Iterate through each page in the PDF
            page = mypdf[page_num]  # Get the page
            text = page.get_text("text")  # Extract text from the page
            all_text += text  # Append the extracted text to the all_text string

        return all_text  # Return the extracted text
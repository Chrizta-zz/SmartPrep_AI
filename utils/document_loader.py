from PyPDF2 import PdfReader
from docx import Document
import os


def load_document(uploaded_file):
    """
    Extract text from PDF, DOCX, or TXT files.
    """

    file_extension = os.path.splitext(uploaded_file.name)[1].lower()

    # PDF
    if file_extension == ".pdf":
        reader = PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text

    # DOCX
    elif file_extension == ".docx":
        doc = Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])

    # TXT
    elif file_extension == ".txt":
        return uploaded_file.read().decode("utf-8")

    else:
        raise ValueError("Unsupported file type.")
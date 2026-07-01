import PyPDF2
from docx import Document


def load_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def load_file_text(uploaded_file, filename):

    file_extension = filename.lower().split(".")[-1]

    if file_extension == "pdf":
        return load_pdf_text(uploaded_file)

    elif file_extension == "docx":
        doc = Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])

    elif file_extension == "txt":
        return uploaded_file.read().decode("utf-8")

    else:
        raise ValueError("Unsupported file type")


# ✅ ADD THIS WRAPPER (IMPORTANT)
def load_document(uploaded_file, filename):
    return load_file_text(uploaded_file, filename)
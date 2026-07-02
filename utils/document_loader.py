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


def load_docx_text(uploaded_file):

    doc = Document(uploaded_file)

    text = ""

    for para in doc.paragraphs:

        text += para.text + "\n"

    return text


def load_txt_text(uploaded_file):

    return uploaded_file.read().decode("utf-8")


def load_document(uploaded_file):

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return load_pdf_text(uploaded_file)

    elif filename.endswith(".docx"):
        return load_docx_text(uploaded_file)

    elif filename.endswith(".txt"):
        return load_txt_text(uploaded_file)

    else:
        raise Exception("Unsupported File Type")
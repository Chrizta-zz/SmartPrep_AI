import os

from dotenv import load_dotenv
from groq import Groq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()


# -------------------------------
# Groq Client
# -------------------------------
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Global vector database
vector_db = None


# -------------------------------
# Create Vector Store
# -------------------------------
def create_vectorstore(document_text):

    global vector_db

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(document_text)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )


# -------------------------------
# Ask Question
# -------------------------------
def ask_document(question):

    global vector_db

    if vector_db is None:
        return "Please upload a document first."

    docs = vector_db.similarity_search(
        question,
        k=4
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = f"""
You are an AI Study Assistant.

Answer ONLY using the information provided below.

If the answer is not present in the document, simply reply:

"I couldn't find that information in the uploaded document."

Document:

{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You answer questions only from the uploaded document."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
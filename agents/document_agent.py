from langchain_groq import ChatGroq

from config import GROQ_API_KEY, MODEL_NAME
from utils.document_loader import load_document
from utils.vector_store import create_vectorstore
from utils.rag_chain import prompt


# -----------------------------
# INITIALIZE LLM
# -----------------------------
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=MODEL_NAME,
)


# -----------------------------
# BUILD VECTOR STORE
# -----------------------------
def process_document(uploaded_file):

    document_text = load_document(uploaded_file)

    vectorstore = create_vectorstore(document_text)

    return vectorstore


# -----------------------------
# ASK QUESTION
# -----------------------------
def ask_document(vectorstore, question):

    docs = vectorstore.similarity_search(
        question,
        k=4
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    chain = prompt | llm

    response = chain.invoke({
        "context": context,
        "question": question
    })

    return response.content
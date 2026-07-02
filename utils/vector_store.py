from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# -----------------------------
# EMBEDDING MODEL
# -----------------------------
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# -----------------------------
# SPLIT DOCUMENT
# -----------------------------
def chunk_text(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    return splitter.split_text(text)


# -----------------------------
# CREATE VECTOR STORE
# -----------------------------
def create_vectorstore(text):

    chunks = chunk_text(text)

    vectorstore = FAISS.from_texts(
        chunks,
        embedding_model
    )

    return vectorstore
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


# =====================================================
# DOCUMENT TUTOR (RAG)
# =====================================================

def create_vectorstore(text):

    # If already chunked
    if isinstance(text, list):
        chunks = text
    else:
        chunks = chunk_text(text)

    vectorstore = FAISS.from_texts(
        chunks,
        embedding_model
    )

    return vectorstore


# =====================================================
# QUIZ GENERATOR
# =====================================================

def build_index(data):
    """
    Builds a FAISS vector store.

    Accepts:
    - Raw document text (str)
    - List of chunks (list)
    """

    return create_vectorstore(data)


def search_similar_chunks(vectorstore, query, k=4):
    """
    Returns the most relevant text chunks.
    """

    docs = vectorstore.similarity_search(
        query,
        k=k
    )

    return [doc.page_content for doc in docs]
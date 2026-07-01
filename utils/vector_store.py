# utils/vector_store.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Global storage
index = None
chunks_store = []


def build_index(text_chunks):
    """
    Create FAISS index from PDF chunks
    """
    global index, chunks_store

    chunks_store = text_chunks

    embeddings = model.encode(text_chunks)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    return index


def search_similar_chunks(query, k=5):
    """
    Semantic search using FAISS
    """
    global index, chunks_store

    if index is None:
        return []

    query_embedding = model.encode([query])

    distances, indices = index.search(np.array(query_embedding), k)

    results = []
    for i in indices[0]:
        if i < len(chunks_store):
            results.append(chunks_store[i])

    return results
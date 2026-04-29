# domains/rag/retriever.py
from domains.rag.ollama_client import embed
from domains.rag.store import VectorStore

def retrieve(question, k=5):
    store = VectorStore()
    q_emb = embed(question)
    return store.search(q_emb, k=k)

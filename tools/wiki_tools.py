# tools/wiki_tools.py
from domains.rag.retriever import retrieve
from domains.rag.indexer import index_wiki_incremental

def answer_from_wiki(question: str, k: int = 5) -> str:
    hits = retrieve(question, k)
    # optional: format hits or hand back raw context
    return hits

def index_wiki() -> str:
    index_wiki_incremental()
    return "Wiki indexed successfully."

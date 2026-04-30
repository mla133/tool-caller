# domains/rag/llm_client.py
import requests

CHAT_BASE = "http://localhost:8123/v1"
CHAT_MODEL = "qwen2.5-coder-14b-instruct"

EMBED_BASE = "http://localhost:8124/v1"
EMBED_MODEL = "nomic-embed-text"

def embed(text: str) -> list[float]:
    r = requests.post(
        f"{EMBED_BASE}/embeddings",
        json={
            "model": EMBED_MODEL,
            "input": text,
        },
    )
    r.raise_for_status()
    return r.json()["data"][0]["embedding"]

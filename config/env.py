from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

LLAMA_SYSTEM_PROMPT_PATH= BASE_DIR / "llama_system_prompt.txt"

LLM_BACKEND = require_env("LLM_BACKEND")
NEWS_API_KEY = require_env("NEWS_API_KEY")
MAX_STEPS = int(require_env("MAX_STEPS"))
LLM_MODEL = require_env("LLM_MODEL")
TIMEOUT = int(require_env("TIMEOUT"))

import os
from dotenv import load_dotenv

load_dotenv()

def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

NEWS_API_KEY = require_env("NEWS_API_KEY")
MAX_STEPS = int(require_env("MAX_STEPS"))
LLM_MODEL = require_env("LLM_MODEL")

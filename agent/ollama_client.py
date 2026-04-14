import json
import urllib.request
import urllib.error

def call_ollama(payload: dict) -> dict:
    try:
        req = urllib.request.Request(
            "http://localhost:11434/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.URLError as e:
        raise RuntimeError(
            "Failed to connect to Ollama. "
            "Is Ollama running at http://localhost:11434?\n"
            f"Underlying error: {e}"
        )

    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Ollama returned invalid JSON: {e}"
        )

    except Exception as e:
        raise RuntimeError(
            f"Unexpected error calling Ollama: {e}"
        )


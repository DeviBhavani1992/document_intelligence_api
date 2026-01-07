import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "gemma:2b"

def summarize_text(text: str) -> str:
    if not text.strip():
        return "No text found to summarize."

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes documents clearly."},
            {"role": "user", "content": f"Summarize the following document:\n\n{text}"}
        ],
        "options": {
            "temperature": 0.3,
            "num_predict": 300
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            stream=True,   # IMPORTANT for streaming responses
            timeout=180
        )
        response.raise_for_status()

        full_text = ""

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "message" in data and "content" in data["message"]:
                    full_text += data["message"]["content"]

                if data.get("done"):
                    break

        return full_text.strip()

    except requests.exceptions.RequestException as e:
        return f"Ollama summarization failed: {str(e)}"

import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2"


def ask_ai(question, context=""):
    prompt = f"""
You are an intelligent AI tutor for an e-learning platform.

Use the study material/context below when it is relevant.

Study Material:
{context}

Student Question:
{question}

Give a clear, simple and educational answer.
Explain step-by-step when necessary.
"""

    data = {
    "model": MODEL_NAME,
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "stream": False,
    "options": {
        "num_predict": 100
    }
}

    response = requests.post(
        OLLAMA_URL,
        json=data,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result["message"]["content"]
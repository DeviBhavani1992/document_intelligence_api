from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text: str) -> str:
    if not text.strip():
        return "No text found to summarize."

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes documents clearly."},
            {"role": "user", "content": f"Summarize the following document:\n\n{text}"}
        ],
        temperature=0.3,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()

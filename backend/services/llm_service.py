from anthropic import Anthropic
import os

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),)


def get_answer(question, context):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"Contexto:\n{context}\n\nPregunta: {question}"}]
    )
    return response.content[0].text
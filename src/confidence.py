import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = None

def _get_client():
    global client
    if client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable not set. "
                "Please add it to your .env file or Streamlit secrets."
            )
        client = Groq(api_key=api_key)
    return client

CONFIDENCE_PROMPT = """
You are a SQL review expert. Given a business question and the SQL query generated to answer it, rate the confidence that the SQL correctly answers the question.

Return ONLY a valid JSON object in this exact format with no extra text, no markdown, no code fences:
{"confidence": "High", "reason": "one sentence explanation"}

Confidence levels:
- High: question maps cleanly to the schema, JOIN path is clear, no ambiguity
- Medium: some assumptions made, question was vague, or multiple interpretations possible  
- Low: question poorly matched to schema, column intent was guessed, result may be unreliable
"""

def get_confidence(question: str, sql: str) -> dict:
    try:
        groq_client = _get_client()
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": CONFIDENCE_PROMPT},
                {"role": "user", "content": f"Question: {question}\n\nSQL:\n{sql}"}
            ],
            temperature=0
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except Exception:
        return {"confidence": "Medium", "reason": "Could not assess confidence for this query."}

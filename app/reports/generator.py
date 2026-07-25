import os
import json
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set. Run: $env:GROQ_API_KEY='your_key'")

client = Groq(api_key=api_key)

def generate_market_briefing(data: dict) -> str:
    prompt = f"""
You are a senior financial analyst at a UK investment bank. Write a concise weekly market briefing (150‑200 words) based on the following data.

Market Data:
{json.dumps(data.get("market_data", {}), indent=2)}

Your briefing should:
- Start with a one‑sentence summary of the week's market movement.
- Mention FTSE 100 and FTSE 250 performance, including percentage changes.
- Highlight any notable bank stock movements (Barclays, Lloyds, HSBC).
- End with a one‑sentence outlook for the coming week.

Return ONLY the briefing text — no JSON, no meta‑commentary.
"""
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=400
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Report generation failed: {e}"
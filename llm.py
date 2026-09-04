import json
import re
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

PROMPT = """
You are a video compliance auditor.

Use ONLY the supplied compliance rules as the reference.
Do not invent laws or rules.

Analyze the transcript and identify possible compliance problems.

Return ONLY valid JSON:
{{
  "status": "PASS" or "FAIL",
  "summary": "short summary",
  "violations": [
    {{
      "category": "rule category",
      "severity": "HIGH" or "MEDIUM" or "LOW",
      "description": "what may be wrong",
      "evidence": "short quote from transcript",
      "recommendation": "how to improve"
    }}
  ]
}}

If no rule is clearly violated, return PASS with an empty violations list.

COMPLIANCE RULES:
{rules}

VIDEO TRANSCRIPT:
{transcript}
"""

def _clean_json(text):
    text = text.strip()
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.S | re.I)
    if match:
        text = match.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        text = text[start:end + 1]
    return text

def ollama_audit(transcript, context):
    rules = "\n\n".join(
        f"[{x['source']} | score={x['score']:.3f}]\n{x['text']}"
        for x in context
    )

    prompt = PROMPT.format(
        rules=rules[:12000],
        transcript=transcript[:30000]
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0}
            },
            timeout=180
        )
        response.raise_for_status()
        raw = response.json().get("response", "")
        return json.loads(_clean_json(raw))
    except (requests.RequestException, json.JSONDecodeError, KeyError):
        return None

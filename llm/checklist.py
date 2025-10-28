import os, requests, json, re

from pydantic import BaseModel

LLM = os.getenv("LLM_ENDPOINT","http://ollama:11434")

class Review(BaseModel):
    summary: str = ""
    suggestion: str = ""
    violation: bool = False

def llm_review(context: dict) -> Review:
    prompt = f"""
Return JSON only: {{"summary":"","suggestion":"","violation":false}}
You're a risk reviewer. No trade commands. Context:
{json.dumps(context, ensure_ascii=False)}
"""
    r = requests.post(f"{LLM}/api/generate",
        json={"model":"phi3:mini","prompt":prompt,"stream":False}, timeout=60)
    text = r.json().get("response","{}")
    m = re.search(r"\{.*\}", text, re.S)
    obj = json.loads(m.group(0)) if m else {}
    return Review(**obj)

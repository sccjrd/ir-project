# app/tokenization/llm_local.py
import json
import requests
from typing import List, Tuple

from app.models import Hack
from app.tokenization.config import IKEA_HACKS_CATEGORIES

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:3b"

SYSTEM_PROMPT = f"""
You are an assistant that tags IKEA hack posts.

You receive a post with:
- title
- content (short, informal text)

Your job:
1. Choose 1–3 high-level categories from this allowed list ONLY:
{", ".join(IKEA_HACKS_CATEGORIES)}

2. Generate 3–5 tags:
   - short phrases
   - IKEA product names (LACK, BILLY, KALLAX, etc.)
   - actions (wall-mounted, painted, added wheels)
   - usage (kids room, shoe storage)

Output strictly this JSON object, nothing else:

{{
  "categories": ["category1", "category2"],
  "tags": ["tag1", "tag2", "tag3"]
}}
"""


def _build_user_prompt(hack: Hack) -> str:
    content = (hack.content or hack.excerpt or "")[:600]
    return f"""
Post:
{{
  "title": {json.dumps(hack.title)},
  "content": {json.dumps(content)}
}}
"""


def tag_hack_with_llm(hack: Hack) -> Tuple[List[str], List[str]]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": _build_user_prompt(hack)},
    ]

    try:
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "stream": False,
            },
            timeout=120,
        )
        r.raise_for_status()
    except Exception as e:
        print(f"[LLM ERROR] local request failed for {hack.title!r}: {e}")
        return [], []

    data = r.json()
    text = data["message"]["content"].strip()

    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()

    try:
        parsed = json.loads(text)
    except Exception as e:
        print(f"[LLM ERROR] JSON parse failed for {hack.title!r}: {e}")
        print("Raw:", text[:400])
        return [], []

    raw_categories = parsed.get("categories") or []
    raw_tags = parsed.get("tags") or []

    categories = [
        c for c in raw_categories
        if isinstance(c, str) and c in IKEA_HACKS_CATEGORIES
    ]

    tags: List[str] = []
    seen = set()
    for t in raw_tags:
        if not isinstance(t, str):
            continue
        t_clean = t.strip()
        if not t_clean:
            continue
        key = t_clean.lower()
        if key in seen:
            continue
        seen.add(key)
        tags.append(t_clean)

    return categories, tags

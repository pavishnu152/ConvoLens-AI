# src/llm_client.py
import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

LMSTUDIO_BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://192.168.43.122:1234")
LMSTUDIO_MODEL = os.getenv("LMSTUDIO_MODEL", "Phi-3-mini-4k-instruct")  # change to your exact id

# Long timeout so local LLM can finish
timeout = httpx.Timeout(
    connect=10.0,
    read=300.0,
    write=30.0,
    pool=30.0,
)
http_client = httpx.Client(timeout=timeout)


def analyze_transcript(transcript: str) -> dict:
    """
    Use local LM Studio model to generate:
    - smart_summary: string
    - key_points: list[str]
    - smart_improvements: list[str]

    This function either returns a dict with these keys
    or raises an exception. It never returns None.
    """
    if not transcript or not transcript.strip():
        raise ValueError("Transcript is empty")

    system_prompt = (
        "You are an expert communication and productivity coach. "
        "You analyze transcripts from calls, lectures, meetings, and videos. "
        "You MUST reply with valid JSON only, with keys:\n"
        "  - smart_summary: string\n"
        "  - key_points: list of strings\n"
        "  - smart_improvements: list of strings\n"
    )

    user_prompt = (
        "Here is the transcript:\n\n"
        f"{transcript}\n\n"
        "Tasks:\n"
        "1) smart_summary: A clear, concise summary of what happened.\n"
        "2) key_points: 3–8 bullet-style key points capturing the most important ideas.\n"
        "3) smart_improvements: 3–8 practical suggestions to improve clarity, structure, or delivery.\n"
        "Return ONLY JSON, no extra text."
    )

    url = f"{LMSTUDIO_BASE_URL}/chat/completions"
    payload = {
        "model": LMSTUDIO_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 256,
    }

    try:
        resp = http_client.post(url, json=payload)
        resp.raise_for_status()
    except Exception as e:
        # Fail loudly so pipeline can show clear error
        raise RuntimeError(f"LM Studio HTTP request failed: {e}")

    data = resp.json()

    try:
        content = data["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"Unexpected LM Studio response structure: {e}, data={data}")

    # Try to parse JSON from model
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        # Fallback: use raw text as summary, keep lists empty
        parsed = {
            "smart_summary": content.strip(),
            "key_points": [],
            "smart_improvements": [],
        }

    smart_summary = parsed.get("smart_summary", "")
    key_points = parsed.get("key_points", [])
    smart_improvements = parsed.get("smart_improvements", [])

    # Normalize list fields
    if isinstance(key_points, str):
        key_points = [key_points]
    elif not isinstance(key_points, list):
        key_points = []

    if isinstance(smart_improvements, str):
        smart_improvements = [smart_improvements]
    elif not isinstance(smart_improvements, list):
        smart_improvements = []

    # Final guaranteed dict
    return {
        "smart_summary": smart_summary,
        "key_points": key_points,
        "smart_improvements": smart_improvements,
    }

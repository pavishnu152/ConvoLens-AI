# src/stt_client.py
import os
import time
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
if not ASSEMBLYAI_API_KEY:
    raise ValueError("ASSEMBLYAI_API_KEY is not set in .env")

AIAI_BASE_URL = "https://api.assemblyai.com/v2"


def _upload_file(file_path: str) -> str:
    """Upload local file to AssemblyAI and return upload URL."""
    headers = {"authorization": ASSEMBLYAI_API_KEY}
    with open(file_path, "rb") as f:
        resp = requests.post(f"{AIAI_BASE_URL}/upload", headers=headers, data=f)
    resp.raise_for_status()
    return resp.json()["upload_url"]


def _create_transcript(audio_url: str, language: Optional[str] = None) -> str:
    """Create a transcript and wait until it is completed, then return text."""
    headers = {
        "authorization": ASSEMBLYAI_API_KEY,
        "content-type": "application/json",
    }
    body = {"audio_url": audio_url}
    if language:
        body["language_code"] = language

    # Create transcript job
    resp = requests.post(f"{AIAI_BASE_URL}/transcript", json=body, headers=headers)
    resp.raise_for_status()
    transcript_id = resp.json()["id"]

    # Poll for completion
    while True:
        status_resp = requests.get(
            f"{AIAI_BASE_URL}/transcript/{transcript_id}", headers=headers
        )
        status_resp.raise_for_status()
        data = status_resp.json()
        status = data["status"]

        if status == "completed":
            return data.get("text", "")
        elif status == "error":
            raise RuntimeError(f"Transcription error: {data.get('error')}")
        else:
            time.sleep(3)


def transcribe_audio(file_path: str, language: Optional[str] = None) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    audio_url = _upload_file(file_path)
    text = _create_transcript(audio_url, language=language)
    if text is None:
        raise RuntimeError("STT provider returned None transcript")

    return text.strip()


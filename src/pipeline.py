# src/pipeline.py
from typing import Dict, Optional

from src.stt_client import transcribe_audio
from src.llm_client import analyze_transcript
from src.youtube_utils import download_youtube_audio


def _validate_analysis(analysis: dict, context: str) -> dict:
    """
    Ensure analyze_transcript returned a proper dict with required keys.
    """
    if analysis is None:
        raise RuntimeError(f"analyze_transcript returned None ({context})")

    if not isinstance(analysis, dict):
        raise RuntimeError(
            f"analyze_transcript returned non-dict ({context}): {type(analysis)}"
        )

    # Ensure required keys exist
    for key in ["smart_summary", "key_points", "smart_improvements"]:
        if key not in analysis:
            raise RuntimeError(
                f"analyze_transcript result missing key '{key}' ({context})"
            )

    return analysis


def process_local_file(file_path: str, language: Optional[str] = None) -> Dict:
    """
    Full pipeline for uploaded audio/video file:
    - Transcribe with STT
    - Analyze with LLM
    """
    transcript = transcribe_audio(file_path, language=language)
    if not transcript:
        raise RuntimeError("transcribe_audio returned empty transcript")

    analysis = analyze_transcript(transcript)
    analysis = _validate_analysis(analysis, context="local_file")

    return {
        "title": "Uploaded File",
        "transcript": transcript,
        **analysis,
    }


def process_youtube_url(url: str, language: Optional[str] = None) -> Dict:
    """
    Full pipeline for YouTube URL:
    - Download audio
    - Transcribe with STT
    - Analyze with LLM
    """
    audio_path, title = download_youtube_audio(url)
    if not audio_path:
        raise RuntimeError("download_youtube_audio returned empty audio_path")

    transcript = transcribe_audio(audio_path, language=language)
    if not transcript:
        raise RuntimeError("transcribe_audio returned empty transcript for YouTube")

    analysis = analyze_transcript(transcript)
    analysis = _validate_analysis(analysis, context="youtube_url")

    return {
        "title": title or "YouTube Video",
        "transcript": transcript,
        **analysis,
    }

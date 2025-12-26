# src/youtube_utils.py
import os
import tempfile
from typing import Tuple

import yt_dlp


def download_youtube_audio(url: str) -> Tuple[str, str]:
    """
    Download only the audio from a YouTube video as an .mp3 file.
    Returns (audio_path, video_title).
    """

    # Create a temp directory for this download
    tmp_dir = tempfile.mkdtemp(prefix="yt_audio_")

    # We ask yt_dlp to extract audio directly to mp3. [web:901][web:925]
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(tmp_dir, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)  # download & extract audio
        video_title = info.get("title", "YouTube Video")

        # After postprocessing, audio file should be title + .mp3
        base = ydl.prepare_filename(info)
        base_no_ext, _ = os.path.splitext(base)
        audio_path = base_no_ext + ".mp3"

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found after download: {audio_path}")

    return audio_path, video_title

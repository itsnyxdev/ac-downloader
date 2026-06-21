import os
import shutil
from pathlib import Path


def detect() -> str | None:
    return _resolve_ffmpeg()


def resolve_ffprobe() -> str | None:
    ffmpeg_path = _resolve_ffmpeg()
    if ffmpeg_path is None:
        return None
    ffprobe_name = "ffprobe.exe" if os.name == "nt" else "ffprobe"
    sibling = Path(ffmpeg_path).parent / ffprobe_name
    if sibling.exists():
        return str(sibling)
    return shutil.which("ffprobe")


def _resolve_ffmpeg() -> str | None:
    return _from_env() or shutil.which("ffmpeg")


def _from_env() -> str | None:
    return os.getenv("FFMPEG_PATH")

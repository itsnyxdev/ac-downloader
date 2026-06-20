import os
import shutil


def detect() -> str | None:
    return _resolve()


def _resolve() -> str | None:
    return _from_env() or shutil.which("ffmpeg")


def _from_env() -> str | None:
    return os.getenv("FFMPEG_PATH")

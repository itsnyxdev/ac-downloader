from pathlib import Path
from typing import Any

import rtoml

from ..config import Settings
from .printer import error

settings = Settings()


def config_path() -> Path:
    config_dir = Path.home() / settings.dir_name
    config_dir.mkdir(parents=True, exist_ok=True)

    return config_dir


def config_file() -> Path:
    return config_path() / "config.toml"


def load() -> dict[str, Any]:
    path = config_file()

    if not path.exists():
        return {}

    try:
        with path.open("r", encoding="utf-8") as file:
            return rtoml.load(file)
    except Exception as e:
        error(f"Failed to load config: {e}")
        return {}


def save(config: dict[str, Any]) -> bool:
    path = config_file()

    try:
        with path.open("w", encoding="utf-8") as file:
            rtoml.dump(config, file)
        return True
    except Exception as e:
        error(f"Failed to save config: {e}")
        return False

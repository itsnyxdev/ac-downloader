from dataclasses import dataclass


@dataclass
class MediaItem:
    name: str
    type: str
    start: int
    end: int


@dataclass
class OutputConfig:
    dir: str
    storage: str
    filename: str
    fps: int
    resolution: str

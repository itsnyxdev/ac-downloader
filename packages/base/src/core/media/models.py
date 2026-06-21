from dataclasses import dataclass, field


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
    ffmpeg_bin: str = field(default="ffmpeg")
    ffprobe_bin: str = field(default="ffprobe")

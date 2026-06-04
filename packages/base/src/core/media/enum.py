from enum import Enum


class CombineType(Enum):
    VIDEO = "video"
    AUDIO = "audio"


class EventType(Enum):
    STREAM_ADDED = "streamAdded"
    STREAM_REMOVED = "streamRemoved"

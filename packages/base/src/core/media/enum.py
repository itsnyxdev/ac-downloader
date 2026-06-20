from enum import Enum


class EventType(Enum):
    STREAM_ADDED = "streamAdded"
    STREAM_REMOVED = "streamRemoved"

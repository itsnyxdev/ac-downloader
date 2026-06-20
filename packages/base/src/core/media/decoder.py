import xml.etree.ElementTree as ElementTree
from pathlib import Path

from loguru import logger

from . import enum as media_enum
from .models import MediaItem


def decode(xml_path: str) -> tuple[list[MediaItem], float]:
    if not Path(xml_path).exists():
        logger.error(f"XML file {xml_path} does not exist.")
        return [], 0.0

    try:
        xml = ElementTree.parse(xml_path)  # noqa: S314
        root = xml.getroot()

        return _process(root)
    except ElementTree.ParseError as e:
        logger.error(f"Error parsing XML file {xml_path}: {e}")
        return [], 0.0


def _process(root: ElementTree.Element) -> tuple[list[MediaItem], float]:
    media: list[MediaItem] = []
    streams: dict[str, dict] = {}
    max_duration_ms = 0

    for message in root.findall("Message"):
        message_time = int(message.get("time", 0))
        max_duration_ms = max(max_duration_ms, message_time)
        event_type = _extract_event_type(message)

        if not event_type:
            continue

        stream_data = _extract_stream_data(message)
        if stream_data:
            _handle_stream_event(event_type, streams, media, stream_data, message_time)

    _handle_remaining_streams(streams, max_duration_ms, media)

    media.sort(key=lambda m: m.start)

    return media, max_duration_ms / 1000.0


def _extract_event_type(message: ElementTree.Element) -> str:
    event_values = {event.value for event in media_enum.EventType}

    for s in message.findall("String"):
        if s.text in event_values:
            return s.text

    return ""


def _extract_stream_data(
    message: ElementTree.Element,
) -> tuple[str, str, str | None, str] | None:
    array = message.find("Array")

    if array is None:
        return None

    object_element = array.find("Object")
    if object_element is None:
        return None

    stream_id = object_element.findtext("streamId")
    stream_name = object_element.findtext("streamName", "").lstrip("/")
    stream_start = object_element.findtext("startTime")
    stream_type = object_element.findtext("streamType", "").lower()

    return stream_id, stream_name, stream_start, stream_type


def _handle_stream_event(
    event_type: str,
    streams: dict[str, dict],
    media: list[MediaItem],
    stream_data: tuple[str, str, str | None, str],
    message_time: int,
) -> None:
    stream_id, stream_name, stream_start, stream_type = stream_data

    if event_type == media_enum.EventType.STREAM_ADDED.value:
        streams[stream_id] = {
            "name": stream_name,
            "type": stream_type,
            "start": int(stream_start) if stream_start else message_time,
        }
    elif (
        event_type == media_enum.EventType.STREAM_REMOVED.value and stream_id in streams
    ):
        data = streams.pop(stream_id)
        media.append(
            MediaItem(
                name=data["name"],
                type=data["type"],
                start=data["start"],
                end=message_time,
            )
        )


def _handle_remaining_streams(
    streams: dict[str, dict], max_duration_ms: int, media: list[MediaItem]
) -> None:
    media.extend(
        MediaItem(
            name=data["name"],
            type=data["type"],
            start=data["start"],
            end=max_duration_ms,
        )
        for data in streams.values()
    )

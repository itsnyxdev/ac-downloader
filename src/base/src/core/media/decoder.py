import os.path
from typing import Tuple, List, Dict, Optional
import xml.etree.ElementTree as ElementTree
from loguru import logger

EVENT_TYPES = ["streamAdded", "streamRemoved"]


def decode(xml_path: str) -> Tuple[List[Dict], float]:
    if not os.path.exists(xml_path):
        logger.error(f"XML file {xml_path} does not exist.")
        return [], 0.0

    try:
        xml = ElementTree.parse(xml_path)
        root = xml.getroot()

        return _process(root)
    except ElementTree.ParseError as e:
        logger.error(f"Error parsing XML file {xml_path}: {e}")


def _process(root: ElementTree.Element) -> Tuple[List[Dict], float]:
    media = []
    streams = {}
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

    media.sort(key=lambda m: m["start"])

    return media, max_duration_ms / 1000.0


def _extract_event_type(message: ElementTree.Element) -> str:
    for s in message.findall("String"):
        if s.text in EVENT_TYPES:
            return s.text

    return ""


def _extract_stream_data(
    message: ElementTree.Element,
) -> Optional[Tuple[str, str, str, str]]:
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
    streams: Dict,
    media: List,
    stream_data: Optional[Tuple[str, str, str, str]],
    message_time: int,
):
    stream_id, stream_name, stream_start, stream_type = stream_data

    if event_type == "streamAdded":
        streams[stream_id] = {
            "name": stream_name,
            "type": stream_type,
            "start": int(stream_start) if stream_start else message_time,
        }
    elif event_type == "streamRemoved":
        if stream_id in streams:
            data = streams.pop(stream_id)
            data["end"] = message_time
            media.append(data)


def _handle_remaining_streams(streams: Dict, max_duration_ms: int, media: List):
    for id, data in streams.items():
        data["end"] = max_duration_ms
        media.append(data)

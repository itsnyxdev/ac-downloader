import tempfile
from pathlib import Path

from core.media.decoder import decode
from core.media.models import MediaItem

VALID_XML = """\
<root>
    <Message time="0" type="data">
        <String>streamAdded</String>
        <Array>
            <Object>
                <streamId>cam_0</streamId>
                <streamName>/camera_0_1</streamName>
                <startTime>1000</startTime>
                <streamType>cameraVoip</streamType>
            </Object>
        </Array>
    </Message>
    <Message time="5000" type="data">
        <String>streamRemoved</String>
        <Array>
            <Object>
                <streamId>cam_0</streamId>
                <streamName>/camera_0_1</streamName>
                <startTime>1000</startTime>
                <streamType>cameraVoip</streamType>
            </Object>
        </Array>
    </Message>
    <Message time="2000" type="data">
        <String>streamAdded</String>
        <Array>
            <Object>
                <streamId>screen_0</streamId>
                <streamName>/screenshare_0</streamName>
                <startTime>2000</startTime>
                <streamType>screenshare</streamType>
            </Object>
        </Array>
    </Message>
    <Message time="8000" type="data">
        <String>streamRemoved</String>
        <Array>
            <Object>
                <streamId>screen_0</streamId>
                <streamName>/screenshare_0</streamName>
                <startTime>2000</startTime>
                <streamType>screenshare</streamType>
            </Object>
        </Array>
    </Message>
</root>
"""

REMAINING_STREAM_XML = """\
<root>
    <Message time="0" type="data">
        <String>streamAdded</String>
        <Array>
            <Object>
                <streamId>cam_0</streamId>
                <streamName>/camera_0_1</streamName>
                <startTime>500</startTime>
                <streamType>cameraVoip</streamType>
            </Object>
        </Array>
    </Message>
    <Message time="10000" type="data">
        <Method>someOtherEvent</Method>
    </Message>
</root>
"""

EMPTY_XML = "<root></root>"

MALFORMED_XML = "<root><broken"


def _write_xml(content: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False) as f:
        f.write(content)
        return f.name


def test_decode_valid_xml():
    path = _write_xml(VALID_XML)
    media, duration = decode(path)

    assert len(media) == 2
    assert duration == 8.0

    assert media[0].name == "camera_0_1"
    assert media[0].type == "cameravoip"
    assert media[0].start == 1000
    assert media[0].end == 5000

    assert media[1].name == "screenshare_0"
    assert media[1].type == "screenshare"
    assert media[1].start == 2000
    assert media[1].end == 8000


def test_decode_remaining_streams():
    path = _write_xml(REMAINING_STREAM_XML)
    media, duration = decode(path)

    assert len(media) == 1
    assert duration == 10.0
    assert media[0].name == "camera_0_1"
    assert media[0].start == 500
    assert media[0].end == 10000


def test_decode_empty_xml():
    path = _write_xml(EMPTY_XML)
    media, duration = decode(path)

    assert media == []
    assert duration == 0.0


def test_decode_malformed_xml():
    path = _write_xml(MALFORMED_XML)
    media, duration = decode(path)

    assert media == []
    assert duration == 0.0


def test_decode_missing_file():
    media, duration = decode("/nonexistent/path.xml")

    assert media == []
    assert duration == 0.0


def test_decode_returns_media_item_instances():
    path = _write_xml(VALID_XML)
    media, _ = decode(path)

    for item in media:
        assert isinstance(item, MediaItem)


def test_decode_sorted_by_start():
    path = _write_xml(VALID_XML)
    media, _ = decode(path)

    for i in range(len(media) - 1):
        assert media[i].start <= media[i + 1].start


def test_decode_stream_name_stripped():
    xml = """\
<root>
    <Message time="0" type="data">
        <String>streamAdded</String>
        <Array>
            <Object>
                <streamId>s1</streamId>
                <streamName>/leading_slash</streamName>
                <startTime>100</startTime>
                <streamType>cameraVoip</streamType>
            </Object>
        </Array>
    </Message>
    <Message time="500" type="data">
        <String>streamRemoved</String>
        <Array>
            <Object>
                <streamId>s1</streamId>
                <streamName>/leading_slash</streamName>
                <startTime>100</startTime>
                <streamType>cameraVoip</streamType>
            </Object>
        </Array>
    </Message>
</root>
"""
    path = _write_xml(xml)
    media, _ = decode(path)

    assert media[0].name == "leading_slash"

from core.media.merger import _detect_streams


def test_detect_streams_both():
    probe = {
        "streams": [
            {"codec_type": "video", "codec_name": "h264"},
            {"codec_type": "audio", "codec_name": "aac"},
        ]
    }
    has_video, has_audio = _detect_streams(probe)
    assert has_video is True
    assert has_audio is True


def test_detect_streams_video_only():
    probe = {"streams": [{"codec_type": "video"}]}
    has_video, has_audio = _detect_streams(probe)
    assert has_video is True
    assert has_audio is False


def test_detect_streams_audio_only():
    probe = {"streams": [{"codec_type": "audio"}]}
    has_video, has_audio = _detect_streams(probe)
    assert has_video is False
    assert has_audio is True


def test_detect_streams_empty():
    probe = {"streams": []}
    has_video, has_audio = _detect_streams(probe)
    assert has_video is False
    assert has_audio is False


def test_detect_streams_no_streams_key():
    has_video, has_audio = _detect_streams({})
    assert has_video is False
    assert has_audio is False


def test_detect_streams_none_input():
    has_video, has_audio = _detect_streams(None)  # type: ignore[arg-type]
    assert has_video is False
    assert has_audio is False

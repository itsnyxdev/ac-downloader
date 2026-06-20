import tempfile
from pathlib import Path
from unittest.mock import patch

from cli.app import app
from cli.commands.convert import OUTPUT_FILENAME, QUALITY_SETTINGS
from cli.enums import Quality
from typer.testing import CliRunner

runner = CliRunner()


@patch("cli.commands.convert.ffmpeg.detect", return_value="/usr/bin/ffmpeg")
def test_convert_missing_indexstream(mock_detect):
    with tempfile.TemporaryDirectory() as tmpdir:
        result = runner.invoke(app, ["convert", tmpdir])
        assert result.exit_code == 1
        assert "No indexstream.xml found" in result.output


def test_convert_nonexistent_dir():
    result = runner.invoke(app, ["convert", "/nonexistent/dir"])
    assert result.exit_code != 0


@patch("cli.commands.convert.ffmpeg.detect", return_value=None)
def test_convert_no_ffmpeg(mock_detect):
    with tempfile.TemporaryDirectory() as tmpdir:
        (Path(tmpdir) / "indexstream.xml").write_text("<root></root>")
        result = runner.invoke(app, ["convert", tmpdir])
        assert result.exit_code == 1
        assert "FFmpeg not found" in result.output


def test_quality_settings_coverage():
    for quality in Quality:
        assert quality in QUALITY_SETTINGS
        settings = QUALITY_SETTINGS[quality]
        assert "x" in settings
        assert "y" in settings
        assert "fps" in settings
        assert isinstance(settings["x"], int)
        assert isinstance(settings["y"], int)
        assert isinstance(settings["fps"], int)


def test_output_filename():
    assert OUTPUT_FILENAME == "output.mp4"

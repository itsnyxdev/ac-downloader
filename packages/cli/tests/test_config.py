import tempfile
from pathlib import Path
from unittest.mock import patch

from cli.utils.config import load, save


@patch("cli.utils.config.config_file")
def test_load_empty_when_no_file(mock_config_file):
    with tempfile.TemporaryDirectory() as tmpdir:
        mock_config_file.return_value = Path(tmpdir) / "config.toml"
        result = load()
        assert result == {}


@patch("cli.utils.config.config_file")
def test_save_and_load_roundtrip(mock_config_file):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "config.toml"
        mock_config_file.return_value = path

        data = {"key": "value", "number": "42"}
        assert save(data) is True

        loaded = load()
        assert loaded["key"] == "value"
        assert loaded["number"] == "42"


@patch("cli.utils.config.config_file")
def test_save_overwrites(mock_config_file):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "config.toml"
        mock_config_file.return_value = path

        save({"old": "data"})
        save({"new": "data"})

        loaded = load()
        assert "old" not in loaded
        assert loaded["new"] == "data"


@patch("cli.utils.config.config_file")
def test_load_returns_empty_on_corrupt_file(mock_config_file):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "config.toml"
        path.write_text("this is not valid toml [[[")
        mock_config_file.return_value = path

        result = load()
        assert result == {}

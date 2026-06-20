from pathlib import Path
from typing import Annotated

import typer
from core.media.decoder import decode
from core.media.merger import generate
from core.media.models import OutputConfig
from loguru import logger
from rich.console import Console

from ..enums import Quality
from ..utils import ffmpeg, printer

console = Console()

QUALITY_SETTINGS = {
    Quality.LOW: {"x": 640, "y": 360, "fps": 24},
    Quality.MEDIUM: {"x": 1280, "y": 720, "fps": 30},
    Quality.HIGH: {"x": 1920, "y": 1080, "fps": 30},
}

OUTPUT_FILENAME = "output.mp4"


def convert(
    input_dir: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            resolve_path=True,
            help="Directory containing the Adobe Connect recording files",
        ),
    ],
    output_dir: Annotated[
        Path | None,
        typer.Option("--output-dir", "-o", help="Directory for generated MP4 file"),
    ] = None,
    quality: Annotated[
        Quality,
        typer.Option(
            "--quality", "-q", help="Video quality preset", case_sensitive=False
        ),
    ] = Quality.MEDIUM,
) -> None:
    if not ffmpeg.detect():
        printer.error(
            "FFmpeg not found. Install it or set FFMPEG_PATH environment variable."
        )
        raise typer.Exit(code=1)

    xml_path = input_dir / "indexstream.xml"
    if not xml_path.exists():
        printer.error(f"No indexstream.xml found in {input_dir}")
        raise typer.Exit(code=1)

    if output_dir is None:
        output_dir = Path("./output")

    settings = QUALITY_SETTINGS[quality]
    resolution = f"{settings['x']}x{settings['y']}"

    config = OutputConfig(
        dir=str(output_dir),
        storage=str(input_dir),
        filename=OUTPUT_FILENAME,
        fps=settings["fps"],
        resolution=resolution,
    )

    _setup_logger()

    printer.info(f"Parsing {xml_path}...")
    media_list, total_duration = decode(str(xml_path))

    if not media_list:
        printer.warning("No media streams found in the recording.")
        raise typer.Exit(code=1)

    printer.info(f"Found {len(media_list)} stream(s), duration: {total_duration:.1f}s")
    printer.info(f"Quality: {quality.value} ({resolution} @ {settings['fps']}fps)")
    printer.info(f"Output: {output_dir / OUTPUT_FILENAME}")

    try:
        generate(media_list, total_duration, config)
        printer.success(f"Conversion complete: {output_dir / OUTPUT_FILENAME}")
    except Exception as e:
        printer.error(f"Conversion failed: {e}")
        raise typer.Exit(code=1) from e


def _setup_logger() -> None:
    logger.remove()
    logger.add(
        lambda msg: console.print(f"  {msg.record['message']}"),
        format="{level.icon} {message}",
        level="INFO",
        filter=lambda record: record["level"].no >= 20,
    )

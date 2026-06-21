from pathlib import Path

import ffmpeg
from loguru import logger

from .models import MediaItem, OutputConfig


def generate(
    media_list: list[MediaItem], total_duration: float, config: OutputConfig
) -> None:
    Path(config.dir).mkdir(parents=True, exist_ok=True)
    output_path = str(Path(config.dir) / config.filename)

    video_streams = [_create_base_video(config.fps, config.resolution, total_duration)]
    audio_streams = [_create_base_audio(total_duration)]

    for item in media_list:
        _process(
            item,
            video_streams,
            audio_streams,
            config.storage,
            config.resolution,
            config.ffprobe_bin,
        )

    _combine(
        video_streams,
        audio_streams,
        output_path,
        total_duration,
        config.ffmpeg_bin,
    )


def _create_base_video(fps: int, resolution_str: str, duration: float) -> ffmpeg.Stream:
    return ffmpeg.input(
        f"color=c=black:s={resolution_str}:r={fps}",
        f="lavfi",
        t=duration,
    )


def _create_base_audio(duration: float) -> ffmpeg.Stream:
    return ffmpeg.input(
        "anullsrc=channel_layout=stereo:sample_rate=44100",
        f="lavfi",
        t=duration,
    )


def _process(
    item: MediaItem,
    video_streams: list[ffmpeg.Stream],
    audio_streams: list[ffmpeg.Stream],
    storage_dir: str,
    resolution_str: str,
    ffprobe_bin: str = "ffprobe",
) -> None:
    file_path = str(Path(storage_dir) / f"{item.name}.flv")

    if not Path(file_path).exists():
        logger.warning(f"File {file_path} doesn't exist")
        return

    start_seconds = item.start / 1000.0

    try:
        probe_data = ffmpeg.probe(file_path, cmd=ffprobe_bin)
        has_video, has_audio = _detect_streams(probe_data)
    except ffmpeg.Error as e:
        logger.warning(f"Failed to probe {file_path}, skipping...")
        logger.debug(f"Probe error: {e}")
        return

    input_node = ffmpeg.input(file_path)

    if has_video:
        _add_video_stream(input_node, video_streams, start_seconds, resolution_str)

    if has_audio:
        _add_audio_stream(input_node, audio_streams, item.start)


def _add_video_stream(
    input_node: ffmpeg.Stream,
    video_streams: list[ffmpeg.Stream],
    start_seconds: float,
    resolution_str: str,
) -> None:
    width, height = resolution_str.split("x")
    video_filter_chain = (
        input_node.video.filter(
            "scale",
            width,
            height,
            force_original_aspect_ratio="increase",
        )
        .filter("crop", width, height)
        .filter("setpts", f"PTS-STARTPTS+{start_seconds}/TB")
    )

    video_streams.append(video_filter_chain)


def _add_audio_stream(
    input_node: ffmpeg.Stream, audio_streams: list[ffmpeg.Stream], start_ms: int
) -> None:
    audio_filter_chain = input_node.audio.filter(
        "adelay", f"{int(start_ms)}|{int(start_ms)}"
    )

    audio_streams.append(audio_filter_chain)


def _detect_streams(probe_data: dict) -> tuple[bool, bool]:
    if not probe_data or "streams" not in probe_data:
        return False, False

    has_video = any(
        stream.get("codec_type") == "video" for stream in probe_data["streams"]
    )
    has_audio = any(
        stream.get("codec_type") == "audio" for stream in probe_data["streams"]
    )

    return has_video, has_audio


def _combine(
    video_streams: list[ffmpeg.Stream],
    audio_streams: list[ffmpeg.Stream],
    output_path: str,
    total_duration: float,
    ffmpeg_bin: str = "ffmpeg",
) -> None:
    final_video = video_streams[0]

    for i in range(1, len(video_streams)):
        final_video = ffmpeg.overlay(final_video, video_streams[i], eof_action="pass")

    if len(audio_streams) == 0:
        logger.error("No audio streams found")
        return

    if len(audio_streams) > 1:
        final_audio = ffmpeg.filter(
            audio_streams, "amix", inputs=len(audio_streams), duration="longest"
        )
    else:
        final_audio = audio_streams[0]

    logger.info("Starting FFmpeg processing (this may take a while)...")
    try:
        (
            ffmpeg.output(
                final_video,
                final_audio,
                output_path,
                vcodec="libx264",
                acodec="aac",
                pix_fmt="yuv420p",
                preset="medium",
                t=total_duration,
            )
            .overwrite_output()
            .run(cmd=ffmpeg_bin, capture_stdout=True, capture_stderr=True)
        )

        logger.success(f"Final video created: {output_path}")
    except ffmpeg.Error as e:
        logger.error(f"FFmpeg Error: {e.stderr.decode()}")
        raise

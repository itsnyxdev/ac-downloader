import os
import xml.etree.ElementTree as Et

import ffmpeg
from loguru import logger


def filter_files(files, start, end, sort=True):
    filtered_files = filter(lambda f: f.startswith(start) and f.endswith(end), files)
    filtered_files = list(filtered_files)

    if sort:
        filtered_files.sort(key=lambda f: f.lower())

    return filtered_files


def convert_media(file: str, output_format: str, output_path="./output/"):
    os.makedirs(output_path, exist_ok=True)

    input_path = "./storage/" + file
    base_name = os.path.splitext(file)[0]
    output_file = output_path + base_name + output_format

    logger.info(f"Converting {file} to {output_format}")
    logger.info(f"Input path: {input_path}")
    logger.info(f"Output path: {output_file}")

    try:
        input_stream = ffmpeg.input(input_path)

        streams = ffmpeg.probe(input_path)

        video_stream = None
        audio_stream = None

        for stream in streams['streams']:
            if stream['codec_type'] == 'video':
                video_stream = input_stream.video
            elif stream['codec_type'] == 'audio':
                audio_stream = input_stream.audio

        logger.debug(f"Video Stream Available: {bool(video_stream)}")
        logger.debug(f"Audio Stream Available: {bool(audio_stream)}")

        if output_format == ".mp4":
            if video_stream and audio_stream:
                processed_stream = ffmpeg.output(video_stream, audio_stream, output_file,
                                                 vcodec="copy", preset="ultrafast", acodec="aac")
            elif video_stream:
                processed_stream = ffmpeg.output(video_stream, output_file, vcodec="libx264", preset="ultrafast", )
            else:
                logger.warning(f"No usable video found in {file} for MP4 conversion.")
                return False

        elif output_format == ".mp3":
            if audio_stream:
                processed_stream = ffmpeg.output(audio_stream, output_file, acodec="libmp3lame")
            else:
                logger.warning(f"No usable audio stream found in {file} for MP3 conversion")
                return False
        elif output_format == ".aac":
            if audio_stream:
                processed_stream = ffmpeg.output(audio_stream, output_file, acodec="aac")
            else:
                logger.warning(f"No usable audio stream found in {file} for AAC conversion")
                return False
        else:
            logger.error(f"Unsupported output format {output_format}")
            return False

        ffmpeg.run(processed_stream, overwrite_output=True)
        logger.success(f"Converted {file} to {output_format} successfully")

        return True

    except ffmpeg.Error as e:
        logger.error(f"FFMPEG error: {e.stderr.decode() if hasattr(e, 'stderr') else str(e)}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred during media conversion: {e}")


def create_videos_streams(video_list: list):
    with open('./storage/streams.txt', 'w') as f:
        for video in video_list:
            abs_path = os.path.abspath(f"./output/{video}")
            f.write(f"file '{abs_path}'\n")


def merge_videos(file_name, streams_dir="./storage/", output_path="./output/"):
    streams_file_path = os.path.join(streams_dir, "streams.txt")

    if not os.path.exists(streams_file_path):
        logger.error(f"Streams file does not exist: {streams_file_path}")
        return

    try:
        merged_video_input = ffmpeg.input(streams_file_path, format="concat", safe=0)
        merged_video_output = ffmpeg.output(merged_video_input, output_path + file_name, c="copy")

        logger.info(f"Merging videos from {streams_file_path} to {output_path + file_name}")

        ffmpeg.run(merged_video_output, overwrite_output=True, capture_stderr=True)
        logger.success(f"Merged {file_name} successfully")
    except ffmpeg.Error as e:
        logger.error(f"FFMPEG error merging videos: {e.stderr.decode()}")
    except Exception as e:
        logger.error(f"An unexpected error merging videos: {e}")


def get_timing(xml_file):
    start_time, end_time = None, None

    try:
        xml = Et.parse(source=f'storage/{xml_file}')
        root = xml.getroot()

        message_elements = [
            msg for msg in root.findall('.//Message')
            if msg.find('Method').text == 'pacingTick'
        ]

        if message_elements:
            first_message = message_elements[0]
            last_message = message_elements[-1]

            start_time = first_message.find('Number').text.strip()
            end_time = last_message.find('Number').text.strip()

            logger.info(f"Start time: {start_time}")
            logger.info(f"End time: {end_time}")

    except Et.ParseError as e:
        logger.error(e)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

    return start_time, end_time


def main():
    logger.add('log.txt')

    storage_files = os.listdir("./storage")

    screen_shares = filter_files(storage_files, "screenshare", ".flv")
    sounds_flv = filter_files(storage_files, "cameraVoip", ".flv")
    sounds_xml = filter_files(storage_files, "cameraVoip", ".xml")

    converted_videos = []

    for v in screen_shares:
        logger.info(f"Processing {v}")
        if convert_media(v, output_format=".mp4"):
            converted_videos.append(os.path.splitext(v)[0] + ".mp4")

    if converted_videos:
        create_videos_streams(converted_videos)
        merge_videos('screenshare.mp4')
    else:
        logger.warning("No videos to merge!")

    for sound in sounds_flv:
        logger.info(f"Processing {sound}")
        if convert_media(sound, output_format=".mp3"):
            logger.info(f"Converted {sound}")
        else:
            logger.error(f"Convertion failed for {sound}")


if __name__ == '__main__':
    main()

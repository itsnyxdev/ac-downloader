import xml.etree.ElementTree as ET
import os
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


def decode_xml(xml_path, media_folder="input_path"):
    if not os.path.exists(xml_path):
        print(f"Error: {xml_path} not found.")
        return

    xml = ET.parse(xml_path)
    root = xml.getroot()
    streams = {}
    media = []
    max_duration_ms = 0

    for message in root.findall('Message'):
        msg_time = int(message.get('time', 0))
        if msg_time > max_duration_ms: 
            max_duration_ms = msg_time
        
        event_type = ""
        for s in message.findall('String'):
            if s.text in ["streamAdded", "streamRemoved"]:
                event_type = s.text
                break
        
        if not event_type: 
            continue

        array = message.find('Array')
        if array is not None:
            obj = array.find('Object')
            if obj is not None:
                s_id = obj.findtext('streamId')
                s_name = obj.findtext('streamName', '').lstrip('/')
                s_start = obj.findtext('startTime')
                s_type = obj.findtext('streamType', '').lower()

                if event_type == "streamAdded":
                    streams[s_id] = {
                        "name": s_name,
                        "type": s_type,
                        "start": int(s_start) if s_start else msg_time
                    }
                elif event_type == "streamRemoved":
                    if s_id in streams:
                        data = streams.pop(s_id)
                        data["end"] = msg_time
                        media.append(data)

    for s_id, data in streams.items():
        data["end"] = max_duration_ms
        media.append(data)

    media.sort(key=lambda x: x['start'])
    return media


def main():
    logger.add('log.txt')

    # Path to the XML recording metadata (adjust if needed)
    XML_PATH = "./storage/indexstream.xml"

    media_list = decode_xml(XML_PATH)
    if not media_list:
        logger.error("No media entries found in XML or XML file missing. Exiting.")
        return

    converted_videos = []   # list of output .mp4 filenames for merging

    for media in media_list:
        base_name = media['name']           
        media_type = media['type']
        file_name = f"{base_name}.flv"

        # Determine output format based on stream type
        if "screenshare" in media_type:
            output_format = ".mp4"
        elif "cameravoip" in media_type:
            output_format = ".mp3"
        else:
            logger.warning(f"Unknown stream type '{media_type}' for {file_name}, skipping.")
            continue

        # Check that the source file actually exists in ./storage/
        source_path = os.path.join("./storage", file_name)
        if not os.path.exists(source_path):
            logger.warning(f"Source file {source_path} not found, skipping.")
            continue

        if convert_media(file_name , output_format=output_format):
            if output_format == ".mp4":
                converted_videos.append(os.path.splitext(file_name)[0] + ".mp4")
        else:
            logger.error(f"Conversion failed for {file_name}")

    # Merge all successfully converted video files
    if converted_videos:
        create_videos_streams(converted_videos)
        merge_videos('screenshare.mp4')
    else:
        logger.warning("No videos converted – skipping merge.")


if __name__ == '__main__':
    main()
import xml.etree.ElementTree as ET
import os
import ffmpeg
from loguru import logger

# Configuration
OUTPUT_RES = "1280x720" 
FPS = 30
STORAGE_DIR = "./storage"
OUTPUT_DIR = "./output"

def decode_xml(xml_path):
    if not os.path.exists(xml_path):
        logger.error(f"Error: {xml_path} not found.")
        return None, 0

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
                        "start_ms": int(s_start) if s_start else msg_time
                    }
                elif event_type == "streamRemoved":
                    if s_id in streams:
                        data = streams.pop(s_id)
                        data["end_ms"] = msg_time
                        media.append(data)

    for s_id, data in streams.items():
        data["end_ms"] = max_duration_ms
        media.append(data)

    media.sort(key=lambda x: x['start_ms'])
    return media, max_duration_ms / 1000.0 

def generate_video(media_list, total_duration, output_filename="final_session.mp4"):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    # 1. Start with a Base: Black video and Silent audio
    base_v = ffmpeg.input(f'color=c=black:s={OUTPUT_RES}:r={FPS}', f='lavfi', t=total_duration)
    base_a = ffmpeg.input('anullsrc=channel_layout=stereo:sample_rate=44100', f='lavfi', t=total_duration)

    video_streams = [base_v]
    audio_streams = [base_a]


    for item in media_list:
        file_path = os.path.join(STORAGE_DIR, f"{item['name']}.flv")
        if not os.path.exists(file_path):
            logger.warning(f"File missing: {file_path}")
            continue

        start_sec = item['start_ms'] / 1000.0
        
        # Probe file to see what it contains
        try:
            probe = ffmpeg.probe(file_path)
            has_video = any(s['codec_type'] == 'video' for s in probe['streams'])
            has_audio = any(s['codec_type'] == 'audio' for s in probe['streams'])
        except ffmpeg.Error:
            continue

        input_node = ffmpeg.input(file_path)

        if has_video:
            v = (
                input_node.video.filter('scale', OUTPUT_RES.split('x')[0], OUTPUT_RES.split('x')[1], force_original_aspect_ratio="increase").filter('crop', OUTPUT_RES.split('x')[0], OUTPUT_RES.split('x')[1]).filter('setpts', f'PTS-STARTPTS+{start_sec}/TB')
            )
            video_streams.append(v)

        if has_audio:
            a = (
                input_node.audio.filter('adelay', f"{int(item['start_ms'])}|{int(item['start_ms'])}")
            )
            audio_streams.append(a)

    all_vid = video_streams[0]
    for i in range(1, len(video_streams)):
        all_vid = ffmpeg.overlay(all_vid, video_streams[i], eof_action='pass')

    if len(audio_streams) > 1:
        all_aud = ffmpeg.filter(audio_streams, 'amix', inputs=len(audio_streams), duration='longest')
    else:
        all_aud = audio_streams[0]

    # 4. Output
    logger.info("Starting FFmpeg processing (this may take a while)...")
    try:
        (
            ffmpeg.output(all_vid, all_aud, output_path, vcodec='libx264', acodec='aac', pix_fmt='yuv420p', preset='medium',t=total_duration).overwrite_output().run(capture_stdout=True, capture_stderr=True)
        )
        logger.success(f"Final video created: {output_path}")
    except ffmpeg.Error as e:
        logger.error(f"FFmpeg Error: {e.stderr.decode()}")

def main():
    logger.add('log.txt')
    XML_PATH = os.path.join(STORAGE_DIR, "indexstream.xml")

    media_list, total_duration = decode_xml(XML_PATH)
    
    if not media_list or total_duration == 0:
        logger.error("No media data found. Exiting.")
        return

    generate_video(media_list, total_duration)

if __name__ == '__main__':
    main()
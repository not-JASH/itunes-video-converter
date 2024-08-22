import os
import shutil
from pymediainfo import MediaInfo

def get_video_info(file_path):
    media_info = MediaInfo.parse(file_path)
    audio_codec = None
    video_codec = None
    for track in media_info.tracks:
        if track.track_type == 'Audio':
            audio_codec = track.codec_id
        elif track.track_type == 'Video':
            video_codec = track.codec_id
    return audio_codec, video_codec

def move_files_with_format_errors(root_dir, dest_dir):
    movie_extensions = ['.mp4', '.avi', '.mkv', '.mov']  # Add more extensions as needed
    for root, dirs, files in os.walk(root_dir, topdown=True):
        dirs[:] = [d for d in dirs if d != 'format error']
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.splitext(file_path)[1].lower() in movie_extensions:
                audio_codec, video_codec = get_video_info(file_path)
                if audio_codec != 'mp4a-40-2' or video_codec != 'avc1':
                    relative_path = os.path.relpath(file_path, root_dir)
                    dest_path = os.path.join(dest_dir, relative_path)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.move(file_path, dest_path)

if __name__ == '__main__':
    root_directory = '.'  # You can change this to the desired root directory
    error_directory = os.path.join(root_directory, 'format error')
    move_files_with_format_errors(root_directory, error_directory)

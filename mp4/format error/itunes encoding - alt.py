import os
import shutil
import subprocess
from pymediainfo import MediaInfo

def encode_video(input_path, output_path):
    audio_codec, video_codec = get_video_info(input_path)
    print(video_codec, input_path)

    if video_codec == "hev1":
        #this command encodes 10 bit video
        cmd = f'ffmpeg -i "{input_path}" -c:v copy -qscale:v 4 -c:a aac  -b:a 128k "{output_path}"'
        
    else:
        cmd = f'ffmpeg -i "{input_path}" -c:v copy -qscale:v 4 -c:a aac  -b:a 128k "{output_path}"'
        #print("not sure which codec to use, skipping...")
        #cmd = f'ffmpeg -i "{input_path}" -c:v h264_nvenc -preset fast -c:a aac -b:a 128k "{output_path}"'

    subprocess.run(cmd, check=True)
    
def create_encoded_folder(base_dir):
    encoded_dir = os.path.join(base_dir, 'encoded')
    os.makedirs(encoded_dir, exist_ok=True)
    return encoded_dir

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

def main():
    base_dir = os.getcwd()
    encoded_dir = create_encoded_folder(base_dir)

    for root, dirs, files in os.walk(base_dir):
        if root == encoded_dir:
            continue

        relative_path = os.path.relpath(root, base_dir)
        encoded_sub_dir = os.path.join(encoded_dir, relative_path)

        os.makedirs(encoded_sub_dir, exist_ok=True)

        for file in files:
            if file.lower().endswith(('.avi', '.mp4', '.mkv')):
                input_path = os.path.join(root, file)
                output_path = os.path.join(encoded_sub_dir, file)
                encode_video(input_path, output_path)

    print("Encoding completed successfully.")

if __name__ == "__main__":
    main()

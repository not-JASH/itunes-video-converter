import tkinter as tk
from tkinter import filedialog
import subprocess
import os

def select_video_file():
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        video_file = filedialog.askopenfilename(title="Select a video file", filetypes=[("Video files", "*.mp4 *.mkv *.avi *.mov")])
        return video_file
    finally:
        root.destroy()

def select_subtitle_files():
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        subtitle_files = filedialog.askopenfilenames(title="Select subtitle files", filetypes=[("Subtitle files", "*.srt *.ass *.vtt")])
        return subtitle_files
    finally:
        root.destroy()

def run_ffmpeg_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"FFmpeg encountered an error:\n{result.stderr}")
            return False
        return True
    except FileNotFoundError:
        print("FFmpeg is not installed or not found in your system's PATH.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while running FFmpeg: {e}")
        return False

def extract_language_from_filename(filename):
    """Extract language from the subtitle filename."""
    # Assuming filename is in format like 'movie.en.srt' or 'movie.eng.srt'
    # You can adjust this logic based on how your subtitles are named
    base = os.path.basename(filename)
    name, ext = os.path.splitext(base)
    parts = name.split('.')
    if len(parts) > 1:
        return parts[-1]  # Assuming last part is the language code
    return "unknown"

def main():
    # Select video file
    video_file = select_video_file()
    if not video_file:
        print("No video file selected. Exiting.")
        return

    # Extract the extension from the selected video file
    video_extension = os.path.splitext(video_file)[1]

    # Select subtitle files
    subtitle_files = select_subtitle_files()
    if not subtitle_files:
        print("No subtitle files selected. Exiting.")
        return

    # Ask for output file name without extension
    output_file_name = input("Enter the output file name (without extension): ")

    # Append the original video file extension to the new output file name
    output_file = output_file_name + video_extension

    # Prepare the ffmpeg command
    ffmpeg_cmd = ["ffmpeg", "-v", "info", "-i", video_file]

    # Add each subtitle file as a separate input
    for subtitle in subtitle_files:
        ffmpeg_cmd.extend(["-i", subtitle])

    # Set video, audio, and subtitle codecs
    ffmpeg_cmd.extend([
        '-c:v', 'h264_nvenc', '-preset', 'p4',
        '-c:a', 'aac', '-b:a', '128k',
        '-c:s', 'mov_text'
    ])

    # Map streams correctly
    ffmpeg_cmd.extend([
        "-map", "0:v",  # Map the video stream
        "-map", "0:a",  # Map the audio stream
    ])

    # Add a map for each subtitle file and set metadata for language
    for i, subtitle in enumerate(subtitle_files, start=1):
        language = extract_language_from_filename(subtitle)
        ffmpeg_cmd.extend([
            "-map", f"{i}:s",  # Map the subtitle stream
            f"-metadata:s:s:{i-1}", f"language={language}"  # Set the subtitle language
        ])

    # Specify the output file format and the final output file
    ffmpeg_cmd.append(output_file)

    # Run the command
    print(f"Running command: {' '.join(ffmpeg_cmd)}")
    if run_ffmpeg_command(ffmpeg_cmd):
        print(f"Video successfully saved to {output_file}")
    else:
        print("Failed to process the video.")

if __name__ == "__main__":
    main()

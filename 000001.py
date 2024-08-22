import os
import shutil
import subprocess
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_to_mp4(input_file, output_file):
    try:
        # Run ffmpeg command
        process = subprocess.Popen(
            [
                'ffmpeg', '-y', '-i', input_file,
                '-c:v', 'h264_nvenc', '-preset', 'p4',
                '-c:a', 'aac', '-b:a', '128k',
                '-c:s', 'mov_text',
                '-ac','2',
                '-map', '0:v', 
                '-map', '0:a?', 
                '-map', '0:s?',
                #'-metadata:s:a:0', 'language=eng',  
                #'-metadata:s:s:0', 'language=eng',  
                '-movflags', '+faststart',
                output_file
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Read and log progress from stderr
        for line in process.stderr:
            logging.info(line.strip())
        
        process.wait()  # Wait for the process to complete

        if process.returncode == 0:
            logging.info(f"Converted {input_file} to {output_file}")
        else:
            logging.error(f"Error converting {input_file}: Process returned non-zero exit status {process.returncode}")

    except FileNotFoundError:
        logging.error("ffmpeg not found. Please ensure ffmpeg is installed and available in your PATH.")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")

def create_mp4_directory_structure(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if 'mp4' in dirnames:
            dirnames.remove('mp4')

        if 'subtitles' in dirnames:
            dirnames.remove('subtitles')

        mp4_dir = os.path.join(root_dir, 'mp4', os.path.relpath(dirpath, root_dir))
        try:
            os.makedirs(mp4_dir, exist_ok=True)
        except PermissionError:
            logging.error(f"Permission denied: Unable to create directory {mp4_dir}")
        except Exception as e:
            logging.error(f"Unexpected error occurred while creating directory {mp4_dir}: {e}")

def convert_videos_to_mp4(root_dir):
    mp4_root_dir = os.path.join(root_dir, 'mp4')
    try:
        os.makedirs(mp4_root_dir, exist_ok=True)
    except PermissionError:
        logging.error(f"Permission denied: Unable to create directory {mp4_root_dir}")
        return
    except Exception as e:
        logging.error(f"Unexpected error occurred while creating directory {mp4_root_dir}: {e}")
        return

    create_mp4_directory_structure(root_dir)

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if 'mp4' in dirnames:
            dirnames.remove('mp4')

        if 'subtitles' in dirnames:
            dirnames.remove('subtitles')

        for filename in filenames:
            if filename.lower().endswith(('.avi', '.mkv', '.mov', '.flv', '.wmv', '.mpg', '.mpeg')):
                input_file = os.path.join(dirpath, filename)
                output_file = os.path.join(mp4_root_dir, os.path.relpath(input_file, root_dir).replace(os.path.splitext(filename)[1], '.mp4'))
                convert_to_mp4(input_file, output_file)
            elif filename.lower().endswith('.mp4'):
                input_file = os.path.join(dirpath, filename)
                output_file = os.path.join(mp4_root_dir, os.path.relpath(input_file, root_dir).replace(os.path.splitext(filename)[1], '.mp4'))
                try:
                    shutil.copyfile(input_file, output_file)
                    logging.info(f"Copied {input_file} to {output_file}")
                except PermissionError:
                    logging.error(f"Permission denied: Unable to copy file {input_file}")
                except FileNotFoundError:
                    logging.error(f"File not found: {input_file}")
                except Exception as e:
                    logging.error(f"Unexpected error occurred while copying file {input_file}: {e}")

if __name__ == "__main__":
    root_directory = os.getcwd()  # Use the current working directory
    convert_videos_to_mp4(root_directory)

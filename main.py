import subprocess
from pathlib import Path
from ffmpeg_commands import build_command
from youtube_video_downloader import download_youtube_video
from clean_path_generator import clean_path_generator
from choose_command import choose_command


# Specify the folder to save downloads

youtube_url = "https://www.youtube.com/watch?v=5vYipYSDhtQ"
base_path = Path("E:/Python_Rcap")

yt_video_folder = base_path / "yt_videos"
yt_video_folder.mkdir(parents=True, exist_ok=True)
# yt-dlp --download-sections "*00:02:30-00:05:10" https://www.youtube.com/watch?v=VIDEO_ID

def main():

    download_youtube_video(youtube_url, yt_video_folder)
    new_path = clean_path_generator(yt_video_folder)

    if new_path is not None:
        # Convert to Path object for easy manipulation
        input_path = Path(new_path)

        output_Folder = base_path / "download"
        output_Folder.mkdir(parents=True, exist_ok=True)
        output_path = output_Folder / f"pro_{input_path.stem}.mp4"

        command = choose_command(input_path, output_path)

        try:
            print(f"Processing {input_path.name}...")
            subprocess.run(command, check=True)
            print(f"Success! Saved to: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e}")
    else:
        print("File cleaning failed or user cancelled.")

if __name__ == "__main__":
    main()
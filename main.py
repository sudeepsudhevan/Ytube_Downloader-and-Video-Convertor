import subprocess
from pathlib import Path
from youtube_video_downloader import download_youtube_video
from clean_path_generator import clean_path_generator
from choose_command import choose_command

# Specify the folder to save downloads

youtube_url = "https://www.youtube.com/watch?v=5vYipYSDhtQ"
base_path = Path("E:/Python_Rcap")

yt_video_folder = base_path / "yt_videos"
yt_video_folder.mkdir(parents=True, exist_ok=True)

local_video_folder = base_path / "local_videos"
local_video_folder.mkdir(parents=True, exist_ok=True)

def main():
    user_input = input("Do you want to download a YouTube video? Y/N: ")

    if user_input.lower() == 'y':
        download_youtube_video(youtube_url, yt_video_folder)
        new_path = clean_path_generator(yt_video_folder)
    else:
        input("Please place your local video files in the 'local_videos' folder and press Enter to continue...")
        new_path = clean_path_generator(local_video_folder)

    if new_path is not None:
        # Convert to Path object for easy manipulation
        input_path = Path(new_path)

        output_Folder = base_path / "download"
        output_Folder.mkdir(parents=True, exist_ok=True)
        output_path = output_Folder / f"pro_{input_path.stem}.mp4"

        # # Do you want to quit before ffmpeg processing?
        # quit_after_cleaning = input("Do you want to quit before ffmpeg processing Y/N: ")
        # if quit_after_cleaning.lower() == 'y':
        #     print("Exiting as per user request.")
        #     return

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
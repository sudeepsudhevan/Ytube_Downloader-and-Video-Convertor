import subprocess
from remove_file_from_folder import remove_video_files_from_folder
from pathlib import Path

def download_youtube_video(youtube_url: str, yt_video_folder: Path) -> None:
    '''
    Downloads a YouTube video to the specified folder.
    '''
    remove_video_files_from_folder(yt_video_folder)

    subprocess.run(
        f"yt-dlp -f bestvideo+bestaudio -o {yt_video_folder}/%(title)s {youtube_url}",
        shell=True,
    )
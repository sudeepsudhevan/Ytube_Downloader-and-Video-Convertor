from pathlib import Path
import mimetypes

# Remove all video files from the folder functionality
def remove_video_files_from_folder(folder: Path) -> None:
    '''
    Removes all video files from the specified folder.
    '''
    for file in folder.iterdir():
        if file.is_file():
            mime, _ = mimetypes.guess_type(file)
            if mime and mime.startswith("video"):
                file.unlink()
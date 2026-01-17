import re
from pathlib import Path
from has_video_stream import has_video_stream

def clean_path_generator(folder_path: Path) -> Path | None:
    """
    Checks the first file in a folder, cleans its name,
    and ensures it is a valid video file using ffprobe.
    """
    folder = Path(folder_path)

    try:
        # 1. Get files and handle empty folder case
        files = [f for f in folder.iterdir() if f.is_file()]
        if not files:
            print(f"No files found in '{folder_path}'.")
            return None

        # Select the file to clean
        for i, f in enumerate(files, start=1):
            print(f"{i}. {f.name}")

        if len(files) == 1:
            index = 0
        else:
            # Display the files with numbers so the user knows what to pick
            for i, file in enumerate(files, 1):
                print(f"{i}. {file.name}")
                
            user_input = int(input(f"Enter the file number to process (1-{len(files)}): "))
            
            # Adjust for 0-based indexing
            index = user_input - 1
        old_file = files[index]

        # 2. Separate name and extension
        file_stem = old_file.stem
        file_ext = old_file.suffix or ".webm"

        # 3. Clean filename
        clean_name = re.sub(r"[_\[\]\(\)]", "", file_stem).replace(" ", "_")

        # 4. 🔥 AUTHORITATIVE CHECK (FFprobe)
        if not has_video_stream(old_file):
            print(f"Skipping '{old_file.name}': No video stream detected.")
            return None

        # 5. Rename safely
        new_file_path = folder / f"{clean_name}{file_ext}"

        if new_file_path != old_file:
            old_file.rename(new_file_path)

        return new_file_path

    except FileNotFoundError:
        print(f"Path '{folder_path}' does not exist.")
    except PermissionError:
        print(f"Permission denied for '{folder_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

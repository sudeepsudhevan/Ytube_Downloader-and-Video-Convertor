from ffmpeg_commands import build_command, FFMPEG_COMMANDS
from pathlib import Path

def choose_command(input_path: Path, output_path: Path) -> list[str]:
    command_list = list(FFMPEG_COMMANDS.keys())

    # 1. Display Menu with Descriptions
    print("\n--- FFmpeg Command Menu ---")
    for i, cmd_key in enumerate(command_list, start=1):
        desc = FFMPEG_COMMANDS[cmd_key]["description"]
        print(f"{i}. {cmd_key.replace('_', ' ').title():<20} | {desc}")

    # 2. Get Selection
    try:
        choice = int(input("\nSelect a command by number: ")) - 1
        if not (0 <= choice < len(command_list)):
            raise ValueError
        selected_key = command_list[choice]
    except (ValueError, IndexError):
        print("❌ Invalid selection.")
        return []

    # 3. Setup default arguments
    kwargs = {
        "input": str(input_path),
        "output": str(output_path)
    }

    # 4. Handle Specific Parameters based on the selected command key
    if selected_key in ["trim_reencode", "trim_copy"]:
        kwargs["start"] = input("Enter start time (HH:MM:SS): ")
        kwargs["end"] = input("Enter end time (HH:MM:SS): ")

    elif selected_key == "split_segments":
        kwargs["duration"] = input("Enter segment duration (seconds): ")
        # Segments need a pattern like 'output_001.mp4'
        kwargs["output_pattern"] = str(output_path.parent / f"{output_path.stem}_%03d{output_path.suffix}")

    elif selected_key == "resize_video":
        kwargs["width"] = input("Enter width (e.g. 1280): ")
        kwargs["height"] = input("Enter height (e.g. 720): ")

    # 5. Build the command
    return build_command(selected_key, **kwargs)
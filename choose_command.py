from ffmpeg_commands import build_command, FFMPEG_COMMANDS
from pathlib import Path

def choose_command(input_path: Path, output_path: Path) -> list[str]:
    command_list = list(FFMPEG_COMMANDS.keys())

    # Numbered list display
    for i, cmd in enumerate(command_list, start=1):
        print(f"{i}. {cmd}")

    choice = int(input("Select a command by number: ")) - 1

    command = build_command(
            command_list[choice], 
            input=str(input_path), 
            output=str(output_path)
        )

    return command

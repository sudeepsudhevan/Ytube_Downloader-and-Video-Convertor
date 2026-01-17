from ffmpeg_commands import build_command, FFMPEG_COMMANDS
from pathlib import Path

def choose_command(input_path: Path, output_path: Path) -> list[str]:
    command_list = list(FFMPEG_COMMANDS.keys())

    # Numbered list display
    for i, cmd in enumerate(command_list, start=1):
        print(f"{i}. {cmd}")

    choice = int(input("Select a command by number: ")) - 1

    if choice < 0 or choice >= len(command_list):
        raise ValueError("Invalid command selection.")
    elif choice == 1 or choice == 2:
        start = input("Enter start time (HH:MM:SS): ")
        end = input("Enter end time (HH:MM:SS): ")
        return build_command(
            command_list[choice], 
            input=str(input_path), 
            output=str(output_path),
            start=start,
            end=end
        )
    elif choice == 0 or choice == 4 or choice == 5 or choice == 6 or choice == 7 or choice == 8 or choice == 10:
        return build_command(
            command_list[choice], 
            input=str(input_path), 
            output=str(output_path)
        )
    
    elif choice == 3:
        duration = input("Enter segment duration in seconds: ")
        return build_command(
            command_list[choice], 
            input=str(input_path), 
            output=str(output_path),
            duration=duration
        )
    
    elif choice == 9:
        width = input("Enter desired width (e.g., 1280): ")
        height = input("Enter desired height (e.g., 720): ")
        return build_command(
            command_list[choice], 
            input=str(input_path), 
            output=str(output_path),
            width=width,
            height=height
        )
        
    else:
        return build_command(
            command_list[choice], 
            input=str(input_path), 
            output=str(output_path)
        )


from ffmpeg_commands import build_command, FFMPEG_COMMANDS

command_list = list(FFMPEG_COMMANDS.keys())

# Numbered list display
for i, cmd in enumerate(command_list, start=1):
    print(f"{i}. {cmd}")

choice = int(input("Select a command by number: ")) - 1

print(command_list[choice])
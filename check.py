
import os
import json


def save_new_profile(profile_name: str, command_list: list, description: str, db_path="ffmpeg_db.json") -> None:
    data = {}
    if os.path.exists(db_path):
        with open(db_path, "r") as f:
            data = json.load(f)
            
    data[profile_name] = {"command": command_list, "description": description}
    
    with open(db_path, "w") as f:
        json.dump(data, f, indent=4)

profile_name = input("Enter a name for the new FFmpeg profile: ")
command_input = input("Enter the FFmpeg command as a space-separated string: ")
command_list = command_input.split()
description = input("Enter a brief description of the profile: ")
save_new_profile(profile_name, command_list, description)
print(f"Profile '{profile_name}' saved successfully.")
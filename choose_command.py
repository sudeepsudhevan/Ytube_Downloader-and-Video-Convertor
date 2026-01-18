from pathlib import Path
from ffmpeg_commands import build_command, get_all_commands 

def choose_command(input_path: Path, output_path: Path) -> list[str]:
    # 1. Get the merged dictionary (The "Single Source of Truth")
    all_commands = get_all_commands()
    command_keys = list(all_commands.keys())

    # 2. Display Menu
    print("\n--- FFmpeg Command Menu ---")
    for i, key in enumerate(command_keys, start=1):
        desc = all_commands[key].get("description", "No description")
        display_name = key.replace("_", " ").title()
        print(f"{i}. {display_name:<25} | {desc}")

    # 3. Get Selection (with loop for better UX)
    selected_key = None
    while not selected_key:
        try:
            choice = int(input("\nSelect a command by number: ")) - 1
            if 0 <= choice < len(command_keys):
                selected_key = command_keys[choice]
            else:
                print("❌ Out of range. Try again.")
        except ValueError:
            print("❌ Please enter a valid number.")

    # 4. Setup arguments
    kwargs = {"input": str(input_path), "output": str(output_path)}

    # 5. Dynamic Parameter Handling
    cmd_template = all_commands[selected_key]["command"]
    cmd_str = " ".join(cmd_template)

    # Check for specific known placeholders
    if "{start}" in cmd_str: kwargs["start"] = input("Enter start time (HH:MM:SS): ")
    if "{end}" in cmd_str: kwargs["end"] = input("Enter end time (HH:MM:SS): ")
    if "{duration}" in cmd_str: kwargs["duration"] = input("Enter segment duration (seconds): ")
    if "{width}" in cmd_str: kwargs["width"] = input("Enter width: ")
    if "{height}" in cmd_str: kwargs["height"] = input("Enter height: ")

    # Handle segment patterns
    if "{output_pattern}" in cmd_str:
        kwargs["output_pattern"] = str(
            output_path.parent / f"{output_path.stem}_%03d{output_path.suffix}"
        )

    if "{factor}" in cmd_str:
        print("\nSlow Motion Factor (e.g., 2.0 = 2x slower, 4.0 = 4x slower)")
        kwargs["factor"] = input("Enter slow-mo factor: ") or "2.0"

    # --- 6. Final Build ---
    # build_command also calls get_all_commands internally, ensuring consistency
    return build_command(selected_key, **kwargs)
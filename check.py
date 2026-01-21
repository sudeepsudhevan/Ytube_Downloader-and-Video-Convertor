import subprocess
import os
import re

# Whitelist of allowed command templates
ALLOWED_COMMANDS = {
    "copy_stream": {
        "command": [
            "ffmpeg",
            "-y",
            "-protocol_whitelist", "file",  # FIX: Prevent SSRF/LFI attacks
            "-i", "{input}",
            "-c", "copy",
            "{output}"
        ],
        "description": "Copy video without re-encoding"
    },
    "h264_convert": {
        "command": [
            "ffmpeg",
            "-y",
            "-protocol_whitelist", "file",  # FIX: Prevent SSRF/LFI attacks
            "-hwaccel", "cuda",
            "-i", "{input}",
            "-c:v", "h264_nvenc",
            "-preset", "p4",
            "-c:a", "aac",
            "{output}"
        ],
        "description": "Convert to H.264"
    }
}

# Configuration
ALLOWED_INPUT_DIRS = [
    "E:\\Python_Rcap\\yt_videos",
    "E:\\Python_Rcap\\local_videos"
]
ALLOWED_OUTPUT_DIR = "E:\\Python_Rcap\\download"

def validate_path(file_path, allowed_dirs):
    """
    FIX: Path Traversal - Validate path is within allowed directories.
    Prevents attackers from writing to system files.
    """
    abs_path = os.path.abspath(file_path)
    
    # Check if path is within allowed directories
    for allowed_dir in allowed_dirs:
        if abs_path.startswith(os.path.abspath(allowed_dir)):
            return True
    
    return False

def is_valid_filename(filename):
    """
    FIX: Format Crash - Prevent dangerous characters in filenames.
    Prevents FFmpeg filter injection.
    """
    # Allow only safe characters: alphanumeric, dash, underscore, dot
    if re.match(r'^[\w\-\.]+$', os.path.basename(filename)):
        return True
    return False

def execute_safe_command(template_name, input_file, output_file):
    """
    Execute a whitelisted command with validated inputs.
    
    Security Fixes:
    - Shell Injection: Uses list format with shell=False
    - Path Traversal: Validates paths against whitelist
    - SSRF/LFI: Uses -protocol_whitelist to disable network/file access
    - Format Crash: Validates filename characters
    """
    
    # 1. Check if command is allowed (FIX: Shell Injection)
    if template_name not in ALLOWED_COMMANDS:
        print(f"❌ Command '{template_name}' not allowed!")
        return False
    
    # 2. Validate input file exists and is in allowed directory
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        return False
    
    if not validate_path(input_file, ALLOWED_INPUT_DIRS):
        print(f"❌ Input file must be in: {', '.join(ALLOWED_INPUT_DIRS)}")
        return False
    
    # 3. Validate output path is safe (FIX: Path Traversal)
    if not validate_path(output_file, [ALLOWED_OUTPUT_DIR]):
        print(f"❌ Output file must be in: {ALLOWED_OUTPUT_DIR}")
        return False
    
    # 4. Validate output filename (FIX: Format Crash)
    if not is_valid_filename(output_file):
        print(f"❌ Invalid filename: contains dangerous characters!")
        return False
    
    # 5. Build command with validated substitution (FIX: Shell Injection - list format)
    template = ALLOWED_COMMANDS[template_name]["command"]
    command = [
        arg.replace("{input}", input_file)
           .replace("{output}", output_file)
        for arg in template
    ]
    
    # 6. Execute safely with shell=False (FIX: Shell Injection)
    print(f"✅ Running: {' '.join(command)}")
    try:
        subprocess.run(command, shell=False, check=True)
        print("✅ Command executed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        return False

# Usage:
execute_safe_command(
    "h264_convert",
    "E:\\Python_Rcap\\yt_videos\\Strongest_10_Year_Old_Girl_｜_Just_For_Laughs_Gags.webm",
    "E:\\Python_Rcap\\download\\output.mp4"
)
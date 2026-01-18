"""
ffmpeg_commands.py
High-quality FFmpeg command templates for audio & video processing.

Usage:
    from ffmpeg_commands import FFMPEG_COMMANDS
"""

import json
import os

FFMPEG_COMMANDS = {

    # =========================
    # 🎯 BASELINE (BEST QUALITY) No. 0
    # =========================
    "base_best_quality": {
        "command": [
            "ffmpeg",
            "-y",
            "-i", "{input}",
            "-map", "0:v:0",
            "-map", "0:a:0?",
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-profile:v", "high",
            "-level", "4.1",
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            "{output}"
        ],
        "description": "Visually lossless video + high quality AAC audio"
    },

    # =========================
    # ✂️ TRIMMING No. 1, 2
    # =========================
    "trim_reencode": {
        "command": [
            "ffmpeg",
            "-y",
            "-ss", "{start}",
            "-to", "{end}",
            "-i", "{input}",
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "18",
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            "{output}"
        ],
        "description": "Frame-accurate trimming with re-encoding"
    },

    "trim_copy": {
        "command": [
            "ffmpeg",
            "-y",
            "-ss", "{start}",
            "-to", "{end}",
            "-i", "{input}",
            "-c", "copy",
            "{output}"
        ],
        "description": "Fast trim without quality loss (keyframe based)"
    },

    # =========================
    # ✂️ SPLITTING No. 3
    # =========================
    "split_segments": {
        "command": [
            "ffmpeg",
            "-y",
            "-i", "{input}",
            "-map", "0",
            "-c", "copy",
            "-f", "segment",
            "-segment_time", "{duration}",
            "-reset_timestamps", "1",
            "{output_pattern}"
        ],
        "description": "Split video into equal-length segments"
    },

    # =========================
    # 📦 COMPRESSION N0. 4, 5
    # =========================
    "compress_high_quality": {
        "command": [
            "ffmpeg",
            "-y",
            "-i", "{input}",
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "160k",
            "-movflags", "+faststart",
            "{output}"
        ],
        "description": "Balanced compression (YouTube-grade quality)"
    },

    "compress_ultra": {
        "command": [
            "ffmpeg",
            "-y",
            "-i", "{input}",
            "-c:v", "libx265",
            "-preset", "slow",
            "-crf", "28",
            "-c:a", "aac",
            "-b:a", "128k",
            "{output}"
        ],
        "description": "Maximum compression using H.265"
    },

    # =========================
    # 🎧 AUDIO EXTRACTION No. 6, 7
    # =========================
    "extract_audio_wav": {
        "command": [
            "ffmpeg",
            "-y",
            "-i", "{input}",
            "-vn",
            "-c:a", "pcm_s16le",
            "{output}"
        ],
        "description": "Extract lossless WAV audio"
    },

    "extract_audio_aac": {
        "command": [
            "ffmpeg",
            "-y",
            "-i", "{input}",
            "-vn",
            "-c:a", "aac",
            "-b:a", "192k",
            "{output}"
        ],
        "description": "Extract high-quality AAC audio"
    },

    # =========================
    # 🎥 VIDEO EXTRACTION No. 8
    # =========================
    "extract_video_only": {
        "command": [
            "ffmpeg",
            "-y",
            "-i", "{input}",
            "-an",
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "18",
            "{output}"
        ],
        "description": "Extract video stream only"
    },

    # =========================
    # 📐 RESIZE / SCALE No.9
    # =========================
    "resize_video": {
        "command": [
            "ffmpeg",
            "-y",
            "-i", "{input}",
            "-vf", "scale={width}:{height}:flags=lanczos",
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "18",
            "-c:a", "aac",
            "-b:a", "192k",
            "{output}"
        ],
        "description": "Resize video using high-quality Lanczos scaling"
    },

    # =========================
    # 🔁 REMUX (NO RE-ENCODE) No. 10
    # =========================
    "remux_copy": {
        "command": [
            "ffmpeg",
            "-y",
            "-i", "{input}",
            "-c", "copy",
            "{output}"
        ],
        "description": "Change container format without re-encoding"
    }
}


def get_all_commands(db_path: str = "ffmpeg_db.json") -> dict:
    """Merges hardcoded dict with external JSON."""
    all_cmds = FFMPEG_COMMANDS.copy()
    if os.path.exists(db_path):
        try:
            with open(db_path, "r") as f:
                all_cmds.update(json.load(f))
        except Exception as e:
            print(f"⚠️ Warning: Load failed: {e}")
    return all_cmds

def build_command(profile: str, **kwargs) -> list:
    """Builds command by looking in the merged database."""
    # Use the helper to get the latest combined list
    commands = get_all_commands()
    
    if profile not in commands:
        raise KeyError(f"Profile '{profile}' not found.")

    template = commands[profile]["command"]
    
    try:
        return [arg.format(**kwargs) for arg in template]
    except KeyError as e:
        print(f"❌ Missing required parameter: {e}")
        return []
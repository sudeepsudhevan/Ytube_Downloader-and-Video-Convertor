"""
ffmpeg_commands.py
High-quality FFmpeg command templates for audio & video processing.

Usage:
    from ffmpeg_commands import FFMPEG_COMMANDS
"""

FFMPEG_COMMANDS = {

    # =========================
    # 🎯 BASELINE (BEST QUALITY)
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
    # ✂️ TRIMMING
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
    # ✂️ SPLITTING
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
    # 📦 COMPRESSION
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
    # 🎧 AUDIO EXTRACTION
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
    # 🎥 VIDEO EXTRACTION
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
    # 📐 RESIZE / SCALE
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
    # 🔁 REMUX (NO RE-ENCODE)
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


def build_command(profile: str, **kwargs) -> list:
    """
    Build an FFmpeg command from a profile.

    Example:
        build_command(
            "trim_reencode",
            input="in.mp4",
            output="out.mp4",
            start="00:00:10",
            end="00:00:30"
        )
    """
    template = FFMPEG_COMMANDS[profile]["command"]
    print(template)
    return [arg.format(**kwargs) for arg in template]

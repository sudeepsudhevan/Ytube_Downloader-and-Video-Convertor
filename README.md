# YouTube Downloader & FFmpeg Converter

A comprehensive Python application that provides both a GUI and CLI for downloading YouTube videos and performing advanced video processing tasks using FFmpeg.

## Features

### 📺 YouTube Downloader
- Download videos in best available quality using `yt-dlp`.
- Simple interface to input URL and track progress.
- Automatic file management in `yt_videos` directory.

### 🛠 FFmpeg Video Tools
Perform professional video operations with ease:
- **Baseline Conversion**: Convert videos to high-quality H.264/AAC.
- **Trimming**: Cut videos with frame-accurate re-encoding or fast stream copying.
- **Splitting**: Split videos into equal-length segments.
- **Compression**: Reduce file size while maintaining quality (H.264 or H.265/HEVC).
- **Audio Extraction**: Extract audio as lossless WAV or high-quality AAC.
- **Video Extraction**: Remove audio tracks.
- **Resizing**: Scale videos with high-quality Lanczos resampling.
- **Remuxing**: Change container formats without re-encoding.

## 💻 Interfaces
- **GUI**: A modern, dark-themed graphical interface built with **Kivy**.
- **CLI**: A simple command-line interface for quick operations.

## Prerequisites

Before running the application, ensure you have the following installed:

1. **Python 3.13**: [Download Python](https://www.python.org/downloads/)
2. **FFmpeg**: Must be installed and added to your system's PATH.
   - [FFmpeg Installation Guide](https://ffmpeg.org/download.html)

## Installation

1. Clone or download this repository.
2. Install the required Python dependencies:

```bash
pip install kivy yt-dlp
```

> **Note**: For Kivy installation on specific platforms, refer to the [official Kivy documentation](https://kivy.org/doc/stable/gettingstarted/installation.html).

## Usage

### Running the GUI
Launch the graphical interface:
```bash
python gui_main.py
```
- **YouTube Section**: Paste a URL and click **Download Video**.
- **FFmpeg Section**:
  1. Enter the full path to your source video file.
  2. Select an operation (e.g., `trim_reencode`, `compress_high_quality`).
  3. Fill in the dynamic parameters (Start Time, Output Filename, etc.).
  4. Click **Run Operation**.

### Running the CLI
Launch the command-line interface:
```bash
python main.py
```
Follow the on-screen prompts to download videos or process local files.

## Project Structure

- `gui_main.py`: Main entry point for the GUI application.
- `main.py`: Entry point for the CLI application.
- `ffmpeg_commands.py`: Contains optimized FFmpeg command templates.
- `youtube_video_downloader.py`: Handles YouTube downloads via `yt-dlp`.
- `yt_videos/`: Default directory for downloaded videos.

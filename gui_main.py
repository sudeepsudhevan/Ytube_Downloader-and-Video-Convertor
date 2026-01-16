import os
import sys
import threading
import subprocess
from pathlib import Path

# Kivy imports
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window

# Local imports
from youtube_video_downloader import download_youtube_video
from ffmpeg_commands import FFMPEG_COMMANDS, build_command

kivy.require('2.0.0')

class ConversionApp(App):
    def build(self):
        self.title = "YouTube Downloader & FFmpeg Converter"
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark background

        # Main Layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # --- Section 1: YouTube Downloader ---
        downloader_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=150, spacing=5)
        downloader_layout.add_widget(Label(text="[b]YouTube Downloader[/b]", markup=True, size_hint_y=None, height=30))
        
        self.url_input = TextInput(hint_text="Enter YouTube URL here...", multiline=False, size_hint_y=None, height=40)
        downloader_layout.add_widget(self.url_input)

        self.download_btn = Button(text="Download Video", size_hint_y=None, height=50, background_color=(0, 0.7, 0.3, 1))
        self.download_btn.bind(on_press=self.start_download_thread)
        downloader_layout.add_widget(self.download_btn)

        main_layout.add_widget(downloader_layout)

        # --- Section 2: FFmpeg Operations ---
        ffmpeg_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=300, spacing=5)
        ffmpeg_layout.add_widget(Label(text="[b]FFmpeg Operations[/b]", markup=True, size_hint_y=None, height=30))

        # File Selection
        file_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.file_path_input = TextInput(hint_text="Path to video file...", multiline=False)
        file_box.add_widget(self.file_path_input)
        ffmpeg_layout.add_widget(file_box)

        # Operation Spinner
        self.profile_keys = list(FFMPEG_COMMANDS.keys())
        self.operation_spinner = Spinner(
            text='Select Operation',
            values=self.profile_keys,
            size_hint_y=None,
            height=40
        )
        self.operation_spinner.bind(text=self.on_operation_select)
        ffmpeg_layout.add_widget(self.operation_spinner)

        # Dynamic Parameters Grid
        self.params_grid = GridLayout(cols=2, spacing=5, size_hint_y=None, height=100)
        ffmpeg_layout.add_widget(self.params_grid)
        self.param_inputs = {} # Store references to inputs

        # Run Operation Button
        self.run_op_btn = Button(text="Run Operation", size_hint_y=None, height=50, background_color=(0.2, 0.5, 0.8, 1))
        self.run_op_btn.bind(on_press=self.start_ffmpeg_thread)
        ffmpeg_layout.add_widget(self.run_op_btn)

        main_layout.add_widget(ffmpeg_layout)

        # --- Section 3: Logs/Status ---
        log_layout = BoxLayout(orientation='vertical', spacing=5)
        log_layout.add_widget(Label(text="Logs / Output:", size_hint_y=None, height=20))
        
        self.log_output = TextInput(text="Ready...\n", readonly=True, size_hint_y=1, background_color=(0,0,0,1), foreground_color=(1,1,1,1))
        log_layout.add_widget(self.log_output)
        
        main_layout.add_widget(log_layout)

        return main_layout

    # --- Downloader Logic ---
    def start_download_thread(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.log("Error: Please enter a URL.")
            return
        
        self.download_btn.disabled = True
        threading.Thread(target=self.run_download, args=(url,), daemon=True).start()

    def run_download(self, url):
        self.log(f"Starting download for: {url}")
        try:
            # Defined in global scope or relative path
            download_path = Path("yt_videos")
            download_path.mkdir(exist_ok=True)
            
            filepath = download_youtube_video(url, download_path)
            
            if filepath:
                self.log(f"Download complete: {filepath}")
                # Auto-fill the file path input
                Clock.schedule_once(lambda dt: setattr(self.file_path_input, 'text', str(filepath)))
            else:
                self.log("Download finished but file not found.")
        except Exception as e:
            self.log(f"Download failed: {str(e)}")
        finally:
            Clock.schedule_once(lambda dt: setattr(self.download_btn, 'disabled', False))

    # --- FFmpeg Logic ---
    def on_operation_select(self, spinner, text):
        # Clear previous params
        self.params_grid.clear_widgets()
        self.param_inputs = {}
        
        profile = FFMPEG_COMMANDS.get(text)
        if not profile:
            return

        command_template = profile['command']
        # Find all placeholders like {input}, {start}, etc.
        # We manually define common params to ask for based on the command string content
        cmd_str = " ".join(command_template)
        
        # Always need Output
        self.add_param_input("output", "Output Filename (e.g. out.mp4)")

        if "{start}" in cmd_str:
            self.add_param_input("start", "Start Time (00:00:00)")
        if "{end}" in cmd_str:
            self.add_param_input("end", "End Time (00:00:05)")
        if "{duration}" in cmd_str:
            self.add_param_input("duration", "Duration (seconds)")
        if "{width}" in cmd_str:
            self.add_param_input("width", "Width (e.g. 1280)")
        if "{height}" in cmd_str:
            self.add_param_input("height", "Height (e.g. 720)")
            
        # Note: {input} is handled by the main file input

    def add_param_input(self, key, hint):
        self.params_grid.add_widget(Label(text=key.capitalize() + ":"))
        ti = TextInput(hint_text=hint, multiline=False)
        self.params_grid.add_widget(ti)
        self.param_inputs[key] = ti

    def start_ffmpeg_thread(self, instance):
        operation = self.operation_spinner.text
        input_file = self.file_path_input.text.strip()
        
        if operation == 'Select Operation':
            self.log("Error: Please select an operation.")
            return
        if not input_file or not os.path.exists(input_file):
            self.log("Error: Invalid input file path.")
            return

        # Collect params
        kwargs = {"input": input_file}
        for key, ti in self.param_inputs.items():
            val = ti.text.strip()
            if not val:
                self.log(f"Error: Parameter '{key}' is required.")
                return
            kwargs[key] = val

            # Auto-handle output path if it's just a filename
            if key == "output" and not os.path.isabs(val):
                # Save to same dir as input
                parent = os.path.dirname(input_file)
                kwargs[key] = os.path.join(parent, val)

        # Build command
        try:
            cmd_list = build_command(operation, **kwargs)
        except Exception as e:
            self.log(f"Error building command: {e}")
            return

        self.run_op_btn.disabled = True
        threading.Thread(target=self.run_ffmpeg, args=(cmd_list,), daemon=True).start()

    def run_ffmpeg(self, cmd_list):
        cmd_str = " ".join(cmd_list)
        self.log(f"Running: {cmd_str}")
        
        try:
            process = subprocess.Popen(
                cmd_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            for line in process.stdout:
                # Update log in real-time (scheduled on main thread)
                # We update in chunks or just print important lines to avoid UI freeze if too fast
                # specific to Kivy: scheduling frequently can be heavy, but let's try direct main thread valid call
                Clock.schedule_once(lambda dt, l=line: self.log(l.strip(), append_newline=True))
            
            process.wait()
            if process.returncode == 0:
                self.log("Operation Success!")
            else:
                self.log(f"Operation Failed with code {process.returncode}")
                
        except Exception as e:
            self.log(f"Execution Error: {e}")
        finally:
            Clock.schedule_once(lambda dt: setattr(self.run_op_btn, 'disabled', False))

    def log(self, message, append_newline=True):
        def _update(dt):
            self.log_output.text += message + ("\n" if append_newline else "")
            # Scroll to bottom
            self.log_output.cursor = (0, len(self.log_output._lines))
        
        if threading.current_thread() is threading.main_thread():
            _update(0)
        else:
            Clock.schedule_once(_update)

if __name__ == '__main__':
    ConversionApp().run()

# Python
import subprocess

try:
    result = subprocess.run(["nvidia-smi"], capture_output=True, text=True, check=True)
    print("NVIDIA GPU detected:")
    print(result.stdout)
except subprocess.CalledProcessError:
    print("No NVIDIA GPU detected.")
except FileNotFoundError:
    print("nvidia-smi tool not found. No NVIDIA GPU detected.")
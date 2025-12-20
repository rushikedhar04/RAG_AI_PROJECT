# Converts the videos to mp3 
import os 
import subprocess

files = os.listdir("videos") 
for file in files:
    # skip non-video files
    if not file.lower().endswith((".mp4", ".mov", ".mkv", ".avi",".webm")):
        continue
    
    tutorial_number = "unknown"
    file_name = os.path.splitext(file)[0]  # fallback: filename without extension

    # try to extract tutorial_number if pattern exists
    if " #" in file:
        parts = file.split(" [")[0].split(" #")
        if len(parts) > 1:
            tutorial_number = parts[1]

    # try to extract clean name if pattern exists
    if " ｜ " in file:
        file_name = file.split(" ｜ ")[0]

    out_name = f"{tutorial_number}_{file_name}.mp3"
    print(file, "->", out_name)

    subprocess.run([
        "ffmpeg", "-i", f"videos/{file}", f"audios/{out_name}"
    ])
import os
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys

def download_video():
    url = url_entry.get()
    format_choice = format_var.get()
    quality_choice = quality_var.get()

    if not url.strip():
        messagebox.showerror("Error", "Please paste a video URL.")
        return

    output_folder = os.path.join(os.getcwd(), "Downloads")
    os.makedirs(output_folder, exist_ok=True)

    cmd = ["yt-dlp", url, "-o", os.path.join(output_folder, "%(title)s.%(ext)s")]

    if format_choice == "MP3":
        cmd += ["-f", "bestaudio", "--extract-audio", "--audio-format", "mp3"]
    elif format_choice == "MP4":
        if quality_choice == "Highest":
            cmd += ["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"]
        else:
            cmd += ["-f", f"bv*[height<={quality_choice}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"]
    elif format_choice == "MKV":
        if quality_choice == "Highest":
            cmd += ["-f", "bestvideo+bestaudio/best", "--merge-output-format", "mkv"]
        else:
            cmd += ["-f", f"bv*[height<={quality_choice}]+ba/b", "--merge-output-format", "mkv"]

    status_label.config(text="Downloading...", foreground="blue")
    root.update()

    try:
        startupinfo = None
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        subprocess.run(cmd, check=True, startupinfo=startupinfo)
        status_label.config(text="Download Complete ✅", foreground="green")
    except subprocess.CalledProcessError:
        status_label.config(text="Download Failed ❌", foreground="red")

root = tk.Tk()
root.title("Custom YouTube Downloader")
root.geometry("480x300")
root.resizable(False, False)

tk.Label(root, text="Paste YouTube/Video URL:").pack(pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

tk.Label(root, text="Select Output Format:").pack(pady=5)
format_var = tk.StringVar(value="MP4")
format_menu = ttk.Combobox(root, textvariable=format_var, values=["MP4", "MKV", "MP3"], state="readonly")
format_menu.pack()

tk.Label(root, text="Select Quality:").pack(pady=5)
quality_var = tk.StringVar(value="Highest")
quality_menu = ttk.Combobox(root, textvariable=quality_var, values=["Highest", "1080", "720", "480", "360"], state="readonly")
quality_menu.pack()

tk.Button(root, text="Download", command=download_video, width=25, bg="green", fg="white").pack(pady=10)
status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()

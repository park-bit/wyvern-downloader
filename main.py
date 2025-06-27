import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
import threading
import sys
import os
import time
import yt_dlp
import tkinter as tk
import webbrowser

def resource_path(relative_path):
    try:
        return os.path.join(sys._MEIPASS, relative_path)
    except Exception:
        return os.path.abspath(relative_path)

class DownloadItem(tb.Frame):
    def __init__(self, master, index, title, fmt, quality, size, cancel_callback, open_callback, pause_callback):
        super().__init__(master, bootstyle="dark")
        self.index = index
        self.cancel_callback = cancel_callback
        self.open_callback = open_callback
        self.pause_callback = pause_callback
        self.download_path = None
        self.is_paused = False

        self.label = tb.Label(self, text=f"{title} | {fmt} | {quality}", anchor="w")
        self.label.pack(fill=X, padx=5, pady=2)

        info_frame = tb.Frame(self)
        info_frame.pack(fill=X, padx=5)

        self.status_label = tb.Label(info_frame, text="Waiting", width=12)
        self.status_label.pack(side=LEFT)

        self.size_label = tb.Label(info_frame, text=f"Size: {size}", width=18)
        self.size_label.pack(side=LEFT, padx=(10, 0))

        self.cancel_btn = tb.Button(info_frame, text="Cancel", bootstyle="danger-outline", width=8, command=self.cancel_download)
        self.cancel_btn.pack(side=RIGHT, padx=2)

        self.pause_btn = tb.Button(info_frame, text="Pause", bootstyle="warning-outline", width=8, command=self.toggle_pause)
        self.pause_btn.pack(side=RIGHT, padx=2)

        self.open_btn = tb.Button(info_frame, text="Open", bootstyle="success-outline", width=8, command=self.open_file, state=DISABLED)
        self.open_btn.pack(side=RIGHT)

        self.progress = tb.Progressbar(self, bootstyle="info-striped", length=780)
        self.progress.pack(padx=5, pady=(5, 10))

    def update_status(self, percent):
        self.progress['value'] = percent

    def set_done(self, path):
        self.status_label.configure(text="Done")
        self.download_path = path
        self.open_btn.configure(state=NORMAL)
        self.progress['value'] = 100

    def set_failed(self):
        self.status_label.configure(text="Failed")

    def cancel_download(self):
        self.cancel_callback(self.index)

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_callback(self.index, self.is_paused)
        self.pause_btn.configure(text="Resume" if self.is_paused else "Pause")

    def open_file(self):
        if self.download_path and os.path.exists(self.download_path):
            self.open_callback(self.download_path)
class WyvernDownloader(tb.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("WyverN")
        self.geometry("900x740")
        self.iconbitmap(resource_path("icon.ico"))
        self.minsize(900, 700)

        self.queue = []
        self.cancel_flags = {}
        self.pause_flags = {}
        self.download_items = []
        self.download_path = None
        self.quality_info = {}

        self.create_widgets()
        self.fade_in()

    def create_widgets(self):
        tb.Label(self, text="YouTube URL:", font=("Segoe UI", 10)).pack(pady=(15, 3))
        self.url_entry = tb.Entry(self, width=80, bootstyle="dark")
        self.url_entry.pack(pady=5, ipady=5)
        self.url_entry.bind("<FocusOut>", lambda e: self.update_quality_options())
        self.url_entry.bind("<KeyRelease>", lambda e: self.update_quality_options())

        combo_frame = tb.Frame(self)
        combo_frame.pack(pady=5)

        tb.Label(combo_frame, text="Format:").grid(row=0, column=0, padx=5)
        self.format_combobox = tb.Combobox(combo_frame, width=10, values=["mp4", "mkv", "mp3", "webm", "flv", "wav"], state="readonly")
        self.format_combobox.set("mp4")
        self.format_combobox.grid(row=0, column=1, padx=5)

        tb.Label(combo_frame, text="Quality:").grid(row=0, column=2, padx=5)
        self.quality_combobox = tb.Combobox(combo_frame, width=25, state="readonly")
        self.quality_combobox.set("Retrieving...")
        self.quality_combobox.grid(row=0, column=3, padx=5)

        self.subs_var = tk.BooleanVar(value=False)
        self.subs_check = tb.Checkbutton(self, text="Download Subtitles", variable=self.subs_var, bootstyle="secondary")
        self.subs_check.pack(pady=(5, 10))

        button_frame = tb.Frame(self)
        button_frame.pack(pady=10)

        tb.Button(button_frame, text="Add to Queue", command=self.add_to_queue, bootstyle="info-outline", width=16).grid(row=0, column=0, padx=10)
        tb.Button(button_frame, text="Start Download", command=self.start_downloads, bootstyle="success", width=16).grid(row=0, column=1, padx=10)

        tb.Label(self, text="Download Queue:").pack(pady=(20, 5))

        self.queue_canvas = tk.Canvas(self, borderwidth=0, background="#222")
        self.queue_frame = tb.Frame(self.queue_canvas)
        self.scrollbar = tb.Scrollbar(self, orient="vertical", command=self.queue_canvas.yview)
        self.queue_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.queue_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.queue_canvas.create_window((0, 0), window=self.queue_frame, anchor="nw")
        self.queue_frame.bind("<Configure>", lambda e: self.queue_canvas.configure(scrollregion=self.queue_canvas.bbox("all")))
    def update_quality_options(self):
        url = self.url_entry.get().strip()
        if not url:
            return

        self.quality_combobox.configure(values=["Retrieving qualities..."])
        self.quality_combobox.set("Retrieving qualities...")

        def fetch():
            try:
                with yt_dlp.YoutubeDL({"quiet": True, "skip_download": True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    formats = info.get('formats', [])
                    title = info.get("title", "Unknown Title")
                    self.quality_info[url] = {"title": title, "formats": formats}

                    resolutions = []
                    for f in formats:
                        height = f.get("height")
                        if height:
                            resolutions.append(f"{height}p")

                    resolutions = sorted(set(resolutions), key=lambda x: int(x[:-1]), reverse=True)
                    quality_options = ["best (highest)", "worst (lowest)", "audio"] + resolutions
            except:
                quality_options = ["best (highest)", "worst (lowest)", "audio"]

            def update():
                self.quality_combobox.configure(values=quality_options)
                self.quality_combobox.set("best (highest)")

            self.after(0, update)

        threading.Thread(target=fetch, daemon=True).start()

    def add_to_queue(self):
        url = self.url_entry.get().strip()
        fmt = self.format_combobox.get()
        quality = self.quality_combobox.get()

        if not url or url not in self.quality_info:
            messagebox.showerror("Error", "Please enter a valid YouTube URL and wait for quality to load.")
            return

        title = self.quality_info[url]["title"]
        formats = self.quality_info[url]["formats"]
        size_str = "Unknown"

        for f in formats:
            height = f.get("height")
            if height and f"{height}p" == quality:
                size = f.get("filesize") or f.get("filesize_approx")
                if size:
                    size_str = f"{round(size / (1024 * 1024), 2)} MB"
                    break

        index = len(self.queue)
        item = DownloadItem(
            self.queue_frame, index, title, fmt, quality,
            size_str, self.cancel_download, self.open_file, self.toggle_pause
        )
        item.pack(fill=X, padx=10, pady=5)

        self.download_items.append(item)
        self.queue.append((url, title, fmt, quality))
        self.cancel_flags[index] = False
        self.pause_flags[index] = False
        self.url_entry.delete(0, END)
    def cancel_download(self, index):
        self.cancel_flags[index] = True
        item = self.download_items[index]
        item.status_label.configure(text="Cancelled")
        if item.download_path and os.path.exists(item.download_path):
            try:
                os.remove(item.download_path)
            except:
                pass

    def toggle_pause(self, index, is_paused):
        self.pause_flags[index] = is_paused

    def open_file(self, path):
        webbrowser.open(path)

    def start_downloads(self):
        if not self.download_path:
            self.download_path = filedialog.askdirectory(title="Select Download Folder")
            if not self.download_path:
                messagebox.showerror("No Folder Selected", "Please select a folder to download.")
                return

        for i, (url, title, fmt, quality) in enumerate(self.queue):
            threading.Thread(target=self.download, args=(i, url, fmt, quality)).start()

    def download(self, index, url, fmt, quality):
        q_map = {
            "4320p": "bestvideo[height=4320]",
            "2160p": "bestvideo[height=2160]",
            "1440p": "bestvideo[height=1440]",
            "1080p": "bestvideo[height=1080]",
            "720p": "bestvideo[height=720]",
            "480p": "bestvideo[height=480]",
            "360p": "bestvideo[height=360]",
            "240p": "bestvideo[height=240]",
            "audio": "bestaudio",
            "best (highest)": "bestvideo+bestaudio/best",
            "worst (lowest)": "worst"
        }

        outtmpl = os.path.join(self.download_path, "%(title)s.%(ext)s")
        opts = {
            "outtmpl": outtmpl,
            "format": q_map.get(quality, "bestvideo+bestaudio/best"),
            "merge_output_format": fmt,
            "progress_hooks": [lambda d: self.hook(d, index)],
            "quiet": True,
        }

        if fmt == "mp3":
            opts.update({"extract_audio": True, "audio_format": "mp3"})

        if self.subs_var.get():
            opts.update({
                "writesubtitles": True,
                "subtitleslangs": ["en"],
                "subtitlesformat": "best"
            })
        else:
            opts.update({"writesubtitles": False})

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url)
                filename = ydl.prepare_filename(info)
                if fmt == "mp3":
                    filename = os.path.splitext(filename)[0] + ".mp3"
                self.download_items[index].set_done(filename)
        except Exception:
            self.download_items[index].set_failed()
    def hook(self, d, index):
        while self.pause_flags.get(index, False):
            time.sleep(0.1)
        if self.cancel_flags.get(index):
            raise yt_dlp.utils.DownloadCancelled()
        if d['status'] == 'downloading':
            percent = float(d.get('_percent_str', '0.0').replace('%', '').strip())
            self.download_items[index].update_status(percent)
        elif d['status'] == 'finished':
            self.download_items[index].update_status(100)

    def fade_in(self):
        self.attributes('-alpha', 0.0)
        for i in range(21):
            self.attributes('-alpha', i / 20)
            self.update()
            time.sleep(0.01)

if __name__ == "__main__":
    WyvernDownloader().mainloop()

### Wyvern Downloader ###

A simple GUI for downloading YouTube videos or audio using `yt-dlp`.

It has buttons. You paste a link, choose a format, click download. That’s pretty much it.







---



## Features ##

- MP4, MKV, MP3, WebM, FLV, WAV format support
- Lets you choose video quality (up to 8K if available)
- Dynamic quality list updates when a link is typed
- Optional subtitle download (toggle)
- Individual download progress bars
- Pause/resume support per queue item
- Open downloaded file after completion
- Cancel button for each item
- Multithreaded queue for parallel downloads
- Uses `yt-dlp`, `ffmpeg`, and `ttkbootstrap` for modern UI
- Output folder of your choice
- No terminal needed once it's built

---

<img src="https://github.com/user-attachments/assets/9a948c26-8b98-4b39-b557-f6f105e1a3cc" width="240"/>



---






## How to Use ##

---

### Running from source: ##


install the requirements from requirements.txt
python main.py

Notes
This uses yt-dlp. You still need ffmpeg if you want merged audio/video.




Or use the .exe.

You can download the executable from the [Releases](https://github.com/park-bit/wyvern-downloader/releases). page

Building the .exe yourself
Requires pyinstaller:

bash
Copy
Edit
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --icon=icon.ico main.py --add-data "yt_dlp;yt_dlp"
The executable will be in the dist/ folder.

Works on Windows. Probably works on Linux and macOS if you run it from Python, but not tested.


Screenshot:

![Screenshot 2025-06-27 201623](https://github.com/user-attachments/assets/2b619281-8170-4cdb-ba2f-e498b063366a)



#Credits#

- **Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp)**  
  All download functionality is handled by yt-dlp and its contributors. This GUI is just a frontend wrapper.

- **UI built using [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap)**  
  A modern-themed styling toolkit for Python’s tkinter.

All actual download logic is powered by yt-dlp and its contributors










License
MIT. Use it however. Comes with no support.


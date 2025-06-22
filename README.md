# Wyvern Downloader

A simple GUI for downloading YouTube videos or audio using `yt-dlp`.

It has buttons. You paste a link, choose a format, click download. That’s pretty much it.

---

## Features

- MP4, MKV, and MP3 support
- Lets you choose video quality (up to 1080p)
- Uses `yt-dlp` and Python's `tkinter`
- Output files go into a `Downloads/` folder
- No terminal needed once it's built





-----------------------------------------------------------
![icon](https://github.com/user-attachments/assets/3d570ee0-a533-4360-b0ea-103bdff68b99)
source: https://in.pinterest.com/pin/6544361948711974/
-----------------------------------------------------------








## How to Use
------------------------------------------------------------
### Running from source:

pip install -r requirements.txt

python main.py

Or use the .exe


You can download the executable from the [Releases](https://github.com/park-bit/wyvern-downloader/releases) page.



------------------------------------------------------------
**Building .exe yourself**



Requires pyinstaller:

pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico main.py



Executable will be in the dist/ folder.
-------------------------------------------------------------
Screenshot




![image](https://github.com/user-attachments/assets/8319251d-62f2-4a0f-b8fc-7deb40be93b3)
















Notes
This uses yt-dlp. You still need ffmpeg if you want merged audio/video.






Works on Windows. Probably works on Linux and macOS if you run it from Python, but not tested.






#Credits#


Built on top of yt-dlp

All actual download logic is handled by yt-dlp and its contributors — this is just a GUI wrapper

yt-dlp is licensed under the Unlicense










License
MIT. Use it however. Comes with no support.


# metadata-editor
A simple, but functional metadata editor for fixing metadata dates in mp4 video files using [FFmpeg](https://ffmpeg.org/). Packaging done with [PyInstaller](https://pythonhosted.org/PyInstaller/index.html). 

## Dependencies
This program uses FFmpeg to update the metadata for the files. Because of that, FFmpeg must already be installed on your system and be available in the system path. You can download and install FFmpeg from their [official site](https://ffmpeg.org/). You can check that it is in your `path` by running `ffmpeg` in your system's terminal or pwershell. 

## Packaging
This app can be packaged for production use by using `pyinstaller`. Simply build the app with 

`pyinstaller --onefile main.py` 

and then find the single-file executable in the `dist` folder.


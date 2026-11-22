# Building Video Convert Pro for Windows

These instructions build the English and Vietnamese editions from the source files in this repository.

## Build environment

- Windows 10/11 x64
- Python 3.14
- PyInstaller 6.22.3
- tkinterdnd2 for drag-and-drop support

Install the build tools in the selected Python 3.14 environment:

```powershell
py -3.14 -m pip install --upgrade pyinstaller==6.22.3 tkinterdnd2
```

## Build English

Run from the repository root:

```powershell
py -3.14 -m PyInstaller --clean --noconfirm --distpath build\dist-en --workpath build\work-en packaging\VideoConvertPro-EN.spec
```

## Build Vietnamese

```powershell
py -3.14 -m PyInstaller --clean --noconfirm --distpath build\dist-vi --workpath build\work-vi packaging\VideoConvertPro-VI.spec
```

The executable and bundled Python runtime are created in the VideoConvertPro folder under the selected dist directory.

## Assemble the portable package

Place the following files beside VideoConvertPro.exe:

- ffmpeg.exe and ffprobe.exe
- All FFmpeg runtime DLLs from the same upstream build
- icon.ico
- README.txt and THIRD_PARTY_NOTICES.txt
- Licenses/ containing the full applicable license texts
- FFmpeg-BUILD-INFO.txt and FFmpeg-SOURCE-INDEX.md

The Video Convert Pro 3.9.5 release uses the BtbN FFmpeg-Builds GPL shared Windows x64 package. Its exact source and build provenance are recorded in docs/FFmpeg-SOURCE-INDEX.md. Do not mix DLLs from different FFmpeg builds or omit the accompanying license/source notices.

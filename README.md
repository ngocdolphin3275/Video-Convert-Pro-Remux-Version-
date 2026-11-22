<!-- Video Convert Pro project overview -->
<p align="center">
  <img src="assets/video-convert-pro-logo.png" alt="Video Convert Pro logo" width="112">
</p>
<h1 align="center">Video Convert Pro</h1>
<p align="center"><strong>Smart remuxing. Controlled conversion.</strong></p>
<p align="center">
  A focused Windows desktop video utility for stream-aware remuxing,
  configurable conversion and batch processing.
</p>
<p align="center">
  <a href="https://ngocdolphincom.wordpress.com/video-convert-pro/">Project website</a>
  ·
  <a href="https://github.com/ngocdolphin3275/Video-Convert-Pro-Remux-Version-/releases">Downloads &amp; releases</a>
  ·
  <a href="https://github.com/ngocdolphin3275/Video-Convert-Pro-Remux-Version-/tree/main/src">Application source code</a>
</p>

---

## About

Video Convert Pro is a Windows desktop application for remuxing and converting video files while keeping control over how each media stream is handled.

Its processing strategy follows a simple priority: **Copy → Convert → Drop**. Compatible streams are copied whenever possible, only incompatible streams are re-encoded when needed, and unsupported or unwanted streams are handled by the conversion plan.

Video Convert Pro is part of **MasterTools**, NgocDolphin's open-source utility project family.

## Features

- **Smart remuxing** — copy compatible video, audio and subtitle streams instead of re-encoding everything.
- **Container selection** — MP4, MKV, WebM, MOV, AVI and TS.
- **Independent stream modes** — choose automatic handling (Copy → Convert), force re-encode or force copy for video and audio separately.
- **Container-aware codecs** — H.264, H.265/HEVC, VP9 and AV1 options are filtered to match the selected output container.
- **Quality controls** — CRF, encoder presets, adaptive quality and an optional bitrate cap.
- **NVIDIA GPU acceleration** — NVENC on supported systems, with runtime capability detection and automatic CPU fallback.
- **Metadata and stream options** — preserve metadata, chapters, cover attachments and supported data streams.
- **Batch workflow** — add files, scan folders, enable or disable queued tasks and cancel processing.
- **Progress and diagnostics** — per-file status, overall progress, processing logs and a completion summary.
- **Convenient file actions** — open a source file or its containing folder, remove tasks and manage the output folder.
- **Output verification** — FFprobe checks the resulting streams and duration against the source.

## Download and run

The latest public release is **Video Convert Pro 3.9.5**, with matching English and Vietnamese portable builds for Windows x64.

### Release downloads

| Edition | Portable package |
|---|---|
| English | [Download Video Convert Pro 3.9.5 — English](https://github.com/ngocdolphin3275/Video-Convert-Pro-Remux-Version-/releases/download/v3.9.5/Video-Convert-Pro-Windows-x64-EN-v3.9.5.zip) |
| Vietnamese | [Tải Video Convert Pro 3.9.5 — Tiếng Việt](https://github.com/ngocdolphin3275/Video-Convert-Pro-Remux-Version-/releases/download/v3.9.5/Video-Convert-Pro-Windows-x64-VI-v3.9.5.zip) |

1. Download the ZIP for your preferred language.
2. Extract the complete ZIP to a writable folder.
3. Open the extracted folder and run **VideoConvertPro.exe**.
4. Keep the extracted folder structure intact.

The portable package includes the application, Python runtime, FFmpeg, FFprobe and the FFmpeg runtime DLLs. No separate Python installation, installer, FFmpeg download or setup script is required.

### Verify your download

Compare the downloaded ZIP with the published SHA-256 checksum:

| File | SHA-256 |
|---|---|
| Video-Convert-Pro-Windows-x64-EN-v3.9.5.zip | C793E47B4E69F92FFAD5E95B6493886C847E0CB59CC735BFAC90F0E0570CC58E |
| Video-Convert-Pro-Windows-x64-VI-v3.9.5.zip | 075A008E6E51AB727DF767DFE9651D7E423D0CFD957171C490563E7A597EE2B1 |

[Download SHA256SUMS.txt](https://github.com/ngocdolphin3275/Video-Convert-Pro-Remux-Version-/releases/download/v3.9.5/SHA256SUMS.txt)

## Platform

- Windows 10/11, 64-bit (x64).
- Portable folder distribution.
- No installer required.
- No macOS or Linux build is currently published.

## Licensing

**Video Convert Pro application source code is open source under the MIT License.** The root LICENSE applies to the application source in the src folder.

The portable packages also include FFmpeg and FFprobe from the BtbN FFmpeg-Builds GPL shared Windows x64 build. FFmpeg is separately licensed under **GNU GPL v3**; the application's MIT license does not relicense FFmpeg or its dependencies.

For third-party details, see:
- docs/THIRD_PARTY_NOTICES.md
- docs/FFmpeg-BUILD-INFO.txt
- docs/FFmpeg-SOURCE-INDEX.md

The matching BtbN build-recipe snapshot is available in the third_party/FFmpeg-Builds folder and as a [companion release archive](https://github.com/ngocdolphin3275/Video-Convert-Pro-Remux-Version-/releases/download/v3.9.5/FFmpeg-Build-Recipes-BtbN-7f2a6b1.zip). The snapshot documents the build scripts and pinned upstream source references; individual third-party components retain their own licenses.

## Project links

- [Video Convert Pro — English project page](https://ngocdolphincom.wordpress.com/video-convert-pro/)
- [Video Convert Pro — Vietnamese project page](https://ngocdolphincom.wordpress.com/vi/video-convert-pro/)
- [GitHub repository](https://github.com/ngocdolphin3275/Video-Convert-Pro-Remux-Version-)
- [GitHub releases](https://github.com/ngocdolphin3275/Video-Convert-Pro-Remux-Version-/releases)
- [NgocDolphin — independent software projects](https://ngocdolphincom.wordpress.com/)

---

<p align="center"><sub>Video Convert Pro · A MasterTools project by NgocDolphin</sub></p>

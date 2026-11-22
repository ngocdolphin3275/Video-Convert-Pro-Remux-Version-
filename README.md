<h1 align="center">Video Convert Pro</h1>
<p align="center"><strong>Smart remuxing. Controlled conversion. Source-matched quality.</strong></p>
<p align="center">
  A Windows desktop video utility built around container-aware stream handling,
  practical batch processing and NVIDIA GPU acceleration.
</p>
<p align="center">
  <a href="https://ngocdolphincom.wordpress.com/video-convert-pro/">Project website (English)</a>
  ·
  <a href="https://ngocdolphincom.wordpress.com/vi/video-convert-pro/">Trang dự án (Tiếng Việt)</a>
  ·
  <a href="https://github.com/ngocdolphin3275/Video-Convert-Pro-Remux-Version-/releases">GitHub releases</a>
</p>

---

## About

Video Convert Pro is a Windows desktop utility for remuxing and converting video files while keeping control over how individual media streams are handled.

The processing engine follows a simple priority: **Copy → Convert → Drop**. It checks which streams the destination container supports, copies compatible streams whenever possible, and only re-encodes streams that need a different format.

Video Convert Pro is part of **MasterTools**, NgocDolphin's open-source utility project family. It is separate from the proprietary PyProjects applications.

## Features

- **Container selection** — MP4, MKV, WebM, MOV, AVI and TS.
- **Independent video and audio modes** — automatic handling (Copy > Convert), force re-encode, or force copy.
- **Container-aware codecs** — H.264, H.265/HEVC, VP9 and AV1 choices are filtered to match the selected container.
- **Quality controls** — CRF, encoder presets, adaptive CRF and optional bitrate cap.
- **NVIDIA GPU acceleration** — NVENC for supported codecs, with a runtime capability check and automatic CPU fallback when a compatible GPU/driver is unavailable.
- **Stream and metadata options** — retain metadata, chapters, cover attachments and supported data streams.
- **Batch processing** — add individual files, scan folders, enable or disable queued tasks, and cancel processing.
- **Progress and diagnostics** — per-file status and progress, overall progress, processing log and a completion summary.
- **Convenient file actions** — right-click a queued item to enable/disable it, open the source or containing folder, or remove it.
- **Output-folder controls** — choose or edit the output path and open it in File Explorer.
- **Drag and drop / command line** — desktop drag-and-drop and opening files or folders with the executable are supported.
- **Output verification** — FFprobe checks resulting streams and duration against the source before a task is treated as complete.

## Supported formats

**Output containers:** MP4, MKV, WebM, MOV, AVI and TS.

**Source extensions:** MP4, M4V, MKV, MOV, AVI, TS, M2TS, MTS, WebM, FLV, WMV, MPEG, MPG, VOB, OGV, 3GP, 3G2, MXF, F4V, RM, RMVB, ASF, DIVX, M2V and MP2V.

Actual stream compatibility depends on the codecs present in each input file and the selected destination container.

## Screenshots

Application screenshots will be added here.

## Download and run

<details>
<summary><strong>Windows x64 — English (Video Convert Pro 3.9.5)</strong></summary>

[**Download English portable build**](https://github.com/ngocdolphin3275/Video-Convert-Pro-Remux-Version-/releases/download/v3.9.5/Video-Convert-Pro-Windows-x64-EN-v3.9.5.zip)

File: Video-Convert-Pro-Windows-x64-EN-v3.9.5.zip

</details>

<details>
<summary><strong>Windows x64 — Tiếng Việt (Video Convert Pro 3.9.5)</strong></summary>

[**Tải bản portable tiếng Việt**](https://github.com/ngocdolphin3275/Video-Convert-Pro-Remux-Version-/releases/download/v3.9.5/Video-Convert-Pro-Windows-x64-VI-v3.9.5.zip)

File: Video-Convert-Pro-Windows-x64-VI-v3.9.5.zip

</details>

### First run

1. Download the ZIP matching your preferred language.
2. Extract the complete folder to a normal writable location.
3. Run **VideoConvertPro.exe**.

The package includes the Python runtime, application libraries, FFmpeg, FFprobe and the DLLs required by FFmpeg. No separate Python installation, runtime installer, FFmpeg download or setup script is required. Keep the extracted folder structure intact.

SHA-256 checksums are included in SHA256SUMS.txt in the release assets.

## Platform

- Windows 10/11, 64-bit (x64).
- Portable onedir distribution.
- No installer required.
- No macOS or Linux build is currently published.

## Source code and licensing

The Video Convert Pro application source is available in the src/ folder under the **MIT License**. The root LICENSE applies to the application source code only.

The portable packages use FFmpeg and FFprobe from the **BtbN FFmpeg-Builds GPL shared Windows x64 build**, version n9.0.2-61-gd59078794d-20261121. FFmpeg is distributed under **GNU GPL v3**. The application's MIT licence does not relicense FFmpeg or any third-party component.

To make the FFmpeg build traceable, this repository includes:
- docs/FFmpeg-BUILD-INFO.txt — exact binary version, configuration and upstream package checksum.
- docs/FFmpeg-SOURCE-INDEX.md — FFmpeg source commit, BtbN build commit and pinned upstream source references for build dependencies.
- docs/THIRD_PARTY_NOTICES.md — third-party notices and licence scope.
- third_party/FFmpeg-Builds/ — the BtbN build recipe snapshot used by the upstream workflow, including dependency scripts and patches.
- FFmpeg-Build-Recipes-BtbN-7f2a6b1.zip — a source snapshot of those build recipes, also attached to the release.

Each bundled third-party component remains subject to its own licence. Review the source index and the licence files before redistributing modified builds.

## Project links

- [Video Convert Pro — English project page](https://ngocdolphincom.wordpress.com/video-convert-pro/)
- [Video Convert Pro — Vietnamese project page](https://ngocdolphincom.wordpress.com/vi/video-convert-pro/)
- [Latest Windows release](https://github.com/ngocdolphin3275/Video-Convert-Pro-Remux-Version-/releases/latest)
- [NgocDolphin — independent software projects](https://ngocdolphincom.wordpress.com/)

---

<p align="center"><sub>Video Convert Pro · A MasterTools project by NgocDolphin</sub></p>

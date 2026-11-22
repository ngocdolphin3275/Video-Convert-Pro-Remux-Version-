<!--
Video Convert Pro project overview.
Product information is aligned with the official NgocDolphin project pages.
-->

<h1 align="center">Video Convert Pro</h1>
<p align="center"><strong>Smart remuxing. Controlled conversion. Source-matched quality.</strong></p>
<p align="center">
  A Windows desktop video utility built around container-aware stream handling and practical batch processing.
</p>
<p align="center">
  <a href="https://ngocdolphincom.wordpress.com/video-convert-pro/">Project website (English)</a>
  ·
  <a href="https://ngocdolphincom.wordpress.com/vi/video-convert-pro/">Trang dự án (Tiếng Việt)</a>
  ·
  <a href="https://github.com/ngocdolphin3275/Video-Convert-Pro-Remux-Version-">GitHub repository</a>
</p>

---

## About

Video Convert Pro is a Windows desktop utility for remuxing and converting video files while keeping control over how individual media streams are handled.

Rather than re-encoding every stream by default, the application first checks whether the selected target container can accept the existing video, audio and subtitle streams. Compatible streams can be copied; conversion is reserved for streams that need it.

The project belongs to **MasterTools**, NgocDolphin's collection of open-source utility projects. It is separate from the proprietary PyProjects applications.

## Processing philosophy

The core strategy is:

**COPY → CONVERT → DROP**

1. **Check the destination container.** The selected container determines which stream codecs can be retained.
2. **Copy compatible streams first.** Avoid re-encoding when the original stream is already suitable for the destination.
3. **Convert only when needed.** Incompatible streams can be re-encoded using the selected options.
4. **Drop only what is unnecessary or unsupported.** The processing plan handles secondary or incompatible streams without arbitrarily discarding the primary video or audio.
5. **Use a fault-tolerant fallback.** When FFmpeg cannot complete a planned operation, the engine can move through a copy, convert and drop fallback sequence where appropriate.

When video re-encoding is required, the engine is designed to preserve the source resolution and timing where possible, avoid upscaling, and retain pixel format, bit depth and colour/HDR metadata when the selected encoder supports them.

## Features

- **Container selection** — MP4, MKV, WebM, MOV, AVI and TS.
- **Independent video and audio modes** — automatic handling (Copy > Convert), force re-encode, or force copy.
- **Video codec controls** — H.264, H.265/HEVC, VP9 and AV1. The codec list is filtered to match the chosen container.
- **Quality controls** — CRF selection, encoder presets and adaptive CRF options for re-encoding.
- **GPU acceleration** — optional NVIDIA NVENC encoding, with CPU encoding as a fallback when the GPU encoder is unavailable.
- **Stream and metadata options** — retain metadata, chapters, cover attachments and supported data streams.
- **Batch queue** — add individual files or scan folders, enable or disable queued tasks, clear completed work, and cancel processing.
- **Progress and diagnostics** — per-file status, progress reporting, an overall progress indicator and a processing log.
- **Output verification** — completed output is probed again to check for the expected video/audio streams and a reasonable duration relative to the source.
- **Drag and drop** — optional desktop drag-and-drop support when `tkinterdnd2` is installed.

## Supported formats

### Output containers

MP4, MKV, WebM, MOV, AVI and TS.

### Source file extensions

MP4, M4V, MKV, MOV, AVI, TS, M2TS, MTS, WebM, FLV, WMV, MPEG, MPG, VOB, OGV, 3GP, 3G2, MXF, F4V, RM, RMVB, ASF, DIVX, M2V and MP2V.

Actual stream compatibility depends on the codecs present in each input file and the selected destination container.

## Requirements

- Windows desktop environment.
- Python with the standard Tkinter GUI module for running from source.
- FFmpeg and FFprobe available through the system PATH or beside the application.
- `tkinterdnd2` is optional and is only needed for drag-and-drop integration.

## Source and project status

This repository is the public project home for Video Convert Pro. The project overview is being published first; the application source files and reproducible setup instructions are not yet present in this repository.

The current project source identifies the application as **Video Convert Pro 3.9.5**. This is a source-version reference, not a statement that a matching GitHub release asset is available.

## Platform

- Windows desktop application.
- Uses FFmpeg and FFprobe for media processing and output inspection.
- No macOS or Linux build is currently documented.

## Licensing

Video Convert Pro is intended to be an open-source MasterTools project. **A project-level LICENSE file has not yet been published in this repository.** Until an explicit license is added, the repository's public visibility should not be interpreted as permission to reuse, modify or redistribute its code.

Third-party components, including FFmpeg and optional Python packages, remain subject to their own licenses and notices. Those notices must accompany the corresponding source and binary distributions when they are published.

## Project links

- [Video Convert Pro — English project page](https://ngocdolphincom.wordpress.com/video-convert-pro/)
- [Video Convert Pro — Vietnamese project page](https://ngocdolphincom.wordpress.com/vi/video-convert-pro/)
- [NgocDolphin — independent software projects](https://ngocdolphincom.wordpress.com/)
- [MasterTools on GitHub](https://github.com/ngocdolphin3275)

---

<p align="center"><sub>Video Convert Pro · A MasterTools project by NgocDolphin</sub></p>

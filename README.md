<!--
Video Convert Pro project overview and Windows release guide.
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
  ·
  <a href="https://github.com/ngocdolphin3275/Video-Convert-Pro-Remux-Version-/releases">All releases</a>
</p>

---

## About

Video Convert Pro is a Windows desktop utility for remuxing and converting video files while keeping control over how individual media streams are handled.

Rather than re-encoding every stream by default, the application checks whether the selected target container can accept the existing video, audio and subtitle streams. Compatible streams can be copied; conversion is reserved for streams that need it.

The project belongs to **MasterTools**, NgocDolphin's utility project family. It is separate from the proprietary PyProjects applications.

## Processing philosophy

**COPY → CONVERT → DROP**

1. **Check the destination container.** The selected container determines which stream codecs can be retained.
2. **Copy compatible streams first.** Avoid re-encoding when the original stream is already suitable for the destination.
3. **Convert only when needed.** Incompatible streams can be re-encoded using the selected options.
4. **Drop only what is unnecessary or unsupported.** The processing plan handles secondary or incompatible streams without arbitrarily discarding primary video or audio.
5. **Use a fault-tolerant fallback.** When FFmpeg cannot complete a planned operation, the engine can move through a copy, convert and drop fallback sequence where appropriate.

When video re-encoding is required, the engine is designed to preserve source resolution and timing where possible, avoid upscaling, and retain pixel format, bit depth and colour/HDR metadata when supported by the selected encoder.

## Features

- **Container selection** — MP4, MKV, WebM, MOV, AVI and TS.
- **Independent video and audio modes** — automatic handling (Copy > Convert), force re-encode, or force copy.
- **Video codec controls** — H.264, H.265/HEVC, VP9 and AV1, filtered by the selected container.
- **Quality controls** — CRF selection, encoder presets and adaptive CRF options for re-encoding.
- **GPU acceleration** — NVIDIA NVENC is available in the Vietnamese 3.9.5 build. The English 3.9 build does not currently include NVENC.
- **Stream and metadata options** — retain metadata, chapters, cover attachments and supported data streams.
- **Batch queue** — add individual files or scan folders, enable or disable queued tasks, clear completed work, and cancel processing.
- **Progress and diagnostics** — per-file status, progress reporting, an overall progress indicator and a processing log.
- **Output verification** — completed output is probed again to check for expected video/audio streams and duration relative to the source.
- **Drag and drop** — included in the portable packages through the optional desktop integration.

## Supported formats

### Output containers

MP4, MKV, WebM, MOV, AVI and TS.

### Source file extensions

MP4, M4V, MKV, MOV, AVI, TS, M2TS, MTS, WebM, FLV, WMV, MPEG, MPG, VOB, OGV, 3GP, 3G2, MXF, F4V, RM, RMVB, ASF, DIVX, M2V and MP2V.

Actual stream compatibility depends on the codecs present in each input file and the selected destination container.

## Screenshots

Application screenshots will be added here as the release gallery is prepared.

## Download and run

<details>
<summary><strong>Windows x64 — English (Video Convert Pro 3.9)</strong></summary>

[**Download English build**](https://github.com/ngocdolphin3275/Video-Convert-Pro-Remux-Version-/releases/download/windows-builds-2026-11-22/Video-Convert-Pro-Windows-x64-EN-v3.9.zip)

File: `Video-Convert-Pro-Windows-x64-EN-v3.9.zip`

</details>

<details>
<summary><strong>Windows x64 — Tiếng Việt (Video Convert Pro 3.9.5)</strong></summary>

[**Tải bản tiếng Việt**](https://github.com/ngocdolphin3275/Video-Convert-Pro-Remux-Version-/releases/download/windows-builds-2026-11-22/Video-Convert-Pro-Windows-x64-VI-v3.9.5.zip)

File: `Video-Convert-Pro-Windows-x64-VI-v3.9.5.zip`

</details>

### First run

1. Download the ZIP matching your preferred language.
2. Extract the complete folder to a normal writable location.
3. Run **Setup-FFmpeg.bat** once. It downloads FFmpeg and FFprobe from Gyan.dev and places them beside the application executable.
4. Run **VideoConvertPro.exe**.

A separate Python installation is not required. Keep the extracted folder structure intact; do not move the executable away from its `_internal` folder.

### Version note

The two language packages are built from the existing language-specific source versions and are not yet feature-identical. English is version **3.9**; Vietnamese is version **3.9.5**. The Vietnamese build includes NVIDIA NVENC support, which is not present in the current English 3.9 source.

### FFmpeg dependency

FFmpeg and FFprobe are **not bundled** in the application ZIPs. The setup helper downloads the Windows Essentials static build directly from Gyan.dev. Gyan's static FFmpeg builds are GPLv3; review the build details and licensing at [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/).

The ZIPs include third-party notices and runtime license texts. See `THIRD_PARTY_NOTICES.txt` and the `Licenses/` folder after extraction.

## Platform

- Windows 10/11, 64-bit (x64).
- Portable onedir distribution.
- FFmpeg and FFprobe are installed separately by the setup helper.
- No macOS or Linux build is currently documented.

## Licensing and source status

Video Convert Pro is intended to be an open-source MasterTools project. The application source files and a formal project-level `LICENSE` have **not yet been published** in this repository.

Until the project license is added, the repository's public visibility should not be interpreted as permission to reuse, modify or redistribute the application's source code. Source publication and the formal project license are follow-up work.

Third-party components remain subject to their own licenses and notices. Their applicable texts are included in the portable packages.

## Project links

- [Video Convert Pro — English project page](https://ngocdolphincom.wordpress.com/video-convert-pro/)
- [Video Convert Pro — Vietnamese project page](https://ngocdolphincom.wordpress.com/vi/video-convert-pro/)
- [Latest Windows release](https://github.com/ngocdolphin3275/Video-Convert-Pro-Remux-Version-/releases/latest)
- [NgocDolphin — independent software projects](https://ngocdolphincom.wordpress.com/)
- [MasterTools on GitHub](https://github.com/ngocdolphin3275)

---

<p align="center"><sub>Video Convert Pro · A MasterTools project by NgocDolphin</sub></p>

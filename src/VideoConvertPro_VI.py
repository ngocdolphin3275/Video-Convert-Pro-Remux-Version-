#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
ðŸŽ¬ VIDEO CONVERTER PRO v3.9.5
===============================================================================

Container-First Â· Stream Sanitizer Â· Smart Fallback Â· Source-Matched Quality

Triáº¿t lÃ½:

    COPY > CONVERT > DROP

NguyÃªn táº¯c:

1. Container Ä‘Ã­ch quyáº¿t Ä‘á»‹nh codec nÃ o Ä‘Æ°á»£c phÃ©p giá»¯.
2. Stream bÃ¬nh thÆ°á»ng Ä‘Æ°á»£c COPY náº¿u cÃ³ thá»ƒ.
3. Stream khÃ´ng tÆ°Æ¡ng thÃ­ch má»›i CONVERT (khÃ´ng Ã©p copy codec ngoÃ i allowlist).
4. Stream rÃ¡c / khÃ´ng cáº§n thiáº¿t má»›i DROP.
5. Khi FFmpeg tháº¥t báº¡i:
       COPY (chá»‹u lá»—i tá»‘i Ä‘a) â†’ CONVERT â†’ DROP
   Video/audio gá»‘c Ä‘Ã£ lá»—i sáºµn â†’ Æ°u tiÃªn copy chá»‹u lá»—i; chá»‰ convert khi
   cÃ´ng cá»¥ thá»±c sá»± tá»« chá»‘i (muxer refuse). KhÃ´ng tá»± Ã½ DROP video/audio chÃ­nh.
6. Khi báº¯t buá»™c re-encode video:
       - Giá»¯ resolution.
       - Giá»¯ timing/FPS náº¿u cÃ³ thá»ƒ (fps_mode passthrough).
       - Giá»¯ pixel format / bit depth náº¿u encoder há»— trá»£.
       - Giá»¯ mÃ u/HDR metadata khi cÃ³ thá»ƒ.
       - KhÃ´ng upscale.
       - Æ¯u tiÃªn cháº¥t lÆ°á»£ng cao.
7. Tolerance flags Ä‘Æ°á»£c báº­t cho Má»ŒI lá»‡nh FFmpeg.
8. Output chá»‰ Ä‘Æ°á»£c xem lÃ  thÃ nh cÃ´ng sau khi probe láº¡i, cÃ³ video + audio
   (náº¿u nguá»“n cÃ³), duration â‰¥ 90% so vá»›i nguá»“n.
9. KhÃ´ng thao tÃ¡c Tkinter trá»±c tiáº¿p tá»« worker thread.

-------------------------------------------------------------------------------
CHANGELOG v3.9.5 (UI only):

[N1] ThÃªm popup thÃ´ng bÃ¡o khi hÃ ng Ä‘á»£i xá»­ lÃ½ xong:
       - Hiá»ƒn thá»‹ tá»•ng sá»‘ file, sá»‘ thÃ nh cÃ´ng / tháº¥t báº¡i / Ä‘Ã£ huá»· / chÆ°a xá»­ lÃ½.
       - KÃ¨m Ä‘Æ°á»ng dáº«n thÆ° má»¥c xuáº¥t.
       - Náº¿u táº¥t cáº£ thÃ nh cÃ´ng â†’ showinfo (âœ… HoÃ n táº¥t).
       - Náº¿u cÃ³ file fail / huá»· / chÆ°a xá»­ lÃ½ â†’ showwarning (âš  Xá»­ lÃ½ xong).
     CHá»ˆ sá»­a UI, khÃ´ng Ä‘á»¥ng logic worker / engine.

CÃ¡c fix tá»« v2.7 â†’ v3.9.4 váº«n giá»¯ nguyÃªn.
KhÃ´ng Ä‘á»¥ng vÃ o: container matrix, plan structure, encoder preset mapping,
DnD core, thread model, naming policy, verify logic, checkbox logic,
cÃ¡c button khÃ¡c, fallback ladder, emergency command.

-------------------------------------------------------------------------------
CHANGELOG v3.9.4 (fix bug thÆ° má»¥c xuáº¥t):

[F14] ThÆ° má»¥c xuáº¥t nháº­p tay khÃ´ng Ä‘Æ°á»£c Ã¡p dá»¥ng khi báº¥m tháº³ng nÃºt Start:
     - Fix: trong start_processing() chá»§ Ä‘á»™ng gá»i _on_outdir_changed()
       Ä‘á»ƒ Ä‘á»“ng bá»™ Entry â†’ self.output_dir ngay trÆ°á»›c khi spawn worker.
     NgoÃ i ra _on_outdir_changed() chuáº©n hoÃ¡ Ä‘Æ°á»ng dáº«n tÆ°Æ¡ng Ä‘á»‘i thÃ nh
     tuyá»‡t Ä‘á»‘i Ä‘á»ƒ trÃ¡nh ghi nháº§m vÃ o CWD.

-------------------------------------------------------------------------------
CHANGELOG v3.9.3 (UI only):

[U2] ThÃªm menu chuá»™t pháº£i (Context Menu) cho tá»«ng file trong danh sÃ¡ch:
       - Báº­t / Táº¯t file (toggle)
       - Má»Ÿ file nguá»“n (báº±ng trÃ¬nh phÃ¡t máº·c Ä‘á»‹nh cá»§a OS)
       - Má»Ÿ thÆ° má»¥c chá»©a file nguá»“n
       - XoÃ¡ khá»i danh sÃ¡ch
     Menu cÃ³ mÃ u tá»‘i Ä‘á»“ng bá»™ vá»›i theme cá»§a app. CHá»ˆ sá»­a UI, khÃ´ng Ä‘á»¥ng logic.

-------------------------------------------------------------------------------
CHANGELOG v3.9.2 (UI only):

[U1] Dropdown "Video Codec" giá» tá»± Ä‘á»™ng lá»c theo Container Ä‘ang chá»n.
     Khi Ä‘á»•i Container, náº¿u codec Ä‘ang chá»n khÃ´ng cÃ²n há»£p lá»‡, tá»± reset vá»
     option Ä‘áº§u tiÃªn vÃ  ghi log cáº£nh bÃ¡o. CHá»ˆ sá»­a UI, khÃ´ng Ä‘á»¥ng logic.

-------------------------------------------------------------------------------
CHANGELOG v3.9.1 (GPU + UI):

[G1] ThÃªm há»— trá»£ NVIDIA NVENC (h264_nvenc / hevc_nvenc / av1_nvenc).
     Tá»± fallback CPU náº¿u GPU/encoder khÃ´ng kháº£ dá»¥ng.
[G2] Fix giáº­t thanh tiáº¿n trÃ¬nh: chá»‰ váº½ láº¡i canvas % cá»§a task Ä‘ang cháº¡y,
     khÃ´ng rebuild toÃ n bá»™ file list má»—i láº§n update progress.
[G3] ThÆ° má»¥c xuáº¥t: cho phÃ©p gÃµ tay Ä‘Æ°á»ng dáº«n (Entry), thÃªm nÃºt "ðŸ“‚ Má»Ÿ"
     Ä‘á»ƒ má»Ÿ thÆ° má»¥c báº±ng trÃ¬nh quáº£n lÃ½ file cá»§a OS.

-------------------------------------------------------------------------------
CHANGELOG v3.9 (fix theo review cuá»‘i):

[F13] attached_pic khi bá»‹ Ã©p convert â†’ DROP thay vÃ¬ táº¡o track "video" giáº£.

CÃ¡c fix tá»« v2.7 â†’ v3.8 váº«n giá»¯ nguyÃªn.

-------------------------------------------------------------------------------
CHANGELOG BUILD/PACKAGING (v3.9.5-pack):

[P1] ThÃªm helper _app_base_dir() / _bundle_dir() / find_binary() /
     find_resource() Ä‘á»ƒ app tá»± tÃ¬m ffmpeg / ffprobe / icon.ico khi Ä‘Ã³ng gÃ³i
     PyInstaller (onedir hoáº·c onefile).
       - Æ¯u tiÃªn 1: cáº¡nh file EXE (onedir: cÃ¹ng folder vá»›i EXE).
       - Æ¯u tiÃªn 2: thÆ° má»¥c _internal / _MEIPASS (bundle PyInstaller).
       - Æ¯u tiÃªn 3: PATH cá»§a OS.
[P2] ConversionEngine.__init__ dÃ¹ng find_binary() Ä‘á»ƒ resolve ffmpeg/ffprobe.
[P3] VideoConverterUI tá»± set icon cá»­a sá»• tá»« icon.ico (cáº¡nh EXE hoáº·c bundle).
     Chá»‰ thÃªm UI setup, khÃ´ng Ä‘á»¥ng logic worker/engine.
[P4] Dark title bar trÃªn Windows 10/11 qua DwmSetWindowAttribute.
     Gá»i 2 láº§n (ngay + after 20ms) Ä‘á»ƒ Ä‘áº£m báº£o HWND Ä‘Ã£ sáºµn sÃ ng.
     TrÃªn OS khÃ¡c tá»± bá» qua im láº·ng. CHá»ˆ sá»­a UI, khÃ´ng Ä‘á»¥ng logic.
[P5] Nháº­n file/thÆ° má»¥c tá»« command line ("Open with...", kÃ©o tháº£ vÃ o exe).
     main() Ä‘á»c sys.argv[1:] vÃ  gá»i load_cli_args() sau khi UI khá»Ÿi Ä‘á»™ng.
     CHá»ˆ thÃªm task vÃ o danh sÃ¡ch, khÃ´ng Ä‘á»¥ng logic convert.
-------------------------------------------------------------------------------
"""

import json
import os
import queue
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
import uuid

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except ImportError:
    HAS_DND = False


# =============================================================================
# 0. FROZEN / RESOURCE PATH HELPERS  (PyInstaller packaging)
# =============================================================================

def _app_base_dir() -> Path:
    """ThÆ° má»¥c gá»‘c chá»©a app.

    - Frozen (PyInstaller): thÆ° má»¥c chá»©a file .exe.
      Onedir  â†’ dist/VideoConvertPro/  (chá»©a exe + _internal/)
      Onefile â†’ thÆ° má»¥c user cháº¡y exe (chá»‰ cÃ³ exe).
    - Dev: thÆ° má»¥c chá»©a script .py.
    """
    if getattr(sys, "frozen", False):
        try:
            return Path(sys.executable).resolve().parent
        except Exception:
            return Path(sys.executable).parent
    return Path(__file__).resolve().parent


def _bundle_dir() -> Optional[Path]:
    """ThÆ° má»¥c táº¡m PyInstaller giáº£i nÃ©n bundle (_MEIPASS).

    PyInstaller â‰¥ 5.x Ä‘áº·t _MEIPASS = .../_internal vá»›i onedir,
    vÃ  = thÆ° má»¥c _MEIxxxx vá»›i onefile. Tráº£ None náº¿u cháº¡y dev.
    """
    meipass = getattr(sys, "_MEIPASS", None)
    if not meipass:
        return None
    try:
        return Path(meipass)
    except Exception:
        return None


def _candidate_dirs() -> List[Path]:
    """Thá»© tá»± Æ°u tiÃªn tÃ¬m binary/resource:
        1. Cáº¡nh EXE (cho phÃ©p user drop thÃªm ffmpeg ngoÃ i cÃ¹ng folder).
        2. _MEIPASS / _internal (bundle PyInstaller).
    """
    dirs: List[Path] = []
    try:
        dirs.append(_app_base_dir())
    except Exception:
        pass
    bd = _bundle_dir()
    if bd is not None and bd not in dirs:
        dirs.append(bd)
    return dirs


def find_binary(name: str) -> str:
    """TÃ¬m binary (ffmpeg, ffprobe).

    Tráº£ absolute path náº¿u tÃ¬m tháº¥y, ngÆ°á»£c láº¡i tráº£ nguyÃªn `name` Ä‘á»ƒ OS
    tá»± resolve qua PATH.
    """
    exe_exts: Tuple[str, ...] = (".exe", "") if os.name == "nt" else ("",)
    for d in _candidate_dirs():
        for ext in exe_exts:
            candidate = d / f"{name}{ext}"
            try:
                if candidate.is_file():
                    return str(candidate)
            except OSError:
                continue
    return name


def find_resource(name: str) -> Optional[Path]:
    """TÃ¬m resource (icon, asset). Tráº£ Path náº¿u cÃ³, None náº¿u khÃ´ng."""
    for d in _candidate_dirs():
        candidate = d / name
        try:
            if candidate.is_file():
                return candidate
        except OSError:
            continue
    return None


# =============================================================================
# 1. CONSTANTS
# =============================================================================

APP_NAME = "Video Converter Pro"
APP_VERSION = "3.9.5"

VIDEO_EXTENSIONS = {
    ".mp4", ".m4v", ".mkv", ".mov", ".avi",
    ".ts", ".m2ts", ".mts", ".webm", ".flv",
    ".wmv", ".mpeg", ".mpg",
    ".vob", ".ogv", ".3gp", ".3g2", ".mxf",
    ".f4v", ".rm", ".rmvb", ".asf", ".divx",
    ".m2v", ".mp2v",
}

BASE_TOLERANCE_FLAGS = [
    "-fflags", "+genpts+igndts+discardcorrupt",
    "-err_detect", "ignore_err",
    "-max_error_rate", "1.0",
    "-analyzeduration", "200M",
    "-probesize", "200M",
]

AGGRESSIVE_TIMESTAMP_FLAGS = [
    "-start_at_zero",
    "-avoid_negative_ts", "make_zero",
]

CONTAINER_COMPAT = {
    "mp4": {
        "video_allowed": {"h264", "hevc", "mpeg4", "mpeg2video", "av1"},
        "video_default": "libx264",
        "audio_allowed": {"aac", "mp3", "ac3", "eac3", "alac"},
        "audio_default": "aac",
        "sub_allowed": {"mov_text"},
        "sub_default": "mov_text",
        "ext": "mp4",
    },
    "mkv": {
        "video_allowed": None,
        "video_default": "libx264",
        "audio_allowed": None,
        "audio_default": "aac",
        "sub_allowed": None,
        "sub_default": "srt",
        "ext": "mkv",
    },
    "webm": {
        "video_allowed": {"vp8", "vp9", "av1"},
        "video_default": "libvpx-vp9",
        "audio_allowed": {"vorbis", "opus"},
        "audio_default": "libopus",
        "sub_allowed": {"webvtt"},
        "sub_default": "webvtt",
        "ext": "webm",
    },
    "mov": {
        "video_allowed": {"h264", "hevc", "prores", "dnxhd", "mpeg4"},
        "video_default": "libx264",
        "audio_allowed": {
            "aac", "mp3", "ac3", "alac",
            "pcm_s16le", "pcm_s24le", "pcm_s16be",
        },
        "audio_default": "aac",
        "sub_allowed": {"mov_text"},
        "sub_default": "mov_text",
        "ext": "mov",
    },
    "avi": {
        "video_allowed": {"mpeg4", "mjpeg", "h264"},
        "video_default": "libx264",
        "audio_allowed": {"mp3", "ac3", "pcm_s16le"},
        "audio_default": "mp3",
        "sub_allowed": set(),
        "sub_default": None,
        "ext": "avi",
    },
    "ts": {
        "video_allowed": {"h264", "hevc", "mpeg2video"},
        "video_default": "libx264",
        "audio_allowed": {"aac", "ac3", "eac3", "mp3"},
        "audio_default": "aac",
        "sub_allowed": set(),
        "sub_default": None,
        "ext": "ts",
    },
}

# [U1] Map Container (label UI) â†’ danh sÃ¡ch codec video (label UI) há»£p lá»‡.
# CHá»ˆ dÃ¹ng Ä‘á»ƒ lá»c dropdown trÃªn UI. Logic engine váº«n dÃ¹ng CONTAINER_COMPAT.
CONTAINER_CODEC_UI_MAP = {
    "MP4":  ["H.264", "H.265 / HEVC", "AV1"],
    "MKV":  ["H.264", "H.265 / HEVC", "VP9", "AV1"],
    "WEBM": ["VP9", "AV1"],
    "MOV":  ["H.264", "H.265 / HEVC"],
    "AVI":  ["H.264"],
    "TS":   ["H.264", "H.265 / HEVC"],
}

DATA_STREAM_CONTAINERS = {"mkv", "ts"}

BITMAP_SUB_CODECS = {
    "hdmv_pgs_subtitle",
    "dvd_subtitle",
    "dvb_subtitle",
    "xsub",
}

TEXT_SUB_CODECS = {
    "srt", "subrip", "ass", "ssa",
    "webvtt", "mov_text", "microdvd",
}

EXPECTED_FORMATS = {
    "mp4": {"mp4", "mov", "m4a", "3gp", "3g2", "mj2"},
    "m4v": {"mp4", "mov", "m4a", "3gp", "3g2", "mj2"},
    "mov": {"mp4", "mov"},
    "mkv": {"matroska"},
    "webm": {"matroska", "webm"},
    "avi": {"avi"},
    "ts": {"mpegts"},
    "m2ts": {"mpegts"},
    "mts": {"mpegts"},
    "flv": {"flv"},
    "wmv": {"asf"},
    "mpeg": {"mpeg", "mpegvideo"},
    "mpg": {"mpeg", "mpegvideo"},
    "vob": {"mpeg", "mpegvideo", "mpegps"},
    "ogv": {"ogg"},
    "3gp": {"mp4", "3gp", "mov"},
    "3g2": {"mp4", "3gp", "mov"},
    "mxf": {"mxf"},
    "f4v": {"flv"},
    "rm": {"rm"},
    "rmvb": {"rm"},
    "asf": {"asf"},
    "divx": {"avi"},
    "m2v": {"mpegvideo"},
    "mp2v": {"mpegvideo"},
}

ENCODER_TO_CODEC_NAME = {
    "libx264": "h264",
    "libx265": "hevc",
    "libvpx-vp9": "vp9",
    "libaom-av1": "av1",
    # NVENC (NVIDIA GPU)
    "h264_nvenc": "h264",
    "hevc_nvenc": "hevc",
    "av1_nvenc": "av1",
}

# Map codec â†’ encoder NVENC tÆ°Æ¡ng á»©ng
NVENC_ENCODER_FOR_CODEC = {
    "h264": "h264_nvenc",
    "hevc": "hevc_nvenc",
    "h265": "hevc_nvenc",
    "av1": "av1_nvenc",
}

# Map preset libx264-style â†’ preset NVENC (p1..p7)
NVENC_PRESET_MAP = {
    "ultrafast": "p1",
    "veryfast": "p2",
    "fast": "p3",
    "medium": "p4",
    "slow": "p5",
    "slower": "p6",
    "veryslow": "p7",
}

LOSSLESS_AUDIO_CODECS = {
    "flac", "alac", "truehd", "mlp", "wavpack", "tta", "ape",
    "pcm_s16le", "pcm_s16be", "pcm_s24le", "pcm_s24be",
    "pcm_s32le", "pcm_s32be", "pcm_f32le", "pcm_f64le",
}

LOSSLESS_AUDIO_TARGET_BY_CONTAINER = {
    "mp4": "alac",
    "mov": "alac",
    "mkv": "flac",
    "avi": "pcm_s16le",
}

LOSSLESS_AUDIO_ENCODE_EXTRA: Dict[str, List[Tuple[str, str]]] = {
    "flac": [("compression_level", "8")],
    "alac": [],
    "pcm_s16le": [],
}

VIDEO_ENCODER_FALLBACK_ORDER = [
    "libx264", "libx265", "libvpx-vp9", "libaom-av1",
]

PIX_FMT_LEGACY_MAP = {
    "yuvj420p": "yuv420p",
    "yuvj422p": "yuv422p",
    "yuvj444p": "yuv444p",
}


# =============================================================================
# 2. ENUMS
# =============================================================================

class IssueType(Enum):
    TIMESTAMP = "timestamp"
    HEADER = "header"
    CONTAINER_MISMATCH = "container_mismatch"
    CODEC_MISMATCH = "codec_mismatch"
    CORRUPT_PACKETS = "corrupt_packets"
    TRUNCATED = "truncated"
    PROBE_WARNING = "probe_warning"


# =============================================================================
# 3. DATA MODELS
# =============================================================================

@dataclass
class VideoStream:
    index: int
    codec_type: str
    codec_name: str

    codec_long_name: str = ""
    profile: str = ""

    width: int = 0
    height: int = 0

    avg_frame_rate: str = ""
    r_frame_rate: str = ""

    bit_rate: int = 0

    sample_rate: int = 0
    channels: int = 0
    channel_layout: str = ""

    language: str = ""
    title: str = ""

    pix_fmt: str = ""
    color_range: str = ""
    color_space: str = ""
    color_transfer: str = ""
    color_primaries: str = ""

    bits_per_raw_sample: int = 0
    level: int = 0

    is_attached_pic: bool = False
    is_default: bool = False
    is_forced: bool = False
    is_commentary: bool = False
    is_hearing_impaired: bool = False

    duration: float = 0.0

    disposition: Dict = field(default_factory=dict)
    tags: Dict = field(default_factory=dict)


@dataclass
class VideoProbe:
    format_name: str = ""
    format_long_name: str = ""

    duration: float = 0.0
    size: int = 0
    bit_rate: int = 0

    streams: List[VideoStream] = field(default_factory=list)
    chapters_count: int = 0


@dataclass
class IssueReport:
    types: Set[IssueType] = field(default_factory=set)
    details: List[str] = field(default_factory=list)

    severity: str = "ok"
    detected_format: Optional[str] = None

    def has_any(self) -> bool:
        return bool(self.types)


@dataclass
class StreamAction:
    stream_index: int
    codec_type: str
    action: str
    reason: str

    target_codec: Optional[str] = None
    target_bitrate: Optional[str] = None

    audio_vbr_quality: Optional[str] = None
    audio_extra_indexed: List[Tuple[str, str]] = field(default_factory=list)

    extra_flags: List[str] = field(default_factory=list)


@dataclass
class ConversionPlan:
    target_container: str
    target_extension: str
    actions: List[StreamAction] = field(default_factory=list)

    @property
    def copy_count(self) -> int:
        return sum(1 for a in self.actions if a.action == "copy")

    @property
    def convert_count(self) -> int:
        return sum(1 for a in self.actions if a.action == "convert")

    @property
    def drop_count(self) -> int:
        return sum(1 for a in self.actions if a.action == "drop")

    @property
    def is_pure_remux(self) -> bool:
        if self.convert_count > 0:
            return False
        for a in self.actions:
            if a.action != "drop":
                continue
            if a.codec_type in {"video", "audio", "subtitle"}:
                return False
        return True

    @property
    def is_remux(self) -> bool:
        return self.convert_count == 0


@dataclass
class VideoConversionProfile:
    target_container: str = "mp4"

    video_mode: str = "auto"
    video_codec: str = "h264"

    video_crf: int = 17
    video_preset: str = "slow"

    audio_mode: str = "auto"
    audio_codec: str = ""
    audio_bitrate: str = ""

    subtitle_mode: str = "auto"

    keep_metadata: bool = True
    keep_chapters: bool = True

    keep_attachments: bool = False
    keep_data_streams: bool = False

    faststart: bool = True

    rate_cap_enabled: bool = True
    reprocess_completed: bool = False

    adaptive_crf: bool = True
    use_gpu: bool = True


@dataclass
class VideoConversionTask:
    source_path: Path

    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "Pending"
    progress: float = 0.0
    error_message: str = ""
    enabled: bool = True

    probe: Optional[VideoProbe] = None
    issue_report: IssueReport = field(default_factory=IssueReport)
    plan: Optional[ConversionPlan] = None

    used_tier: int = 0
    used_attempt: int = 0
    badge_type: str = ""

    dropped_streams: List[str] = field(default_factory=list)
    converted_streams: List[str] = field(default_factory=list)


# =============================================================================
# 4. UTILITY
# =============================================================================

def safe_int(value, default=0):
    try:
        if value in (None, "", "N/A"):
            return default
        return int(float(value))
    except Exception:
        return default


def safe_float(value, default=0.0):
    try:
        if value in (None, "", "N/A"):
            return default
        return float(value)
    except Exception:
        return default


def normalize_codec(codec) -> str:
    return (str(codec) if codec else "unknown").strip().lower()


def is_video_file(path: Path) -> bool:
    return path.suffix.lower() in VIDEO_EXTENSIONS


def format_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    if size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MB"
    return f"{size / (1024 * 1024 * 1024):.2f} GB"


def format_duration(seconds: float) -> str:
    try:
        s = int(max(0, seconds))
    except Exception:
        return "?"
    if s < 60:
        return f"{s}s"
    m, s = divmod(s, 60)
    if m < 60:
        return f"{m}m {s}s"
    h, m = divmod(m, 60)
    return f"{h}h {m}m"


def parse_fraction(value: str) -> float:
    if not value or value in ("0/0", "N/A"):
        return 0.0
    try:
        if "/" in value:
            a, b = value.split("/", 1)
            a, b = float(a), float(b)
            if b == 0:
                return 0.0
            return a / b
        return float(value)
    except Exception:
        return 0.0


def estimate_source_bpp(
    stream: "VideoStream",
    probe: "VideoProbe",
    all_streams: Optional[List["VideoStream"]] = None,
) -> float:
    fps = parse_fraction(stream.avg_frame_rate) or parse_fraction(stream.r_frame_rate)
    if fps <= 0:
        fps = 24.0
    pixels = stream.width * stream.height
    if pixels <= 0:
        return 0.0

    bitrate = stream.bit_rate

    if bitrate <= 0 and probe.bit_rate > 0:
        total = probe.bit_rate
        if all_streams:
            other_audio_bitrate = sum(
                (s.bit_rate or 0)
                for s in all_streams
                if s.index != stream.index and s.codec_type == "audio"
            )
            if other_audio_bitrate > 0:
                bitrate = max(0, total - other_audio_bitrate)
            else:
                bitrate = int(total * 0.85)
        else:
            bitrate = int(total * 0.85)

    if bitrate <= 0:
        return 0.0
    return bitrate / (pixels * fps)


def adaptive_crf(bpp: float, base_crf: int) -> int:
    if bpp <= 0:
        return base_crf
    if bpp >= 0.12:
        return base_crf - 3
    if bpp >= 0.08:
        return base_crf - 1
    if bpp <= 0.02:
        return base_crf + 3
    if bpp <= 0.04:
        return base_crf + 1
    return base_crf


def compute_rate_cap(
    stream: "VideoStream",
    probe: "VideoProbe",
) -> Tuple[Optional[str], Optional[str]]:
    source_bitrate = stream.bit_rate or probe.bit_rate
    if source_bitrate <= 0:
        return None, None
    floor_bps = 500_000
    cap_bps = max(int(source_bitrate * 1.5), floor_bps)
    maxrate = f"{cap_bps // 1000}k"
    bufsize = f"{(cap_bps * 2) // 1000}k"
    return maxrate, bufsize


def smart_lossy_audio_bitrate(channels: int) -> str:
    ch = channels if channels and channels > 0 else 2
    extra = max(0, ch - 2) * 96
    kbps = max(256, min(640, 256 + extra))
    return f"{kbps}k"


# =============================================================================
# 5. CONVERSION ENGINE
# =============================================================================

class ConversionEngine:

    def __init__(self, ffmpeg_path=None, ffprobe_path=None):
        # [P2] Tá»± resolve ffmpeg / ffprobe:
        #   - Æ°u tiÃªn file cáº¡nh EXE
        #   - sau Ä‘Ã³ tá»›i _internal/_MEIPASS (bundle PyInstaller)
        #   - cuá»‘i cÃ¹ng má»›i Ä‘á»ƒ OS tÃ¬m trong PATH
        self.ffmpeg = ffmpeg_path or find_binary("ffmpeg")
        self.ffprobe = ffprobe_path or find_binary("ffprobe")
        self._encoder_cache: Dict[str, bool] = {}
        self._pix_fmt_cache: Dict[str, bool] = {}
        self._muxer_cache: Dict[str, bool] = {}
        self._version_cache: Optional[Tuple[int, int]] = None
        self._nvenc_runtime_cache: Dict[str, bool] = {}

    def check_tools(self) -> Tuple[bool, str]:
        for name, exe in (("FFmpeg", self.ffmpeg), ("FFprobe", self.ffprobe)):
            try:
                result = subprocess.run(
                    [exe, "-version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=10,
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                )
                if result.returncode != 0:
                    return False, f"{name} khÃ´ng cháº¡y Ä‘Æ°á»£c."
            except Exception as exc:
                return False, f"KhÃ´ng tÃ¬m tháº¥y {name}: {exc}"
        return True, "FFmpeg / FFprobe OK."

    def _get_ffmpeg_version(self) -> Tuple[int, int]:
        if self._version_cache is not None:
            return self._version_cache
        version: Tuple[int, int] = (0, 0)
        try:
            result = subprocess.run(
                [self.ffmpeg, "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            m = re.search(
                r"ffmpeg\s+version\s+(\d+)\.(\d+)",
                result.stdout or "",
                re.IGNORECASE,
            )
            if m:
                version = (int(m.group(1)), int(m.group(2)))
        except Exception:
            pass
        self._version_cache = version
        return version

    def _fps_mode_flags(self, out_idx: int) -> List[str]:
        major, minor = self._get_ffmpeg_version()
        if (major, minor) != (0, 0) and (major, minor) < (5, 1):
            return [f"-vsync:v:{out_idx}", "0"]
        return [f"-fps_mode:v:{out_idx}", "passthrough"]

    def has_encoder(self, name: str) -> bool:
        if name in self._encoder_cache:
            return self._encoder_cache[name]
        available = False
        try:
            result = subprocess.run(
                [self.ffmpeg, "-hide_banner", "-encoders"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            available = bool(
                re.search(rf"\b{re.escape(name)}\b", result.stdout or "")
            )
        except Exception:
            available = False
        self._encoder_cache[name] = available
        return available

    def _nvenc_is_available(self, encoder: str) -> bool:
        """Kiá»ƒm tra NVENC thá»±c táº¿ má»™t láº§n vÃ  cache káº¿t quáº£ theo tá»«ng encoder."""
        if encoder in self._nvenc_runtime_cache:
            return self._nvenc_runtime_cache[encoder]
        if not self.has_encoder(encoder):
            self._nvenc_runtime_cache[encoder] = False
            return False
        command = [
            self.ffmpeg, "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", "color=c=black:s=64x64:d=0.1",
            "-frames:v", "1", "-an", "-c:v", encoder, "-f", "null", "-",
        ]
        available = False
        try:
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=15,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            available = result.returncode == 0
        except Exception:
            available = False
        self._nvenc_runtime_cache[encoder] = available
        return available

    def _pick_nvenc_encoder(
        self,
        requested_codec: str,
        allowed_codecs,
    ) -> Optional[str]:
        """Chá»n NVENC encoder phÃ¹ há»£p náº¿u GPU + codec kháº£ dá»¥ng."""
        codec_name_map = {
            "h264_nvenc": "h264",
            "hevc_nvenc": "hevc",
            "av1_nvenc": "av1",
        }

        def _ok(enc: str) -> bool:
            if not self._nvenc_is_available(enc):
                return False
            cname = codec_name_map[enc]
            return allowed_codecs is None or cname in allowed_codecs

        if requested_codec:
            nvenc = NVENC_ENCODER_FOR_CODEC.get(requested_codec)
            if nvenc and _ok(nvenc):
                return nvenc
            return None

        # Auto: thá»­ láº§n lÆ°á»£t h264 â†’ hevc â†’ av1
        for enc in ("h264_nvenc", "hevc_nvenc", "av1_nvenc"):
            if _ok(enc):
                return enc
        return None

    def has_muxer(self, name: str) -> bool:
        if name in self._muxer_cache:
            return self._muxer_cache[name]
        available = False
        try:
            result = subprocess.run(
                [self.ffmpeg, "-hide_banner", "-muxers"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            available = bool(
                re.search(
                    rf"^\s*\S+\s+{re.escape(name)}\b",
                    result.stdout or "",
                    re.MULTILINE | re.IGNORECASE,
                )
            )
        except Exception:
            available = False
        self._muxer_cache[name] = available
        return available

    def encoder_supports_pix_fmt(self, encoder: str, pix_fmt: str) -> bool:
        if not encoder or not pix_fmt:
            return False

        normalized_pix_fmt = PIX_FMT_LEGACY_MAP.get(
            pix_fmt.lower(), pix_fmt.lower(),
        )

        key = f"{encoder}|{normalized_pix_fmt}"
        if key in self._pix_fmt_cache:
            return self._pix_fmt_cache[key]

        supported = False
        try:
            result = subprocess.run(
                [self.ffmpeg, "-hide_banner", "-h", f"encoder={encoder}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=5,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )

            lines = (result.stdout or "").splitlines()
            formats: Set[str] = set()

            for i, line in enumerate(lines):
                if not re.search(
                    r"Supported pixel formats:",
                    line,
                    re.IGNORECASE,
                ):
                    continue

                formats.update(line.split(":", 1)[1].split())

                for next_line in lines[i + 1:]:
                    if not next_line.strip() or not next_line[0].isspace():
                        break
                    stripped = next_line.strip()
                    if stripped.startswith("-"):
                        break
                    formats.update(stripped.split())

                break

            normalized_formats = {
                PIX_FMT_LEGACY_MAP.get(fmt.lower(), fmt.lower())
                for fmt in formats
            }

            supported = normalized_pix_fmt in normalized_formats

        except Exception:
            supported = False

        self._pix_fmt_cache[key] = supported
        return supported

    def is_lossless_audio(self, codec_name: str) -> bool:
        return (codec_name or "").lower() in LOSSLESS_AUDIO_CODECS

    def plan_audio_target(
        self,
        stream: VideoStream,
        target_container: str,
        profile: VideoConversionProfile,
    ) -> Tuple[str, Optional[str], Optional[str], List[Tuple[str, str]], str]:
        compat = CONTAINER_COMPAT.get(target_container, CONTAINER_COMPAT["mp4"])

        if profile.audio_codec:
            allowed = compat.get("audio_allowed")
            if allowed is None or profile.audio_codec in allowed:
                if self.has_encoder(profile.audio_codec):
                    bitrate: Optional[str] = profile.audio_bitrate or None
                    if self.is_lossless_audio(profile.audio_codec):
                        bitrate = None
                    return (
                        profile.audio_codec, bitrate, None, [],
                        "NgÆ°á»i dÃ¹ng chá»‰ Ä‘á»‹nh codec audio.",
                    )

        source_is_lossless = self.is_lossless_audio(stream.codec_name)

        if source_is_lossless:
            lossless_codec = LOSSLESS_AUDIO_TARGET_BY_CONTAINER.get(target_container)
            if lossless_codec and self.has_encoder(lossless_codec):
                extra = LOSSLESS_AUDIO_ENCODE_EXTRA.get(lossless_codec, [])
                return (
                    lossless_codec, None, None, extra,
                    f"Nguá»“n lossless â†’ giá»¯ lossless ({lossless_codec}).",
                )
            downgrade_prefix = (
                f"Nguá»“n lossless nhÆ°ng {target_container} khÃ´ng cÃ³ "
                f"codec lossless kháº£ dá»¥ng â†’ háº¡ xuá»‘ng lossy cháº¥t lÆ°á»£ng cao nháº¥t: "
            )
        else:
            downgrade_prefix = ""

        if target_container == "webm":
            bitrate = smart_lossy_audio_bitrate(stream.channels)
            return (
                "libopus", bitrate, None, [("vbr", "on")],
                downgrade_prefix + f"Opus VBR cháº¥t lÆ°á»£ng cao (~{bitrate}).",
            )

        if target_container == "avi":
            return (
                "libmp3lame", None, "0", [],
                downgrade_prefix + "MP3 VBR cháº¥t lÆ°á»£ng cao nháº¥t (-q:a 0).",
            )

        if self.has_encoder("libfdk_aac"):
            return (
                "libfdk_aac", None, "5", [],
                downgrade_prefix + "AAC VBR cháº¥t lÆ°á»£ng cao nháº¥t (libfdk_aac, tÆ°Æ¡ng Ä‘Æ°Æ¡ng chuáº©n Apple).",
            )

        target_bitrate = profile.audio_bitrate or smart_lossy_audio_bitrate(
            stream.channels
        )
        return (
            "aac", target_bitrate, None, [],
            downgrade_prefix
            + f"AAC cháº¥t lÆ°á»£ng cao (FFmpeg AAC gá»‘c, CBR co giÃ£n theo kÃªnh: {target_bitrate}).",
        )

    def run_ffprobe_raw(self, source: Path, analyze_time="10M"):
        cmd = [
            self.ffprobe, "-hide_banner",
            "-print_format", "json",
            "-show_error", "-show_format", "-show_streams", "-show_chapters",
            "-analyzeduration", analyze_time,
            "-probesize", analyze_time,
            str(source),
        ]
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                errors="replace",
                timeout=60,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            if result.stdout:
                try:
                    return json.loads(result.stdout), result.stderr or ""
                except json.JSONDecodeError:
                    pass
            return None, result.stderr or ""
        except subprocess.TimeoutExpired:
            return None, "FFprobe timeout."
        except Exception as exc:
            return None, str(exc)

    def lenient_probe(self, source: Path) -> Tuple[Optional[VideoProbe], IssueReport]:
        report = IssueReport()

        data, stderr = self.run_ffprobe_raw(source, "10M")

        if not data:
            data, stderr2 = self.run_ffprobe_raw(source, "200M")
            stderr += "\n" + stderr2
            if data:
                report.types.add(IssueType.HEADER)
                report.details.append("Probe cáº§n má»©c phÃ¢n tÃ­ch 200M.")

        if not data:
            report.types.add(IssueType.HEADER)
            report.severity = "critical"
            report.details.append("KhÃ´ng thá»ƒ Ä‘á»c metadata báº±ng FFprobe.")
            if stderr.strip():
                report.details.append(stderr.strip()[-1500:])
            return None, report

        format_info = data.get("format", {})
        streams_info = data.get("streams", [])

        streams: List[VideoStream] = []
        for raw in streams_info:
            disposition = raw.get("disposition", {}) or {}
            tags = raw.get("tags", {}) or {}

            codec_type = raw.get("codec_type", "unknown")
            codec_name = normalize_codec(raw.get("codec_name", "unknown"))

            title = str(tags.get("title", ""))
            language = str(tags.get("language", "")).lower()
            title_lower = title.lower()

            stream = VideoStream(
                index=safe_int(raw.get("index"), 0),
                codec_type=codec_type,
                codec_name=codec_name,
                codec_long_name=str(raw.get("codec_long_name", "")),
                profile=str(raw.get("profile", "")),
                width=safe_int(raw.get("width"), 0),
                height=safe_int(raw.get("height"), 0),
                avg_frame_rate=str(raw.get("avg_frame_rate", "")),
                r_frame_rate=str(raw.get("r_frame_rate", "")),
                bit_rate=safe_int(raw.get("bit_rate"), 0),
                sample_rate=safe_int(raw.get("sample_rate"), 0),
                channels=safe_int(raw.get("channels"), 0),
                channel_layout=str(raw.get("channel_layout", "")),
                language=language,
                title=title,
                pix_fmt=str(raw.get("pix_fmt", "")),
                color_range=str(raw.get("color_range", "")),
                color_space=str(raw.get("color_space", "")),
                color_transfer=str(raw.get("color_transfer", "")),
                color_primaries=str(raw.get("color_primaries", "")),
                bits_per_raw_sample=safe_int(raw.get("bits_per_raw_sample"), 0),
                level=safe_int(raw.get("level"), 0),
                is_attached_pic=bool(disposition.get("attached_pic", 0)),
                is_default=bool(disposition.get("default", 0)),
                is_forced=bool(disposition.get("forced", 0)),
                is_commentary=(
                    bool(disposition.get("comment", 0))
                    or "commentary" in title_lower
                ),
                is_hearing_impaired=bool(disposition.get("hearing_impaired", 0)),
                duration=safe_float(
                    raw.get("duration"),
                    safe_float(format_info.get("duration"), 0.0),
                ),
                disposition=disposition,
                tags=tags,
            )
            streams.append(stream)

        probe = VideoProbe(
            format_name=str(format_info.get("format_name", "")),
            format_long_name=str(format_info.get("format_long_name", "")),
            duration=safe_float(format_info.get("duration"), 0.0),
            size=safe_int(format_info.get("size"), 0),
            bit_rate=safe_int(format_info.get("bit_rate"), 0),
            streams=streams,
            chapters_count=len(data.get("chapters", [])),
        )

        ext = source.suffix.lower().lstrip(".")
        real_format = probe.format_name.lower().split(",")[0]

        expected = EXPECTED_FORMATS.get(ext)
        if expected and real_format and real_format not in expected:
            report.types.add(IssueType.CONTAINER_MISMATCH)
            report.detected_format = real_format
            report.details.append(
                f"Extension .{ext} nhÆ°ng container thá»±c táº¿ lÃ  {real_format}."
            )

        if not probe.streams:
            report.types.add(IssueType.HEADER)
            report.severity = "critical"
            report.details.append("KhÃ´ng tÃ¬m tháº¥y stream.")
            return probe, report

        if not any(
            s.codec_type == "video" and not s.is_attached_pic
            for s in probe.streams
        ):
            report.types.add(IssueType.HEADER)
            report.details.append("KhÃ´ng tÃ¬m tháº¥y video chÃ­nh.")

        if probe.duration <= 0:
            report.types.add(IssueType.TRUNCATED)
            report.details.append("Duration báº±ng 0 hoáº·c header báº¥t thÆ°á»ng.")

        if stderr.strip():
            lower = stderr.lower()
            corruption_words = (
                "corrupt", "invalid nal", "decode error",
                "error while decoding", "missing reference",
                "packet corrupt", "invalid data", "truncat",
            )
            if any(w in lower for w in corruption_words):
                report.types.add(IssueType.CORRUPT_PACKETS)
                report.details.append(
                    "FFprobe phÃ¡t hiá»‡n dáº¥u hiá»‡u packet/decode báº¥t thÆ°á»ng."
                )

        if report.has_any() and report.severity == "ok":
            report.severity = "warning"

        return probe, report

    def choose_primary_video(self, streams: List[VideoStream]) -> Optional[VideoStream]:
        candidates = [
            s for s in streams
            if (
                s.codec_type == "video"
                and not s.is_attached_pic
                and s.width > 0
                and s.height > 0
            )
        ]
        if not candidates:
            return None
        candidates.sort(
            key=lambda s: (
                s.width * s.height,
                1 if s.is_default else 0,
                s.bit_rate,
                -s.index,
            ),
            reverse=True,
        )
        return candidates[0]

    def choose_primary_audio(self, streams: List[VideoStream]) -> Optional[VideoStream]:
        candidates = [s for s in streams if s.codec_type == "audio"]
        if not candidates:
            return None
        candidates.sort(
            key=lambda s: (
                1 if s.is_default else 0,
                0 if s.is_commentary else 1,
                0 if s.is_hearing_impaired else 1,
                s.channels,
                s.bit_rate,
                -s.index,
            ),
            reverse=True,
        )
        return candidates[0]

    def stream_is_junk(
        self,
        stream: VideoStream,
        profile: VideoConversionProfile,
    ) -> Tuple[bool, str]:
        if stream.is_attached_pic:
            if not profile.keep_attachments:
                return True, "Cover art / attached picture."
            return False, ""

        if stream.codec_type == "data":
            if not profile.keep_data_streams:
                return True, "Data stream khÃ´ng cáº§n thiáº¿t."
            return False, ""

        if stream.codec_type == "unknown":
            if not profile.keep_data_streams:
                if stream.codec_name in {
                    "unknown", "bin_data", "scte_35",
                    "timed_id3", "epg", "null",
                }:
                    return True, f"Unknown data codec: {stream.codec_name}"
            return False, ""

        return False, ""

    def map_codec_to_encoder(self, codec: str, fallback="libx264") -> str:
        codec = (codec or "").lower()
        if codec in {"h264", "libx264"}:
            return "libx264"
        if codec in {"hevc", "h265", "libx265"}:
            return "libx265"
        if codec in {"vp9", "libvpx-vp9"}:
            return "libvpx-vp9"
        if codec in {"av1", "libaom-av1"}:
            return "libaom-av1"
        return fallback

    def target_video_encoder(
        self,
        profile: VideoConversionProfile,
        target_container: str,
    ) -> Tuple[str, str]:
        compat = CONTAINER_COMPAT.get(
            target_container, CONTAINER_COMPAT["mp4"],
        )
        allowed = compat.get("video_allowed")
        requested = (profile.video_codec or "").lower()

        # [GPU] Æ¯u tiÃªn NVENC khi user báº­t vÃ  GPU kháº£ dá»¥ng.
        if getattr(profile, "use_gpu", False):
            nvenc = self._pick_nvenc_encoder(requested, allowed)
            if nvenc:
                return nvenc, "GPU NVENC"

        if requested in {"h264", "hevc", "h265", "vp9", "av1"}:
            encoder = self.map_codec_to_encoder(requested)
            codec_name = ENCODER_TO_CODEC_NAME.get(encoder, "")
            container_ok = allowed is None or codec_name in allowed
            if container_ok and self.has_encoder(encoder):
                return encoder, ""
            if not container_ok:
                why = f"{target_container} khÃ´ng há»— trá»£ {codec_name}"
            else:
                why = f"FFmpeg hiá»‡n táº¡i thiáº¿u encoder {encoder}"
            for fb_encoder in VIDEO_ENCODER_FALLBACK_ORDER:
                fb_codec_name = ENCODER_TO_CODEC_NAME.get(fb_encoder, "")
                if (allowed is None or fb_codec_name in allowed) and self.has_encoder(fb_encoder):
                    return fb_encoder, (
                        f"{why} â†’ dÃ¹ng {fb_codec_name} thay cho "
                        f"{requested} báº¡n Ä‘Ã£ chá»n."
                    )
            default_encoder = compat.get("video_default", "libx264")
            return default_encoder, (
                f"{why} â†’ dÃ¹ng {default_encoder} thay cho {requested} báº¡n Ä‘Ã£ chá»n."
            )

        for encoder in VIDEO_ENCODER_FALLBACK_ORDER:
            codec_name = ENCODER_TO_CODEC_NAME.get(encoder, "")
            if (allowed is None or codec_name in allowed) and self.has_encoder(encoder):
                return encoder, ""

        return compat.get("video_default", "libx264"), ""

    def choose_pix_fmt(self, stream: VideoStream, encoder: str) -> Optional[str]:
        pix = (stream.pix_fmt or "").lower()
        if not pix:
            return None

        normalized_pix = PIX_FMT_LEGACY_MAP.get(pix, pix)

        if self.encoder_supports_pix_fmt(encoder, normalized_pix):
            return normalized_pix

        return None

    def _preset_flags_for_encoder(
        self,
        encoder: str,
        user_preset: str,
        out_idx: int,
    ) -> List[str]:
        if encoder in {"h264_nvenc", "hevc_nvenc", "av1_nvenc"}:
            preset = NVENC_PRESET_MAP.get(user_preset, "p4")
            return [
                f"-preset:v:{out_idx}", preset,
                f"-tune:v:{out_idx}", "hq",
            ]

        if encoder in {"libx264", "libx265"}:
            return [f"-preset:v:{out_idx}", user_preset]

        if encoder == "libvpx-vp9":
            mapping = {
                "ultrafast": ("realtime", "8"),
                "veryfast":  ("realtime", "6"),
                "fast":      ("good",     "5"),
                "medium":    ("good",     "3"),
                "slow":      ("good",     "2"),
                "slower":    ("good",     "1"),
                "veryslow":  ("best",     "0"),
            }
            deadline, cpu_used = mapping.get(user_preset, mapping["medium"])
            return [
                f"-deadline:v:{out_idx}", deadline,
                f"-cpu-used:v:{out_idx}", cpu_used,
            ]

        if encoder == "libaom-av1":
            mapping = {
                "ultrafast": "8",
                "veryfast":  "7",
                "fast":      "6",
                "medium":    "5",
                "slow":      "3",
                "slower":    "2",
                "veryslow":  "0",
            }
            cpu_used = mapping.get(user_preset, mapping["medium"])
            return [f"-cpu-used:v:{out_idx}", cpu_used]

        return []

    def build_video_encode_flags(
        self,
        out_idx: int,
        src: VideoStream,
        encoder: str,
        profile: VideoConversionProfile,
        probe: VideoProbe,
        base_crf_max: int = 22,
    ) -> List[str]:
        flags: List[str] = [f"-c:v:{out_idx}", encoder]

        if profile.adaptive_crf:
            bpp = estimate_source_bpp(src, probe, probe.streams)
            crf = adaptive_crf(bpp, int(profile.video_crf))
            crf = max(14, min(crf, base_crf_max))
        else:
            crf = int(profile.video_crf)

        if encoder in {"h264_nvenc", "hevc_nvenc", "av1_nvenc"}:
            # NVENC: dÃ¹ng -rc vbr + -cq (constant quality), -b:v 0 = quality mode.
            flags += [f"-rc:v:{out_idx}", "vbr"]
            flags += [f"-cq:v:{out_idx}", str(crf)]
            flags += [f"-b:v:{out_idx}", "0"]
            flags += self._preset_flags_for_encoder(
                encoder, profile.video_preset, out_idx,
            )
            if profile.rate_cap_enabled:
                maxrate, bufsize = compute_rate_cap(src, probe)
                if maxrate and bufsize:
                    flags += [
                        f"-maxrate:v:{out_idx}", maxrate,
                        f"-bufsize:v:{out_idx}", bufsize,
                    ]
        elif encoder in {"libvpx-vp9", "libaom-av1"}:
            if profile.rate_cap_enabled:
                maxrate, bufsize = compute_rate_cap(src, probe)
                if maxrate and bufsize:
                    flags += [f"-b:v:{out_idx}", maxrate]
                    flags += [
                        f"-maxrate:v:{out_idx}", maxrate,
                        f"-bufsize:v:{out_idx}", bufsize,
                    ]
                else:
                    flags += [f"-b:v:{out_idx}", "0"]
            else:
                flags += [f"-b:v:{out_idx}", "0"]
            flags += [f"-crf:v:{out_idx}", str(crf)]
            flags += self._preset_flags_for_encoder(
                encoder, profile.video_preset, out_idx,
            )
        else:
            flags += [f"-crf:v:{out_idx}", str(crf)]
            flags += self._preset_flags_for_encoder(
                encoder, profile.video_preset, out_idx,
            )
            if profile.rate_cap_enabled:
                maxrate, bufsize = compute_rate_cap(src, probe)
                if maxrate and bufsize:
                    flags += [
                        f"-maxrate:v:{out_idx}", maxrate,
                        f"-bufsize:v:{out_idx}", bufsize,
                    ]

        pix_fmt = self.choose_pix_fmt(src, encoder)
        if pix_fmt:
            flags += [f"-pix_fmt:v:{out_idx}", pix_fmt]

        if src.color_range:
            flags += [f"-color_range:v:{out_idx}", src.color_range]
        if src.color_space:
            flags += [f"-colorspace:v:{out_idx}", src.color_space]
        if src.color_transfer:
            flags += [f"-color_trc:v:{out_idx}", src.color_transfer]
        if src.color_primaries:
            flags += [f"-color_primaries:v:{out_idx}", src.color_primaries]

        flags += self._fps_mode_flags(out_idx)

        return flags

    def get_current_action(
        self,
        plan: ConversionPlan,
        stream_index: int,
        overrides: Dict[int, str],
    ) -> Optional[str]:
        if stream_index in overrides:
            return overrides[stream_index]
        for action in plan.actions:
            if action.stream_index == stream_index:
                return action.action
        return None

    def build_conversion_plan(
        self,
        probe: VideoProbe,
        profile: VideoConversionProfile,
        overrides: Optional[Dict[int, str]] = None,
    ) -> ConversionPlan:
        overrides = overrides or {}
        target = profile.target_container.lower()
        compat = CONTAINER_COMPAT.get(target, CONTAINER_COMPAT["mp4"])

        actions: List[StreamAction] = []
        primary_video = self.choose_primary_video(probe.streams)
        primary_audio = self.choose_primary_audio(probe.streams)

        for stream in probe.streams:

            if stream.index not in overrides:
                junk, junk_reason = self.stream_is_junk(stream, profile)
                if junk:
                    actions.append(StreamAction(
                        stream.index, stream.codec_type, "drop", junk_reason,
                    ))
                    continue

            if stream.index in overrides:
                forced = overrides[stream.index]

                if forced == "drop":
                    if stream.codec_type == "video" and stream is primary_video:
                        forced = "convert"
                    elif stream.codec_type == "audio" and stream is primary_audio:
                        forced = "convert"
                    else:
                        actions.append(StreamAction(
                            stream.index, stream.codec_type, "drop",
                            "Fallback: DROP",
                        ))
                        continue

                if forced == "convert":
                    # F13: attached_pic bá»‹ Ã©p convert â†’ DROP.
                    # ffprobe bÃ¡o codec_type="video" cho cover art, nÃªn
                    # náº¿u khÃ´ng check is_attached_pic trÆ°á»›c, code sáº½ rÆ¡i
                    # vÃ o nhÃ¡nh video convert bÃªn dÆ°á»›i vÃ  táº¡o track
                    # "video" giáº£ khÃ´ng cÃ³ disposition attached_pic.
                    # Cover art lÃ  phá»¥ â€” há»ng thÃ¬ drop, khÃ´ng Ä‘Ã¡ng convert.
                    if stream.is_attached_pic:
                        actions.append(StreamAction(
                            stream.index, "attachment", "drop",
                            "Cover art khÃ´ng cÃ²n giá»¯ Ä‘Æ°á»£c (fallback).",
                        ))
                        continue

                    if stream.codec_type == "video":
                        v_encoder, v_note = self.target_video_encoder(profile, target)
                        actions.append(StreamAction(
                            stream.index, "video", "convert",
                            "Fallback: video CONVERT" + (f" â€” {v_note}" if v_note else ""),
                            target_codec=v_encoder,
                        ))
                    elif stream.codec_type == "audio":
                        codec, bitrate, vbr_q, extra_idx, reason = (
                            self.plan_audio_target(stream, target, profile)
                        )
                        actions.append(StreamAction(
                            stream.index, "audio", "convert",
                            f"Fallback: audio CONVERT â€” {reason}",
                            target_codec=codec,
                            target_bitrate=bitrate,
                            audio_vbr_quality=vbr_q,
                            audio_extra_indexed=extra_idx,
                        ))
                    elif stream.codec_type == "subtitle":
                        if compat["sub_default"]:
                            actions.append(StreamAction(
                                stream.index, "subtitle", "convert",
                                "Fallback: subtitle CONVERT",
                                target_codec=compat["sub_default"],
                            ))
                        else:
                            actions.append(StreamAction(
                                stream.index, "subtitle", "drop",
                                "Fallback: subtitle DROP",
                            ))
                    else:
                        actions.append(StreamAction(
                            stream.index, stream.codec_type, "drop",
                            "Fallback: DROP (unknown type)",
                        ))
                    continue

            if stream.is_attached_pic:
                if profile.keep_attachments:
                    actions.append(StreamAction(
                        stream.index, "attachment", "copy",
                        "Cover art giá»¯ nguyÃªn.",
                    ))
                continue

            if stream.codec_type == "video":
                if profile.video_mode == "reencode":
                    v_encoder, v_note = self.target_video_encoder(profile, target)
                    actions.append(StreamAction(
                        stream.index, "video", "convert",
                        "User chá»n Force Re-encode" + (f" â€” {v_note}" if v_note else ""),
                        target_codec=v_encoder,
                    ))
                    continue

                if profile.video_mode == "copy":
                    actions.append(StreamAction(
                        stream.index, "video", "copy",
                        "User chá»n Force Copy",
                    ))
                    continue

                allowed = compat["video_allowed"]
                compatible = (allowed is None or stream.codec_name in allowed)
                if compatible:
                    actions.append(StreamAction(
                        stream.index, "video", "copy",
                        "Video codec tÆ°Æ¡ng thÃ­ch.",
                    ))
                else:
                    v_encoder, v_note = self.target_video_encoder(profile, target)
                    reason = f"Codec {stream.codec_name} khÃ´ng tÆ°Æ¡ng thÃ­ch {target}."
                    if v_note:
                        reason += f" {v_note}"
                    actions.append(StreamAction(
                        stream.index, "video", "convert",
                        reason,
                        target_codec=v_encoder,
                    ))
                continue

            if stream.codec_type == "audio":
                if profile.audio_mode == "reencode":
                    codec, bitrate, vbr_q, extra_idx, reason = (
                        self.plan_audio_target(stream, target, profile)
                    )
                    actions.append(StreamAction(
                        stream.index, "audio", "convert",
                        f"User chá»n Force Re-encode â€” {reason}",
                        target_codec=codec,
                        target_bitrate=bitrate,
                        audio_vbr_quality=vbr_q,
                        audio_extra_indexed=extra_idx,
                    ))
                    continue

                if profile.audio_mode == "copy":
                    actions.append(StreamAction(
                        stream.index, "audio", "copy",
                        "User chá»n Force Copy",
                    ))
                    continue

                allowed = compat["audio_allowed"]
                compatible = (allowed is None or stream.codec_name in allowed)
                if compatible:
                    actions.append(StreamAction(
                        stream.index, "audio", "copy",
                        "Audio codec tÆ°Æ¡ng thÃ­ch.",
                    ))
                else:
                    codec, bitrate, vbr_q, extra_idx, reason = (
                        self.plan_audio_target(stream, target, profile)
                    )
                    actions.append(StreamAction(
                        stream.index, "audio", "convert",
                        f"Codec {stream.codec_name} khÃ´ng tÆ°Æ¡ng thÃ­ch {target}. {reason}",
                        target_codec=codec,
                        target_bitrate=bitrate,
                        audio_vbr_quality=vbr_q,
                        audio_extra_indexed=extra_idx,
                    ))
                continue

            if stream.codec_type == "subtitle":
                if profile.subtitle_mode == "drop":
                    actions.append(StreamAction(
                        stream.index, "subtitle", "drop",
                        "Subtitle mode = DROP.",
                    ))
                    continue

                allowed = compat["sub_allowed"]

                if allowed is not None and len(allowed) == 0:
                    actions.append(StreamAction(
                        stream.index, "subtitle", "drop",
                        f"{target} khÃ´ng há»— trá»£ subtitle.",
                    ))
                    continue

                if stream.codec_name in BITMAP_SUB_CODECS:
                    if target == "mkv":
                        actions.append(StreamAction(
                            stream.index, "subtitle", "copy",
                            "Bitmap subtitle giá»¯ nguyÃªn trong MKV.",
                        ))
                    else:
                        actions.append(StreamAction(
                            stream.index, "subtitle", "drop",
                            f"Bitmap subtitle {stream.codec_name} khÃ´ng phÃ¹ há»£p {target}.",
                        ))
                    continue

                if allowed is None or stream.codec_name in allowed:
                    actions.append(StreamAction(
                        stream.index, "subtitle", "copy",
                        "Subtitle codec tÆ°Æ¡ng thÃ­ch.",
                    ))
                    continue

                if stream.codec_name in TEXT_SUB_CODECS:
                    if compat["sub_default"]:
                        actions.append(StreamAction(
                            stream.index, "subtitle", "convert",
                            "Text subtitle convert.",
                            target_codec=compat["sub_default"],
                        ))
                    else:
                        actions.append(StreamAction(
                            stream.index, "subtitle", "drop",
                            "KhÃ´ng cÃ³ subtitle encoder phÃ¹ há»£p.",
                        ))
                    continue

                actions.append(StreamAction(
                    stream.index, "subtitle", "drop",
                    "Subtitle codec khÃ´ng tÆ°Æ¡ng thÃ­ch.",
                ))
                continue

            if stream.codec_type == "data":
                if profile.keep_data_streams and target in DATA_STREAM_CONTAINERS:
                    actions.append(StreamAction(
                        stream.index, "data", "copy",
                        f"Data stream giá»¯ nguyÃªn trong {target}.",
                    ))
                else:
                    reason = (
                        "Data stream khÃ´ng cáº§n thiáº¿t."
                        if not profile.keep_data_streams
                        else f"{target} khÃ´ng há»— trá»£ data stream."
                    )
                    actions.append(StreamAction(
                        stream.index, "data", "drop", reason,
                    ))
                continue

            actions.append(StreamAction(
                stream.index, stream.codec_type, "drop",
                f"Stream type '{stream.codec_type}' khÃ´ng Ä‘Æ°á»£c há»— trá»£.",
            ))

        active_video = [
            a for a in actions
            if a.codec_type == "video" and a.action != "drop"
        ]
        if not active_video and primary_video:
            v_encoder, v_note = self.target_video_encoder(profile, target)
            actions.append(StreamAction(
                primary_video.index, "video", "convert",
                "Báº£o vá»‡ video chÃ­nh." + (f" {v_note}" if v_note else ""),
                target_codec=v_encoder,
            ))

        return ConversionPlan(
            target_container=target,
            target_extension=compat["ext"],
            actions=actions,
        )

    def build_ffmpeg_command(
        self,
        source: Path,
        plan: ConversionPlan,
        temp_output: Path,
        profile: VideoConversionProfile,
        probe: VideoProbe,
        tolerance_level: int = 1,
    ) -> List[str]:

        cmd = [self.ffmpeg, "-hide_banner", "-nostdin"]
        cmd += BASE_TOLERANCE_FLAGS

        if tolerance_level >= 2:
            cmd += AGGRESSIVE_TIMESTAMP_FLAGS

        cmd += ["-ignore_unknown", "-y", "-i", str(source)]

        source_streams: Dict[int, VideoStream] = {
            s.index: s for s in probe.streams
        }

        out_video_idx = 0
        out_audio_idx = 0
        out_sub_idx = 0
        out_data_idx = 0

        video_convert_specs: List[Tuple[int, VideoStream, str]] = []

        for action in plan.actions:
            if action.action == "drop":
                continue

            cmd += ["-map", f"0:{action.stream_index}"]

            if action.codec_type == "video":
                out = out_video_idx
                out_video_idx += 1

                if action.action == "copy":
                    cmd += [f"-c:v:{out}", "copy"]
                else:
                    src = source_streams.get(action.stream_index)
                    encoder = action.target_codec or "libx264"
                    if src is None:
                        cmd += [f"-c:v:{out}", encoder]
                    else:
                        video_convert_specs.append((out, src, encoder))

            elif action.codec_type == "audio":
                out = out_audio_idx
                out_audio_idx += 1

                if action.action == "copy":
                    cmd += [f"-c:a:{out}", "copy"]
                else:
                    cmd += [f"-c:a:{out}", action.target_codec or "aac"]
                    if action.audio_vbr_quality is not None:
                        cmd += [f"-q:a:{out}", action.audio_vbr_quality]
                    elif action.target_bitrate:
                        cmd += [f"-b:a:{out}", action.target_bitrate]
                    for flag_name, flag_val in action.audio_extra_indexed:
                        cmd += [f"-{flag_name}:a:{out}", flag_val]

            elif action.codec_type == "subtitle":
                out = out_sub_idx
                out_sub_idx += 1

                if action.action == "copy":
                    cmd += [f"-c:s:{out}", "copy"]
                else:
                    cmd += [f"-c:s:{out}", action.target_codec or "mov_text"]

            elif action.codec_type == "attachment":
                out = out_video_idx
                out_video_idx += 1
                cmd += [f"-c:v:{out}", "copy"]
                cmd += [f"-disposition:v:{out}", "attached_pic"]
                for flag in action.extra_flags:
                    cmd.append(flag)

            elif action.codec_type == "data":
                out = out_data_idx
                out_data_idx += 1
                if action.action == "copy":
                    cmd += [f"-c:d:{out}", "copy"]

        for out_idx, src, encoder in video_convert_specs:
            cmd += self.build_video_encode_flags(
                out_idx=out_idx,
                src=src,
                encoder=encoder,
                profile=profile,
                probe=probe,
                base_crf_max=22,
            )

        cmd += [
            "-map_metadata", "0" if profile.keep_metadata else "-1",
            "-map_chapters", "0" if profile.keep_chapters else "-1",
        ]

        if plan.target_container in {"mp4", "mov"} and profile.faststart:
            cmd += ["-movflags", "+faststart"]

        cmd += ["-max_muxing_queue_size", "8192"]

        cmd.append(str(temp_output))
        return cmd

    def build_emergency_command(
        self,
        source: Path,
        probe: VideoProbe,
        temp_output: Path,
        profile: VideoConversionProfile,
    ) -> List[str]:

        target = profile.target_container

        primary = self.choose_primary_video(probe.streams)
        if not primary:
            return []

        cmd = [self.ffmpeg, "-hide_banner", "-nostdin"]
        cmd += BASE_TOLERANCE_FLAGS
        cmd += AGGRESSIVE_TIMESTAMP_FLAGS
        cmd += ["-ignore_unknown", "-y", "-i", str(source)]

        cmd += ["-map", f"0:{primary.index}"]

        encoder, _v_note = self.target_video_encoder(profile, target)

        cmd += self.build_video_encode_flags(
            out_idx=0,
            src=primary,
            encoder=encoder,
            profile=profile,
            probe=probe,
            base_crf_max=20,
        )

        audio = self.choose_primary_audio(probe.streams)
        if audio:
            cmd += ["-map", f"0:{audio.index}"]
            codec, bitrate, vbr_q, extra_idx, _reason = (
                self.plan_audio_target(audio, target, profile)
            )
            cmd += ["-c:a:0", codec]
            if vbr_q is not None:
                cmd += ["-q:a:0", vbr_q]
            elif bitrate:
                cmd += ["-b:a:0", bitrate]
            for flag_name, flag_val in extra_idx:
                cmd += [f"-{flag_name}:a:0", flag_val]

        if target in {"mp4", "mov"} and profile.faststart:
            cmd += ["-movflags", "+faststart"]

        cmd += [
            "-map_metadata", "0" if profile.keep_metadata else "-1",
            "-map_chapters", "0" if profile.keep_chapters else "-1",
        ]

        cmd += ["-max_muxing_queue_size", "8192"]

        cmd.append(str(temp_output))
        return cmd

    def parse_stderr_for_bad_stream(self, stderr: str) -> Optional[int]:
        if not stderr:
            return None
        patterns = [
            r"Error\s+(?:while\s+)?decoding\s+stream\s+#0:(\d+)",
            r"Error\s+opening\s+decoder\s+for\s+stream\s+#0:(\d+)",
            r"Could\s+not\s+(?:find|open|decode)\s+.*?stream\s+#0:(\d+)",
            r"Failed\s+to\s+decode\s+stream\s+#0:(\d+)",
            r"Invalid\s+data\s+found.*?stream\s+#0:(\d+)",
            r"stream\s+#0:(\d+).*?(?:invalid|corrupt|error|fail)",
        ]
        for pattern in patterns:
            m = re.search(pattern, stderr, re.IGNORECASE)
            if m:
                try:
                    return int(m.group(1))
                except Exception:
                    pass
        return None

    def stderr_indicates_timestamp_problem(self, stderr: str) -> bool:
        text = (stderr or "").lower()
        patterns = (
            "non monotonically increasing dts",
            "invalid dts",
            "invalid pts",
            "negative timestamp",
            "non-monotonic",
        )
        return any(p in text for p in patterns)

    def stderr_indicates_muxer_refusal(self, stderr: str) -> Optional[int]:
        if not stderr:
            return None
        patterns = [
            r"Codec\s+\S+\s+not\s+supported\s+in\s+container",
            r"Could\s+not\s+write\s+header\s+for\s+output\s+file",
            r"Tag\s+\S+\s+incompatible\s+with\s+output\s+codec",
            r"Unsupported\s+codec\s+in\s+container",
            r"muxer\s+does\s+not\s+support",
            r"Could\s+not\s+find\s+a\s+suitable\s+output\s+format",
        ]
        for pattern in patterns:
            if re.search(pattern, stderr, re.IGNORECASE):
                m = re.search(r"stream\s+#0:(\d+)", stderr, re.IGNORECASE)
                if m:
                    try:
                        return int(m.group(1))
                    except Exception:
                        pass
                return -1
        return None

    def terminate_process(self, process: subprocess.Popen):
        if process.poll() is not None:
            return
        try:
            if os.name == "nt":
                try:
                    process.send_signal(signal.CTRL_BREAK_EVENT)
                except Exception:
                    process.terminate()
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    process.kill()
            else:
                process.terminate()
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    process.kill()
        except Exception:
            try:
                process.kill()
            except Exception:
                pass

    def execute_ffmpeg_process(
        self,
        cmd: List[str],
        duration: float,
        progress_callback=None,
        cancel_event=None,
    ) -> Tuple[int, str]:

        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        if os.name == "nt":
            creationflags |= getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
                errors="replace",
                bufsize=1,
                creationflags=creationflags,
            )
        except Exception as exc:
            return -1, f"KhÃ´ng thá»ƒ cháº¡y FFmpeg: {exc}"

        stderr_lines: List[str] = []
        stderr_lock = threading.Lock()
        time_pattern = re.compile(
            r"time=(\d+):(\d+):(\d+(?:\.\d+)?)"
        )

        def reader():
            try:
                for line in process.stderr:
                    with stderr_lock:
                        stderr_lines.append(line)
                        if len(stderr_lines) > 4000:
                            del stderr_lines[:1000]

                    if progress_callback and duration > 0:
                        m = time_pattern.search(line)
                        if m:
                            try:
                                h = float(m.group(1))
                                mi = float(m.group(2))
                                s = float(m.group(3))
                                current = h * 3600 + mi * 60 + s
                                progress = min(0.99, max(0.0, current / duration))
                                progress_callback(progress)
                            except Exception:
                                pass
            except Exception:
                pass

        reader_thread = threading.Thread(target=reader, daemon=True)
        reader_thread.start()

        while process.poll() is None:
            if cancel_event and cancel_event.is_set():
                self.terminate_process(process)
                reader_thread.join(timeout=2)
                return -1, "Cancelled"
            time.sleep(0.15)

        reader_thread.join(timeout=3)

        with stderr_lock:
            stderr = "".join(stderr_lines)

        if progress_callback:
            progress_callback(1.0 if process.returncode == 0 else 0.0)

        return process.returncode, stderr

    def verify_output(
        self,
        output: Path,
        source_probe: VideoProbe,
        plan: Optional[ConversionPlan] = None,
    ) -> Tuple[bool, str, Optional[VideoProbe]]:
        if not output.exists():
            return False, "Output khÃ´ng tá»“n táº¡i.", None

        try:
            size = output.stat().st_size
        except Exception:
            size = 0

        if size <= 0:
            return False, "Output dung lÆ°á»£ng báº±ng 0.", None

        probe, report = self.lenient_probe(output)
        if not probe:
            return False, "KhÃ´ng probe Ä‘Æ°á»£c output.", None

        has_video = any(
            s.codec_type == "video" and not s.is_attached_pic
            for s in probe.streams
        )
        if not has_video:
            return False, "Output khÃ´ng cÃ³ video chÃ­nh.", probe

        source_audio = [
            s for s in source_probe.streams if s.codec_type == "audio"
        ]
        output_audio = [
            s for s in probe.streams if s.codec_type == "audio"
        ]
        if source_audio and not output_audio:
            return False, "Output thiáº¿u audio (source cÃ³ audio).", probe

        warnings: List[str] = []
        if source_probe.duration > 0 and probe.duration > 0:
            ratio = probe.duration / source_probe.duration
            if ratio < 0.90:
                return (
                    False,
                    f"Output quÃ¡ ngáº¯n: {ratio * 100:.1f}% so vá»›i nguá»“n "
                    f"({probe.duration:.2f}s / {source_probe.duration:.2f}s).",
                    probe,
                )
            if ratio < 0.99:
                warnings.append(f"duration {ratio * 100:.1f}%")

        if plan:
            for action in plan.actions:
                if action.action == "drop":
                    continue
                if action.codec_type not in {"video", "audio"}:
                    continue

                action_ordinal = 0
                for previous in plan.actions:
                    if previous is action:
                        break
                    if (
                        previous.action != "drop"
                        and previous.codec_type == action.codec_type
                    ):
                        action_ordinal += 1

                actual_streams = [
                    s for s in probe.streams
                    if s.codec_type == action.codec_type
                    and not (
                        action.codec_type == "video"
                        and s.is_attached_pic
                    )
                ]

                if action_ordinal >= len(actual_streams):
                    return (
                        False,
                        (
                            f"Plan yÃªu cáº§u {action.codec_type}"
                            f"[{action_ordinal}] ({action.action}"
                            + (
                                f" â†’ {action.target_codec}"
                                if action.target_codec else ""
                            )
                            + f") nhÆ°ng output khÃ´ng cÃ³ stream tÆ°Æ¡ng á»©ng "
                            f"(output cÃ³ {len(actual_streams)} "
                            f"{action.codec_type})."
                        ),
                        probe,
                    )

                expected_codec = action.target_codec
                if not expected_codec:
                    continue

                if action.codec_type == "video":
                    expected_codec = ENCODER_TO_CODEC_NAME.get(
                        expected_codec, expected_codec,
                    )
                else:
                    audio_map = {
                        "libfdk_aac": "aac", "libopus": "opus",
                        "libmp3lame": "mp3", "libvorbis": "vorbis",
                    }
                    expected_codec = audio_map.get(
                        expected_codec, expected_codec,
                    )

                actual_codec = actual_streams[action_ordinal].codec_name

                if actual_codec != expected_codec:
                    warnings.append(
                        f"{action.codec_type}[{action_ordinal}] "
                        f"{actual_codec}â‰ {expected_codec}"
                    )

        if report and IssueType.CORRUPT_PACKETS in report.types:
            warnings.append("cÃ³ packet corrupt trong output")

        if warnings:
            return (
                True,
                f"Output verified (cáº£nh bÃ¡o: {', '.join(warnings)}).",
                probe,
            )

        return True, "Output verified.", probe


# =============================================================================
# 6. ROOT APP BASE (drag & drop conditional)
# =============================================================================

if HAS_DND:
    class _AppBase(tk.Tk, TkinterDnD.DnDWrapper):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            try:
                self.TkdndVersion = TkinterDnD._require(self)
            except Exception as exc:
                print(f"[dnd] tkdnd load failed: {exc}", file=sys.stderr)
                self.TkdndVersion = None
else:
    class _AppBase(tk.Tk):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.TkdndVersion = None


# =============================================================================
# 7. GUI
# =============================================================================

class VideoConverterUI(_AppBase):

    MAX_ATTEMPTS = 7
    DND_HIGHLIGHT_BG = "#1b2a4a"
    PROGRESS_THROTTLE_SEC = 0.5

    def __init__(self):
        super().__init__()

        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("1120x820")
        self.minsize(960, 700)

        # [P3] Set icon cá»­a sá»• tá»« icon.ico (cáº¡nh EXE hoáº·c trong bundle).
        self._set_window_icon()

        self.engine = ConversionEngine()

        self.tasks: List[VideoConversionTask] = []
        self.output_dir = Path.home() / "Videos" / "Converted"

        self.is_processing = False
        self.cancel_event = threading.Event()
        self.ui_queue: "queue.Queue" = queue.Queue()

        self._reserved_names: Set[str] = set()
        self._drag_active = False
        self._default_canvas_bg = None

        # LÆ°u reference tá»›i (canvas, label%) Ä‘á»ƒ cáº­p nháº­t tiáº¿n trÃ¬nh táº¡i chá»—,
        # trÃ¡nh re-render toÃ n bá»™ danh sÃ¡ch gÃ¢y giáº­t hÃ¬nh.
        self._progress_widgets: Dict[str, Tuple[tk.Canvas, tk.Label]] = {}

        self._scan_cancel_event = threading.Event()
        self._scan_in_progress = False

        # Chá»‰ hiá»‡n popup tá»•ng káº¿t khi batch cÃ³ Ã­t nháº¥t 1 task Ä‘Æ°á»£c xá»­ lÃ½.
        self._batch_task_count = 0

        self._setup_styles()
        self._build_layout()
        self._setup_drag_drop()

        # [P4] Dark title bar â€” gá»i sau khi layout xong.
        # Gá»i 2 láº§n: ngay bÃ¢y giá» + sau 20ms Ä‘á»ƒ cháº¯c cháº¯n HWND Ä‘Ã£ sáºµn sÃ ng
        # (má»™t sá»‘ build Windows cáº§n Ä‘á»£i cá»­a sá»• hiá»‡n ra má»›i Äƒn attribute).
        self._enable_dark_titlebar()
        self.after(20, self._enable_dark_titlebar)

        self.root_after_drain = self.after(80, self._drain_ui_queue)

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._cleanup_stale_temp_files()

        self._log("Ready. FFmpeg / FFprobe sáº½ Ä‘Æ°á»£c kiá»ƒm tra khi báº¯t Ä‘áº§u.")
        if HAS_DND and getattr(self, "TkdndVersion", None):
            self._log("ðŸ’¡ KÃ©o & tháº£ file video hoáº·c thÆ° má»¥c vÃ o cá»­a sá»• Ä‘á»ƒ thÃªm nhanh.")
        else:
            self._log(
                "â„¹ CÃ i `tkinterdnd2` Ä‘á»ƒ báº­t kÃ©o & tháº£: pip install tkinterdnd2"
            )

    # -------------------------------------------------------------------------
    # [P3] Window icon
    # -------------------------------------------------------------------------

    def _set_window_icon(self):
        """Náº¡p icon.ico cho cá»­a sá»• Tkinter.

        TÃ¬m theo thá»© tá»±: cáº¡nh EXE â†’ bundle _internal/_MEIPASS.
        Chá»‰ Ã¡p dá»¥ng cho Windows/Linux (iconbitmap há»— trá»£ .ico).
        """
        try:
            icon_path = find_resource("icon.ico")
            if not icon_path:
                return
            # Æ¯u tiÃªn default= Ä‘á»ƒ má»i Toplevel cÅ©ng cÃ³ icon.
            try:
                self.iconbitmap(default=str(icon_path))
            except Exception:
                try:
                    self.iconbitmap(str(icon_path))
                except Exception:
                    pass
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # [P4] Dark title bar (Windows 10/11)
    # -------------------------------------------------------------------------

    def _enable_dark_titlebar(self):
        """Báº­t dark mode cho thanh tiÃªu Ä‘á» Windows.

        Chá»‰ cÃ³ tÃ¡c dá»¥ng trÃªn Windows 10 build 17763+ / Windows 11.
        TrÃªn OS khÃ¡c hoáº·c Windows cÅ© hÆ¡n, hÃ m tá»± bá» qua im láº·ng.
        """
        if os.name != "nt":
            return
        try:
            import ctypes

            # Äáº£m báº£o native window Ä‘Ã£ tá»“n táº¡i trÆ°á»›c khi láº¥y HWND.
            try:
                self.update_idletasks()
            except Exception:
                pass

            # Tk toplevel: winfo_id() tráº£ HWND cá»§a widget, parent má»›i lÃ 
            # HWND top-level tháº­t sá»± mÃ  DWM cáº§n.
            try:
                hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            except Exception:
                hwnd = 0
            if not hwnd:
                hwnd = self.winfo_id()

            value = ctypes.c_int(1)

            # Attribute ID:
            #   20 â†’ Windows 11 / Windows 10 build 19041+
            #   19 â†’ Windows 10 build 17763 â€“ 19041 (fallback)
            for attr in (20, 19):
                try:
                    res = ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        hwnd,
                        attr,
                        ctypes.byref(value),
                        ctypes.sizeof(value),
                    )
                    if res == 0:
                        break
                except Exception:
                    continue

            # (Tuá»³ chá»n) Ã©p mÃ u caption khá»›p bg app â€” Windows 11 22000+
            try:
                # COLORREF = 0x00BBGGRR (Ä‘áº£o ngÆ°á»£c RGB)
                r, g, b = 0x0d, 0x11, 0x17
                colorref = (b << 16) | (g << 8) | r
                c_color = ctypes.c_int(colorref)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, 35,  # DWMWA_CAPTION_COLOR
                    ctypes.byref(c_color),
                    ctypes.sizeof(c_color),
                )
                # Text trÃªn caption
                c_text = ctypes.c_int(0x00E6EDF3)  # #e6edf3 (text color)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, 36,  # DWMWA_TEXT_COLOR
                    ctypes.byref(c_text),
                    ctypes.sizeof(c_text),
                )
            except Exception:
                pass
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # UI thread helpers
    # -------------------------------------------------------------------------

    def _ui(self, callback):
        try:
            self.ui_queue.put(callback)
        except Exception:
            pass

    def _drain_ui_queue(self):
        try:
            for _ in range(60):
                try:
                    cb = self.ui_queue.get_nowait()
                except queue.Empty:
                    break
                try:
                    cb()
                except Exception:
                    pass
        finally:
            try:
                self.root_after_drain = self.after(80, self._drain_ui_queue)
            except tk.TclError:
                pass

    def _log(self, message: str):
        def update():
            try:
                self.txt_log.insert(
                    "end",
                    f"[{time.strftime('%H:%M:%S')}] {message}\n",
                )
                self.txt_log.see("end")
            except tk.TclError:
                pass
        self._ui(update)

    def _on_close(self):
        if self.is_processing or self._scan_in_progress:
            if not messagebox.askokcancel(
                "ThoÃ¡t",
                "Äang xá»­ lÃ½. Dá»«ng vÃ  thoÃ¡t?",
            ):
                return
            self.cancel_event.set()
            self._scan_cancel_event.set()
        try:
            self.destroy()
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # Styles
    # -------------------------------------------------------------------------

    def _setup_styles(self):
        self.colors = {
            "bg": "#0d1117",
            "surface": "#161b22",
            "surface2": "#1f242d",
            "surface3": "#282e39",
            "border": "#30363d",
            "text": "#e6edf3",
            "muted": "#8b949e",
            "accent": "#4f8cff",
            "success": "#2ea043",
            "success_hover": "#238636",
            "danger": "#da3633",
            "danger_hover": "#b02525",
            "warning": "#d29922",
        }

        self.configure(bg=self.colors["bg"])

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background=self.colors["bg"])
        style.configure("Surface.TFrame", background=self.colors["surface"])
        style.configure("Card.TFrame", background=self.colors["surface2"])

        style.configure(
            "TLabel", background=self.colors["bg"],
            foreground=self.colors["text"], font=("Segoe UI", 10),
        )
        style.configure(
            "Surface.TLabel", background=self.colors["surface"],
            foreground=self.colors["text"], font=("Segoe UI", 10),
        )
        style.configure(
            "Muted.TLabel", background=self.colors["surface"],
            foreground=self.colors["muted"], font=("Segoe UI", 9),
        )
        style.configure(
            "CardMuted.TLabel", background=self.colors["surface2"],
            foreground=self.colors["muted"], font=("Segoe UI", 9),
        )
        style.configure(
            "Title.TLabel", background=self.colors["bg"],
            foreground=self.colors["accent"], font=("Segoe UI", 14, "bold"),
        )
        style.configure(
            "TCheckbutton", background=self.colors["surface"],
            foreground=self.colors["text"], font=("Segoe UI", 9),
        )
        style.map(
            "TCheckbutton",
            background=[("active", self.colors["surface"])],
            foreground=[("disabled", self.colors["muted"])],
        )

        style.configure(
            "TButton", background=self.colors["surface2"],
            foreground=self.colors["text"],
            bordercolor=self.colors["border"],
            darkcolor=self.colors["surface2"],
            lightcolor=self.colors["surface2"],
            focuscolor="none", font=("Segoe UI", 10),
        )
        style.map("TButton", background=[("active", self.colors["border"])])

        style.configure(
            "TCombobox", fieldbackground=self.colors["surface2"],
            background=self.colors["border"], foreground=self.colors["text"],
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", self.colors["surface2"])],
        )

        style.configure(
            "Horizontal.TProgressbar", background=self.colors["accent"],
            troughcolor=self.colors["surface2"],
            bordercolor=self.colors["border"],
            lightcolor=self.colors["accent"],
            darkcolor=self.colors["accent"],
        )

    # -------------------------------------------------------------------------
    # Layout
    # -------------------------------------------------------------------------

    def _build_layout(self):

        header = ttk.Frame(self, padding=12)
        header.pack(fill="x")

        ttk.Label(
            header, text="ðŸŽ¬ Video Converter Pro",
            style="Title.TLabel",
        ).pack(side="left")

        ttk.Label(
            header,
            text=" Remux all video formats with losslessly original quality",
            style="Muted.TLabel",
        ).pack(side="left", padx=10, pady=4)

        opts = ttk.Frame(self, style="Surface.TFrame", padding=12)
        opts.pack(fill="x", padx=12, pady=4)

        self.controls = {}

        fields = [
            ("Container:", ["MP4", "MKV", "WEBM", "MOV", "AVI", "TS"], "cb_target"),
            ("Video:", [
                "Auto (Copy > Convert)",
                "Force Re-encode",
                "Force Copy",
            ], "cb_vmode"),
            ("Audio:", [
                "Auto (Copy > Convert)",
                "Force Re-encode",
                "Force Copy",
            ], "cb_amode"),
            ("Video Codec:", ["H.264", "H.265 / HEVC", "VP9", "AV1"], "cb_vcodec"),
            ("CRF:", [str(i) for i in range(14, 23)], "cb_crf"),
            ("Preset:", ["medium", "slow", "slower", "veryslow"], "cb_preset"),
        ]

        for idx, (label, values, key) in enumerate(fields):
            row = idx // 3
            col = (idx % 3) * 2
            ttk.Label(opts, text=label, style="Surface.TLabel").grid(
                row=row, column=col, sticky="w", padx=4, pady=4,
            )
            cb = ttk.Combobox(opts, values=values, state="readonly", width=22)
            cb.current(0)
            cb.grid(row=row, column=col + 1, sticky="w", padx=8, pady=4)
            self.controls[key] = cb

        self.controls["cb_crf"].set("17")
        self.controls["cb_preset"].set("slow")

        # [U1] Lá»c codec theo container + Ä‘á»“ng bá»™ khi user Ä‘á»•i container.
        self.controls["cb_target"].bind(
            "<<ComboboxSelected>>", self._on_container_changed,
        )
        self._refresh_codec_options(initial=True)

        filter_frame = ttk.Frame(self, style="Surface.TFrame", padding=10)
        filter_frame.pack(fill="x", padx=12, pady=4)

        self.keep_metadata_var = tk.BooleanVar(value=True)
        self.keep_chapters_var = tk.BooleanVar(value=True)
        self.keep_attachments_var = tk.BooleanVar(value=False)
        self.keep_data_var = tk.BooleanVar(value=False)
        self.rate_cap_var = tk.BooleanVar(value=True)
        self.reprocess_completed_var = tk.BooleanVar(value=False)
        self.adaptive_crf_var = tk.BooleanVar(value=True)
        self.use_gpu_var = tk.BooleanVar(value=True)

        row1 = ttk.Frame(filter_frame, style="Surface.TFrame")
        row1.pack(fill="x")
        row2 = ttk.Frame(filter_frame, style="Surface.TFrame")
        row2.pack(fill="x", pady=(4, 0))

        self._chk_metadata = ttk.Checkbutton(
            row1, text="Giá»¯ metadata",
            variable=self.keep_metadata_var,
        )
        self._chk_metadata.pack(side="left", padx=8)

        self._chk_chapters = ttk.Checkbutton(
            row1, text="Giá»¯ chapters",
            variable=self.keep_chapters_var,
        )
        self._chk_chapters.pack(side="left", padx=8)

        self._chk_attachments = ttk.Checkbutton(
            row1, text="Giá»¯ cover/attachments",
            variable=self.keep_attachments_var,
        )
        self._chk_attachments.pack(side="left", padx=8)

        self._chk_data = ttk.Checkbutton(
            row1, text="Giá»¯ data stream (MKV/TS)",
            variable=self.keep_data_var,
        )
        self._chk_data.pack(side="left", padx=8)

        self._chk_rate_cap = ttk.Checkbutton(
            row2, text="Báº­t tráº§n bitrate (maxrate/bufsize, khuyÃªn dÃ¹ng)",
            variable=self.rate_cap_var,
        )
        self._chk_rate_cap.pack(side="left", padx=8)

        self._chk_reprocess = ttk.Checkbutton(
            row2, text="Xá»­ lÃ½ láº¡i file Ä‘Ã£ Completed",
            variable=self.reprocess_completed_var,
        )
        self._chk_reprocess.pack(side="left", padx=8)

        self._chk_adaptive_crf = ttk.Checkbutton(
            row2, text="Adaptive CRF theo nguá»“n (khuyÃªn dÃ¹ng)",
            variable=self.adaptive_crf_var,
        )
        self._chk_adaptive_crf.pack(side="left", padx=8)

        self._chk_use_gpu = ttk.Checkbutton(
            row2, text="DÃ¹ng GPU NVIDIA (NVENC)",
            variable=self.use_gpu_var,
        )
        self._chk_use_gpu.pack(side="left", padx=8)

        action_bar = ttk.Frame(self, padding=8)
        action_bar.pack(fill="x", padx=12)

        self.btn_add = ttk.Button(
            action_bar, text="âž• ThÃªm File", command=self.add_files,
        )
        self.btn_add.pack(side="left", padx=4)

        self.btn_add_folder = ttk.Button(
            action_bar, text="ðŸ“ ThÃªm ThÆ° Má»¥c", command=self.add_folder,
        )
        self.btn_add_folder.pack(side="left", padx=4)

        self.btn_enable_all = ttk.Button(
            action_bar, text="âœ“ Báº­t háº¿t",
            command=lambda: self._set_all_enabled(True),
        )
        self.btn_enable_all.pack(side="left", padx=2)

        self.btn_disable_all = ttk.Button(
            action_bar, text="â˜ Táº¯t háº¿t",
            command=lambda: self._set_all_enabled(False),
        )
        self.btn_disable_all.pack(side="left", padx=2)

        self.btn_clear_completed = ttk.Button(
            action_bar, text="ðŸ—‘ XoÃ¡ Ä‘Ã£ xá»­ lÃ½", command=self.clear_completed,
        )
        self.btn_clear_completed.pack(side="left", padx=2)

        self.btn_clear_all = ttk.Button(
            action_bar,
            text="âœ– XoÃ¡ háº¿t", command=self.clear_all,
        )
        self.btn_clear_all.pack(side="left", padx=2)

        self.btn_start = tk.Button(
            action_bar,
            text="â–¶  Báº®T Äáº¦U CONVERT",
            command=self.start_processing,
            bg=self.colors["success"],
            fg="#ffffff",
            activebackground=self.colors["success_hover"],
            activeforeground="#ffffff",
            disabledforeground="#c9d1d9",
            bd=0,
            relief="flat",
            highlightthickness=0,
            takefocus=0,
            cursor="hand2",
            padx=18, pady=8,
            font=("Segoe UI", 10, "bold"),
        )
        self.btn_start.pack(side="right", padx=4)

        self.btn_cancel = tk.Button(
            action_bar,
            text="â–   HUá»¶",
            command=self.cancel_processing,
            bg=self.colors["danger"],
            fg="#ffffff",
            activebackground=self.colors["danger_hover"],
            activeforeground="#ffffff",
            disabledforeground="#c9d1d9",
            bd=0,
            relief="flat",
            highlightthickness=0,
            takefocus=0,
            cursor="hand2",
            padx=18, pady=8,
            font=("Segoe UI", 10, "bold"),
            state="disabled",
        )
        self.btn_cancel.pack(side="right", padx=4)

        list_header = ttk.Frame(self, style="Surface.TFrame", padding=(12, 6))
        list_header.pack(fill="x", padx=12, pady=(6, 0))

        ttk.Label(
            list_header, text="ðŸ“‹ DANH SÃCH FILE",
            style="Surface.TLabel", font=("Segoe UI", 10, "bold"),
        ).pack(side="left")

        self.lbl_list_counter = ttk.Label(
            list_header, text="ChÆ°a cÃ³ file", style="Muted.TLabel",
        )
        self.lbl_list_counter.pack(side="right", padx=4)

        list_container = ttk.Frame(self, padding=4)
        list_container.pack(fill="both", expand=True, padx=12, pady=(0, 4))

        self.canvas = tk.Canvas(
            list_container, bg=self.colors["bg"], highlightthickness=0,
        )
        self._default_canvas_bg = self.colors["bg"]

        self.scrollbar = ttk.Scrollbar(
            list_container, orient="vertical", command=self.canvas.yview,
        )
        self.file_list_frame = ttk.Frame(self.canvas)

        self.file_list_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.file_list_frame, anchor="nw",
        )
        self.canvas.bind("<Configure>", self._resize_canvas_window)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

        output_bar = ttk.Frame(self, style="Surface.TFrame", padding=8)
        output_bar.pack(fill="x", padx=12, pady=4)

        ttk.Label(
            output_bar, text="ðŸ“‚ ThÆ° má»¥c xuáº¥t:", style="Surface.TLabel",
        ).pack(side="left", padx=4)

        self.outdir_var = tk.StringVar(value=str(self.output_dir))
        self.entry_outdir = ttk.Entry(
            output_bar, textvariable=self.outdir_var,
            font=("Segoe UI", 9),
        )
        self.entry_outdir.pack(side="left", padx=8, fill="x", expand=True)
        self.entry_outdir.bind("<Return>", self._on_outdir_changed)
        self.entry_outdir.bind("<FocusOut>", self._on_outdir_changed)

        self.btn_open_output = ttk.Button(
            output_bar, text="ðŸ“‚ Má»Ÿ", command=self.open_output_dir,
        )
        self.btn_open_output.pack(side="right", padx=4)

        self.btn_choose_output = ttk.Button(
            output_bar, text="Chá»n ThÆ° Má»¥c...",
            command=self.choose_output_dir,
        )
        self.btn_choose_output.pack(side="right", padx=4)

        log_frame = ttk.Frame(self, padding=4)
        log_frame.pack(fill="x", padx=12, pady=4)

        self.txt_log = tk.Text(
            log_frame, height=6,
            bg=self.colors["surface"], fg=self.colors["text"],
            insertbackground="white", font=("Consolas", 9), relief="flat",
        )
        self.txt_log.pack(fill="x")

        self.global_progress = ttk.Progressbar(
            self, style="Horizontal.TProgressbar", mode="determinate",
        )
        self.global_progress.pack(fill="x", padx=12, pady=(0, 8))

    def _on_mousewheel(self, event):
        try:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass

    def _bind_mousewheel(self, _event=None):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, _event=None):
        self.canvas.unbind_all("<MouseWheel>")

    def _resize_canvas_window(self, event):
        try:
            self.canvas.itemconfigure(self.canvas_window, width=event.width)
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # [U1] Codec filter theo container
    # -------------------------------------------------------------------------

    def _on_container_changed(self, _event=None):
        """User vá»«a Ä‘á»•i container â†’ cáº­p nháº­t láº¡i danh sÃ¡ch codec há»£p lá»‡."""
        self._refresh_codec_options(initial=False)

    def _refresh_codec_options(self, initial: bool = False):
        """Äá»“ng bá»™ dropdown Video Codec theo Container Ä‘ang chá»n.

        CHá»ˆ can thiá»‡p UI: giÃ¡ trá»‹ truyá»n vÃ o engine váº«n qua get_profile_from_ui
        vá»›i Ä‘Ãºng label user tháº¥y. Náº¿u codec Ä‘ang chá»n khÃ´ng há»£p lá»‡ cho container
        má»›i, tá»± reset vá» option Ä‘áº§u tiÃªn vÃ  ghi log cáº£nh bÃ¡o.
        """
        try:
            container_label = self.controls["cb_target"].get()
        except Exception:
            return

        allowed_codecs = CONTAINER_CODEC_UI_MAP.get(
            container_label,
            ["H.264", "H.265 / HEVC", "VP9", "AV1"],
        )

        try:
            codec_cb = self.controls["cb_vcodec"]
            current = codec_cb.get()

            codec_cb.configure(values=allowed_codecs)

            if current in allowed_codecs:
                # Giá»¯ nguyÃªn lá»±a chá»n cÅ© náº¿u váº«n há»£p lá»‡.
                codec_cb.set(current)
            else:
                codec_cb.set(allowed_codecs[0])
                if not initial:
                    self._log(
                        f"â„¹ Container {container_label} khÃ´ng há»— trá»£ "
                        f"codec '{current}' â†’ tá»± chuyá»ƒn sang "
                        f"'{allowed_codecs[0]}'."
                    )
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # UI lock
    # -------------------------------------------------------------------------

    def _set_ui_locked(self, locked: bool):
        readonly = "disabled" if locked else "readonly"
        normal = "disabled" if locked else "normal"

        for cb in self.controls.values():
            try:
                cb.configure(state=readonly)
            except Exception:
                pass

        for btn in [
            self.btn_add, self.btn_add_folder,
            self.btn_enable_all, self.btn_disable_all,
            self.btn_clear_completed, self.btn_clear_all,
            self.btn_choose_output, self.btn_open_output,
        ]:
            try:
                btn.configure(state=normal)
            except Exception:
                pass

        for chk in [
            self._chk_metadata, self._chk_chapters,
            self._chk_attachments, self._chk_data,
            self._chk_rate_cap, self._chk_reprocess,
            self._chk_adaptive_crf, self._chk_use_gpu,
        ]:
            try:
                chk.configure(state=normal)
            except Exception:
                pass

        try:
            self.entry_outdir.configure(state=normal)
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # Startup temp cleanup
    # -------------------------------------------------------------------------

    def _cleanup_stale_temp_files(self):
        try:
            if not self.output_dir.exists():
                return
            now = time.time()
            removed = 0
            for p in self.output_dir.glob(".vcp_*"):
                try:
                    if p.is_file() and (now - p.stat().st_mtime) > 6 * 3600:
                        p.unlink()
                        removed += 1
                except Exception:
                    continue
            if removed:
                self.after(
                    500,
                    lambda: self._log(
                        f"ðŸ§¹ ÄÃ£ xoÃ¡ {removed} file táº¡m tá»« session trÆ°á»›c."
                    ),
                )
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # Drag & drop
    # -------------------------------------------------------------------------

    def _setup_drag_drop(self):
        if not HAS_DND:
            return
        if not getattr(self, "TkdndVersion", None):
            return
        try:
            self.drop_target_register(DND_FILES)
            self.dnd_bind("<<Drop>>", self._on_drop)
            self.dnd_bind("<<DragEnter>>", self._on_drag_enter)
            self.dnd_bind("<<DragLeave>>", self._on_drag_leave)
        except Exception as exc:
            print(f"[dnd] register failed: {exc}", file=sys.stderr)

    def _set_drag_highlight(self, active: bool):
        if active == self._drag_active:
            return
        self._drag_active = active
        try:
            if active:
                self.canvas.configure(bg=self.DND_HIGHLIGHT_BG)
                self.file_list_frame.configure(style="Card.TFrame")
            else:
                self.canvas.configure(bg=self._default_canvas_bg)
                self.file_list_frame.configure(style="TFrame")
        except Exception:
            pass

    def _on_drag_enter(self, _event):
        if self.is_processing:
            return
        self._set_drag_highlight(True)

    def _on_drag_leave(self, _event):
        self._set_drag_highlight(False)

    def _on_drop(self, event):
        self._set_drag_highlight(False)

        if self.is_processing:
            self._log("âš  Äang convert â€” bá» qua thao tÃ¡c kÃ©o & tháº£.")
            return

        try:
            raw_paths = self.tk.splitlist(event.data)
        except Exception as exc:
            self._log(f"âœ— KhÃ´ng Ä‘á»c Ä‘Æ°á»£c dá»¯ liá»‡u kÃ©o & tháº£: {exc}")
            return

        if not raw_paths:
            return

        files_to_add: List[Path] = []
        folders_to_scan: List[Path] = []
        rejected: List[str] = []

        for raw in raw_paths:
            if not raw:
                continue
            try:
                p = Path(raw)
            except (OSError, ValueError):
                continue
            try:
                if p.is_dir():
                    folders_to_scan.append(p)
                    continue
                if p.is_file():
                    if p.suffix.lower() in VIDEO_EXTENSIONS:
                        files_to_add.append(p)
                    else:
                        rejected.append(p.name)
                    continue
            except OSError:
                continue

        added = 0
        for f in files_to_add:
            if self._add_task_path(f):
                added += 1

        if added > 0:
            self._log(f"âœ“ ÄÃ£ thÃªm {added} file (tá»•ng: {len(self.tasks)}).")
            self._ui(self.render_file_list)

        if rejected:
            preview = ", ".join(rejected[:5])
            suffix = "" if len(rejected) <= 5 else f" (+{len(rejected) - 5})"
            self._log(f"âš  Bá» qua {len(rejected)} file khÃ´ng pháº£i video: {preview}{suffix}")

        if folders_to_scan:
            self._start_folder_scan(folders_to_scan, source_label="KÃ©o & tháº£")

    # -------------------------------------------------------------------------
    # Output folder
    # -------------------------------------------------------------------------

    def choose_output_dir(self):
        if self.is_processing:
            return
        directory = filedialog.askdirectory(initialdir=str(self.output_dir))
        if directory:
            self.output_dir = Path(directory)
            self.outdir_var.set(str(self.output_dir))

    def _on_outdir_changed(self, _event=None):
        """Cho phÃ©p ngÆ°á»i dÃ¹ng gÃµ tay Ä‘Æ°á»ng dáº«n thÆ° má»¥c xuáº¥t.

        [F14] Chuáº©n hoÃ¡ path tÆ°Æ¡ng Ä‘á»‘i thÃ nh absolute Ä‘á»ƒ trÃ¡nh ghi nháº§m
        vÃ o CWD khi user gÃµ path kiá»ƒu `output` hoáº·c `./out`.
        """
        raw = self.outdir_var.get().strip()
        if not raw:
            self.outdir_var.set(str(self.output_dir))
            return
        try:
            new_path = Path(raw).expanduser()
            # Chuáº©n hoÃ¡ thÃ nh absolute náº¿u user gÃµ path tÆ°Æ¡ng Ä‘á»‘i.
            if not new_path.is_absolute():
                new_path = new_path.resolve()
        except Exception:
            self.outdir_var.set(str(self.output_dir))
            return
        self.output_dir = new_path
        self.outdir_var.set(str(self.output_dir))

    def open_output_dir(self):
        """Má»Ÿ thÆ° má»¥c xuáº¥t báº±ng trÃ¬nh quáº£n lÃ½ file cá»§a há»‡ Ä‘iá»u hÃ nh."""
        path = self.output_dir
        try:
            if not path.exists():
                messagebox.showwarning(
                    "ThÃ´ng bÃ¡o",
                    f"ThÆ° má»¥c chÆ°a tá»“n táº¡i:\n{path}",
                )
                return
            if os.name == "nt":
                os.startfile(str(path))  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(path)])
            else:
                subprocess.Popen(["xdg-open", str(path)])
        except Exception as exc:
            self._log(f"âœ— KhÃ´ng má»Ÿ Ä‘Æ°á»£c thÆ° má»¥c: {exc}")

    # -------------------------------------------------------------------------
    # [P5] Command line input ("Open with...", kÃ©o vÃ o exe)
    # -------------------------------------------------------------------------

    def load_cli_args(self, args: List[str]):
        """Náº¡p file/thÆ° má»¥c Ä‘Æ°á»£c truyá»n tá»« command line.

        KÃ­ch hoáº¡t khi:
          - Right-click file video â†’ Open with â†’ VideoConvertPro.exe
          - KÃ©o file/thÆ° má»¥c tháº£ tháº³ng vÃ o file .exe (Windows)
          - Cháº¡y dÃ²ng lá»‡nh: VideoConvertPro.exe file1.mp4 folder1

        CHá»ˆ thÃªm task vÃ o danh sÃ¡ch, khÃ´ng Ä‘á»¥ng logic convert.
        """
        if not args:
            return

        files_to_add: List[Path] = []
        folders_to_scan: List[Path] = []
        rejected: List[str] = []

        for raw in args:
            if not raw:
                continue
            # Bá» qua flags kiá»ƒu --foo (dÃ nh cho tÆ°Æ¡ng lai)
            if raw.startswith("-"):
                continue
            try:
                p = Path(raw)
            except (OSError, ValueError):
                continue
            try:
                if p.is_dir():
                    folders_to_scan.append(p)
                    continue
                if p.is_file():
                    if p.suffix.lower() in VIDEO_EXTENSIONS:
                        files_to_add.append(p)
                    else:
                        rejected.append(p.name)
                    continue
            except OSError:
                continue

        added = 0
        for f in files_to_add:
            if self._add_task_path(f):
                added += 1

        if added > 0:
            self._log(f"âœ“ Nháº­n {added} file tá»« command line.")
            self.render_file_list()

        if rejected:
            preview = ", ".join(rejected[:5])
            suffix = "" if len(rejected) <= 5 else f" (+{len(rejected) - 5})"
            self._log(
                f"âš  Bá» qua {len(rejected)} file khÃ´ng pháº£i video: "
                f"{preview}{suffix}"
            )

        if folders_to_scan:
            self._start_folder_scan(
                folders_to_scan, source_label="Command line",
            )

    def _update_task_progress(self, task_id: str, progress: float):
        """Chá»‰ váº½ láº¡i thanh tiáº¿n trÃ¬nh cá»§a 1 task â€” khÃ´ng rebuild cáº£ list."""
        entry = self._progress_widgets.get(task_id)
        if not entry:
            return
        canvas, label = entry
        try:
            if not canvas.winfo_exists():
                return
            w = canvas.winfo_width()
            if w > 1:
                canvas.delete("all")
                fill_w = int(w * progress)
                canvas.create_rectangle(
                    0, 0, fill_w, 6,
                    fill=self.colors["accent"], outline="",
                )
            label.config(text=f"{int(progress * 100)}%")
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # [U2] Context menu (chuá»™t pháº£i)
    # -------------------------------------------------------------------------

    def _show_context_menu(self, event, task: VideoConversionTask):
        """Hiá»ƒn thá»‹ menu chuá»™t pháº£i cho 1 task trong danh sÃ¡ch."""
        if self.is_processing:
            return

        menu = tk.Menu(
            self,
            tearoff=0,
            bg=self.colors["surface2"],
            fg=self.colors["text"],
            activebackground=self.colors["accent"],
            activeforeground="#ffffff",
            bd=1,
            relief="solid",
            font=("Segoe UI", 9),
        )

        toggle_label = "â˜‘ Báº­t file nÃ y" if task.enabled else "â˜ Báº­t file nÃ y"
        menu.add_command(
            label=toggle_label,
            command=lambda tid=task.task_id: self._toggle_task(tid),
        )

        menu.add_separator()

        menu.add_command(
            label="ðŸ“‚ Má»Ÿ file nguá»“n",
            command=lambda t=task: self._open_source_file(t),
        )
        menu.add_command(
            label="ðŸ“ Má»Ÿ thÆ° má»¥c chá»©a",
            command=lambda t=task: self._open_containing_folder(t),
        )

        menu.add_separator()

        menu.add_command(
            label="ðŸ—‘ XoÃ¡ khá»i danh sÃ¡ch",
            command=lambda tid=task.task_id: self.remove_task(tid),
        )

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            try:
                menu.grab_release()
            except Exception:
                pass

    def _open_source_file(self, task: VideoConversionTask):
        """Má»Ÿ file nguá»“n báº±ng trÃ¬nh phÃ¡t máº·c Ä‘á»‹nh cá»§a OS."""
        path = task.source_path
        try:
            if not path.exists():
                self._log(f"âœ— File khÃ´ng tá»“n táº¡i: {path}")
                return
            if os.name == "nt":
                os.startfile(str(path))  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(path)])
            else:
                subprocess.Popen(["xdg-open", str(path)])
        except Exception as exc:
            self._log(f"âœ— KhÃ´ng má»Ÿ Ä‘Æ°á»£c file: {exc}")

    def _open_containing_folder(self, task: VideoConversionTask):
        """Má»Ÿ thÆ° má»¥c chá»©a file nguá»“n báº±ng trÃ¬nh quáº£n lÃ½ file cá»§a OS."""
        folder = task.source_path.parent
        try:
            if not folder.exists():
                self._log(f"âœ— ThÆ° má»¥c khÃ´ng tá»“n táº¡i: {folder}")
                return
            if os.name == "nt":
                os.startfile(str(folder))  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(folder)])
            else:
                subprocess.Popen(["xdg-open", str(folder)])
        except Exception as exc:
            self._log(f"âœ— KhÃ´ng má»Ÿ Ä‘Æ°á»£c thÆ° má»¥c: {exc}")

    # -------------------------------------------------------------------------
    # Folder scan worker
    # -------------------------------------------------------------------------

    def _start_folder_scan(
        self,
        root_paths: Union[Path, List[Path]],
        source_label: str = "",
    ):
        if isinstance(root_paths, Path):
            roots: List[Path] = [root_paths]
        else:
            roots = list(root_paths)

        if not roots:
            return

        if self._scan_in_progress:
            self._log("âš  Äang quÃ©t thÆ° má»¥c khÃ¡c â€” bá» qua.")
            return

        self._scan_in_progress = True
        self._scan_cancel_event.clear()

        if len(roots) == 1:
            self._log(f"ðŸ“ Äang quÃ©t: {roots[0]}")
        else:
            self._log(f"ðŸ“ Äang quÃ©t {len(roots)} thÆ° má»¥c...")

        def worker():
            found: List[Path] = []
            for root in roots:
                if self._scan_cancel_event.is_set():
                    break
                try:
                    root_resolved = root.resolve()
                except Exception:
                    root_resolved = root
                try:
                    for dirpath, dirnames, filenames in os.walk(
                        str(root), followlinks=False,
                    ):
                        if self._scan_cancel_event.is_set():
                            break

                        safe_dirnames = []
                        for d in dirnames:
                            try:
                                if not os.path.islink(os.path.join(dirpath, d)):
                                    safe_dirnames.append(d)
                            except OSError:
                                continue
                        dirnames[:] = safe_dirnames

                        for name in filenames:
                            if self._scan_cancel_event.is_set():
                                break
                            p = Path(dirpath) / name
                            try:
                                if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS:
                                    try:
                                        p_resolved = p.resolve()
                                    except Exception:
                                        p_resolved = p
                                    try:
                                        p_resolved.relative_to(root_resolved)
                                    except ValueError:
                                        continue
                                    found.append(p)
                            except OSError:
                                continue
                except Exception as exc:
                    self._ui(
                        lambda r=root, e=exc: self._log(
                            f"âš  KhÃ´ng quÃ©t Ä‘Æ°á»£c {r}: {e}"
                        )
                    )
                    continue

            def finish():
                added = 0
                for p in found:
                    if self._add_task_path(p):
                        added += 1
                self._scan_in_progress = False
                label = f" ({source_label})" if source_label else ""
                self._log(
                    f"âœ“ QuÃ©t xong{label}: thÃªm {added} file "
                    f"(tá»•ng: {len(self.tasks)})."
                )
                self.render_file_list()

            self._ui(finish)

        threading.Thread(target=worker, daemon=True).start()

    # -------------------------------------------------------------------------
    # Add files
    # -------------------------------------------------------------------------

    def add_files(self):
        if self.is_processing:
            return
        files = filedialog.askopenfilenames(
            filetypes=[
                (
                    "Video Files",
                    "*.mp4 *.m4v *.mkv *.avi *.mov *.ts *.m2ts *.mts "
                    "*.webm *.flv *.wmv *.mpeg *.mpg *.vob *.ogv "
                    "*.3gp *.3g2 *.mxf *.f4v *.rm *.rmvb *.asf *.divx "
                    "*.m2v *.mp2v",
                ),
                ("All Files", "*.*"),
            ]
        )
        added = 0
        for file in files:
            if self._add_task_path(Path(file)):
                added += 1
        if added:
            self._log(f"âœ“ ÄÃ£ thÃªm {added} file (tá»•ng: {len(self.tasks)}).")
            self._ui(self.render_file_list)

    def add_folder(self):
        if self.is_processing:
            return
        directory = filedialog.askdirectory()
        if not directory:
            return
        self._start_folder_scan([Path(directory)], source_label="ThÃªm thÆ° má»¥c")

    def _add_task_path(self, path: Path) -> bool:
        try:
            path = path.resolve()
        except Exception:
            pass
        if not path.exists() or not path.is_file():
            return False
        if not is_video_file(path):
            return False
        if any(t.source_path == path for t in self.tasks):
            return False

        self.tasks.append(VideoConversionTask(source_path=path))
        return True

    # -------------------------------------------------------------------------
    # Cleanup
    # -------------------------------------------------------------------------

    def clear_completed(self):
        if self.is_processing:
            return
        before = len(self.tasks)
        self.tasks = [
            t for t in self.tasks
            if t.status not in {"Completed", "Failed", "Cancelled"}
        ]
        removed = before - len(self.tasks)
        if removed:
            self._log(f"ðŸ—‘ ÄÃ£ xoÃ¡ {removed} file Ä‘Ã£ xá»­ lÃ½.")
        self.render_file_list()

    def clear_all(self):
        if self.is_processing:
            return
        if not self.tasks:
            return
        if not messagebox.askokcancel(
            "XoÃ¡ háº¿t",
            f"XoÃ¡ toÃ n bá»™ {len(self.tasks)} file khá»i danh sÃ¡ch?",
        ):
            return
        self.tasks.clear()
        self.render_file_list()
        self._log("ðŸ—‘ ÄÃ£ xoÃ¡ toÃ n bá»™ danh sÃ¡ch.")

    def remove_task(self, task_id: str):
        if self.is_processing:
            return
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.task_id != task_id]
        if len(self.tasks) != before:
            self.render_file_list()

    # -------------------------------------------------------------------------
    # Enable/disable
    # -------------------------------------------------------------------------

    def _set_all_enabled(self, enabled: bool):
        if self.is_processing:
            return
        for t in self.tasks:
            t.enabled = enabled
        self.render_file_list()

    def _toggle_task(self, task_id: str):
        if self.is_processing:
            return
        for t in self.tasks:
            if t.task_id == task_id:
                t.enabled = not t.enabled
                break
        self.render_file_list()

    # -------------------------------------------------------------------------
    # Render file list
    # -------------------------------------------------------------------------

    def render_file_list(self):
        for w in self.file_list_frame.winfo_children():
            w.destroy()
        self._progress_widgets.clear()

        total = len(self.tasks)
        enabled = sum(1 for t in self.tasks if t.enabled)

        if total == 0:
            self.lbl_list_counter.configure(
                text="ChÆ°a cÃ³ file", foreground=self.colors["muted"],
            )
            self._render_empty_state()
            return

        self.lbl_list_counter.configure(
            text=f"â˜‘ {enabled}/{total} file Ä‘Æ°á»£c báº­t",
            foreground=self.colors["accent"] if enabled > 0 else self.colors["muted"],
        )

        for task in self.tasks:
            self._render_task_card(task)

    def _render_empty_state(self):
        empty = tk.Frame(self.file_list_frame, bg=self.colors["bg"])
        empty.pack(fill="both", expand=True, pady=60)

        tk.Label(
            empty, text="ðŸ“­", bg=self.colors["bg"],
            fg=self.colors["muted"], font=("Segoe UI Emoji", 40),
        ).pack()

        tk.Label(
            empty, text="ChÆ°a cÃ³ file nÃ o trong danh sÃ¡ch",
            bg=self.colors["bg"], fg=self.colors["text"],
            font=("Segoe UI", 12, "bold"),
        ).pack(pady=(10, 4))

        hint = (
            "KÃ©o & tháº£ file video hoáº·c thÆ° má»¥c vÃ o Ä‘Ã¢y\n"
            "hoáº·c báº¥m 'ThÃªm File' / 'ThÃªm ThÆ° Má»¥c'"
            if HAS_DND and getattr(self, "TkdndVersion", None)
            else "Báº¥m 'ThÃªm File' / 'ThÃªm ThÆ° Má»¥c' Ä‘á»ƒ báº¯t Ä‘áº§u"
        )

        tk.Label(
            empty, text=hint, bg=self.colors["bg"],
            fg=self.colors["muted"], font=("Segoe UI", 10), justify="center",
        ).pack(pady=(0, 8))

    def _render_task_card(self, task: VideoConversionTask):
        card_bg = self.colors["surface2"]
        if not task.enabled:
            card_bg = self.colors["bg"]

        card = tk.Frame(
            self.file_list_frame, bg=card_bg,
            highlightthickness=1,
            highlightbackground=self.colors["border"],
        )
        card.pack(fill="x", expand=True, pady=3, padx=4)

        row1 = tk.Frame(card, bg=card_bg)
        row1.pack(fill="x", padx=10, pady=(8, 2))

        if task.enabled:
            toggle_char = "â˜‘"
            toggle_fg = self.colors["success"]
        else:
            toggle_char = "â˜"
            toggle_fg = self.colors["muted"]

        toggle_btn = tk.Button(
            row1,
            text=toggle_char,
            command=lambda tid=task.task_id: self._toggle_task(tid),
            bg=card_bg,
            fg=toggle_fg,
            activebackground=card_bg,
            activeforeground=toggle_fg,
            disabledforeground=self.colors["muted"],
            bd=0,
            padx=2, pady=0,
            font=("Segoe UI", 16),
            cursor="hand2",
            relief="flat",
            highlightthickness=0,
            takefocus=0,
        )
        if self.is_processing:
            toggle_btn.configure(state="disabled")
        toggle_btn.pack(side="left", padx=(0, 8))

        name_color = self.colors["text"] if task.enabled else self.colors["muted"]
        tk.Label(
            row1, text=task.source_path.name, bg=card_bg,
            fg=name_color, font=("Segoe UI", 10, "bold"), anchor="w",
        ).pack(side="left", fill="x", expand=True)

        remove_btn = tk.Button(
            row1, text="âœ•",
            command=lambda tid=task.task_id: self.remove_task(tid),
            bg=card_bg, fg=self.colors["muted"],
            activebackground=self.colors["danger"],
            activeforeground="white",
            bd=0, padx=6, pady=0,
            font=("Segoe UI", 10), cursor="hand2",
            relief="flat",
            highlightthickness=0,
            takefocus=0,
        )
        if self.is_processing:
            remove_btn.configure(state="disabled")
        remove_btn.pack(side="right", padx=(4, 0))

        status_color = self.colors["text"]
        if task.status == "Completed":
            status_color = self.colors["success"]
        elif task.status == "Failed":
            status_color = self.colors["danger"]
        elif task.status in ("Processing", "Probing"):
            status_color = self.colors["accent"]
        elif task.status == "Cancelled":
            status_color = self.colors["warning"]

        tk.Label(
            row1, text=f"â— {task.status}", bg=card_bg,
            fg=status_color, font=("Segoe UI", 9),
        ).pack(side="right", padx=6)

        try:
            size_text = format_size(task.source_path.stat().st_size)
        except Exception:
            size_text = "?"
        tk.Label(
            row1, text=size_text, bg=card_bg,
            fg=self.colors["muted"], font=("Segoe UI", 9),
        ).pack(side="right", padx=6)

        if task.badge_type:
            badge_bg = self.colors["surface3"]
            if "REMUX" in task.badge_type:
                badge_bg = self.colors["success"]
            elif "EMERGENCY" in task.badge_type:
                badge_bg = self.colors["danger"]
            elif "SMART" in task.badge_type:
                badge_bg = self.colors["accent"]

            tk.Label(
                row1, text=task.badge_type, bg=badge_bg, fg="white",
                font=("Segoe UI", 8, "bold"), padx=6, pady=1,
            ).pack(side="right", padx=6)

        row2 = tk.Frame(card, bg=card_bg)
        row2.pack(fill="x", padx=(34, 10), pady=(0, 4))

        tk.Label(
            row2, text=str(task.source_path.parent), bg=card_bg,
            fg=self.colors["muted"], font=("Segoe UI", 8), anchor="w",
        ).pack(side="left", fill="x", expand=True)

        if task.status in ("Processing", "Probing") or (0 < task.progress < 1):
            row3 = tk.Frame(card, bg=card_bg)
            row3.pack(fill="x", padx=(34, 10), pady=(0, 6))

            pb = tk.Canvas(
                row3, height=6, bg=self.colors["surface3"],
                highlightthickness=0, bd=0,
            )
            pb.pack(fill="x", side="left", expand=True)

            def draw_progress(event=None, c=pb, t=task):
                try:
                    w = c.winfo_width()
                    c.delete("all")
                    fill_w = int(w * t.progress)
                    c.create_rectangle(
                        0, 0, fill_w, 6,
                        fill=self.colors["accent"], outline="",
                    )
                except Exception:
                    pass

            pb.bind("<Configure>", draw_progress)
            self.after(30, draw_progress)

            percent_lbl = tk.Label(
                row3, text=f"{int(task.progress * 100)}%",
                bg=card_bg, fg=self.colors["accent"],
                font=("Segoe UI", 8), width=4,
            )
            percent_lbl.pack(side="right", padx=(6, 0))

            self._progress_widgets[task.task_id] = (pb, percent_lbl)

        if task.plan:
            row4 = tk.Frame(card, bg=card_bg)
            row4.pack(fill="x", padx=(34, 10), pady=(0, 6))

            plan = task.plan
            parts = []
            if plan.copy_count:
                parts.append(f"âš¡ {plan.copy_count} copy")
            if plan.convert_count:
                parts.append(f"ðŸ”„ {plan.convert_count} convert")
            if plan.drop_count:
                parts.append(f"ðŸ§¹ {plan.drop_count} drop")

            tk.Label(
                row4, text=" Â· ".join(parts) if parts else "â€”",
                bg=card_bg, fg=self.colors["muted"],
                font=("Segoe UI", 9), anchor="w",
            ).pack(side="left", fill="x", expand=True)

            if task.used_attempt > 0:
                tk.Label(
                    row4,
                    text=f"Attempt {task.used_attempt}/{self.MAX_ATTEMPTS}",
                    bg=card_bg, fg=self.colors["muted"], font=("Segoe UI", 8),
                ).pack(side="right", padx=4)

        if task.converted_streams:
            row5 = tk.Frame(card, bg=card_bg)
            row5.pack(fill="x", padx=(34, 10), pady=(0, 2))
            tk.Label(
                row5,
                text="Converted: " + " | ".join(task.converted_streams[:4]),
                bg=card_bg, fg=self.colors["accent"], font=("Segoe UI", 8),
                anchor="w", wraplength=900, justify="left",
            ).pack(side="left", fill="x", expand=True)

        if task.dropped_streams:
            row6 = tk.Frame(card, bg=card_bg)
            row6.pack(fill="x", padx=(34, 10), pady=(0, 2))
            tk.Label(
                row6,
                text="Filtered: " + " | ".join(task.dropped_streams[:4]),
                bg=card_bg, fg=self.colors["warning"], font=("Segoe UI", 8),
                anchor="w", wraplength=900, justify="left",
            ).pack(side="left", fill="x", expand=True)

        if task.error_message:
            row7 = tk.Frame(card, bg=card_bg)
            row7.pack(fill="x", padx=(34, 10), pady=(0, 8))
            tk.Label(
                row7, text=task.error_message[:400],
                bg=card_bg, fg=self.colors["danger"], font=("Segoe UI", 8),
                anchor="w", wraplength=900, justify="left",
            ).pack(side="left", fill="x", expand=True)

        tk.Frame(card, bg=card_bg, height=4).pack(fill="x")

        # [U2] Bind chuá»™t pháº£i cho toÃ n bá»™ card + widget con.
        self._bind_context_menu_recursive(card, task)

    def _bind_context_menu_recursive(self, widget, task: VideoConversionTask):
        """Gáº¯n sá»± kiá»‡n chuá»™t pháº£i cho widget vÃ  toÃ n bá»™ widget con."""
        try:
            widget.bind(
                "<Button-3>",
                lambda e, t=task: self._show_context_menu(e, t),
            )
            # macOS dÃ¹ng Button-2 cho right-click / control-click.
            widget.bind(
                "<Button-2>",
                lambda e, t=task: self._show_context_menu(e, t),
            )
        except Exception:
            pass

        try:
            for child in widget.winfo_children():
                self._bind_context_menu_recursive(child, task)
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # Profile from UI
    # -------------------------------------------------------------------------

    def get_profile_from_ui(self) -> VideoConversionProfile:
        target_map = {
            "MP4": "mp4", "MKV": "mkv", "WEBM": "webm",
            "MOV": "mov", "AVI": "avi", "TS": "ts",
        }
        mode_map = {
            "Auto (Copy > Convert)": "auto",
            "Force Re-encode": "reencode",
            "Force Copy": "copy",
        }
        codec_map = {
            "H.264": "h264", "H.265 / HEVC": "hevc",
            "VP9": "vp9", "AV1": "av1",
        }

        return VideoConversionProfile(
            target_container=target_map[self.controls["cb_target"].get()],
            video_mode=mode_map[self.controls["cb_vmode"].get()],
            video_codec=codec_map[self.controls["cb_vcodec"].get()],
            video_crf=int(self.controls["cb_crf"].get()),
            video_preset=self.controls["cb_preset"].get(),
            audio_mode=mode_map[self.controls["cb_amode"].get()],
            audio_codec="",
            audio_bitrate="",
            subtitle_mode="auto",
            keep_metadata=self.keep_metadata_var.get(),
            keep_chapters=self.keep_chapters_var.get(),
            keep_attachments=self.keep_attachments_var.get(),
            keep_data_streams=self.keep_data_var.get(),
            faststart=True,
            rate_cap_enabled=self.rate_cap_var.get(),
            reprocess_completed=self.reprocess_completed_var.get(),
            adaptive_crf=self.adaptive_crf_var.get(),
            use_gpu=self.use_gpu_var.get(),
        )

    # -------------------------------------------------------------------------
    # Start / Cancel
    # -------------------------------------------------------------------------

    def start_processing(self):
        if self.is_processing:
            return

        # [F14] Äá»“ng bá»™ Entry â†’ self.output_dir TRÆ¯á»šC khi spawn worker.
        # FocusOut/Return cÃ³ thá»ƒ chÆ°a ká»‹p báº¯n khi user gÃµ tay Ä‘Æ°á»ng dáº«n
        # rá»“i báº¥m tháº³ng nÃºt Start (nháº¥t lÃ  khi nÃºt cÃ³ takefocus=0).
        self._on_outdir_changed()

        enabled_tasks = [t for t in self.tasks if t.enabled]
        if not enabled_tasks:
            messagebox.showinfo(
                "ThÃ´ng bÃ¡o",
                "KhÃ´ng cÃ³ file nÃ o Ä‘Æ°á»£c báº­t Ä‘á»ƒ convert.\n\n"
                "HÃ£y tick chá»n file báº¡n muá»‘n xá»­ lÃ½.",
            )
            return

        ok, msg = self.engine.check_tools()
        if not ok:
            messagebox.showerror("FFmpeg Error", msg)
            return

        profile = self.get_profile_from_ui()

        self.is_processing = True
        self.cancel_event.clear()
        self._reserved_names.clear()

        # [N1] Ghi nhá»› sá»‘ task cá»§a batch Ä‘á»ƒ popup tá»•ng káº¿t chá»‰ hiá»‡n
        # khi thá»±c sá»± cÃ³ task Ä‘Æ°á»£c xá»­ lÃ½.
        self._batch_task_count = len(enabled_tasks)

        self._set_ui_locked(True)

        self.btn_start.config(state="disabled")
        self.btn_cancel.config(state="normal")
        self.global_progress.configure(value=0)

        self.render_file_list()

        # Log Ä‘á»ƒ dá»… debug â€” xÃ¡c nháº­n Ä‘Ãºng thÆ° má»¥c Ä‘ang dÃ¹ng.
        self._log(f"ðŸ“‚ ThÆ° má»¥c xuáº¥t: {self.output_dir}")

        worker = threading.Thread(
            target=self._process_worker,
            args=(profile, enabled_tasks),
            daemon=True,
        )
        worker.start()

    def cancel_processing(self):
        if self.is_processing:
            self.cancel_event.set()
            self._log("âš  ÄÃ£ gá»­i yÃªu cáº§u huá»·.")
        if self._scan_in_progress:
            self._scan_cancel_event.set()
            self._log("âš  ÄÃ£ gá»­i yÃªu cáº§u huá»· quÃ©t thÆ° má»¥c.")

    # -------------------------------------------------------------------------
    # Worker â€” Ä‘iá»u phá»‘i batch
    # -------------------------------------------------------------------------

    def _process_worker(
        self,
        profile: VideoConversionProfile,
        tasks_snapshot: List[VideoConversionTask],
    ):
        try:
            try:
                self.output_dir.mkdir(parents=True, exist_ok=True)
            except Exception as exc:
                self._log(f"âœ— KhÃ´ng thá»ƒ táº¡o output folder: {exc}")
                return

            total = len(tasks_snapshot)

            for idx, task in enumerate(tasks_snapshot, start=1):
                if self.cancel_event.is_set():
                    if task.status not in {"Completed", "Failed"}:
                        task.status = "Cancelled"
                        self._ui(self.render_file_list)
                    break

                if task.status == "Completed" and not profile.reprocess_completed:
                    self._log(
                        f"[{idx}/{total}] Bá» qua (Ä‘Ã£ Completed): "
                        f"{task.source_path.name}"
                    )
                    progress = idx / max(total, 1) * 100
                    self._ui(
                        lambda v=progress: self.global_progress.configure(value=v)
                    )
                    continue

                try:
                    self._process_one_task_iteration(task, profile, idx, total)
                except Exception as exc:
                    task.status = "Failed"
                    task.error_message = f"Worker exception: {exc}"
                    self._log(
                        f"âœ— Worker exception task "
                        f"{task.source_path.name}: {exc}"
                    )
                    self._ui(self.render_file_list)

                progress = idx / max(total, 1) * 100
                self._ui(
                    lambda v=progress: self.global_progress.configure(value=v)
                )
                self._ui(self.render_file_list)
        except Exception as exc:
            self._log(f"âœ— Worker fatal error: {exc}")
        finally:
            self._processing_finished()

    def _process_one_task_iteration(
        self,
        task: VideoConversionTask,
        profile: VideoConversionProfile,
        idx: int,
        total: int,
    ):
        task.status = "Probing"
        task.progress = 0.0
        task.error_message = ""
        task.badge_type = ""
        task.dropped_streams = []
        task.converted_streams = []
        task.used_attempt = 0
        task.used_tier = 0
        self._ui(self.render_file_list)

        self._log(f"[{idx}/{total}] Báº¯t Ä‘áº§u: {task.source_path.name}")

        success = self._process_one_task(task, profile)

        if success:
            task.status = "Completed"
            self._log(f"âœ“ HoÃ n táº¥t: {task.source_path.name}")
        else:
            if self.cancel_event.is_set():
                task.status = "Cancelled"
            else:
                task.status = "Failed"
            self._log(
                f"âœ— {task.status}: {task.source_path.name} "
                f"- {task.error_message}"
            )

    def _processing_finished(self):
        self.is_processing = False
        self._ui(lambda: self._set_ui_locked(False))
        self._ui(lambda: self.btn_start.config(state="normal"))
        self._ui(lambda: self.btn_cancel.config(state="disabled"))
        self._ui(self.render_file_list)
        self._log("ðŸ HÃ ng Ä‘á»£i Ä‘Ã£ káº¿t thÃºc.")
        # [N1] Popup tá»•ng káº¿t khi batch xá»­ lÃ½ xong.
        self._ui(self._show_completion_popup)

    # -------------------------------------------------------------------------
    # [N1] Popup tá»•ng káº¿t khi xá»­ lÃ½ xong
    # -------------------------------------------------------------------------

    def _show_completion_popup(self):
        """Popup tá»•ng káº¿t batch khi worker káº¿t thÃºc.

        Chá»‰ hiá»‡n khi batch cÃ³ task thá»±c sá»± Ä‘Æ°á»£c xá»­ lÃ½ (khÃ´ng hiá»‡n khi
        start_processing bá»‹ cháº·n sá»›m do khÃ´ng cÃ³ file / thiáº¿u FFmpeg).
        """
        if self._batch_task_count <= 0:
            return

        total = len(self.tasks)
        if total == 0:
            return

        completed = sum(1 for t in self.tasks if t.status == "Completed")
        failed = sum(1 for t in self.tasks if t.status == "Failed")
        cancelled = sum(1 for t in self.tasks if t.status == "Cancelled")
        # CÃ¡c task cÃ²n status Pending/Processing/Probing coi nhÆ° chÆ°a xá»­ lÃ½
        # (thÆ°á»ng xáº£y ra khi user huá»· giá»¯a batch).
        pending = total - completed - failed - cancelled

        lines: List[str] = []
        lines.append(f"Tá»•ng sá»‘ file trong danh sÃ¡ch: {total}")
        lines.append(f"âœ… ThÃ nh cÃ´ng: {completed}")
        if failed:
            lines.append(f"âŒ Tháº¥t báº¡i: {failed}")
        if cancelled:
            lines.append(f"ðŸš« ÄÃ£ huá»·: {cancelled}")
        if pending:
            lines.append(f"â¸ ChÆ°a xá»­ lÃ½: {pending}")
        lines.append("")
        lines.append(f"ðŸ“‚ ThÆ° má»¥c xuáº¥t:\n{self.output_dir}")

        body = "\n".join(lines)

        try:
            if failed == 0 and cancelled == 0 and pending == 0 and completed > 0:
                messagebox.showinfo("âœ… HoÃ n táº¥t", body)
            elif completed > 0 or failed > 0 or cancelled > 0:
                messagebox.showwarning("âš  Xá»­ lÃ½ xong", body)
            # Náº¿u khÃ´ng cÃ³ gÃ¬ xá»­ lÃ½ xong thÃ¬ im láº·ng.
        except Exception:
            pass

        # Reset counter sau khi Ä‘Ã£ hiá»ƒn thá»‹ popup.
        self._batch_task_count = 0

    # -------------------------------------------------------------------------
    # Output filename
    # -------------------------------------------------------------------------

    def _name_key(self, path: Path) -> str:
        try:
            resolved = str(path.resolve())
        except Exception:
            resolved = str(path)
        if os.name == "nt" or sys.platform == "darwin":
            return resolved.lower()
        return resolved

    def make_unique_output_path(self, source: Path, extension: str) -> Path:
        def is_available(p: Path) -> bool:
            try:
                if p.resolve() == source.resolve():
                    return False
            except Exception:
                pass
            if p.exists():
                return False
            if self._name_key(p) in self._reserved_names:
                return False
            return True

        def reserve(p: Path) -> Path:
            self._reserved_names.add(self._name_key(p))
            return p

        base = self.output_dir / f"{source.stem}.{extension}"
        if is_available(base):
            return reserve(base)

        for i in range(1, 10000):
            candidate = self.output_dir / f"{source.stem} ({i}).{extension}"
            if is_available(candidate):
                return reserve(candidate)

        fallback = self.output_dir / (
            f"{source.stem}_{uuid.uuid4().hex[:8]}.{extension}"
        )
        return reserve(fallback)

    def _unreserve_output_path(self, path: Path):
        try:
            self._reserved_names.discard(self._name_key(path))
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # Attempt helpers
    # -------------------------------------------------------------------------

    def _compute_tolerance_and_emergency(self, attempt: int) -> Tuple[int, bool]:
        if attempt == 1:
            return 1, False
        if attempt == self.MAX_ATTEMPTS:
            return 2, True
        return 2, False

    def _compute_badge(self, plan: ConversionPlan, emergency: bool) -> str:
        if emergency:
            return "ðŸ”¥ EMERGENCY"
        if plan.is_pure_remux:
            return "âš¡ PURE REMUX"
        if plan.convert_count > 0 and plan.drop_count > 0:
            return "ðŸ§¹ SMART"
        if plan.convert_count > 0:
            return "ðŸ”„ SMART"
        return "ðŸ§¹ FILTERED"

    def _apply_attempt_mutation(
        self,
        attempt: int,
        overrides: Dict[int, str],
        probe: VideoProbe,
        task: VideoConversionTask,
    ):
        if attempt == 3:
            primary = self.engine.choose_primary_video(probe.streams)
            if primary and overrides.get(primary.index) != "convert":
                overrides[primary.index] = "convert"
                self._log(
                    f"  â†’ KhÃ´ng rÃµ stream lá»—i; "
                    f"video chÃ­nh #{primary.index} â†’ CONVERT."
                )
        elif attempt == 4:
            for s in probe.streams:
                if s.codec_type == "audio" and overrides.get(s.index) != "convert":
                    overrides[s.index] = "convert"
                    self._log(f"  â†’ Audio #{s.index} nÃ¢ng lÃªn CONVERT.")
                    break
        elif attempt == 5:
            changed = False
            for s in probe.streams:
                if s.codec_type == "audio" and overrides.get(s.index) != "convert":
                    overrides[s.index] = "convert"
                    changed = True
            if changed:
                self._log("  â†’ Ã‰p toÃ n bá»™ audio CONVERT.")
        elif attempt == 6:
            changed = False
            for s in probe.streams:
                if s.codec_type == "subtitle":
                    overrides[s.index] = "drop"
                    changed = True
            if changed:
                self._log("  â†’ Loáº¡i subtitle Ä‘á»ƒ tÄƒng kháº£ nÄƒng hoÃ n táº¥t.")

    def _escalate_muxer_refused(
        self,
        overrides: Dict[int, str],
        plan: ConversionPlan,
        probe: VideoProbe,
        task: VideoConversionTask,
    ) -> bool:
        changed = False
        for action in plan.actions:
            if action.action != "copy":
                continue
            if action.codec_type not in {"video", "audio"}:
                continue
            if overrides.get(action.stream_index) == "convert":
                continue
            overrides[action.stream_index] = "convert"
            changed = True
            stream = next(
                (s for s in probe.streams if s.index == action.stream_index),
                None,
            )
            codec_name = stream.codec_name if stream else "?"
            self._log(
                f"  â†’ Muxer tá»« chá»‘i (khÃ´ng rÃµ stream cá»¥ thá»ƒ): "
                f"#{action.stream_index} {action.codec_type}/{codec_name} "
                f"COPY â†’ CONVERT"
            )
        return changed

    def _warn_force_copy_mismatch(
        self,
        profile: VideoConversionProfile,
        probe: VideoProbe,
    ):
        target = profile.target_container.lower()
        compat = CONTAINER_COMPAT.get(target, CONTAINER_COMPAT["mp4"])

        if profile.video_mode == "copy":
            allowed = compat.get("video_allowed")
            if allowed is not None:
                for s in probe.streams:
                    if s.codec_type != "video" or s.is_attached_pic:
                        continue
                    if s.codec_name not in allowed:
                        self._log(
                            f"  âš  Force Copy video #{s.index}: "
                            f"codec {s.codec_name} khÃ´ng thuá»™c allowlist "
                            f"{target} â€” cÃ³ thá»ƒ fail; sáº½ tá»± chuyá»ƒn convert "
                            f"khi cÃ´ng cá»¥ tá»« chá»‘i."
                        )

        if profile.audio_mode == "copy":
            allowed = compat.get("audio_allowed")
            if allowed is not None:
                for s in probe.streams:
                    if s.codec_type != "audio":
                        continue
                    if s.codec_name not in allowed:
                        self._log(
                            f"  âš  Force Copy audio #{s.index}: "
                            f"codec {s.codec_name} khÃ´ng thuá»™c allowlist "
                            f"{target} â€” cÃ³ thá»ƒ fail; sáº½ tá»± chuyá»ƒn convert "
                            f"khi cÃ´ng cá»¥ tá»« chá»‘i."
                        )

    # -------------------------------------------------------------------------
    # Single task orchestration
    # -------------------------------------------------------------------------

    def _process_one_task(
        self,
        task: VideoConversionTask,
        profile: VideoConversionProfile,
    ) -> bool:

        probe, report = self.engine.lenient_probe(task.source_path)
        task.probe = probe
        task.issue_report = report

        if not probe:
            task.error_message = (
                "Probe tháº¥t báº¡i. " + " ".join(report.details[-3:])
            )
            return False

        primary = self.engine.choose_primary_video(probe.streams)
        if not primary:
            task.error_message = "File khÃ´ng cÃ³ video chÃ­nh."
            return False

        self._log(
            f"  Probe: {probe.format_name or '?'} Â· "
            f"{format_size(probe.size)} Â· "
            f"{format_duration(probe.duration)} Â· "
            f"{len(probe.streams)} streams"
        )

        self._warn_force_copy_mismatch(profile, probe)

        for stream in probe.streams:
            junk, reason = self.engine.stream_is_junk(stream, profile)
            if junk:
                desc = f"#{stream.index} {stream.codec_type}/{stream.codec_name}"
                task.dropped_streams.append(desc)
                self._log(f"  ðŸ§¹ DROP stream {desc}: {reason}")

        compat = CONTAINER_COMPAT.get(
            profile.target_container.lower(),
            CONTAINER_COMPAT["mp4"],
        )
        extension = compat["ext"]

        final_output = self.make_unique_output_path(
            task.source_path, extension,
        )
        temp_output = self.output_dir / (
            f".vcp_{uuid.uuid4().hex}.{extension}"
        )

        task.status = "Processing"
        self._ui(self.render_file_list)

        success = False
        try:
            success = self._execute_task_attempts(
                task, profile, temp_output, final_output,
            )
        finally:
            self._cleanup_temp(temp_output)
            if not success:
                self._unreserve_output_path(final_output)

        return success

    # -------------------------------------------------------------------------
    # Fallback ladder â€” 7 attempt
    # -------------------------------------------------------------------------

    def _execute_task_attempts(
        self,
        task: VideoConversionTask,
        profile: VideoConversionProfile,
        temp_output: Path,
        final_output: Path,
    ) -> bool:
        probe = task.probe
        overrides: Dict[int, str] = {}
        last_error = ""
        last_plan_sig = None
        last_render_ts = {"t": 0.0}

        def progress_cb(p):
            task.progress = p
            now = time.time()
            # Chá»‰ váº½ láº¡i thanh % â€” KHÃ”NG re-render cáº£ file list.
            if now - last_render_ts["t"] >= 0.12:
                last_render_ts["t"] = now
                self._ui(
                    lambda tid=task.task_id, pr=p:
                    self._update_task_progress(tid, pr)
                )

        for attempt in range(1, self.MAX_ATTEMPTS + 1):
            if self.cancel_event.is_set():
                task.error_message = "ÄÃ£ huá»·."
                return False

            self._cleanup_temp(temp_output)

            task.used_attempt = attempt
            tolerance, emergency = self._compute_tolerance_and_emergency(attempt)
            task.used_tier = 3 if emergency else tolerance

            plan = self.engine.build_conversion_plan(probe, profile, overrides)
            task.plan = plan
            task.badge_type = self._compute_badge(plan, emergency)
            task.converted_streams = [
                f"#{a.stream_index} {a.codec_type} â†’ {a.target_codec or '?'} ({a.reason})"
                for a in plan.actions
                if a.action == "convert"
            ]
            task.dropped_streams = [
                f"#{a.stream_index} {a.codec_type} ({a.reason})"
                for a in plan.actions
                if a.action == "drop"
            ]
            self._ui(self.render_file_list)

            plan_sig = (
                tolerance,
                tuple(
                    (a.stream_index, a.action, a.target_codec or "")
                    for a in plan.actions
                ),
            )
            if not emergency and plan_sig == last_plan_sig:
                self._log(
                    f"  Attempt {attempt}/{self.MAX_ATTEMPTS}: "
                    f"plan khÃ´ng Ä‘á»•i â†’ bá» qua."
                )
                self._apply_attempt_mutation(attempt, overrides, probe, task)
                continue
            last_plan_sig = plan_sig

            self._log(
                f"  Attempt {attempt}/{self.MAX_ATTEMPTS} "
                f"Â· tier {task.used_tier} "
                f"Â· {plan.copy_count} copy / "
                f"{plan.convert_count} convert / "
                f"{plan.drop_count} drop"
            )

            if emergency:
                cmd = self.engine.build_emergency_command(
                    task.source_path, probe, temp_output, profile,
                )
                if not cmd:
                    last_error = "Emergency command build failed."
                    break
                self._log("  â†’ Emergency: full re-encode + transcode audio.")
            else:
                cmd = self.engine.build_ffmpeg_command(
                    task.source_path, plan, temp_output,
                    profile, probe, tolerance_level=tolerance,
                )

            rc, stderr = self.engine.execute_ffmpeg_process(
                cmd,
                duration=probe.duration,
                progress_callback=progress_cb,
                cancel_event=self.cancel_event,
            )

            if rc == -1 and self.cancel_event.is_set():
                task.error_message = "ÄÃ£ huá»·."
                return False

            if rc == 0:
                verify_plan = None if emergency else plan
                valid, reason, _ = self.engine.verify_output(
                    temp_output, probe, plan=verify_plan,
                )
                if valid:
                    try:
                        shutil.move(str(temp_output), str(final_output))
                    except Exception as exc:
                        last_error = f"KhÃ´ng thá»ƒ move output: {exc}"
                        break

                    task.progress = 1.0
                    self._log(f"  âœ“ {reason} â†’ {final_output.name}")
                    return True

                last_error = f"Verify tháº¥t báº¡i: {reason}"
                self._log(f"  âš  FFmpeg OK nhÆ°ng verify fail: {reason}")
            else:
                last_error = (
                    stderr.strip()[-2500:]
                    if stderr and stderr.strip()
                    else f"FFmpeg exit code {rc}"
                )

            bad_stream = self.engine.parse_stderr_for_bad_stream(stderr)
            timestamp_problem = self.engine.stderr_indicates_timestamp_problem(stderr)
            muxer_refused = self.engine.stderr_indicates_muxer_refusal(stderr)

            if timestamp_problem:
                self._log("  âš  PhÃ¡t hiá»‡n lá»—i timestamp/DTS/PTS.")

            if bad_stream is not None:
                stream = next(
                    (s for s in probe.streams if s.index == bad_stream),
                    None,
                )
                if stream:
                    current = self.engine.get_current_action(
                        plan, bad_stream, overrides,
                    )
                    if current is None:
                        current = "copy"

                    if current == "copy":
                        if muxer_refused is None and attempt < 2:
                            self._log(
                                f"  â†’ Stream #{bad_stream} "
                                f"{stream.codec_type}/{stream.codec_name}: "
                                f"copy lá»—i decode; thá»­ láº¡i vá»›i tolerance "
                                f"cao hÆ¡n trÆ°á»›c khi convert."
                            )
                            continue

                        overrides[bad_stream] = "convert"
                        desc = f"#{stream.index} {stream.codec_type}/{stream.codec_name}"
                        if desc not in task.converted_streams:
                            task.converted_streams.append(desc)
                        if muxer_refused is not None:
                            self._log(
                                f"  â†’ Stream #{bad_stream} "
                                f"{stream.codec_type}/{stream.codec_name}: "
                                f"muxer/container tá»« chá»‘i copy â†’ CONVERT"
                            )
                        else:
                            self._log(
                                f"  â†’ Stream #{bad_stream} "
                                f"{stream.codec_type}/{stream.codec_name}: "
                                f"copy fail á»Ÿ tolerance cao nháº¥t â†’ CONVERT"
                            )
                        continue

                    if current == "convert":
                        primary = self.engine.choose_primary_video(probe.streams)
                        if primary and stream.index == primary.index:
                            self._log(
                                f"  â†’ Video chÃ­nh #{bad_stream} "
                                f"khÃ´ng Ä‘Æ°á»£c DROP; chuyá»ƒn emergency."
                            )
                            continue

                        if stream.codec_type in {"subtitle", "data", "unknown"}:
                            overrides[bad_stream] = "drop"
                            self._log(
                                f"  â†’ Stream #{bad_stream} CONVERT fail â†’ DROP"
                            )
                            continue

                        if stream.codec_type == "audio":
                            primary_audio = self.engine.choose_primary_audio(
                                probe.streams,
                            )
                            if primary_audio and stream.index == primary_audio.index:
                                self._log(
                                    f"  â†’ Audio chÃ­nh #{bad_stream} "
                                    f"khÃ´ng Ä‘Æ°á»£c DROP; giá»¯ CONVERT."
                                )
                                continue

                            audio_streams = [
                                s for s in probe.streams
                                if s.codec_type == "audio"
                            ]
                            if len(audio_streams) > 1:
                                overrides[bad_stream] = "drop"
                                self._log(
                                    f"  â†’ Audio phá»¥ #{bad_stream} "
                                    f"CONVERT fail â†’ DROP"
                                )
                                continue
                            self._log(
                                f"  â†’ Audio chÃ­nh #{bad_stream} giá»¯, tiáº¿p tá»¥c."
                            )
                            continue

                    self._apply_attempt_mutation(attempt, overrides, probe, task)
            elif muxer_refused is not None:
                escalated = self._escalate_muxer_refused(
                    overrides, plan, probe, task,
                )
                if not escalated:
                    self._apply_attempt_mutation(attempt, overrides, probe, task)
            else:
                self._apply_attempt_mutation(attempt, overrides, probe, task)

        task.error_message = (
            last_error or "Xá»­ lÃ½ tháº¥t báº¡i sau toÃ n bá»™ fallback."
        )[:2500]
        return False

    def _cleanup_temp(self, temp_path: Optional[Path]):
        if temp_path and temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                pass


# =============================================================================
# 8. MAIN
# =============================================================================

def main():
    app = VideoConverterUI()

    # [P5] Nháº­n file tá»« "Open with..." / kÃ©o tháº£ vÃ o exe / command line.
    # DÃ¹ng after() Ä‘á»ƒ Ä‘áº£m báº£o UI Ä‘Ã£ render xong trÆ°á»›c khi add task,
    # trÃ¡nh race vá»›i _drain_ui_queue khá»Ÿi Ä‘á»™ng trong __init__.
    cli_args = sys.argv[1:]
    if cli_args:
        app.after(50, lambda: app.load_cli_args(cli_args))

    app.mainloop()


if __name__ == "__main__":
    main()

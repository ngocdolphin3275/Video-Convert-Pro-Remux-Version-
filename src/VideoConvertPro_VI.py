#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
🎬 VIDEO CONVERTER PRO v3.9.5
===============================================================================

Container-First · Stream Sanitizer · Smart Fallback · Source-Matched Quality

Triết lý:

    COPY > CONVERT > DROP

Nguyên tắc:

1. Container đích quyết định codec nào được phép giữ.
2. Stream bình thường được COPY nếu có thể.
3. Stream không tương thích mới CONVERT (không ép copy codec ngoài allowlist).
4. Stream rác / không cần thiết mới DROP.
5. Khi FFmpeg thất bại:
       COPY (chịu lỗi tối đa) → CONVERT → DROP
   Video/audio gốc đã lỗi sẵn → ưu tiên copy chịu lỗi; chỉ convert khi
   công cụ thực sự từ chối (muxer refuse). Không tự ý DROP video/audio chính.
6. Khi bắt buộc re-encode video:
       - Giữ resolution.
       - Giữ timing/FPS nếu có thể (fps_mode passthrough).
       - Giữ pixel format / bit depth nếu encoder hỗ trợ.
       - Giữ màu/HDR metadata khi có thể.
       - Không upscale.
       - Ưu tiên chất lượng cao.
7. Tolerance flags được bật cho MỌI lệnh FFmpeg.
8. Output chỉ được xem là thành công sau khi probe lại, có video + audio
   (nếu nguồn có), duration ≥ 90% so với nguồn.
9. Không thao tác Tkinter trực tiếp từ worker thread.

-------------------------------------------------------------------------------
CHANGELOG v3.9.5 (UI only):

[N1] Thêm popup thông báo khi hàng đợi xử lý xong:
       - Hiển thị tổng số file, số thành công / thất bại / đã huỷ / chưa xử lý.
       - Kèm đường dẫn thư mục xuất.
       - Nếu tất cả thành công → showinfo (✅ Hoàn tất).
       - Nếu có file fail / huỷ / chưa xử lý → showwarning (⚠ Xử lý xong).
     CHỈ sửa UI, không đụng logic worker / engine.

Các fix từ v2.7 → v3.9.4 vẫn giữ nguyên.
Không đụng vào: container matrix, plan structure, encoder preset mapping,
DnD core, thread model, naming policy, verify logic, checkbox logic,
các button khác, fallback ladder, emergency command.

-------------------------------------------------------------------------------
CHANGELOG v3.9.4 (fix bug thư mục xuất):

[F14] Thư mục xuất nhập tay không được áp dụng khi bấm thẳng nút Start:
     - Fix: trong start_processing() chủ động gọi _on_outdir_changed()
       để đồng bộ Entry → self.output_dir ngay trước khi spawn worker.
     Ngoài ra _on_outdir_changed() chuẩn hoá đường dẫn tương đối thành
     tuyệt đối để tránh ghi nhầm vào CWD.

-------------------------------------------------------------------------------
CHANGELOG v3.9.3 (UI only):

[U2] Thêm menu chuột phải (Context Menu) cho từng file trong danh sách:
       - Bật / Tắt file (toggle)
       - Mở file nguồn (bằng trình phát mặc định của OS)
       - Mở thư mục chứa file nguồn
       - Xoá khỏi danh sách
     Menu có màu tối đồng bộ với theme của app. CHỈ sửa UI, không đụng logic.

-------------------------------------------------------------------------------
CHANGELOG v3.9.2 (UI only):

[U1] Dropdown "Video Codec" giờ tự động lọc theo Container đang chọn.
     Khi đổi Container, nếu codec đang chọn không còn hợp lệ, tự reset về
     option đầu tiên và ghi log cảnh báo. CHỈ sửa UI, không đụng logic.

-------------------------------------------------------------------------------
CHANGELOG v3.9.1 (GPU + UI):

[G1] Thêm hỗ trợ NVIDIA NVENC (h264_nvenc / hevc_nvenc / av1_nvenc).
     Tự fallback CPU nếu GPU/encoder không khả dụng.
[G2] Fix giật thanh tiến trình: chỉ vẽ lại canvas % của task đang chạy,
     không rebuild toàn bộ file list mỗi lần update progress.
[G3] Thư mục xuất: cho phép gõ tay đường dẫn (Entry), thêm nút "📂 Mở"
     để mở thư mục bằng trình quản lý file của OS.

-------------------------------------------------------------------------------
CHANGELOG v3.9 (fix theo review cuối):

[F13] attached_pic khi bị ép convert → DROP thay vì tạo track "video" giả.

Các fix từ v2.7 → v3.8 vẫn giữ nguyên.

-------------------------------------------------------------------------------
CHANGELOG BUILD/PACKAGING (v3.9.5-pack):

[P1] Thêm helper _app_base_dir() / _bundle_dir() / find_binary() /
     find_resource() để app tự tìm ffmpeg / ffprobe / icon.ico khi đóng gói
     PyInstaller (onedir hoặc onefile).
       - Ưu tiên 1: cạnh file EXE (onedir: cùng folder với EXE).
       - Ưu tiên 2: thư mục _internal / _MEIPASS (bundle PyInstaller).
       - Ưu tiên 3: PATH của OS.
[P2] ConversionEngine.__init__ dùng find_binary() để resolve ffmpeg/ffprobe.
[P3] VideoConverterUI tự set icon cửa sổ từ icon.ico (cạnh EXE hoặc bundle).
     Chỉ thêm UI setup, không đụng logic worker/engine.
[P4] Dark title bar trên Windows 10/11 qua DwmSetWindowAttribute.
     Gọi 2 lần (ngay + after 20ms) để đảm bảo HWND đã sẵn sàng.
     Trên OS khác tự bỏ qua im lặng. CHỈ sửa UI, không đụng logic.
[P5] Nhận file/thư mục từ command line ("Open with...", kéo thả vào exe).
     main() đọc sys.argv[1:] và gọi load_cli_args() sau khi UI khởi động.
     CHỈ thêm task vào danh sách, không đụng logic convert.
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
    """Thư mục gốc chứa app.

    - Frozen (PyInstaller): thư mục chứa file .exe.
      Onedir  → dist/VideoConvertPro/  (chứa exe + _internal/)
      Onefile → thư mục user chạy exe (chỉ có exe).
    - Dev: thư mục chứa script .py.
    """
    if getattr(sys, "frozen", False):
        try:
            return Path(sys.executable).resolve().parent
        except Exception:
            return Path(sys.executable).parent
    return Path(__file__).resolve().parent


def _bundle_dir() -> Optional[Path]:
    """Thư mục tạm PyInstaller giải nén bundle (_MEIPASS).

    PyInstaller ≥ 5.x đặt _MEIPASS = .../_internal với onedir,
    và = thư mục _MEIxxxx với onefile. Trả None nếu chạy dev.
    """
    meipass = getattr(sys, "_MEIPASS", None)
    if not meipass:
        return None
    try:
        return Path(meipass)
    except Exception:
        return None


def _candidate_dirs() -> List[Path]:
    """Thứ tự ưu tiên tìm binary/resource:
        1. Cạnh EXE (cho phép user drop thêm ffmpeg ngoài cùng folder).
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
    """Tìm binary (ffmpeg, ffprobe).

    Trả absolute path nếu tìm thấy, ngược lại trả nguyên `name` để OS
    tự resolve qua PATH.
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
    """Tìm resource (icon, asset). Trả Path nếu có, None nếu không."""
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

# [U1] Map Container (label UI) → danh sách codec video (label UI) hợp lệ.
# CHỈ dùng để lọc dropdown trên UI. Logic engine vẫn dùng CONTAINER_COMPAT.
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

# Map codec → encoder NVENC tương ứng
NVENC_ENCODER_FOR_CODEC = {
    "h264": "h264_nvenc",
    "hevc": "hevc_nvenc",
    "h265": "hevc_nvenc",
    "av1": "av1_nvenc",
}

# Map preset libx264-style → preset NVENC (p1..p7)
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
        # [P2] Tự resolve ffmpeg / ffprobe:
        #   - ưu tiên file cạnh EXE
        #   - sau đó tới _internal/_MEIPASS (bundle PyInstaller)
        #   - cuối cùng mới để OS tìm trong PATH
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
                    return False, f"{name} không chạy được."
            except Exception as exc:
                return False, f"Không tìm thấy {name}: {exc}"
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
        """Kiểm tra NVENC thực tế một lần và cache kết quả theo từng encoder."""
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
        """Chọn NVENC encoder phù hợp nếu GPU + codec khả dụng."""
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

        # Auto: thử lần lượt h264 → hevc → av1
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
                        "Người dùng chỉ định codec audio.",
                    )

        source_is_lossless = self.is_lossless_audio(stream.codec_name)

        if source_is_lossless:
            lossless_codec = LOSSLESS_AUDIO_TARGET_BY_CONTAINER.get(target_container)
            if lossless_codec and self.has_encoder(lossless_codec):
                extra = LOSSLESS_AUDIO_ENCODE_EXTRA.get(lossless_codec, [])
                return (
                    lossless_codec, None, None, extra,
                    f"Nguồn lossless → giữ lossless ({lossless_codec}).",
                )
            downgrade_prefix = (
                f"Nguồn lossless nhưng {target_container} không có "
                f"codec lossless khả dụng → hạ xuống lossy chất lượng cao nhất: "
            )
        else:
            downgrade_prefix = ""

        if target_container == "webm":
            bitrate = smart_lossy_audio_bitrate(stream.channels)
            return (
                "libopus", bitrate, None, [("vbr", "on")],
                downgrade_prefix + f"Opus VBR chất lượng cao (~{bitrate}).",
            )

        if target_container == "avi":
            return (
                "libmp3lame", None, "0", [],
                downgrade_prefix + "MP3 VBR chất lượng cao nhất (-q:a 0).",
            )

        if self.has_encoder("libfdk_aac"):
            return (
                "libfdk_aac", None, "5", [],
                downgrade_prefix + "AAC VBR chất lượng cao nhất (libfdk_aac, tương đương chuẩn Apple).",
            )

        target_bitrate = profile.audio_bitrate or smart_lossy_audio_bitrate(
            stream.channels
        )
        return (
            "aac", target_bitrate, None, [],
            downgrade_prefix
            + f"AAC chất lượng cao (FFmpeg AAC gốc, CBR co giãn theo kênh: {target_bitrate}).",
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
                report.details.append("Probe cần mức phân tích 200M.")

        if not data:
            report.types.add(IssueType.HEADER)
            report.severity = "critical"
            report.details.append("Không thể đọc metadata bằng FFprobe.")
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
                f"Extension .{ext} nhưng container thực tế là {real_format}."
            )

        if not probe.streams:
            report.types.add(IssueType.HEADER)
            report.severity = "critical"
            report.details.append("Không tìm thấy stream.")
            return probe, report

        if not any(
            s.codec_type == "video" and not s.is_attached_pic
            for s in probe.streams
        ):
            report.types.add(IssueType.HEADER)
            report.details.append("Không tìm thấy video chính.")

        if probe.duration <= 0:
            report.types.add(IssueType.TRUNCATED)
            report.details.append("Duration bằng 0 hoặc header bất thường.")

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
                    "FFprobe phát hiện dấu hiệu packet/decode bất thường."
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
                return True, "Data stream không cần thiết."
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

        # [GPU] Ưu tiên NVENC khi user bật và GPU khả dụng.
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
                why = f"{target_container} không hỗ trợ {codec_name}"
            else:
                why = f"FFmpeg hiện tại thiếu encoder {encoder}"
            for fb_encoder in VIDEO_ENCODER_FALLBACK_ORDER:
                fb_codec_name = ENCODER_TO_CODEC_NAME.get(fb_encoder, "")
                if (allowed is None or fb_codec_name in allowed) and self.has_encoder(fb_encoder):
                    return fb_encoder, (
                        f"{why} → dùng {fb_codec_name} thay cho "
                        f"{requested} bạn đã chọn."
                    )
            default_encoder = compat.get("video_default", "libx264")
            return default_encoder, (
                f"{why} → dùng {default_encoder} thay cho {requested} bạn đã chọn."
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
            # NVENC: dùng -rc vbr + -cq (constant quality), -b:v 0 = quality mode.
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
                    # F13: attached_pic bị ép convert → DROP.
                    # ffprobe báo codec_type="video" cho cover art, nên
                    # nếu không check is_attached_pic trước, code sẽ rơi
                    # vào nhánh video convert bên dưới và tạo track
                    # "video" giả không có disposition attached_pic.
                    # Cover art là phụ — hỏng thì drop, không đáng convert.
                    if stream.is_attached_pic:
                        actions.append(StreamAction(
                            stream.index, "attachment", "drop",
                            "Cover art không còn giữ được (fallback).",
                        ))
                        continue

                    if stream.codec_type == "video":
                        v_encoder, v_note = self.target_video_encoder(profile, target)
                        actions.append(StreamAction(
                            stream.index, "video", "convert",
                            "Fallback: video CONVERT" + (f" — {v_note}" if v_note else ""),
                            target_codec=v_encoder,
                        ))
                    elif stream.codec_type == "audio":
                        codec, bitrate, vbr_q, extra_idx, reason = (
                            self.plan_audio_target(stream, target, profile)
                        )
                        actions.append(StreamAction(
                            stream.index, "audio", "convert",
                            f"Fallback: audio CONVERT — {reason}",
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
                        "Cover art giữ nguyên.",
                    ))
                continue

            if stream.codec_type == "video":
                if profile.video_mode == "reencode":
                    v_encoder, v_note = self.target_video_encoder(profile, target)
                    actions.append(StreamAction(
                        stream.index, "video", "convert",
                        "User chọn Force Re-encode" + (f" — {v_note}" if v_note else ""),
                        target_codec=v_encoder,
                    ))
                    continue

                if profile.video_mode == "copy":
                    actions.append(StreamAction(
                        stream.index, "video", "copy",
                        "User chọn Force Copy",
                    ))
                    continue

                allowed = compat["video_allowed"]
                compatible = (allowed is None or stream.codec_name in allowed)
                if compatible:
                    actions.append(StreamAction(
                        stream.index, "video", "copy",
                        "Video codec tương thích.",
                    ))
                else:
                    v_encoder, v_note = self.target_video_encoder(profile, target)
                    reason = f"Codec {stream.codec_name} không tương thích {target}."
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
                        f"User chọn Force Re-encode — {reason}",
                        target_codec=codec,
                        target_bitrate=bitrate,
                        audio_vbr_quality=vbr_q,
                        audio_extra_indexed=extra_idx,
                    ))
                    continue

                if profile.audio_mode == "copy":
                    actions.append(StreamAction(
                        stream.index, "audio", "copy",
                        "User chọn Force Copy",
                    ))
                    continue

                allowed = compat["audio_allowed"]
                compatible = (allowed is None or stream.codec_name in allowed)
                if compatible:
                    actions.append(StreamAction(
                        stream.index, "audio", "copy",
                        "Audio codec tương thích.",
                    ))
                else:
                    codec, bitrate, vbr_q, extra_idx, reason = (
                        self.plan_audio_target(stream, target, profile)
                    )
                    actions.append(StreamAction(
                        stream.index, "audio", "convert",
                        f"Codec {stream.codec_name} không tương thích {target}. {reason}",
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
                        f"{target} không hỗ trợ subtitle.",
                    ))
                    continue

                if stream.codec_name in BITMAP_SUB_CODECS:
                    if target == "mkv":
                        actions.append(StreamAction(
                            stream.index, "subtitle", "copy",
                            "Bitmap subtitle giữ nguyên trong MKV.",
                        ))
                    else:
                        actions.append(StreamAction(
                            stream.index, "subtitle", "drop",
                            f"Bitmap subtitle {stream.codec_name} không phù hợp {target}.",
                        ))
                    continue

                if allowed is None or stream.codec_name in allowed:
                    actions.append(StreamAction(
                        stream.index, "subtitle", "copy",
                        "Subtitle codec tương thích.",
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
                            "Không có subtitle encoder phù hợp.",
                        ))
                    continue

                actions.append(StreamAction(
                    stream.index, "subtitle", "drop",
                    "Subtitle codec không tương thích.",
                ))
                continue

            if stream.codec_type == "data":
                if profile.keep_data_streams and target in DATA_STREAM_CONTAINERS:
                    actions.append(StreamAction(
                        stream.index, "data", "copy",
                        f"Data stream giữ nguyên trong {target}.",
                    ))
                else:
                    reason = (
                        "Data stream không cần thiết."
                        if not profile.keep_data_streams
                        else f"{target} không hỗ trợ data stream."
                    )
                    actions.append(StreamAction(
                        stream.index, "data", "drop", reason,
                    ))
                continue

            actions.append(StreamAction(
                stream.index, stream.codec_type, "drop",
                f"Stream type '{stream.codec_type}' không được hỗ trợ.",
            ))

        active_video = [
            a for a in actions
            if a.codec_type == "video" and a.action != "drop"
        ]
        if not active_video and primary_video:
            v_encoder, v_note = self.target_video_encoder(profile, target)
            actions.append(StreamAction(
                primary_video.index, "video", "convert",
                "Bảo vệ video chính." + (f" {v_note}" if v_note else ""),
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
            return -1, f"Không thể chạy FFmpeg: {exc}"

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
            return False, "Output không tồn tại.", None

        try:
            size = output.stat().st_size
        except Exception:
            size = 0

        if size <= 0:
            return False, "Output dung lượng bằng 0.", None

        probe, report = self.lenient_probe(output)
        if not probe:
            return False, "Không probe được output.", None

        has_video = any(
            s.codec_type == "video" and not s.is_attached_pic
            for s in probe.streams
        )
        if not has_video:
            return False, "Output không có video chính.", probe

        source_audio = [
            s for s in source_probe.streams if s.codec_type == "audio"
        ]
        output_audio = [
            s for s in probe.streams if s.codec_type == "audio"
        ]
        if source_audio and not output_audio:
            return False, "Output thiếu audio (source có audio).", probe

        warnings: List[str] = []
        if source_probe.duration > 0 and probe.duration > 0:
            ratio = probe.duration / source_probe.duration
            if ratio < 0.90:
                return (
                    False,
                    f"Output quá ngắn: {ratio * 100:.1f}% so với nguồn "
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
                            f"Plan yêu cầu {action.codec_type}"
                            f"[{action_ordinal}] ({action.action}"
                            + (
                                f" → {action.target_codec}"
                                if action.target_codec else ""
                            )
                            + f") nhưng output không có stream tương ứng "
                            f"(output có {len(actual_streams)} "
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
                        f"{actual_codec}≠{expected_codec}"
                    )

        if report and IssueType.CORRUPT_PACKETS in report.types:
            warnings.append("có packet corrupt trong output")

        if warnings:
            return (
                True,
                f"Output verified (cảnh báo: {', '.join(warnings)}).",
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

        # [P3] Set icon cửa sổ từ icon.ico (cạnh EXE hoặc trong bundle).
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

        # Lưu reference tới (canvas, label%) để cập nhật tiến trình tại chỗ,
        # tránh re-render toàn bộ danh sách gây giật hình.
        self._progress_widgets: Dict[str, Tuple[tk.Canvas, tk.Label]] = {}

        self._scan_cancel_event = threading.Event()
        self._scan_in_progress = False

        # Chỉ hiện popup tổng kết khi batch có ít nhất 1 task được xử lý.
        self._batch_task_count = 0

        self._setup_styles()
        self._build_layout()
        self._setup_drag_drop()

        # [P4] Dark title bar — gọi sau khi layout xong.
        # Gọi 2 lần: ngay bây giờ + sau 20ms để chắc chắn HWND đã sẵn sàng
        # (một số build Windows cần đợi cửa sổ hiện ra mới ăn attribute).
        self._enable_dark_titlebar()
        self.after(20, self._enable_dark_titlebar)

        self.root_after_drain = self.after(80, self._drain_ui_queue)

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._cleanup_stale_temp_files()

        self._log("Ready. FFmpeg / FFprobe sẽ được kiểm tra khi bắt đầu.")
        if HAS_DND and getattr(self, "TkdndVersion", None):
            self._log("💡 Kéo & thả file video hoặc thư mục vào cửa sổ để thêm nhanh.")
        else:
            self._log(
                "ℹ Cài `tkinterdnd2` để bật kéo & thả: pip install tkinterdnd2"
            )

    # -------------------------------------------------------------------------
    # [P3] Window icon
    # -------------------------------------------------------------------------

    def _set_window_icon(self):
        """Nạp icon.ico cho cửa sổ Tkinter.

        Tìm theo thứ tự: cạnh EXE → bundle _internal/_MEIPASS.
        Chỉ áp dụng cho Windows/Linux (iconbitmap hỗ trợ .ico).
        """
        try:
            icon_path = find_resource("icon.ico")
            if not icon_path:
                return
            # Ưu tiên default= để mọi Toplevel cũng có icon.
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
        """Bật dark mode cho thanh tiêu đề Windows.

        Chỉ có tác dụng trên Windows 10 build 17763+ / Windows 11.
        Trên OS khác hoặc Windows cũ hơn, hàm tự bỏ qua im lặng.
        """
        if os.name != "nt":
            return
        try:
            import ctypes

            # Đảm bảo native window đã tồn tại trước khi lấy HWND.
            try:
                self.update_idletasks()
            except Exception:
                pass

            # Tk toplevel: winfo_id() trả HWND của widget, parent mới là
            # HWND top-level thật sự mà DWM cần.
            try:
                hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            except Exception:
                hwnd = 0
            if not hwnd:
                hwnd = self.winfo_id()

            value = ctypes.c_int(1)

            # Attribute ID:
            #   20 → Windows 11 / Windows 10 build 19041+
            #   19 → Windows 10 build 17763 – 19041 (fallback)
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

            # (Tuỳ chọn) ép màu caption khớp bg app — Windows 11 22000+
            try:
                # COLORREF = 0x00BBGGRR (đảo ngược RGB)
                r, g, b = 0x0d, 0x11, 0x17
                colorref = (b << 16) | (g << 8) | r
                c_color = ctypes.c_int(colorref)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, 35,  # DWMWA_CAPTION_COLOR
                    ctypes.byref(c_color),
                    ctypes.sizeof(c_color),
                )
                # Text trên caption
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
                "Thoát",
                "Đang xử lý. Dừng và thoát?",
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
            header, text="🎬 Video Converter Pro",
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

        # [U1] Lọc codec theo container + đồng bộ khi user đổi container.
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
            row1, text="Giữ metadata",
            variable=self.keep_metadata_var,
        )
        self._chk_metadata.pack(side="left", padx=8)

        self._chk_chapters = ttk.Checkbutton(
            row1, text="Giữ chapters",
            variable=self.keep_chapters_var,
        )
        self._chk_chapters.pack(side="left", padx=8)

        self._chk_attachments = ttk.Checkbutton(
            row1, text="Giữ cover/attachments",
            variable=self.keep_attachments_var,
        )
        self._chk_attachments.pack(side="left", padx=8)

        self._chk_data = ttk.Checkbutton(
            row1, text="Giữ data stream (MKV/TS)",
            variable=self.keep_data_var,
        )
        self._chk_data.pack(side="left", padx=8)

        self._chk_rate_cap = ttk.Checkbutton(
            row2, text="Bật trần bitrate (maxrate/bufsize, khuyên dùng)",
            variable=self.rate_cap_var,
        )
        self._chk_rate_cap.pack(side="left", padx=8)

        self._chk_reprocess = ttk.Checkbutton(
            row2, text="Xử lý lại file đã Completed",
            variable=self.reprocess_completed_var,
        )
        self._chk_reprocess.pack(side="left", padx=8)

        self._chk_adaptive_crf = ttk.Checkbutton(
            row2, text="Adaptive CRF theo nguồn (khuyên dùng)",
            variable=self.adaptive_crf_var,
        )
        self._chk_adaptive_crf.pack(side="left", padx=8)

        self._chk_use_gpu = ttk.Checkbutton(
            row2, text="Dùng GPU NVIDIA (NVENC)",
            variable=self.use_gpu_var,
        )
        self._chk_use_gpu.pack(side="left", padx=8)

        action_bar = ttk.Frame(self, padding=8)
        action_bar.pack(fill="x", padx=12)

        self.btn_add = ttk.Button(
            action_bar, text="➕ Thêm File", command=self.add_files,
        )
        self.btn_add.pack(side="left", padx=4)

        self.btn_add_folder = ttk.Button(
            action_bar, text="📁 Thêm Thư Mục", command=self.add_folder,
        )
        self.btn_add_folder.pack(side="left", padx=4)

        self.btn_enable_all = ttk.Button(
            action_bar, text="✓ Bật hết",
            command=lambda: self._set_all_enabled(True),
        )
        self.btn_enable_all.pack(side="left", padx=2)

        self.btn_disable_all = ttk.Button(
            action_bar, text="☐ Tắt hết",
            command=lambda: self._set_all_enabled(False),
        )
        self.btn_disable_all.pack(side="left", padx=2)

        self.btn_clear_completed = ttk.Button(
            action_bar, text="🗑 Xoá đã xử lý", command=self.clear_completed,
        )
        self.btn_clear_completed.pack(side="left", padx=2)

        self.btn_clear_all = ttk.Button(
            action_bar,
            text="✖ Xoá hết", command=self.clear_all,
        )
        self.btn_clear_all.pack(side="left", padx=2)

        self.btn_start = tk.Button(
            action_bar,
            text="▶  BẮT ĐẦU CONVERT",
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
            text="■  HUỶ",
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
            list_header, text="📋 DANH SÁCH FILE",
            style="Surface.TLabel", font=("Segoe UI", 10, "bold"),
        ).pack(side="left")

        self.lbl_list_counter = ttk.Label(
            list_header, text="Chưa có file", style="Muted.TLabel",
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
            output_bar, text="📂 Thư mục xuất:", style="Surface.TLabel",
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
            output_bar, text="📂 Mở", command=self.open_output_dir,
        )
        self.btn_open_output.pack(side="right", padx=4)

        self.btn_choose_output = ttk.Button(
            output_bar, text="Chọn Thư Mục...",
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
        """User vừa đổi container → cập nhật lại danh sách codec hợp lệ."""
        self._refresh_codec_options(initial=False)

    def _refresh_codec_options(self, initial: bool = False):
        """Đồng bộ dropdown Video Codec theo Container đang chọn.

        CHỈ can thiệp UI: giá trị truyền vào engine vẫn qua get_profile_from_ui
        với đúng label user thấy. Nếu codec đang chọn không hợp lệ cho container
        mới, tự reset về option đầu tiên và ghi log cảnh báo.
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
                # Giữ nguyên lựa chọn cũ nếu vẫn hợp lệ.
                codec_cb.set(current)
            else:
                codec_cb.set(allowed_codecs[0])
                if not initial:
                    self._log(
                        f"ℹ Container {container_label} không hỗ trợ "
                        f"codec '{current}' → tự chuyển sang "
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
                        f"🧹 Đã xoá {removed} file tạm từ session trước."
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
            self._log("⚠ Đang convert — bỏ qua thao tác kéo & thả.")
            return

        try:
            raw_paths = self.tk.splitlist(event.data)
        except Exception as exc:
            self._log(f"✗ Không đọc được dữ liệu kéo & thả: {exc}")
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
            self._log(f"✓ Đã thêm {added} file (tổng: {len(self.tasks)}).")
            self._ui(self.render_file_list)

        if rejected:
            preview = ", ".join(rejected[:5])
            suffix = "" if len(rejected) <= 5 else f" (+{len(rejected) - 5})"
            self._log(f"⚠ Bỏ qua {len(rejected)} file không phải video: {preview}{suffix}")

        if folders_to_scan:
            self._start_folder_scan(folders_to_scan, source_label="Kéo & thả")

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
        """Cho phép người dùng gõ tay đường dẫn thư mục xuất.

        [F14] Chuẩn hoá path tương đối thành absolute để tránh ghi nhầm
        vào CWD khi user gõ path kiểu `output` hoặc `./out`.
        """
        raw = self.outdir_var.get().strip()
        if not raw:
            self.outdir_var.set(str(self.output_dir))
            return
        try:
            new_path = Path(raw).expanduser()
            # Chuẩn hoá thành absolute nếu user gõ path tương đối.
            if not new_path.is_absolute():
                new_path = new_path.resolve()
        except Exception:
            self.outdir_var.set(str(self.output_dir))
            return
        self.output_dir = new_path
        self.outdir_var.set(str(self.output_dir))

    def open_output_dir(self):
        """Mở thư mục xuất bằng trình quản lý file của hệ điều hành."""
        path = self.output_dir
        try:
            if not path.exists():
                messagebox.showwarning(
                    "Thông báo",
                    f"Thư mục chưa tồn tại:\n{path}",
                )
                return
            if os.name == "nt":
                os.startfile(str(path))  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(path)])
            else:
                subprocess.Popen(["xdg-open", str(path)])
        except Exception as exc:
            self._log(f"✗ Không mở được thư mục: {exc}")

    # -------------------------------------------------------------------------
    # [P5] Command line input ("Open with...", kéo vào exe)
    # -------------------------------------------------------------------------

    def load_cli_args(self, args: List[str]):
        """Nạp file/thư mục được truyền từ command line.

        Kích hoạt khi:
          - Right-click file video → Open with → VideoConvertPro.exe
          - Kéo file/thư mục thả thẳng vào file .exe (Windows)
          - Chạy dòng lệnh: VideoConvertPro.exe file1.mp4 folder1

        CHỈ thêm task vào danh sách, không đụng logic convert.
        """
        if not args:
            return

        files_to_add: List[Path] = []
        folders_to_scan: List[Path] = []
        rejected: List[str] = []

        for raw in args:
            if not raw:
                continue
            # Bỏ qua flags kiểu --foo (dành cho tương lai)
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
            self._log(f"✓ Nhận {added} file từ command line.")
            self.render_file_list()

        if rejected:
            preview = ", ".join(rejected[:5])
            suffix = "" if len(rejected) <= 5 else f" (+{len(rejected) - 5})"
            self._log(
                f"⚠ Bỏ qua {len(rejected)} file không phải video: "
                f"{preview}{suffix}"
            )

        if folders_to_scan:
            self._start_folder_scan(
                folders_to_scan, source_label="Command line",
            )

    def _update_task_progress(self, task_id: str, progress: float):
        """Chỉ vẽ lại thanh tiến trình của 1 task — không rebuild cả list."""
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
    # [U2] Context menu (chuột phải)
    # -------------------------------------------------------------------------

    def _show_context_menu(self, event, task: VideoConversionTask):
        """Hiển thị menu chuột phải cho 1 task trong danh sách."""
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

        toggle_label = "☑ Bật file này" if task.enabled else "☐ Bật file này"
        menu.add_command(
            label=toggle_label,
            command=lambda tid=task.task_id: self._toggle_task(tid),
        )

        menu.add_separator()

        menu.add_command(
            label="📂 Mở file nguồn",
            command=lambda t=task: self._open_source_file(t),
        )
        menu.add_command(
            label="📁 Mở thư mục chứa",
            command=lambda t=task: self._open_containing_folder(t),
        )

        menu.add_separator()

        menu.add_command(
            label="🗑 Xoá khỏi danh sách",
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
        """Mở file nguồn bằng trình phát mặc định của OS."""
        path = task.source_path
        try:
            if not path.exists():
                self._log(f"✗ File không tồn tại: {path}")
                return
            if os.name == "nt":
                os.startfile(str(path))  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(path)])
            else:
                subprocess.Popen(["xdg-open", str(path)])
        except Exception as exc:
            self._log(f"✗ Không mở được file: {exc}")

    def _open_containing_folder(self, task: VideoConversionTask):
        """Mở thư mục chứa file nguồn bằng trình quản lý file của OS."""
        folder = task.source_path.parent
        try:
            if not folder.exists():
                self._log(f"✗ Thư mục không tồn tại: {folder}")
                return
            if os.name == "nt":
                os.startfile(str(folder))  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(folder)])
            else:
                subprocess.Popen(["xdg-open", str(folder)])
        except Exception as exc:
            self._log(f"✗ Không mở được thư mục: {exc}")

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
            self._log("⚠ Đang quét thư mục khác — bỏ qua.")
            return

        self._scan_in_progress = True
        self._scan_cancel_event.clear()

        if len(roots) == 1:
            self._log(f"📁 Đang quét: {roots[0]}")
        else:
            self._log(f"📁 Đang quét {len(roots)} thư mục...")

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
                            f"⚠ Không quét được {r}: {e}"
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
                    f"✓ Quét xong{label}: thêm {added} file "
                    f"(tổng: {len(self.tasks)})."
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
            self._log(f"✓ Đã thêm {added} file (tổng: {len(self.tasks)}).")
            self._ui(self.render_file_list)

    def add_folder(self):
        if self.is_processing:
            return
        directory = filedialog.askdirectory()
        if not directory:
            return
        self._start_folder_scan([Path(directory)], source_label="Thêm thư mục")

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
            self._log(f"🗑 Đã xoá {removed} file đã xử lý.")
        self.render_file_list()

    def clear_all(self):
        if self.is_processing:
            return
        if not self.tasks:
            return
        if not messagebox.askokcancel(
            "Xoá hết",
            f"Xoá toàn bộ {len(self.tasks)} file khỏi danh sách?",
        ):
            return
        self.tasks.clear()
        self.render_file_list()
        self._log("🗑 Đã xoá toàn bộ danh sách.")

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
                text="Chưa có file", foreground=self.colors["muted"],
            )
            self._render_empty_state()
            return

        self.lbl_list_counter.configure(
            text=f"☑ {enabled}/{total} file được bật",
            foreground=self.colors["accent"] if enabled > 0 else self.colors["muted"],
        )

        for task in self.tasks:
            self._render_task_card(task)

    def _render_empty_state(self):
        empty = tk.Frame(self.file_list_frame, bg=self.colors["bg"])
        empty.pack(fill="both", expand=True, pady=60)

        tk.Label(
            empty, text="📭", bg=self.colors["bg"],
            fg=self.colors["muted"], font=("Segoe UI Emoji", 40),
        ).pack()

        tk.Label(
            empty, text="Chưa có file nào trong danh sách",
            bg=self.colors["bg"], fg=self.colors["text"],
            font=("Segoe UI", 12, "bold"),
        ).pack(pady=(10, 4))

        hint = (
            "Kéo & thả file video hoặc thư mục vào đây\n"
            "hoặc bấm 'Thêm File' / 'Thêm Thư Mục'"
            if HAS_DND and getattr(self, "TkdndVersion", None)
            else "Bấm 'Thêm File' / 'Thêm Thư Mục' để bắt đầu"
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
            toggle_char = "☑"
            toggle_fg = self.colors["success"]
        else:
            toggle_char = "☐"
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
            row1, text="✕",
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
            row1, text=f"● {task.status}", bg=card_bg,
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
                parts.append(f"⚡ {plan.copy_count} copy")
            if plan.convert_count:
                parts.append(f"🔄 {plan.convert_count} convert")
            if plan.drop_count:
                parts.append(f"🧹 {plan.drop_count} drop")

            tk.Label(
                row4, text=" · ".join(parts) if parts else "—",
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

        # [U2] Bind chuột phải cho toàn bộ card + widget con.
        self._bind_context_menu_recursive(card, task)

    def _bind_context_menu_recursive(self, widget, task: VideoConversionTask):
        """Gắn sự kiện chuột phải cho widget và toàn bộ widget con."""
        try:
            widget.bind(
                "<Button-3>",
                lambda e, t=task: self._show_context_menu(e, t),
            )
            # macOS dùng Button-2 cho right-click / control-click.
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

        # [F14] Đồng bộ Entry → self.output_dir TRƯỚC khi spawn worker.
        # FocusOut/Return có thể chưa kịp bắn khi user gõ tay đường dẫn
        # rồi bấm thẳng nút Start (nhất là khi nút có takefocus=0).
        self._on_outdir_changed()

        enabled_tasks = [t for t in self.tasks if t.enabled]
        if not enabled_tasks:
            messagebox.showinfo(
                "Thông báo",
                "Không có file nào được bật để convert.\n\n"
                "Hãy tick chọn file bạn muốn xử lý.",
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

        # [N1] Ghi nhớ số task của batch để popup tổng kết chỉ hiện
        # khi thực sự có task được xử lý.
        self._batch_task_count = len(enabled_tasks)

        self._set_ui_locked(True)

        self.btn_start.config(state="disabled")
        self.btn_cancel.config(state="normal")
        self.global_progress.configure(value=0)

        self.render_file_list()

        # Log để dễ debug — xác nhận đúng thư mục đang dùng.
        self._log(f"📂 Thư mục xuất: {self.output_dir}")

        worker = threading.Thread(
            target=self._process_worker,
            args=(profile, enabled_tasks),
            daemon=True,
        )
        worker.start()

    def cancel_processing(self):
        if self.is_processing:
            self.cancel_event.set()
            self._log("⚠ Đã gửi yêu cầu huỷ.")
        if self._scan_in_progress:
            self._scan_cancel_event.set()
            self._log("⚠ Đã gửi yêu cầu huỷ quét thư mục.")

    # -------------------------------------------------------------------------
    # Worker — điều phối batch
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
                self._log(f"✗ Không thể tạo output folder: {exc}")
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
                        f"[{idx}/{total}] Bỏ qua (đã Completed): "
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
                        f"✗ Worker exception task "
                        f"{task.source_path.name}: {exc}"
                    )
                    self._ui(self.render_file_list)

                progress = idx / max(total, 1) * 100
                self._ui(
                    lambda v=progress: self.global_progress.configure(value=v)
                )
                self._ui(self.render_file_list)
        except Exception as exc:
            self._log(f"✗ Worker fatal error: {exc}")
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

        self._log(f"[{idx}/{total}] Bắt đầu: {task.source_path.name}")

        success = self._process_one_task(task, profile)

        if success:
            task.status = "Completed"
            self._log(f"✓ Hoàn tất: {task.source_path.name}")
        else:
            if self.cancel_event.is_set():
                task.status = "Cancelled"
            else:
                task.status = "Failed"
            self._log(
                f"✗ {task.status}: {task.source_path.name} "
                f"- {task.error_message}"
            )

    def _processing_finished(self):
        self.is_processing = False
        self._ui(lambda: self._set_ui_locked(False))
        self._ui(lambda: self.btn_start.config(state="normal"))
        self._ui(lambda: self.btn_cancel.config(state="disabled"))
        self._ui(self.render_file_list)
        self._log("🏁 Hàng đợi đã kết thúc.")
        # [N1] Popup tổng kết khi batch xử lý xong.
        self._ui(self._show_completion_popup)

    # -------------------------------------------------------------------------
    # [N1] Popup tổng kết khi xử lý xong
    # -------------------------------------------------------------------------

    def _show_completion_popup(self):
        """Popup tổng kết batch khi worker kết thúc.

        Chỉ hiện khi batch có task thực sự được xử lý (không hiện khi
        start_processing bị chặn sớm do không có file / thiếu FFmpeg).
        """
        if self._batch_task_count <= 0:
            return

        total = len(self.tasks)
        if total == 0:
            return

        completed = sum(1 for t in self.tasks if t.status == "Completed")
        failed = sum(1 for t in self.tasks if t.status == "Failed")
        cancelled = sum(1 for t in self.tasks if t.status == "Cancelled")
        # Các task còn status Pending/Processing/Probing coi như chưa xử lý
        # (thường xảy ra khi user huỷ giữa batch).
        pending = total - completed - failed - cancelled

        lines: List[str] = []
        lines.append(f"Tổng số file trong danh sách: {total}")
        lines.append(f"✅ Thành công: {completed}")
        if failed:
            lines.append(f"❌ Thất bại: {failed}")
        if cancelled:
            lines.append(f"🚫 Đã huỷ: {cancelled}")
        if pending:
            lines.append(f"⏸ Chưa xử lý: {pending}")
        lines.append("")
        lines.append(f"📂 Thư mục xuất:\n{self.output_dir}")

        body = "\n".join(lines)

        try:
            if failed == 0 and cancelled == 0 and pending == 0 and completed > 0:
                messagebox.showinfo("✅ Hoàn tất", body)
            elif completed > 0 or failed > 0 or cancelled > 0:
                messagebox.showwarning("⚠ Xử lý xong", body)
            # Nếu không có gì xử lý xong thì im lặng.
        except Exception:
            pass

        # Reset counter sau khi đã hiển thị popup.
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
            return "🔥 EMERGENCY"
        if plan.is_pure_remux:
            return "⚡ PURE REMUX"
        if plan.convert_count > 0 and plan.drop_count > 0:
            return "🧹 SMART"
        if plan.convert_count > 0:
            return "🔄 SMART"
        return "🧹 FILTERED"

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
                    f"  → Không rõ stream lỗi; "
                    f"video chính #{primary.index} → CONVERT."
                )
        elif attempt == 4:
            for s in probe.streams:
                if s.codec_type == "audio" and overrides.get(s.index) != "convert":
                    overrides[s.index] = "convert"
                    self._log(f"  → Audio #{s.index} nâng lên CONVERT.")
                    break
        elif attempt == 5:
            changed = False
            for s in probe.streams:
                if s.codec_type == "audio" and overrides.get(s.index) != "convert":
                    overrides[s.index] = "convert"
                    changed = True
            if changed:
                self._log("  → Ép toàn bộ audio CONVERT.")
        elif attempt == 6:
            changed = False
            for s in probe.streams:
                if s.codec_type == "subtitle":
                    overrides[s.index] = "drop"
                    changed = True
            if changed:
                self._log("  → Loại subtitle để tăng khả năng hoàn tất.")

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
                f"  → Muxer từ chối (không rõ stream cụ thể): "
                f"#{action.stream_index} {action.codec_type}/{codec_name} "
                f"COPY → CONVERT"
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
                            f"  ⚠ Force Copy video #{s.index}: "
                            f"codec {s.codec_name} không thuộc allowlist "
                            f"{target} — có thể fail; sẽ tự chuyển convert "
                            f"khi công cụ từ chối."
                        )

        if profile.audio_mode == "copy":
            allowed = compat.get("audio_allowed")
            if allowed is not None:
                for s in probe.streams:
                    if s.codec_type != "audio":
                        continue
                    if s.codec_name not in allowed:
                        self._log(
                            f"  ⚠ Force Copy audio #{s.index}: "
                            f"codec {s.codec_name} không thuộc allowlist "
                            f"{target} — có thể fail; sẽ tự chuyển convert "
                            f"khi công cụ từ chối."
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
                "Probe thất bại. " + " ".join(report.details[-3:])
            )
            return False

        primary = self.engine.choose_primary_video(probe.streams)
        if not primary:
            task.error_message = "File không có video chính."
            return False

        self._log(
            f"  Probe: {probe.format_name or '?'} · "
            f"{format_size(probe.size)} · "
            f"{format_duration(probe.duration)} · "
            f"{len(probe.streams)} streams"
        )

        self._warn_force_copy_mismatch(profile, probe)

        for stream in probe.streams:
            junk, reason = self.engine.stream_is_junk(stream, profile)
            if junk:
                desc = f"#{stream.index} {stream.codec_type}/{stream.codec_name}"
                task.dropped_streams.append(desc)
                self._log(f"  🧹 DROP stream {desc}: {reason}")

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
    # Fallback ladder — 7 attempt
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
            # Chỉ vẽ lại thanh % — KHÔNG re-render cả file list.
            if now - last_render_ts["t"] >= 0.12:
                last_render_ts["t"] = now
                self._ui(
                    lambda tid=task.task_id, pr=p:
                    self._update_task_progress(tid, pr)
                )

        for attempt in range(1, self.MAX_ATTEMPTS + 1):
            if self.cancel_event.is_set():
                task.error_message = "Đã huỷ."
                return False

            self._cleanup_temp(temp_output)

            task.used_attempt = attempt
            tolerance, emergency = self._compute_tolerance_and_emergency(attempt)
            task.used_tier = 3 if emergency else tolerance

            plan = self.engine.build_conversion_plan(probe, profile, overrides)
            task.plan = plan
            task.badge_type = self._compute_badge(plan, emergency)
            task.converted_streams = [
                f"#{a.stream_index} {a.codec_type} → {a.target_codec or '?'} ({a.reason})"
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
                    f"plan không đổi → bỏ qua."
                )
                self._apply_attempt_mutation(attempt, overrides, probe, task)
                continue
            last_plan_sig = plan_sig

            self._log(
                f"  Attempt {attempt}/{self.MAX_ATTEMPTS} "
                f"· tier {task.used_tier} "
                f"· {plan.copy_count} copy / "
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
                self._log("  → Emergency: full re-encode + transcode audio.")
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
                task.error_message = "Đã huỷ."
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
                        last_error = f"Không thể move output: {exc}"
                        break

                    task.progress = 1.0
                    self._log(f"  ✓ {reason} → {final_output.name}")
                    return True

                last_error = f"Verify thất bại: {reason}"
                self._log(f"  ⚠ FFmpeg OK nhưng verify fail: {reason}")
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
                self._log("  ⚠ Phát hiện lỗi timestamp/DTS/PTS.")

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
                                f"  → Stream #{bad_stream} "
                                f"{stream.codec_type}/{stream.codec_name}: "
                                f"copy lỗi decode; thử lại với tolerance "
                                f"cao hơn trước khi convert."
                            )
                            continue

                        overrides[bad_stream] = "convert"
                        desc = f"#{stream.index} {stream.codec_type}/{stream.codec_name}"
                        if desc not in task.converted_streams:
                            task.converted_streams.append(desc)
                        if muxer_refused is not None:
                            self._log(
                                f"  → Stream #{bad_stream} "
                                f"{stream.codec_type}/{stream.codec_name}: "
                                f"muxer/container từ chối copy → CONVERT"
                            )
                        else:
                            self._log(
                                f"  → Stream #{bad_stream} "
                                f"{stream.codec_type}/{stream.codec_name}: "
                                f"copy fail ở tolerance cao nhất → CONVERT"
                            )
                        continue

                    if current == "convert":
                        primary = self.engine.choose_primary_video(probe.streams)
                        if primary and stream.index == primary.index:
                            self._log(
                                f"  → Video chính #{bad_stream} "
                                f"không được DROP; chuyển emergency."
                            )
                            continue

                        if stream.codec_type in {"subtitle", "data", "unknown"}:
                            overrides[bad_stream] = "drop"
                            self._log(
                                f"  → Stream #{bad_stream} CONVERT fail → DROP"
                            )
                            continue

                        if stream.codec_type == "audio":
                            primary_audio = self.engine.choose_primary_audio(
                                probe.streams,
                            )
                            if primary_audio and stream.index == primary_audio.index:
                                self._log(
                                    f"  → Audio chính #{bad_stream} "
                                    f"không được DROP; giữ CONVERT."
                                )
                                continue

                            audio_streams = [
                                s for s in probe.streams
                                if s.codec_type == "audio"
                            ]
                            if len(audio_streams) > 1:
                                overrides[bad_stream] = "drop"
                                self._log(
                                    f"  → Audio phụ #{bad_stream} "
                                    f"CONVERT fail → DROP"
                                )
                                continue
                            self._log(
                                f"  → Audio chính #{bad_stream} giữ, tiếp tục."
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
            last_error or "Xử lý thất bại sau toàn bộ fallback."
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

    # [P5] Nhận file từ "Open with..." / kéo thả vào exe / command line.
    # Dùng after() để đảm bảo UI đã render xong trước khi add task,
    # tránh race với _drain_ui_queue khởi động trong __init__.
    cli_args = sys.argv[1:]
    if cli_args:
        app.after(50, lambda: app.load_cli_args(cli_args))

    app.mainloop()


if __name__ == "__main__":
    main()

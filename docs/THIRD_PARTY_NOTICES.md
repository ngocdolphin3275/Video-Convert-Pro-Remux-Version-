# Third-party notices

The root MIT License applies to the Video Convert Pro application source code in this repository only. It does not replace the licences of separately distributed third-party components.

## FFmpeg and FFprobe

The Video Convert Pro 3.9.5 Windows portable packages include FFmpeg and FFprobe from the BtbN FFmpeg-Builds GPL shared Windows x64 build.

- Exact FFmpeg version: n9.0.2-61-gd59078794d-20261121
- FFmpeg source commit: https://github.com/FFmpeg/FFmpeg/commit/d59078794d80f5256d5def27e10bb5400a13195c
- BtbN build-script commit: https://github.com/BtbN/FFmpeg-Builds/tree/7f2a6b1050d302144de8366afa37a75e46f326aa
- Upstream successful build workflow: https://github.com/FFmpeg-Builds/FFmpeg-Builds/actions/runs/44902425207
- Upstream binary package SHA-256: e20801968256e40cf2edd0d3a0b7f5e7c9394c96691530a86a42f1f35807b49f
- Licence: GNU General Public License version 3 (GPLv3). The complete GPL text is included in each portable package at Licenses/FFmpeg-GPL-3.0.txt.

The upstream BtbN build recipes are included under third_party/FFmpeg-Builds/ and preserve the MIT licence from that repository. The pinned source repository references and build configuration are documented in FFmpeg-SOURCE-INDEX.md and FFmpeg-BUILD-INFO.txt.

FFmpeg and FFprobe are separate operating-system processes launched by Video Convert Pro. The application does not link against FFmpeg libraries. The application's MIT licence does not relicense FFmpeg or its external libraries.

## Python and application runtime

The portable Windows package is built with Python 3.14 and PyInstaller.

- Python: Python Software Foundation License. The full text is included in the portable package.
- PyInstaller: copying terms and bootloader notice are included in the portable package.
- tkinterdnd2: MIT License text is included in the portable package.
- Tcl/Tk: licence terms are included in the portable package.

Each third-party component remains subject to its own licence. Consult the pinned source references and upstream licence files before redistributing modified builds.

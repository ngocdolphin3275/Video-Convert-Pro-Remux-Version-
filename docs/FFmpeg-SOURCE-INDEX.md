# FFmpeg 9.0.2 — Corresponding Source and build provenance

This Video Convert Pro portable release uses the BtbN FFmpeg-Builds GPL shared Windows x64 build. The executable is a separate process called by the application; it is not linked into the Python application.

## Exact binary identity

- FFmpeg version string: n9.0.2-61-gd59078794d-20261121
- FFmpeg upstream source commit: d59078794d80f5256d5def27e10bb5400a13195c (https://github.com/FFmpeg/FFmpeg/commit/d59078794d80f5256d5def27e10bb5400a13195c)
- BtbN build-script repository commit: 7f2a6b1050d302144de8366afa37a75e46f326aa (https://github.com/BtbN/FFmpeg-Builds/tree/7f2a6b1050d302144de8366afa37a75e46f326aa)
- Successful upstream workflow run: Build FFmpeg — 21 November 2026 (https://github.com/FFmpeg-Builds/FFmpeg-Builds/actions/runs/44902425207)
- Build target and variant: win64, gpl-shared, add-in 9.0
- Upstream binary package: ffmpeg-n9.0-latest-win64-gpl-shared-9.0.zip (https://github.com/FFmpeg-Builds/FFmpeg-Builds/releases/download/latest/ffmpeg-n9.0-latest-win64-gpl-shared-9.0.zip)
- Upstream package SHA-256: e20801968256e40cf2edd0d3a0b7f5e7c9394c96691530a86a42f1f35807b49f
- FFmpeg licence: GNU General Public License v3.0; the complete licence text is distributed with each application ZIP at Licenses/FFmpeg-GPL-3.0.txt.

## Build scripts supplied with this project

The exact BtbN build recipe snapshot used by the successful upstream workflow is included in third_party/FFmpeg-Builds/. Its MIT license is preserved in that folder. The snapshot includes the variant configuration, addins/9.0.sh, build/download/generate scripts, dependency recipes, patches and tool utilities.

To reproduce the same build on a suitable Linux/Docker build host, use the included source snapshot at the commit above and the BtbN instructions. The original BtbN project documents ./build.sh win64 gpl-shared 9.0 for this target/variant.

## Pinned upstream source repositories

The BtbN scripts.d recipes record the upstream repositories and source commits used for third-party components. The table below is generated from that exact recipe snapshot. Some entries describe optional components that are not enabled by the selected target/variant; the build scripts determine the dependency graph for win64/gpl-shared/9.0.

| Build recipe | Upstream source repository | Pinned commit or branch |
|---|---|---|
| scripts.d/10-mingw-std-threads.sh | https://github.com/meganz/mingw-std-threads.git | c931bac289dd431f1dd30fc4a5d1a7be36668073 |
| scripts.d/10-mingw.sh | https://git.code.sf.net/p/mingw-w64/mingw-w64.git | 41eb042358a52011b35350392130dcdc94a8ead8 |
| scripts.d/10-xorg-macros.sh | https://gitlab.freedesktop.org/xorg/util/macros.git | ea1e15a4909ac8b03b2c5a08ac3810b385985157 |
| scripts.d/20-libiconv.sh | https://git.savannah.gnu.org/git/libiconv.git | baaba39736e3b498e1597bf0e5e899b1f753fb01 |
| scripts.d/20-libiconv.sh | https://git.savannah.gnu.org/git/gnulib.git | f9e4c24e9bf3f878a11505a8d06bec965f0fca02 |
| scripts.d/20-zlib.sh | https://github.com/madler/zlib.git | 99623ef7097352da7993ba614161fd6a311e046e |
| scripts.d/25-fftw3.sh | https://github.com/FFTW/fftw3.git | a7b679c528330cf6258253d6dcf5ec90552e6c93 |
| scripts.d/25-fribidi.sh | https://github.com/fribidi/fribidi.git | 15393e4937aa95bcf865d92143735746aeb654fa |
| scripts.d/25-gmp.sh | https://github.com/BtbN/gmplib.git | f9095918ead819c0a2340232891b5acac24b8085 |
| scripts.d/25-libogg.sh | https://github.com/xiph/ogg.git | 06a5e0262cdc28aa4ae6797627a783b5010440f0 |
| scripts.d/25-libpng.sh | https://github.com/glennrp/libpng.git | 5408ee7a2e56555cc4b0acc4051ae241fee38cf3 |
| scripts.d/25-libxml2.sh | https://github.com/GNOME/libxml2.git | 21c8223ac091b81d5914c52eb20b1b063e29cb92 |
| scripts.d/25-openssl.sh | https://github.com/openssl/openssl.git | openssl-3.6.5 |
| scripts.d/25-xz.sh | https://github.com/tukaani-project/xz.git | f54febc540607b3bdee0a0e6793355df2a7e9f61 |
| scripts.d/45-brotli.sh | https://github.com/google/brotli.git | 3dce8720b74194027c7b4cf42dee5bd159786df5 |
| scripts.d/45-fonts/25-freetype.sh | https://gitlab.freedesktop.org/freetype/freetype.git | dbb00e529e69a2be629a9ef98498e4f9b188aab1 |
| scripts.d/45-fonts/35-fontconfig.sh | https://gitlab.freedesktop.org/fontconfig/fontconfig.git | bb21be622280981392c0335fc22202fbba46d247 |
| scripts.d/45-fonts/45-harfbuzz.sh | https://github.com/harfbuzz/harfbuzz.git | 8f1a4e0634a35182e5dd04401edcf57acf5eb12e |
| scripts.d/45-fonts/50-freetype.sh | https://gitlab.freedesktop.org/freetype/freetype.git | dbb00e529e69a2be629a9ef98498e4f9b188aab1 |
| scripts.d/45-lcms2.sh | https://github.com/mm2/Little-CMS.git | ed288c301bd85eaabcb9e1ae0f73540c5f129e1e |
| scripts.d/45-libffi.sh | https://github.com/libffi/libffi.git | de7afe7aa9e8ab7ac36429428a7222caae1e7988 |
| scripts.d/45-libsamplerate.sh | https://github.com/libsndfile/libsamplerate.git | 0844c208f683527c08ea8a80acc13b398aa9c8bf |
| scripts.d/45-libudfread.sh | https://code.videolan.org/videolan/libudfread.git | b0bc6957e7e07d5f35391f210596d9eb71cffdd9 |
| scripts.d/45-libunibreak.sh | https://github.com/adah1972/libunibreak.git | ff24f284a567a006c183b3507b6c650d6ec68b94 |
| scripts.d/45-libvorbis.sh | https://github.com/xiph/vorbis.git | 1b75110b5a2754ba1931d82dd83cb822b266a21d |
| scripts.d/45-opencl.sh | https://github.com/KhronosGroup/OpenCL-Headers.git | 82f60316cc142e7b21dc1d8983b26de18858fbd9 |
| scripts.d/45-opencl.sh | https://github.com/KhronosGroup/OpenCL-ICD-Loader.git | d0be526adb156de7f701024acc811182c984d4c5 |
| scripts.d/45-pcre2.sh | https://github.com/PCRE2Project/pcre2.git | 49d26bca00694ae940adde6d8bd056d8bfc168fa |
| scripts.d/45-pixman.sh | https://gitlab.freedesktop.org/pixman/pixman.git | b88b92e512a33a222e08352e87ff90a57d33c7b5 |
| scripts.d/45-pulseaudio.sh | https://gitlab.freedesktop.org/pulseaudio/pulseaudio.git | 819f2c06ccdc105739e1c714de968f2af1d3e205 |
| scripts.d/45-vmaf.sh | https://github.com/Netflix/vmaf.git | cf677baaa039723876fff8c2677164f25102e684 |
| scripts.d/45-x11/10-xcbproto.sh | https://gitlab.freedesktop.org/xorg/proto/xcbproto.git | dea37a7033abfdef3376dc9ad5e8756e9fee959b |
| scripts.d/45-x11/10-xproto.sh | https://gitlab.freedesktop.org/xorg/proto/xorgproto.git | 6d3907b6d5dc4aa7d7ee6ee5d7d8714e7466630b |
| scripts.d/45-x11/10-xtrans.sh | https://gitlab.freedesktop.org/xorg/lib/libxtrans.git | 79f6b0bfe2170496e8c37626043d009f4cd3f1e1 |
| scripts.d/45-x11/20-libxau.sh | https://gitlab.freedesktop.org/xorg/lib/libxau.git | be1daeb909f1d678e7859ac1555e90b4e768d5c4 |
| scripts.d/45-x11/30-libxcb.sh | https://gitlab.freedesktop.org/xorg/lib/libxcb.git | aa7f3256060451ad65a38feeccf792f44181a4e0 |
| scripts.d/45-x11/40-libx11.sh | https://gitlab.freedesktop.org/xorg/lib/libx11.git | bf893321132251b17b5224fa8830787b45aec4f6 |
| scripts.d/45-x11/50-libxext.sh | https://gitlab.freedesktop.org/xorg/lib/libxext.git | 4770cdff013c036ba4f043b2c895d1b0bfeb0973 |
| scripts.d/45-x11/50-libxfixes.sh | https://gitlab.freedesktop.org/xorg/lib/libxfixes.git | 156e1e39c518f0443073e9c27071e4eceb02e3c0 |
| scripts.d/45-x11/50-libxi.sh | https://gitlab.freedesktop.org/xorg/lib/libxi.git | 9584453906a144fb8b4dbe92d9bf79219391f8e1 |
| scripts.d/45-x11/50-libxinerama.sh | https://gitlab.freedesktop.org/xorg/lib/libxinerama.git | 92d8f35d672537721dcd3a071d04306aa065c29b |
| scripts.d/45-x11/50-libxrender.sh | https://gitlab.freedesktop.org/xorg/lib/libxrender.git | 3aff9046bc91b31cc3dd6974876c29bc309a250a |
| scripts.d/45-x11/50-libxscrnsaver.sh | https://gitlab.freedesktop.org/xorg/lib/libxscrnsaver.git | 723953c9a8dba44bcb1866cf06a54be74fbb8089 |
| scripts.d/45-x11/50-libxxf86vm.sh | https://gitlab.freedesktop.org/xorg/lib/libxxf86vm.git | cf0c73fe2d5847eec3fb966487769f460c722cc4 |
| scripts.d/45-x11/60-libglvnd.sh | https://gitlab.freedesktop.org/glvnd/libglvnd.git | 8731041dbd78566bffafb5145aec8b8df8b5260e |
| scripts.d/45-x11/60-libxcursor.sh | https://gitlab.freedesktop.org/xorg/lib/libxcursor.git | 15efad7ccd035f5d1ddc8d437e047569d1775fa7 |
| scripts.d/45-x11/60-libxrandr.sh | https://gitlab.freedesktop.org/xorg/lib/libxrandr.git | cc7082d2af97458dbb6d7e4bbda7b8884030e05f |
| scripts.d/45-x11/60-libxv.sh | https://gitlab.freedesktop.org/xorg/lib/libxv.git | f315ec50fcad9bdbaed46c3e78dc5e7fe209f933 |
| scripts.d/45-xxhash.sh | https://github.com/Cyan4973/xxHash.git | 2ec67caeb18ec15ae60c0853174331089acddfc0 |
| scripts.d/45-zstd.sh | https://github.com/facebook/zstd.git | de6359d7ea2949afa1407ed2fc2423777ebf1e23 |
| scripts.d/47-vulkan/40-vulkan-headers.sh | https://github.com/KhronosGroup/Vulkan-Headers.git | v1.4.368 |
| scripts.d/47-vulkan/45-vulkan-loader.sh | https://github.com/BtbN/Vulkan-Shim-Loader.git | 65b3936528cd92eb4ea3de485d03f858a3850484 |
| scripts.d/47-vulkan/45-vulkan-loader.sh | https://github.com/KhronosGroup/Vulkan-Headers.git | v1.4.368 |
| scripts.d/47-vulkan/50-shaderc.sh | https://github.com/google/shaderc.git | 05814952134d09f8b54ae925afe578fc341cf6c1 |
| scripts.d/47-vulkan/55-spirv-cross.sh | https://github.com/KhronosGroup/SPIRV-Cross.git | 57e4efcc84112abcd426dc5ec248b5339bee04f2 |
| scripts.d/47-vulkan/60-spirv-headers.sh | https://github.com/KhronosGroup/SPIRV-Headers.git | 5c6004e758e0c80185ef2cee93ae5c10fa342a5b |
| scripts.d/50-amf.sh | https://github.com/GPUOpen-LibrariesAndSDKs/AMF.git | 57ee0cfb0e1a08d9041f77435653794c1b012be0 |
| scripts.d/50-aom.sh | https://aomedia.googlesource.com/aom | aac27b8f291ed449fac576bcce0ad0ca189be851 |
| scripts.d/50-avisynth.sh | https://github.com/AviSynth/AviSynthPlus.git | 5da089a5889a69ebacc25139c7718b4ab12f3cfb |
| scripts.d/50-chromaprint.sh | https://github.com/acoustid/chromaprint.git | 3b38c100022bdfb49be7797c4828a476f1621d55 |
| scripts.d/50-dav1d.sh | https://code.videolan.org/videolan/dav1d.git | 6c7bee685677fd997a431302be4fea8ea4017606 |
| scripts.d/50-davs2.sh | https://github.com/pkuvcl/davs2.git | b41cf117452e2d73d827f02d3e30aa20f1c721ac |
| scripts.d/50-dvd/30-libdvdcss.sh | https://code.videolan.org/videolan/libdvdcss.git | 811ce97a1d4d1c9d936f4b2707f533a9ef768251 |
| scripts.d/50-dvd/40-libdvdread.sh | https://code.videolan.org/videolan/libdvdread.git | 0f30df53125b564ef45903714403ce0a1e6c5e9e |
| scripts.d/50-dvd/50-libdvdnav.sh | https://code.videolan.org/videolan/libdvdnav.git | 8147ccd35e5aae4afdd21171cf7b6b4d8f179d28 |
| scripts.d/50-fdk-aac.sh | https://github.com/mstorsjo/fdk-aac.git | ec82feb39662ac77e24ee9b324d5962e91bc79c5 |
| scripts.d/50-ffnvcodec.sh | https://github.com/FFmpeg/nv-codec-headers.git | f2053071ea93137255b6dcf42e9b4c9e0965a44e |
| scripts.d/50-ffnvcodec.sh | https://github.com/FFmpeg/nv-codec-headers.git | ced4f8eba3ba5dd431932cba17928f0dffdaeb2b |
| scripts.d/50-ffnvcodec.sh | https://github.com/FFmpeg/nv-codec-headers.git | 833faee5f7b8d3f56444347c587f4aed11ee213f |
| scripts.d/50-frei0r.sh | https://github.com/dyne/frei0r.git | f09dad3aeb8160244febac49589e47a1513549d4 |
| scripts.d/50-gme.sh | https://github.com/libgme/game-music-emu.git | 8238afd9503a59ffcec0e2685584d5ce819ad7c6 |
| scripts.d/50-kvazaar.sh | https://github.com/ultravideo/kvazaar.git | ec7562da7f5971f9fa3f984db358371e74bf3c7d |
| scripts.d/50-lcevcdec.sh | https://github.com/v-novaltd/LCEVCdec.git | e295d8438ba554bc541fb269baa9cbd567b626a8 |
| scripts.d/50-libaribb24.sh | https://github.com/nkoriyama/aribb24.git | 5e9be272f96e00f15a2f3c5f8ba7e124862aec38 |
| scripts.d/50-libaribcaption.sh | https://github.com/xqq/libaribcaption.git | d59c9d6403645dd7e8098b02b887a6723b15259b |
| scripts.d/50-libass.sh | https://github.com/libass/libass.git | 21b5a54fceff49c126c201d4b51c6445287a5072 |
| scripts.d/50-libbluray.sh | https://code.videolan.org/videolan/libbluray.git | 4613535451af402c6d72665e8cd88be1b29c9158 |
| scripts.d/50-libcurl/40-libpsl.sh | https://github.com/rockdaboot/libpsl.git | 88331dae18f1824ab033f7e77880cf65814fc21a |
| scripts.d/50-libcurl/40-libpsl.sh | https://github.com/publicsuffix/list.git | ee4f2faaca9387a7cf3d433e68484b82c9542543 |
| scripts.d/50-libcurl/40-nghttp2.sh | https://github.com/nghttp2/nghttp2.git | c785bf23f9d77966085ae1b32717f3e8c8d12090 |
| scripts.d/50-libcurl/40-nghttp3.sh | https://github.com/ngtcp2/nghttp3.git | e06a63ac6a0267149b480cd7fe04c8ea9a366d9e |
| scripts.d/50-libcurl/40-ngtcp2.sh | https://github.com/ngtcp2/ngtcp2.git | 9595a0dda7990b95cc2ff728d2524d7db0a8b7f3 |
| scripts.d/50-libcurl/50-libcurl.sh | https://github.com/curl/curl.git | d999cc6c6bb1f73ca60593355e522f97240317ad |
| scripts.d/50-libjxl/50-libjxl.sh | https://github.com/libjxl/libjxl.git | a14f4e0ff32c07cbd19eae144c850e8bbfee2261 |
| scripts.d/50-libmp3lame.sh | https://svn.code.sf.net/p/lame/svn/trunk/lame | See pinned download recipe |
| scripts.d/50-libopus.sh | https://github.com/xiph/opus.git | f1afc4222aff7c5456d27581ec618ae64158fbe1 |
| scripts.d/50-libplacebo.sh | https://code.videolan.org/videolan/libplacebo.git | e608e5b799b6515af2689fddbbed66ffae7b724c |
| scripts.d/50-librist/40-mbedtls.sh | https://github.com/ARMmbed/mbedtls.git | v4.3.0 |
| scripts.d/50-librist/50-librist.sh | https://code.videolan.org/rist/librist.git | a911bee8904d88beb1ccd3349ff9a3de1cadc1a6 |
| scripts.d/50-librsvg/10-glib.sh | https://github.com/GNOME/glib.git | 5cf924587ed152260d85c6ca8733546bcad5ee42 |
| scripts.d/50-librsvg/20-cairo.sh | https://gitlab.freedesktop.org/cairo/cairo.git | 07adef44b00a9765e9bdb92c4e6f3772debc83c2 |
| scripts.d/50-librsvg/30-pango.sh | https://github.com/GNOME/pango.git | 6bd640fdbdfe4d751cc17e0fff25caa6a372d303 |
| scripts.d/50-librsvg/99-librsvg.sh | https://github.com/GNOME/librsvg.git | a6ab2529560de5e17551a9ca3ed9e8a9b9bc9a2e |
| scripts.d/50-libssh.sh | https://gitlab.com/libssh/libssh-mirror.git | 5138d46fd3b844d525b05938bf55a6d0d924c8d2 |
| scripts.d/50-libtheora.sh | https://github.com/xiph/theora.git | 28fd5ec77f0ad0e07a371cef1047828116f6bd8a |
| scripts.d/50-libvpx.sh | https://chromium.googlesource.com/webm/libvpx | 7e000a41a7727d5b9477dbbe5727431560d6a16c |
| scripts.d/50-libwebp.sh | https://chromium.googlesource.com/webm/libwebp | 67b8354c37d21f36d6d5cdd027ca0bcf94d3243d |
| scripts.d/50-libzmq.sh | https://github.com/zeromq/libzmq.git | 46493370217ac135246617fa2f6ac819d8b61bfc |
| scripts.d/50-lilv/96-lv2.sh | https://github.com/lv2/lv2.git | 3c57dae600a5ad8d05acd53ee3490f7d91cb7be6 |
| scripts.d/50-lilv/96-serd.sh | https://github.com/drobilla/serd.git | b621b0bc790d1e8102d3138ead16b974ddda8432 |
| scripts.d/50-lilv/96-zix.sh | https://github.com/drobilla/zix.git | 17d632393f5addb6fa24dda2927b96515407cca7 |
| scripts.d/50-lilv/97-sord.sh | https://github.com/drobilla/sord.git | 4b5232bb91e7f2f1b84df384494d073fabbcd312 |
| scripts.d/50-lilv/98-sratom.sh | https://github.com/lv2/sratom.git | 9e8ee84eed502e6030ce8bb49694fd28542b08fc |
| scripts.d/50-lilv/99-lilv.sh | https://github.com/lv2/lilv.git | 4b8f30055fa5cb4134a2eb45fc1555bc04289314 |
| scripts.d/50-onevpl.sh | https://github.com/intel/libvpl.git | 412c5cffe3022d5ebb8a955c3b30afe7bd2e3929 |
| scripts.d/50-openal.sh | https://github.com/kcat/openal-soft.git | 0609c8df5848040a13d67d790ac65ed95fad265f |
| scripts.d/50-openapv.sh | https://github.com/AcademySoftwareFoundation/openapv.git | 3f0291391dbb1fbc27229b2543aad4ce778b0d72 |
| scripts.d/50-opencore-amr.sh | https://git.code.sf.net/p/opencore-amr/code | 7dba8c32238418ce0b316a852b2224df586ca896 |
| scripts.d/50-openh264.sh | https://github.com/cisco/openh264.git | 1bca62311e447fd9c39fc93de2c4b96cd5ce971c |
| scripts.d/50-openjpeg.sh | https://github.com/uclouvain/openjpeg.git | 8314119b067c0fc77834731168daaebd379fdb12 |
| scripts.d/50-openmpt.sh | https://github.com/OpenMPT/openmpt.git | ad7ba02b3fd1212e65cca02c41476af4368491ce |
| scripts.d/50-rav1e.sh | https://github.com/xiph/rav1e.git | 31435de9d76fddd38f6dcc31d4014574cebb2092 |
| scripts.d/50-rubberband.sh | https://github.com/breakfastquay/rubberband.git | e4296ac80b1170018a110bc326fd0d45a0eb27d6 |
| scripts.d/50-sdl.sh | https://github.com/libsdl-org/SDL.git | fe30456e94e89ef2cab50172121bffb7f7f50830 |
| scripts.d/50-snappy.sh | https://github.com/google/snappy.git | 946606459314e55d029c85f9a8c46f8809467f0f |
| scripts.d/50-soxr.sh | https://git.code.sf.net/p/soxr/code | 945b592b70470e29f917f4de89b4281fbbd540c0 |
| scripts.d/50-srt.sh | https://github.com/Haivision/srt.git | 23af65f7dafb0f65b80312b859f80aeece557924 |
| scripts.d/50-svtav1.sh | https://github.com/AOMediaCodec/SVT-AV1.git | 5fdf6b2f373bd96256bb6b45f892077b1b4431d9 |
| scripts.d/50-twolame.sh | https://github.com/njh/twolame.git | 6fced852d4d5cfad58cf9dbe3ea619b08e87d398 |
| scripts.d/50-uavs3d.sh | https://github.com/uavs3/uavs3d.git | 0e20d2c291853f196c68922a264bcd8471d75b68 |
| scripts.d/50-vaapi/30-libpciaccess.sh | https://gitlab.freedesktop.org/xorg/lib/libpciaccess.git | e33aa5fd28f63b9842e36c1a8a954577eec042e3 |
| scripts.d/50-vaapi/40-libdrm.sh | https://gitlab.freedesktop.org/mesa/drm.git | 33fab8cbca7f7581e955a675597d14412702edc4 |
| scripts.d/50-vaapi/50-libva.sh | https://github.com/intel/libva.git | f052e984e0c8bf10784198cc311b23c567b1367f |
| scripts.d/50-vapoursynth.sh | https://github.com/vapoursynth/vapoursynth.git | R82 |
| scripts.d/50-vidstab.sh | https://github.com/georgmartius/vid.stab.git | e2445c4081658318223762a696eb1c645c2d7168 |
| scripts.d/50-vvenc.sh | https://github.com/fraunhoferhhi/vvenc.git | 7804c92e133983e5d81c88d0ae642201d73ee457 |
| scripts.d/50-whisper.sh | https://github.com/ggml-org/whisper.cpp.git | aba02defd6bb6ff5de63721c21e3456645c153e2 |
| scripts.d/50-x264.sh | https://code.videolan.org/videolan/x264.git | 0480cb05fa188d37ae87e8f4fd8f1aea3711f7ee |
| scripts.d/50-x265.sh | https://github.com/Multicorewareinc/x265.git | 217c4f9b88a06513afb7ea44d55b832d6618f80c |
| scripts.d/50-xavs2.sh | https://github.com/pkuvcl/xavs2.git | eae1e8b9d12468059bdd7dee893508e470fa83d8 |
| scripts.d/50-xvid.sh | https://svn.xvid.org/trunk/xvidcore | See pinned download recipe |
| scripts.d/50-zimg.sh | https://github.com/sekrit-twc/zimg.git | 67e0603271c080e22c8429856dd4a8a56587e61e |
| scripts.d/50-zvbi.sh | https://github.com/zapping-vbi/zvbi | 34bb6f660c5c1bacd4a66cc7b22311e4ca3c1ab5 |

## Licensing and scope

This file and the accompanying BtbN source snapshot provide the build-system provenance and pinned upstream source locations for the bundled FFmpeg distribution. Third-party components retain their individual licences; the FFmpeg GPL v3 text does not replace those licences. The root MIT licence in this repository applies only to Video Convert Pro application source code.

The BtbN source snapshot contains the scripts that identify each component's repository and pinned revision. When reproducing or redistributing the FFmpeg binaries, preserve the corresponding upstream source references, applicable licence texts, and the build instructions required by the GPL and by each component's own licence.

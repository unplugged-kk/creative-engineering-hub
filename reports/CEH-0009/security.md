# CEH-0009 · remotion-dev/remotion

https://github.com/remotion-dev/remotion

**Gate:** review (worst finding: medium)  
Scanned files: 12108

## Findings
- [medium] pipe remote script to shell — .circleci/config.yml:20
- [medium] pipe remote script to shell — .github/workflows/ffmpeg.yml:38
- [medium] privilege escalation — packages/chrome-compile/linux-arm64/Dockerfile:30
- [medium] privilege escalation — packages/chrome-compile/linux-arm64/README.md:74
- [medium] privilege escalation — packages/chrome-compile/linux-x64/Dockerfile:30
- [medium] privilege escalation — packages/chrome-compile/linux-x64/README.md:60
- [medium] privilege escalation — packages/chrome-compile/mac-arm64/build-chromium.sh:47
- [medium] committed binary — packages/compositor-darwin-arm64/libavcodec.dylib
- [medium] committed binary — packages/compositor-darwin-arm64/libavdevice.dylib
- [medium] committed binary — packages/compositor-darwin-arm64/libavfilter.dylib
- [medium] committed binary — packages/compositor-darwin-arm64/libavformat.dylib
- [medium] committed binary — packages/compositor-darwin-arm64/libavutil.dylib
- [medium] committed binary — packages/compositor-darwin-arm64/libswresample.dylib
- [medium] committed binary — packages/compositor-darwin-arm64/libswscale.dylib
- [medium] committed binary — packages/compositor-darwin-x64/libavcodec.dylib
- [medium] committed binary — packages/compositor-darwin-x64/libavdevice.dylib
- [medium] committed binary — packages/compositor-darwin-x64/libavfilter.dylib
- [medium] committed binary — packages/compositor-darwin-x64/libavformat.dylib
- [medium] committed binary — packages/compositor-darwin-x64/libavutil.dylib
- [medium] committed binary — packages/compositor-darwin-x64/libswresample.dylib
- [medium] committed binary — packages/compositor-darwin-x64/libswscale.dylib
- [medium] committed binary — packages/compositor-linux-arm64-gnu/libavcodec.so
- [medium] committed binary — packages/compositor-linux-arm64-gnu/libavdevice.so
- [medium] committed binary — packages/compositor-linux-arm64-gnu/libavfilter.so
- [medium] committed binary — packages/compositor-linux-arm64-gnu/libavformat.so
- [medium] committed binary — packages/compositor-linux-arm64-gnu/libavutil.so
- [medium] committed binary — packages/compositor-linux-arm64-gnu/libswresample.so
- [medium] committed binary — packages/compositor-linux-arm64-gnu/libswscale.so
- [medium] committed binary — packages/compositor-linux-arm64-musl/libavcodec.so
- [medium] committed binary — packages/compositor-linux-arm64-musl/libavdevice.so
- [medium] committed binary — packages/compositor-linux-arm64-musl/libavfilter.so
- [medium] committed binary — packages/compositor-linux-arm64-musl/libavformat.so
- [medium] committed binary — packages/compositor-linux-arm64-musl/libavutil.so
- [medium] committed binary — packages/compositor-linux-arm64-musl/libswresample.so
- [medium] committed binary — packages/compositor-linux-arm64-musl/libswscale.so
- [medium] committed binary — packages/compositor-linux-x64-gnu/libavcodec.so
- [medium] committed binary — packages/compositor-linux-x64-gnu/libavdevice.so
- [medium] committed binary — packages/compositor-linux-x64-gnu/libavfilter.so
- [medium] committed binary — packages/compositor-linux-x64-gnu/libavformat.so
- [medium] committed binary — packages/compositor-linux-x64-gnu/libavutil.so
- [medium] committed binary — packages/compositor-linux-x64-gnu/libswresample.so
- [medium] committed binary — packages/compositor-linux-x64-gnu/libswscale.so
- [medium] committed binary — packages/compositor-linux-x64-musl/libavcodec.so
- [medium] committed binary — packages/compositor-linux-x64-musl/libavdevice.so
- [medium] committed binary — packages/compositor-linux-x64-musl/libavfilter.so
- [medium] committed binary — packages/compositor-linux-x64-musl/libavformat.so
- [medium] committed binary — packages/compositor-linux-x64-musl/libavutil.so
- [medium] committed binary — packages/compositor-linux-x64-musl/libswresample.so
- [medium] committed binary — packages/compositor-linux-x64-musl/libswscale.so
- [medium] committed binary — packages/compositor-win32-x64-msvc/avcodec-61.dll
- [medium] committed binary — packages/compositor-win32-x64-msvc/avdevice-61.dll
- [medium] committed binary — packages/compositor-win32-x64-msvc/avfilter-10.dll
- [medium] committed binary — packages/compositor-win32-x64-msvc/avformat-61.dll
- [medium] committed binary — packages/compositor-win32-x64-msvc/avutil-59.dll
- [medium] committed binary — packages/compositor-win32-x64-msvc/ffmpeg.exe
- [medium] committed binary — packages/compositor-win32-x64-msvc/ffprobe.exe
- [medium] committed binary — packages/compositor-win32-x64-msvc/libgcc_s_seh-1.dll
- [medium] committed binary — packages/compositor-win32-x64-msvc/libssp-0.dll
- [medium] committed binary — packages/compositor-win32-x64-msvc/libstdc++-6.dll
- [medium] committed binary — packages/compositor-win32-x64-msvc/libvpx-1.dll
- [medium] committed binary — packages/compositor-win32-x64-msvc/libwinpthread-1.dll
- [medium] committed binary — packages/compositor-win32-x64-msvc/msvcr100.dll
- [medium] committed binary — packages/compositor-win32-x64-msvc/remotion.exe
- [medium] committed binary — packages/compositor-win32-x64-msvc/swresample-5.dll
- [medium] committed binary — packages/compositor-win32-x64-msvc/swscale-8.dll
- [medium] committed binary — packages/compositor-win32-x64-msvc/zlib1.dll
- [medium] pipe remote script to shell — packages/compositor/ffmpeg/build/Dockerfile:17
- [medium] pipe remote script to shell — packages/compositor/ffmpeg/build/Dockerfile-aws:17
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — packages/docs/docusaurus.config.ts:93
- [medium] secret-shaped string in test, docs or comment (Google API key) — packages/docs/src/components/GoogleMaps.tsx:22
- [medium] pipe remote script to shell — packages/docs/vercel.ts:741
- [medium] pipe remote script to shell — packages/lambda-binaries/build-chrome.sh:409
- [medium] privilege escalation — packages/lambda-binaries/build-chrome.sh:6
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — packages/licensing/src/test/register.test.ts:10
- [medium] privilege escalation — packages/template-stargazer/.github/workflows/render-video.yml:34
- [medium] npm prepare hook runs on install — package.json: git config core.hooksPath .githooks

## Notes
- 29 large or binary files not scanned
- osv.dev checked 0 pinned packages

Static scan only. No resource code was installed or executed.

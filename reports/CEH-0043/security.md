# CEH-0043 · ggml-org/whisper.cpp

https://github.com/ggml-org/whisper.cpp

**Gate:** review (worst finding: medium)  
Scanned files: 345

## Findings
- [medium] privilege escalation — .github/workflows/build-clang.yml:127
- [medium] privilege escalation — .github/workflows/build-cpu.yml:65
- [medium] privilege escalation — .github/workflows/build-freebsd.yml:53
- [medium] privilege escalation — .github/workflows/build-gcc.yml:117
- [medium] privilege escalation — .github/workflows/build-sanitize.yml:61
- [medium] privilege escalation — .github/workflows/build-sycl.yml:68
- [medium] privilege escalation — .github/workflows/docker.yml:44
- [medium] privilege escalation — .github/workflows/examples.yml:26
- [medium] privilege escalation — .github/workflows/release.yml:111
- [medium] privilege escalation — README.md:547
- [medium] privilege escalation — README_sycl.md:63
- [medium] committed binary — bindings/java/gradle/wrapper/gradle-wrapper.jar
- [medium] privilege escalation — examples/command/README.md:42
- [medium] privilege escalation — examples/stream/README.md:65
- [medium] privilege escalation — examples/talk-llama/README.md:20
- [medium] committed binary — examples/whisper.android.java/gradle/wrapper/gradle-wrapper.jar
- [medium] committed binary — examples/whisper.android/gradle/wrapper/gradle-wrapper.jar
- [medium] privilege escalation — examples/whisper.swiftui/README.md:15

## Notes
- osv.dev checked 0 pinned packages

Static scan only. No resource code was installed or executed.

# CEH-0040 · remsky/Kokoro-FastAPI

https://github.com/remsky/Kokoro-FastAPI

**Gate:** review (worst finding: medium)  
Scanned files: 286

## Findings
- [medium] privilege escalation — .github/workflows/ci.yml:37
- [medium] privilege escalation — .github/workflows/release.yml:116
- [medium] privilege escalation — .github/workflows/test_build.yml:91
- [medium] pipe remote script to shell — docker/rocm/Dockerfile:27
- [medium] pipe remote script to shell — docker/test-client/Dockerfile:29

## Notes
- osv.dev checked 4 pinned packages

Static scan only. No resource code was installed or executed.

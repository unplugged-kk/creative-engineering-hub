# CEH-0014 · heygen-com/hyperframes

https://github.com/heygen-com/hyperframes

**Gate:** review (worst finding: medium)  
Scanned files: 7162

## Findings
- [medium] privilege escalation — DOCS_GUIDELINES.md:105
- [medium] privilege escalation — README.md:346
- [medium] secret-shaped string in test, docs or comment (private key) — packages/cli/src/capture/contentExtractor.test.ts:477
- [medium] pipe remote script to shell — packages/gcp-cloud-run/Dockerfile:81
- [medium] pipe remote script to shell — scripts/test-skills-fresh.sh:109
- [medium] npm prepare hook runs on install — package.json: test -d .git && lefthook install || true

## Notes
- 18 large or binary files not scanned
- osv.dev checked 0 pinned packages

Static scan only. No resource code was installed or executed.

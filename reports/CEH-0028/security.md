# CEH-0028 · harry0703/MoneyPrinterTurbo

https://github.com/harry0703/MoneyPrinterTurbo

**Gate:** review (worst finding: medium)  
Scanned files: 246

## Findings
- [medium] pipe remote script to shell — docs/skill/SKILL.md:50
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — test/services/test_mpt_agent_skill.py:514
- [medium] known vulnerability — PyPI:python-multipart@0.0.27 GHSA-5rvq-cxj2-64vf, GHSA-6jv3-5f52-599m, GHSA-v9pg-7xvm-68hf, GHSA-vffw-93wf-4j4q, PYSEC-2026-3036, PYSEC-2026-3037, PYSEC-2026-3040, PYSEC-2026-3041
- [medium] known vulnerability — PyPI:litellm@1.86.2 GHSA-3cv6-jpf6-8222, GHSA-g5ff-637f-6q2m, PYSEC-2026-4066

## Notes
- osv.dev checked 21 pinned packages

Static scan only. No resource code was installed or executed.

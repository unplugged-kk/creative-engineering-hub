# CEH-0026 · morluto/rea

https://github.com/morluto/rea

**Gate:** block (worst finding: high)  
Scanned files: 7731

## Findings
- [medium] privilege escalation — .github/workflows/ci.yml:653
- [medium] privilege escalation — .github/workflows/real-agentenv.yml:68
- [medium] privilege escalation — .github/workflows/real-binary-layout.yml:60
- [medium] privilege escalation — .github/workflows/real-cutter.yml:30
- [medium] privilege escalation — .github/workflows/real-ghidra-windows.yml:32
- [medium] privilege escalation — .github/workflows/real-termux.yml:43
- [medium] privilege escalation — .github/workflows/website-check.yml:30
- [medium] privilege escalation — .github/workflows/website-pages.yml:63
- [medium] pipe remote script to shell — docs/getting-started/installation.md:2043
- [medium] pipe remote script to shell — install.sh:5
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — scripts/fixtures/browser-verifier-site.mjs:232
- [medium] hardcoded credential — scripts/lib/browser-scenario-storage-fingerprints-e2e.mjs:17
- [high] obfuscated execution — scripts/verify-qwen-client.mjs:333
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — src/browser/PlaywrightScenarioSession.test.ts:1755
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — src/cutter/cutterBridgeMac.test.ts:7
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — src/domain/desktop/appTaskChecks.test.ts:19
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — src/frida/FridaInstrumentationManager.test.ts:1430
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — tests/acceptance/browser/browserScenarioLaunchFailure.test.ts:12
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — tests/boundary/cli/cutterCommands.test.ts:136
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — tests/boundary/cli/cutterStatusAttributionCli.test.ts:19
- [medium] pipe remote script to shell — tests/boundary/filesystem/installScript.test.ts:302
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — tests/boundary/mcp/cutterCancellationMcp.test.ts:70
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — tests/boundary/mcp/cutterMcp.test.ts:202
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — tests/boundary/mcp/fridaMcp.test.ts:166
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — tests/boundary/mcp/ghidraFailureDiagnostics.test.ts:33
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — tests/boundary/process/ProcessEvidence.test.ts:120
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — tests/boundary/providers/CutterBridgeCapacity.test.ts:22
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — tests/boundary/providers/CutterBridgeClient.test.ts:109
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — tests/boundary/providers/CutterBridgeNullIdentity.test.ts:13
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — tests/boundary/providers/CutterCommandCancellation.test.ts:100
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — tests/boundary/providers/CutterStatusProof.test.ts:17
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — tests/boundary/providers/cutterBridgeRequestLimit.test.ts:19
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — tests/boundary/providers/ghidra/ghidraLauncher.test.ts:794
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — tests/composition/browserScenarioStartupRedaction.test.ts:17
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — tests/process-global/cutterDescriptorLifetime.test.ts:67
- [medium] pipe remote script to shell — website/public/get-started/index.html:383
- [medium] npm prepare hook runs on install — package.json: node scripts/prepare.mjs
- [medium] known vulnerability — npm:minimatch@10.2.5 GHSA-g3hv-75wg-m249

## Notes
- 1 large or binary files not scanned
- osv.dev checked 966 pinned packages

Static scan only. No resource code was installed or executed.

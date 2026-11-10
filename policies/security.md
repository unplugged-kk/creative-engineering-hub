# Security policy

- Intake is static: no install, no script, no build. Lab clones have no checkout.
- Scanned: secrets (private keys, cloud and API tokens, hardcoded credentials), obfuscated execution, piping remote scripts to a shell,
  `sudo`, committed binaries, npm install hooks, and known vulnerabilities of pinned dependencies (osv.dev).
- Gates: high = block (cannot approve), medium = review (needs `--security-reviewed`), low = pass.
- Running anything (benchmarks, prototypes) happens under `lab/`, with the user's approval, never with real credentials.
- No automatic publishing, spending, deployment or credential use.

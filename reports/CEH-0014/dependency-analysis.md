# CEH-0014 · heygen-com/hyperframes

https://github.com/heygen-com/hyperframes

```json
{
  "manifests": [
    "package.json",
    "packages/aws-lambda/package.json",
    "packages/cli/package.json",
    "packages/core/package.json",
    "packages/engine/package.json",
    "packages/gcp-cloud-run/package.json",
    "packages/lint/package.json",
    "packages/parsers/package.json",
    "packages/player/package.json",
    "packages/producer/package.json",
    "packages/sdk-playground/package.json",
    "packages/sdk/package.json",
    "packages/shader-transitions/package.json",
    "packages/studio-server/package.json",
    "packages/studio/package.json"
  ],
  "npm": {},
  "npm_dev": {
    "@commitlint/cli": "^20.5.0",
    "@commitlint/config-conventional": "^20.5.0",
    "@hyperframes/player": "workspace:*",
    "@types/node": "^25.0.10",
    "concurrently": "^8.2.0",
    "fallow": "^2.75.0",
    "happy-dom": "^20.9.0",
    "knip": "^6.0.3",
    "lefthook": "^2.1.4",
    "oxfmt": "^0.41.0",
    "oxlint": "^1.56.0",
    "tsx": "^4.21.0",
    "typescript": "^5.0.0",
    "vitest": "^4.1.11",
    "yaml": "^2.9.0"
  },
  "install_hooks": {
    "prepare": "test -d .git && lefthook install || true"
  }
}
```

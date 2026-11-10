# CEH-0038 · CopilotKit/CopilotKit

https://github.com/CopilotKit/CopilotKit

**Gate:** review (worst finding: medium)  
Scanned files: 21975

## Findings
- [medium] privilege escalation — .github/workflows/showcase_validate.yml:709
- [medium] pipe remote script to shell — examples/canvas/llamaindex/README.md:56
- [medium] pipe remote script to shell — examples/integrations/adk/Dockerfile:21
- [medium] committed binary — examples/integrations/adk/docker/Dockerfile.app
- [medium] pipe remote script to shell — examples/integrations/agno/Dockerfile:28
- [medium] committed binary — examples/integrations/agno/docker/Dockerfile.app
- [medium] pipe remote script to shell — examples/integrations/antigravity/Dockerfile:27
- [medium] committed binary — examples/integrations/antigravity/docker/Dockerfile.app
- [medium] pipe remote script to shell — examples/integrations/claude-sdk-python/Dockerfile:29
- [medium] committed binary — examples/integrations/claude-sdk-python/docker/Dockerfile.app
- [medium] committed binary — examples/integrations/claude-sdk-typescript/docker/Dockerfile.app
- [medium] pipe remote script to shell — examples/integrations/crewai-crews/Dockerfile:21
- [medium] committed binary — examples/integrations/crewai-crews/docker/Dockerfile.app
- [medium] committed binary — examples/integrations/crewai-flows/docker/Dockerfile.app
- [medium] pipe remote script to shell — examples/integrations/langgraph-fastapi/Dockerfile:31
- [medium] committed binary — examples/integrations/langgraph-fastapi/docker/Dockerfile.app
- [medium] committed binary — examples/integrations/langgraph-js/docker/Dockerfile.app
- [medium] pipe remote script to shell — examples/integrations/langgraph-python/Dockerfile:31
- [medium] committed binary — examples/integrations/langgraph-python/docker/Dockerfile.app
- [medium] pipe remote script to shell — examples/integrations/llamaindex/Dockerfile:28
- [medium] committed binary — examples/integrations/llamaindex/docker/Dockerfile.app
- [medium] committed binary — examples/integrations/mastra/docker/Dockerfile.app
- [medium] pipe remote script to shell — examples/integrations/ms-agent-framework-dotnet/Dockerfile:35
- [medium] pipe remote script to shell — examples/integrations/ms-agent-framework-dotnet/README.md:15
- [medium] committed binary — examples/integrations/ms-agent-framework-dotnet/docker/Dockerfile.app
- [medium] pipe remote script to shell — examples/integrations/ms-agent-framework-python/Dockerfile:25
- [medium] committed binary — examples/integrations/ms-agent-framework-python/docker/Dockerfile.app
- [medium] pipe remote script to shell — examples/integrations/pydantic-ai/Dockerfile:28
- [medium] committed binary — examples/integrations/pydantic-ai/docker/Dockerfile.app
- [medium] pipe remote script to shell — examples/integrations/strands-python/Dockerfile:29
- [medium] committed binary — examples/integrations/strands-python/docker/Dockerfile.app
- [medium] committed binary — examples/integrations/strands-typescript/docker/Dockerfile.app
- [medium] pipe remote script to shell — examples/showcases/antigravity-repo-doctor/agent/tests/test_tools.py:295
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — examples/showcases/reskinnable-demo/src/app/api/commerce/v1/dev/reset/route.test.ts:447
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — examples/showcases/reskinnable-demo/src/lib/redact-secrets.test.ts:13
- [medium] committed binary — examples/v2/react-native/demo/android/gradle/wrapper/gradle-wrapper.jar
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — packages/channels-intelligence/src/delivery-transport.test.ts:1456
- [medium] secret-shaped string in test, docs or comment (OpenAI/Anthropic key) — packages/runtime/src/v2/runtime/core/__tests__/channel-activation-config.test.ts:67
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — packages/runtime/src/v2/runtime/core/__tests__/channel-activation-config.test.ts:67
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — packages/runtime/tests/service-adapters/unify/unify-adapter-language-model.test.ts:23
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — scripts/__tests__/integration-intelligence-migration.test.ts:2833
- [medium] secret-shaped string in test, docs or comment (OpenAI/Anthropic key) — showcase/angular/scripts/check-browser-artifact.test.ts:30
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — showcase/harness/src/cvdiag/ab-hmac.test.ts:25
- [medium] secret-shaped string in test, docs or comment (OpenAI/Anthropic key) — showcase/harness/src/cvdiag/emit.test.ts:510
- [medium] secret-shaped string in test, docs or comment (OpenAI/Anthropic key) — showcase/harness/src/cvdiag/raw-byte-capture.test.ts:157
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — showcase/harness/src/cvdiag/raw-byte-capture.test.ts:87
- [medium] secret-shaped string in test, docs or comment (OpenAI/Anthropic key) — showcase/harness/src/cvdiag/schema.test.ts:178
- [medium] secret-shaped string in test, docs or comment (OpenAI/Anthropic key) — showcase/harness/src/cvdiag/scrub.test.ts:74
- [medium] secret-shaped string in test, docs or comment (OpenAI/Anthropic key) — showcase/harness/src/cvdiag/scrub.ts:22
- [medium] secret-shaped string in test, docs or comment (OpenAI/Anthropic key) — showcase/harness/src/cvdiag/staged-ts-scrub-parity.test.ts:21
- [medium] pipe remote script to shell — showcase/integrations/ag2/Dockerfile:32
- [medium] pipe remote script to shell — showcase/integrations/agno/Dockerfile:31
- [medium] secret-shaped string in test, docs or comment (OpenAI/Anthropic key) — showcase/integrations/built-in-agent/src/cvdiag/scrub.ts:22
- [medium] pipe remote script to shell — showcase/integrations/claude-sdk-python/Dockerfile:31
- [medium] secret-shaped string in test, docs or comment (OpenAI/Anthropic key) — showcase/integrations/claude-sdk-typescript/src/cvdiag/scrub.ts:22
- [medium] pipe remote script to shell — showcase/integrations/crewai-conversational-flows/Dockerfile:31
- [medium] pipe remote script to shell — showcase/integrations/crewai-crews/Dockerfile:31
- [medium] pipe remote script to shell — showcase/integrations/google-adk/Dockerfile:32
- [medium] pipe remote script to shell — showcase/integrations/google-antigravity/Dockerfile:31
- [medium] pipe remote script to shell — showcase/integrations/langgraph-fastapi/Dockerfile:31
- [medium] pipe remote script to shell — showcase/integrations/langgraph-python/Dockerfile:31
- [medium] secret-shaped string in test, docs or comment (OpenAI/Anthropic key) — showcase/integrations/langgraph-typescript/src/cvdiag/scrub.ts:22
- [medium] pipe remote script to shell — showcase/integrations/langroid/Dockerfile:31
- [medium] pipe remote script to shell — showcase/integrations/llamaindex/Dockerfile:33
- [medium] secret-shaped string in test, docs or comment (OpenAI/Anthropic key) — showcase/integrations/mastra/src/cvdiag/scrub.ts:22
- [medium] pipe remote script to shell — showcase/integrations/ms-agent-dotnet/Dockerfile:28
- [medium] pipe remote script to shell — showcase/integrations/ms-agent-harness-dotnet/Dockerfile:26
- [medium] pipe remote script to shell — showcase/integrations/ms-agent-python/Dockerfile:33
- [medium] pipe remote script to shell — showcase/integrations/openai-agents-python/Dockerfile:31
- [medium] pipe remote script to shell — showcase/integrations/pydantic-ai/Dockerfile:33
- [medium] pipe remote script to shell — showcase/integrations/spring-ai/Dockerfile:58
- [medium] secret-shaped string in test, docs or comment (OpenAI/Anthropic key) — showcase/integrations/strands-typescript/src/cvdiag/scrub.ts:22
- [medium] pipe remote script to shell — showcase/integrations/strands/Dockerfile:35
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — showcase/pocketbase/tests/result-capacity.integration.mjs:98
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — showcase/pocketbase/tests/retention.integration.mjs:126
- [medium] pipe remote script to shell — showcase/scripts/create-integration/index.ts:1216
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — showcase/scripts/lib/__tests__/railway-token.test.ts:31
- [medium] hardcoded credential — tools/runtime-conformance/platform.mjs:80
- [medium] npm prepare hook runs on install — package.json: lefthook install

## Notes
- 2 large or binary files not scanned
- osv.dev checked 0 pinned packages

Static scan only. No resource code was installed or executed.

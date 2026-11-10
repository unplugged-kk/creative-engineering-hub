# CEH-0039 · ag-ui-protocol/ag-ui

https://github.com/ag-ui-protocol/ag-ui

**Gate:** review (worst finding: medium)  
Scanned files: 4090

## Findings
- [medium] pipe remote script to shell — apps/dojo/README.md:27
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — integrations/aws-strands/typescript/src/__tests__/url-fetch-policy.test.ts:2159
- [medium] secret-shaped string in test, docs or comment (hardcoded credential) — integrations/langgraph/python/tests/test_internal_model_calls.py:19
- [medium] privilege escalation — sdks/community/c++/README.md:57
- [medium] committed binary — sdks/community/kotlin/examples/chatapp-java/gradle/wrapper/gradle-wrapper.jar
- [medium] committed binary — sdks/community/kotlin/examples/chatapp-swiftui/gradle/wrapper/gradle-wrapper.jar
- [medium] committed binary — sdks/community/kotlin/examples/chatapp-wearos/gradle/wrapper/gradle-wrapper.jar
- [medium] committed binary — sdks/community/kotlin/examples/chatapp/gradle/wrapper/gradle-wrapper.jar
- [medium] committed binary — sdks/community/kotlin/examples/tools/gradle/wrapper/gradle-wrapper.jar
- [medium] committed binary — sdks/community/kotlin/library/gradle/wrapper/gradle-wrapper.jar

## Notes
- 2 large or binary files not scanned
- osv.dev checked 0 pinned packages

Static scan only. No resource code was installed or executed.

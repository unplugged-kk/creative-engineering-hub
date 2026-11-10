# Security and licensing review

The optional VF consumer accepts a bounded local JSON document and validates an independent trusted catalog fingerprint,
strict schema, approval evidence, provenance pins, licence restrictions, deprecation and compatibility. It does not fetch URLs,
load skill text, import code, spawn commands, install packages or wire itself into the production pipeline. Invalid/unavailable
catalogs select nothing and preserve existing routing. Human-readable guidance is untrusted data, not execution authority.

Digests are integrity checks, not signatures. An operator must review evidence before configuring a fingerprint. Evidence
references are not automatically fetched or proven; no claim of third-party signing or complete legal verification is made.

Independent QA found and corrected generic-word task matching, huge-version conversion and malformed-environment failures.
Hostile fixtures cover unapproved entries, NC licence, invalid schema, malformed nested types, tampered digest, missing dependencies,
unsupported renderers, duplicate/conflicting versions, deprecation and missing files. Contract snapshots are tested identically in CEH/VF.

Two new skills contain original instructions, pinned source attribution, no copied third-party code/assets and no executable scripts.
Source code licences are documented separately from CEH's original-prose redistribution licence, which the owner has not assigned.
No fonts, models, footage or music are distributed. Production approval is absent and production publication stays empty.

No transitive dependency completeness or zero-vulnerability guarantee is claimed. Existing OSV/static findings retain their scan dates.
No new host dependencies, account services, secrets or paid services are used. Sandbox benchmark evidence separately documents
filesystem/network restrictions and denial probes. Authored test audio is synthetic and carries no third-party music attribution.

Publisher review also found release-envelope changes could reuse stale approvals. The final producer independently binds skill
version/bytes and exact reviewed catalog metadata digest, checks every source URL/pin/review gate, rejects bundle symlinks and
requires matching approval actor/time. Independent tests mutate post-approval workflow and bytes and confirm exclusion.
Asset licence checks reject non-commercial and unknown terms separately from code licensing, including optional listed assets.

Final review recorded no remaining material issue in the reviewed producer/consumer paths. This is a scoped review, not a
formal security certification or complete transitive dependency audit. The isolated full VF test run reused pre-existing pinned
dependencies via a temporary task-owned symlink, removed afterward; it did not install dependencies into production.

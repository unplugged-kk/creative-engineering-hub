# CEH read-only catalog contract v2

Schema identifier: `ceh-video-factory-catalog/2`. Machine schema: `catalog.schema.json`.
The standalone standard-library reference implementation is `ceh/catalog.py`.

This contract carries declarative capability and workflow guidance. It does not carry an executable adapter,
installation command, Python module, shell command, plugin endpoint or automatically loaded skill file.
Unknown fields are rejected at every defined object boundary. The consumer must never execute guidance text.

## Trust and opt-in

The consumer is disabled by default. Enabling it requires an explicit local catalog path and a separately configured
expected catalog SHA256 digest. A digest carried inside the same untrusted file only detects accidental changes;
it does not authenticate the publisher or prove that a human approved anything. The trusted expected digest must
be accepted separately by the operator after reviewing the catalog. Never read the expected digest from the catalog itself.

`load_catalog(path, enabled=True, expected_digest=trusted_digest)` checks both schema and whole-catalog fingerprint.
It rejects invalid schema versions, unknown fields, duplicate JSON keys, unsupported JSON constants, malformed nested
objects, missing evidence, unapproved entries, restricted licences, deprecated entries and digest mismatches.
It reads at most 2,000,001 bytes and rejects a catalog larger than 2,000,000 bytes. Missing files, decoding failures
and excessive nesting return a structured unavailable result with no entries. No fallback to a legacy or guessed catalog
is allowed. Video Factory must retain its existing workflow when the optional catalog is unavailable.

## Envelope and entries

An envelope has exactly `schema`, `generated`, `entries` and `digest`. An empty v2 envelope is valid and exposes nothing.
Entries are sorted by ID and version during publication. Only one version of a capability ID may be published at once;
duplicate IDs, including differing versions, invalidate the entire catalog rather than silently choosing a winner.

Each entry has these required fields:

| Fields | Meaning |
|---|---|
| `id`, `name`, `description`, `version` | Stable capability identity; numeric major.minor.patch version |
| `status`, `approval` | Explicit APPROVED state plus actor, timestamp and nonempty approval evidence references |
| `capabilities`, `categories`, `tags` | Discovery metadata |
| `resources` | CEH resource IDs, HTTPS provenance URLs and full 40/64-character commit pins |
| `skills` | Canonical skill name, version and SHA256 digest; references only, never automatically loaded paths |
| `licence` | SPDX label, explicit commercial allowance, restrictions and nonempty licence-review evidence |
| `requirements` | Runtime and dependency names mapped to version constraints |
| `renderers`, `agents` | Explicit allow-lists; an empty renderer list is invalid |
| `inputs`, `outputs` | Named typed inputs with required flags and output descriptions |
| `assets` | Named assets, required flags, attribution and licence labels |
| `compatibility` | Explicit language and output-format allow-lists |
| `evaluation` | Nonempty evaluation and benchmark evidence references; separate nullable 0-5 visual/performance scores |
| `limitations`, `deprecation` | Declared limitations, deprecation state, optional replacement and reason |
| `workflow` | `kind: guidance` and descriptive planning steps |
| `digest` | SHA256 of the canonical entry excluding its own digest |

Non-commercial, NOASSERTION, NONE and unknown licence labels are rejected even if the publisher also sets
`commercial: true`. Commercial usage must be reviewed before publication. An evidence string is a reference,
not a proof: producer governance and operator review must verify the referenced evidence. Asset licence labels are checked independently: non-commercial, unknown, NOASSERTION, NONE and unlicensed
assets invalidate the entry even when the code licence is commercial. Asset licence review must be included in
producer governance; the consumer does not fetch assets or infer their legal status.

## Canonical integrity

For each entry, canonical JSON is UTF-8, Unicode preserved, keys sorted, separators `,` and `:`, no NaN/Infinity,
with its top-level `digest` field omitted. The lowercase hexadecimal SHA256 becomes the entry digest.
The catalog digest uses the same procedure, includes each entry digest, and omits only the envelope digest.
SHA256 is not a signature. The independently configured expected envelope digest binds the reviewed snapshot.

`seal_entry(entry)` and `seal_catalog(entries, generated=timestamp)` calculate digests but confer no approval.
The producer must first verify registry state, approval evidence, review gates, curation pins and benchmark evidence.
The consumer does not ratify historically marked PRODUCTION records.

## Selection and requirements

After a successful trusted load, `select_capabilities(catalog, task=..., renderer=..., ...)` produces structured
`selected`, `rejected` and `errors` arrays. It never invokes a renderer or mutates the catalog. Selection is stable by
capability ID, preserves the caller's renderer and explains each compatibility rejection. Callers supply observed
runtime and dependency versions, typed inputs, available asset IDs and optional agent, language and output-format
requirements. Missing observations fail the relevant requirement rather than assuming compatibility.

Version constraints use numeric major.minor.patch values and exact matches or `==`, `>=`, `<=`, `>` and `<`,
with comma-separated intersections. npm ranges, prereleases and platform-specific package resolution are deliberately
unsupported and rejected. Empty language/output lists make no compatibility claim: a requested language/format
is rejected unless explicitly listed. Actual renderer execution, QA, approval and publishing remain VF responsibilities.

## Migration and rollback

Version 1 is not accepted by the v2 reader. The existing CEH v1 writer remains independent until explicitly migrated;
a missing v1 catalog currently exposes no approved capabilities. Do not silently reinterpret v1 records as v2 evidence.
Keep the initial production v2 catalog empty until specific capabilities receive authorized review and publication.
For rollback disable the feature or restore an earlier reviewed catalog and its independently configured digest.
No production pins, renderer defaults, dependencies, skill files or quality gates change as part of reading the catalog.

## Producer operation

`uv run ceh catalog export --json` writes `catalog-v2.json` without granting any approval or changing lifecycle state.
It considers only resources already in the legacy publication catalog, with a current pin-bound approval and passing gates.
Historical PRODUCTION status alone does not qualify. Each resource must reference canonical `library_skills` whose metadata
explicitly marks production approval and contains a reviewed `catalog_release.entry` with the complete v2 shape.
The entry actor and approval time must match the registry's approval, provenance must bind its pin, and skill content must
match the reviewed digest. Missing evidence excludes that release with a reason; invalid final documents fail publication.

Skill digests bind sorted relative file names and SHA256 content hashes, reject symlinks, and canonicalize skill.yaml while
excluding its `catalog_release` and `approval` envelopes to avoid self-referential hashes. All other metadata and guidance bytes are bound.
The release envelope itself is covered by entry and catalog digests. Publication is not a substitute for reviewing evidence.
The current exported catalog is empty because no real capabilities have been authorized and verified for this release.

Skill approval binds its exact version and bundle digest plus actor/time matching the resource approval. Every source URL/pin and gate is checked against the registry before export. Approval envelopes are excluded from bundle hashes to avoid self-reference; the catalog fingerprint binds the complete release.

The skill approval also binds `catalog_entry_digest`, the canonical reviewed entry payload. Changing requirements, guidance, evidence, licensing or any other release metadata invalidates publication even when skill bytes remain unchanged.

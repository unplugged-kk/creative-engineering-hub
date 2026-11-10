# ADR 0003: Video Factory consumes a catalog; CEH never edits Video Factory

Status: accepted (2026-11-10)

Video Factory is a working production system with its own renderer registry, approvals and tests. CEH publishes
`integrations/video-factory/catalog.json` containing only resources that passed `ceh approve` and `ceh integrate`.
Video Factory decides when and how to read it. `ceh integrate --test` runs Video Factory's own test command first and refuses
to publish on failure. Trade-off: one small reader on the Video Factory side is still needed (a separate, approved change),
in exchange for production never depending on experimental resources.

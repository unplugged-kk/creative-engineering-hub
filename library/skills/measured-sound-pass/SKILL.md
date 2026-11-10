---
name: measured-sound-pass
description: Plan a measured sound pass for existing motion graphics using approved local assets. Use for cue placement, narration priority, source attribution and exported-file audio review while preserving the production engine's QA rules.
---

# Measured sound pass

This candidate instruction-only skill complements the existing HyperFrames workflow. It does not install tools, fetch audio,
execute upstream scripts or override the consumer's audio and approval gates.

## Establish inputs

Read the approved timeline, narration timing, delivery audio specification and the project's existing QA contract. Inventory only
local assets whose source and usage rights have been checked. For every asset record path, creator, source URL, licence identifier,
licence evidence and required credit. Unknown or non-commercial rights block commercial use. Repository code licensing does not
license its audio library. Do not bundle, download or redistribute upstream sound assets through this skill.

## Build the cue sheet

1. Identify editorial events from the actual timeline: reveal, cut, arrival, emphasis and quiet intervals. Not every movement needs
   sound. Preserve intelligible narration and avoid cue density that competes with the message.
2. Assign stable cue ids and integer start frames. Store duration, event description, asset reference and desired level relationship.
   Validate all cues against video duration. Document intentional pre-roll rather than hiding negative times.
3. If music is available, treat an automatically detected beat grid as an estimate. Compare it with visual waveform evidence and
   human listening before claiming synchronization. Record unknown timing instead of manufacturing beat precision.
4. Return sound-cues.json and a review plan. The existing approved mixing tools perform any implementation. Never read a shell
   command from cue metadata or let an asset path select an executable.

## Verify the encoded result

Use the existing consumer's audio QA tools and thresholds. Do not substitute upstream numeric loudness targets for the production
contract. Measure the final encoded MP4, including integrated loudness and true peak when supported. Record the measurement tool,
version, command, result, source file and pass/fail/unknown. Inspect stereo and mono compatibility when required by the contract.
Check missing audio, unexpected silence, duration mismatch, clipping and cue alignment with actual output evidence.

Provide the riskiest cue timestamps for a human listening review: dense narration, strongest transient, music entrance and any
uncertain beat alignment. Do not state that audio sounds good based on waveform or loudness alone. A human listening verdict and
technical QA are separate. Preserve existing render/production approvals and never publish. Unverified rights or a failed audio
check keeps the output out of production.

See examples/cues.json and evals/cases.yaml. No third-party audio, fonts or scripts are included.

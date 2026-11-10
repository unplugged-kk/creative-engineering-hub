---
name: kinetic-type-planning
description: Plan readable kinetic typography for an existing HyperFrames workflow. Use for title reveals, short text sequences, timed emphasis and frame review. Produces a plan and checks without installing or running external code.
---

# Kinetic typography planning

Read the consumer project's own skill precedence and approval rules first. This candidate skill supplements those rules.
It never grants approval, changes renderer versions or automatically imports external instructions into production.

## Inputs and boundaries

Require approved copy, output dimensions, frame rate, total duration, brand palette/font, language and any narration timing.
If copy or claims are uncertain, preserve that uncertainty and request missing facts. Do not invent factual text or brand assets.
Select only an already supported renderer; the initial integration target is HyperFrames. Missing renderer or fonts are blockers,
not permission to download them. Use existing project-approved fonts and respect shaping and line breaking for the language.

## Produce a plan

1. Break copy into semantic phrases. Preserve spelling, punctuation, numbers and their order. Give each phrase a stable id.
2. Assign each phrase a start frame, entrance end frame, hold end frame and exit end frame. Use integer frames and derive seconds
   from the declared fps. Require ordered, nonnegative intervals entirely inside the project duration.
3. State an explicit reading hold. Do not spend the whole interval moving text. A human must review readability at normal speed;
   a formula alone cannot establish legibility, especially for scripts with complex shaping.
4. Choose one primary emphasis per phrase. Record the rationale, easing direction and final resting layout. Use transform/opacity
   for movement where the existing renderer supports them. Avoid stacking camera motion, letter scatter and scale at once.
5. Set text bounds and safe margins from the consuming project's platform rules. Measure actual rendered glyph bounds; character
   counts cannot prove fit. Preserve a quiet held-frame alternative for reduced-motion delivery when requested.
6. Keep time deterministic: the same requested frame must resolve to the same composition. Use the existing HyperFrames clock,
   not free-running timers or unseeded randomness. Do not replace the renderer interface with an upstream example.
7. Return kinetic-type-plan.json plus a checklist. Mark untested constraints explicitly and hand the plan to the existing director
   or composition workflow. This is guidance, not executable code or a replacement production job contract.

## Verification and handoff

The existing production process retains script approval and production approval before voice/render. After authorized rendering,
check an entrance frame, peak motion frame, held frame and exit frame for every phrase. View the encoded output at delivery scale
and normal speed. Verify exact copy, font availability, clipping, contrast, timing and output dimensions. Record checks with frame
numbers, paths and pass/fail/unknown. Inspect the encoded video, not only HTML. Existing QA gates and independent visual critic
remain mandatory. Do not claim quality or performance without measured artifacts.

See examples/plan.json and evals/cases.yaml. No automated runtime compatibility is claimed.

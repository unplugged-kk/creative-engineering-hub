# Canonical skill invocation - Codex planning evidence

Date: 2026-11-10. Agent: the active Codex curation subagent in this continuation. The tool API does not expose a precise agent
binary/model version; version is **not verified**. Invocation method: read the canonical
`library/skills/kinetic-type-planning/SKILL.md` 0.1.0 directly, then apply its instructions to the controlled task below.
This is evidence of one current agent following guidance, not a standalone CLI run, cross-agent compatibility, production
approval or successful rendering. No other agents are claimed to have invoked the skill.

## Controlled task

Prepare a six-second vertical title plan at 30 fps for the exact copy `Revenue target 20%`. It is an illustrative target,
not a measured result. Renderer remains the existing HyperFrames baseline. There are no approved brand/font inputs in this test.
Do not install fonts, change renderer pins, execute upstream code, grant production approvals or claim rendered quality.

## Result produced by the agent

```json
{
  "schema": "ceh-kinetic-type-plan/1",
  "skill": {"name": "kinetic-type-planning", "version": "0.1.0"},
  "mode": "controlled-planning-test",
  "status": "blocked-before-production",
  "renderer": "hyperframes",
  "width": 1080,
  "height": 1920,
  "fps": 30,
  "duration_frames": 180,
  "language": "en",
  "copy": "Revenue target 20%",
  "claim_kind": "illustrative target, not achieved result",
  "required_visible_label": "Illustrative target",
  "phrases": [{
    "id": "target-title",
    "text": "Revenue target 20%",
    "start_frame": 0,
    "entrance_end_frame": 18,
    "hold_end_frame": 150,
    "exit_end_frame": 180,
    "emphasis": "20%",
    "rationale": "One emphasis identifies the target without changing the claim.",
    "motion": "One vertical entrance, ease-out; still reading hold; ease-in exit.",
    "resting_layout": "Centered in platform-safe text bounds, pending font and bounds verification."
  }],
  "clock": "Existing HyperFrames timeline, integer frames; no independent timers or randomness.",
  "blockers": ["Approved brand palette/font absent", "Actual glyph bounds not measured"],
  "required_checks": ["Exact copy and visible illustrative label", "Frames 0, 9, 18, 90, 150, 179", "Normal-speed delivery-size readability", "Contrast and clipping", "Encoded output dimensions", "Existing independent visual and technical QA"],
  "unverified": ["Rendered output", "Readability", "Performance", "Font availability", "Production gate approval"]
}
```

The frame intervals are ordered and within 180 frames. Entrance: 0.6 seconds. Reading hold: 4.4 seconds. Exit: 1.0 second.
These timings are a test proposal, not measured readability evidence. The phrase and percent sign are preserved verbatim.
The visible label is additional context and does not silently turn a target into a result. Brand/font blockers remain explicit.

## Evaluation cases followed

| Case from canonical evals/cases.yaml | Observed outcome |
|---|---|
| preserves-copy | Exact text kept, target separated from achieved result and labelled illustrative |
| deterministic-handoff | Integer frames, bounded timeline, quiet hold, existing renderer clock and unchanged gates |
| no-quality-fabrication | Rendering, readability and performance explicitly unverified |
| missing-font | Missing approved font blocks production; no install or shaping claim made |

## Reproduce or challenge

Read the same canonical SKILL.md, supply the controlled task above to the agent under test, and inspect whether it preserves
copy, provides a bounded plan, reports blockers and respects execution/approval boundaries. Record that agent's actual version
and raw invocation separately. A human or independent critic must review any subsequently rendered output.
This document stores the planning result directly; it does not claim a separate JSON artifact or MP4 was generated.

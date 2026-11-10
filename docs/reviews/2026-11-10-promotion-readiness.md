# First catalog promotion: decision prepared

No approval, integration, upstream adoption or resource execution is performed by this review.

## Proposed resource

CEH-0018, LottieFiles/motion-design-skill, is a CANDIDATE. Its code licence is MIT and the licence gate passes.
The refreshed static security scan examined 20 files, found no findings and passes. No bundled media, fonts or models
were detected. See reports/CEH-0018/licensing.md and security.md for scope and limitations.

Its registered capabilities cover motion graphics, transitions, camera movement, data visualization,
2D animation and documentary storytelling. Detected renderer compatibility is Lottie. Existing HyperFrames covers
motion graphics too; this candidate should contribute reusable motion guidance rather than replace the production renderer.
GSAP skills (CEH-0011) overlaps on 2D animation. Neither comparison establishes superior rendered quality.

The recorded score is 4.0/5 at 70% evidence coverage. Visual quality and performance remain unknown.
Agent compatibility is detected statically; actual invocation across agents has not been demonstrated.

## Concrete approval scope

The proposed first integration would run `uv run ceh approve CEH-0018` followed by
`uv run ceh integrate CEH-0018 --test`. This publishes the approved record to CEH's
integrations/video-factory/catalog.json and runs the configured VF regression suite. It does not install upstream code,
advance a production pin or create a VF-side catalog reader. A failing VF baseline must be reported explicitly.

The user must explicitly select and authorize this resource before those commands run. Other candidates and all seven
historically marked PRODUCTION records remain separate decisions. Their historical usage does not constitute CEH approval.

## Other pending decisions

- Render benchmarks under lab/ only after authorization to install or execute the selected resource code.
- Authorize a VF-side catalog reader separately; CEH does not modify the VF checkout.
- Decide whether to schedule weekly upstream checks. Policy frequency alone does not schedule execution.
- Read reports/CEH-0014/upstream-analysis.md before deciding on HyperFrames adoption. Its pin is unchanged.

## Verified baseline

The VF suite rerun on 2026-11-10 passed: 1023 passed, 8 skipped in 140.70 seconds, using the documented dedicated Python
environment. The earlier handover's whisper-cli failure did not reproduce. This is the current baseline, not an integration test
for this candidate: approval and publication have not occurred.

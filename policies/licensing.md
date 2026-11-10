# Licensing policy

Classes and gates live in `policy.yaml`. Rules:

- **Code licence is not asset licence.** Reports list bundled media, fonts and models separately; each needs its own terms.
- `permissive` passes. `copyleft` (GPL/AGPL/LGPL/CC-BY-SA) and `unknown`/`custom` (incl. Remotion's company licence) need
  `ceh approve --licence-reviewed "<what was checked>"`. Copyleft code may only run as an isolated external process; never
  copy it into Video Factory.
- `non-commercial` (CC-BY-NC*, PolyForm Noncommercial) is **never approvable**. Status becomes RESTRICTED; the method may be
  referenced, the code and assets may not be used.
- Detection: GitHub API SPDX first, then LICENSE text fingerprints. A reading of licence files is not legal advice.

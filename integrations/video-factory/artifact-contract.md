# Production artifact contract (ceh-artifact/1)

A renderer adapter returns a project folder:

| Path | Required | Content |
|---|---|---|
| manifest.json | yes | `{schema, renderer, output, ...}`; `output` names the final video (default `output.mp4`) |
| output.mp4 (or `manifest.output`) | yes | Final render; must be readable by ffprobe |
| preview.mp4 | no | Low-resolution preview |
| assets/ | no | Inputs used, with provenance in sources.json |
| sources.json | no | Every third-party asset: url, licence, attribution |
| render-log.json | no | Commands, versions, timings |
| quality-report.json | no | Visual and audio QA results |

Video Factory's job folders (`manifest.json` with `renderer`, `final_artifact`, `qa/`, `renders/`) map onto this contract
through an adapter; the contract does not require Video Factory to change its layout.

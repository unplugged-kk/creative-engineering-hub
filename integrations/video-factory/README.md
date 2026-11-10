# Video Factory integration

CEH is upstream management and R&D; Video Factory (`~/git/video-factory`) is production. The boundary:

- **catalog.json** (`schema: ceh-video-factory-catalog/1`): written only by `ceh integrate`. Each entry: id, name, url, type,
  capabilities, renderers, pinned_commit, licence (spdx, class, review note), skills, approval record, integrated_at.
  Video Factory should treat it as the allow-list of external capabilities.
- **Renderers**: Video Factory keeps its own registry (`contentos/renderers/registry.py`: hyperframes default, mpt, remotion).
  CEH ids map to those through `registry/renderers.yaml` (`video_factory` key).
- **Tests**: `ceh integrate --test` and `ceh upstream report --run-tests` run Video Factory's own suite (command in
  `policies/policy.yaml: video_factory.test_command`) and refuse to publish on failure.
- **Artifact contract**: see `artifact-contract.md`; check any renderer output with `ceh artifact <dir>`.

Not done here, by design: any change inside Video Factory. A small reader of `catalog.json` there is a separate, approved task.

"""Prepare synthetic test-only metadata and invoke the read-only VF consumer.

This does not approve a real skill/resource or write either production catalog.
Runtime versions must be supplied from prior measurements; no runtime probes run.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ceh.catalog import seal_catalog, seal_entry, validate_catalog  # noqa: E402
from ceh.catalog_publish import skill_digest  # noqa: E402
from ceh.store import read_yaml  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('vf', 'python', 'output'):
        parser.add_argument('--' + name, required=True, type=Path)
    for name in ('node-version', 'hyperframes-version'):
        parser.add_argument('--' + name, required=True)
    args = parser.parse_args()
    vf, output = args.vf.resolve(), args.output.resolve()
    if not (vf / 'contentos/ceh_catalog.py').is_file():
        parser.error('--vf must identify the isolated consumer checkout, not an unchanged production checkout')
    for repo in (ROOT, vf):
        if output == repo or repo in output.parents:
            parser.error('output must be outside both repositories')
    if output.exists():
        parser.error('output must be a new directory; existing evidence is preserved')
    for value in (args.node_version, args.hyperframes_version):
        if not re.fullmatch(r'[0-9]{1,6}\.[0-9]{1,6}\.[0-9]{1,6}', value):
            parser.error('versions must be measured numeric major.minor.patch values')
    python = args.python.absolute()
    if not python.is_file():
        parser.error('--python must identify an existing interpreter')
    directory = ROOT / 'library/skills/kinetic-type-planning'
    metadata = read_yaml(directory / 'skill.yaml')
    timestamp = datetime.now(timezone.utc).isoformat()
    entry = seal_entry(dict(
        id='kinetic-type-planning', name='Synthetic kinetic typography fixture',
        description='Kinetic typography planning for an explicitly synthetic test, not production approval.',
        version=metadata['version'], status='APPROVED', capabilities=['kinetic-typography'],
        categories=['motion'], tags=['synthetic-test-only'],
        resources=[dict(id='fixture:synthetic-source', url='https://example.invalid/ceh/synthetic-test-only',
                        pinned_commit='0' * 40)],
        skills=[dict(name=metadata['name'], version=metadata['version'], digest=skill_digest(directory))],
        approval=dict(status='APPROVED', by='synthetic-test-fixture-not-owner', at=timestamp,
                      evidence=['test-only:synthetic approval fixture; no real lifecycle or approval mutation']),
        licence=dict(spdx='MIT', commercial=True, restrictions=['Synthetic fixture values only; not a real licence determination.'],
                     review_evidence=['test-only:synthetic licence fixture, not commercial approval of canonical skill']),
        requirements=dict(runtimes=dict(node='>=' + args.node_version + ',<25.0.0'),
                          dependencies=dict(hyperframes='==' + args.hyperframes_version)),
        renderers=['hyperframes'], agents=['codex'],
        inputs=dict(title=dict(type='string', required=True)), outputs=['motion-plan'], assets=[],
        compatibility=dict(languages=['en'], output_formats=['mp4']),
        evaluation=dict(evidence=['test-only:consumer fixture'], benchmarks=['test-only:authored render fixture'],
                        visual_quality=None, performance=None),
        limitations=['Synthetic approval only. No owner approval or production capability.',
                     'Source URL and all-zero pin are deliberately synthetic, not an upstream identity.',
                     'MIT/commercial fields are test inputs, not a licence conclusion for original CEH instructions.',
                     'Guidance is not loaded or executed by the consumer.'],
        deprecation=dict(deprecated=False, replacement=None, reason=''),
        workflow=dict(kind='guidance', steps=[
            'Prepare kinetic-type-plan.json from the candidate canonical instruction-only skill as a test.',
            'Render only the authored fixture using existing HyperFrames in the verified sandbox.',
            'Apply existing VF QA and independent visual review; preserve production approval boundaries.']),
    ))
    catalog = seal_catalog([entry], generated=timestamp)
    errors = validate_catalog(catalog)
    if errors:
        raise ValueError(errors)
    environment = dict(runtimes=dict(node=args.node_version), dependencies=dict(hyperframes=args.hyperframes_version),
                       inputs=dict(title='Make the idea clear.'), agent='codex', language='en', output_format='mp4')
    output.mkdir(parents=True)
    (output / 'home').mkdir()
    for name, data in [('fixture-catalog.json', catalog), ('environment.json', environment)]:
        (output / name).write_text(json.dumps(data, indent=2) + '\n')
    command = [str(python), '-m', 'contentos.ceh_catalog', '--enable', '--catalog', str(output / 'fixture-catalog.json'),
               '--trusted-digest', catalog['digest'], '--task', 'kinetic-typography', '--renderer', 'hyperframes',
               '--environment', str(output / 'environment.json')]
    env = dict(PATH='/usr/bin:/bin', HOME=str(output / 'home'), PYTHONPATH=str(vf), PYTHONDONTWRITEBYTECODE='1')
    (output / 'selection-command.json').write_text(json.dumps(dict(argv=command, environment=env), indent=2) + '\n')
    result = subprocess.run(command, cwd=vf, env=env, capture_output=True, text=True, timeout=30)
    (output / 'selection.json').write_text(result.stdout)
    (output / 'selection.stderr.log').write_text(result.stderr)
    if result.returncode:
        raise RuntimeError(f'read-only VF consumer failed ({result.returncode}); see {output}')
    selected = json.loads(result.stdout)
    if not selected.get('available') or selected.get('errors') or not selected.get('selected'):
        raise RuntimeError('fixture was not selected; inspect selection.json')
    print(json.dumps(dict(scope='synthetic test only; no production approval', selection=str(output / 'selection.json'),
                          catalog_digest=catalog['digest'], skill_digest=entry['skills'][0]['digest']), indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

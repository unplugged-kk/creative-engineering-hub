"""Render an authored fixture using existing tools inside the macOS native sandbox.

No install, downloads, production approval or execution of catalog content is performed.
"""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import time
import wave

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def literal(path: Path | str) -> str:
    return json.dumps(str(path))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ('vf', 'node', 'chrome', 'ffmpeg', 'ffprobe', 'python', 'selection', 'output'):
        ap.add_argument('--' + name, required=True, type=Path)
    args = ap.parse_args()
    vf, out = args.vf.resolve(), args.output.resolve()
    for repo in (ROOT, vf):
        if out == repo or repo in out.parents:
            ap.error('output must be outside both repositories')
    if out.exists():
        ap.error('output must be a new directory; existing artifacts are preserved')
    selection = json.loads(args.selection.read_text())
    selected = selection.get('selected')
    if not isinstance(selected, list) or not selected or any(e.get('renderer') != 'hyperframes' for e in selected):
        ap.error('selection must contain a nonempty hyperframes selected list')
    if selection.get('errors'):
        ap.error('selection has errors')
    if not shutil.which('sandbox-exec'):
        ap.error('macOS sandbox-exec is required; there is no unsandboxed fallback')
    binaries = {key: getattr(args, key).resolve(strict=True) for key in ('node', 'chrome', 'ffmpeg', 'ffprobe', 'python')}
    out.mkdir(parents=True)
    project = out / 'project'
    project.mkdir()
    for name in ('home', 'tmp'):
        (out / name).mkdir()
    shutil.copyfile(HERE / 'index.html', project / 'index.html')
    shutil.copyfile(vf / 'contentos/templates/gsap.min.js', project / 'gsap.min.js')
    shutil.copyfile(HERE / 'probe.cjs', out / 'probe.cjs')
    qa = (HERE / 'qa.py').read_text().replace('/tmp/ceh-benchmark/video.mp4', str(out / 'video.mp4'))
    (out / 'qa.py').write_text(qa)
    plan = json.loads((ROOT / 'library/skills/kinetic-type-planning/examples/plan.json').read_text())
    plan['copy'] = 'Make the idea clear.'
    plan['phrases'][0]['text'] = plan['copy']
    plan['selection'] = selected
    (out / 'kinetic-type-plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    (out / 'selection.json').write_text(json.dumps(selection, indent=2) + '\n')
    (project / 'hyperframes.json').write_text(json.dumps(dict(width=1080, height=1920, fps=30, duration=6)))
    with wave.open(str(project / 'tone.wav'), 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(48000)
        samples = bytearray()
        for i in range(6 * 48000):
            t = i / 48000
            envelope = max(0, min(1, t / .05, (6 - t) / .05))
            samples.extend(struct.pack('<h', int(.18 * envelope * math.sin(2 * math.pi * 440 * t) * 32767)))
        wav.writeframes(samples)
    paths = [out, binaries['node'].parent.parent, binaries['chrome'].parent, vf / 'node_modules',
             vf / 'contentos', ROOT / '.venv', binaries['python'].parent.parent]
    allow = '\n'.join(f'(allow file-read* (subpath {literal(p)}))' for p in paths)
    profile = f'''(version 1)
(allow default)
(deny file-read* (subpath "/Users") (subpath "/private/var/folders") (subpath "/private/tmp") (subpath "/tmp") (subpath "/Volumes"))
{allow}
(allow file-read* (literal {literal(vf)}) (literal {literal(vf / 'config/quality.yaml')}))
(allow file-read-metadata)
(deny file-write*)
(allow file-write* (subpath {literal(out)}) (literal "/dev/null"))
(deny network*)
(allow network-inbound (local ip "localhost:*"))
(allow network-outbound (remote ip "localhost:*"))
'''
    (out / 'profile.sb').write_text(profile)
    env = dict(HOME=str(out / 'home'), TMPDIR=str(out / 'tmp'),
               PATH=os.pathsep.join([str(binaries['node'].parent), str(binaries['ffmpeg'].parent), '/usr/bin', '/bin']),
               HYPERFRAMES_NO_TELEMETRY='1', DO_NOT_TRACK='1', HYPERFRAMES_BROWSER_PATH=str(binaries['chrome']),
               HYPERFRAMES_FFMPEG_PATH=str(binaries['ffmpeg']), HYPERFRAMES_FFPROBE_PATH=str(binaries['ffprobe']),
               PYTHONPATH=str(vf), PYTHONDONTWRITEBYTECODE='1')
    prefix = ['/usr/bin/sandbox-exec', '-f', str(out / 'profile.sb')]
    commands = []

    def run(name: str, cmd: list[str], *, timed: bool = False) -> None:
        command = (['/usr/bin/time', '-l'] if timed else []) + prefix + cmd
        commands.append(dict(name=name, argv=command, environment=env))
        with (out / name).open('w') as log:
            completed = subprocess.run(command, cwd=project, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=180)
        (out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
        if completed.returncode:
            raise RuntimeError(f'{name} failed ({completed.returncode}); see {out / name}; no unsandboxed retry')

    probe = (out / 'probe.cjs').read_text()
    probe = probe.replace('/Users/kishore/git/creative-engineering-hub/README.md', str(ROOT / 'README.md'))
    probe = probe.replace('/Users/kishore/.contentos/secrets', str(Path.home() / '.contentos/secrets'))
    (out / 'probe.cjs').write_text(probe)
    run('probe.json', [str(binaries['node']), str(out / 'probe.cjs')])
    evidence = json.loads((out / 'probe.json').read_text())
    required = dict(private_home='EPERM', outside_write='EPERM', loopback='allowed', external_network='EPERM')
    if any(evidence.get(k) != v for k, v in required.items()):
        raise RuntimeError('sandbox isolation probe failed; render not attempted')
    if evidence.get('private_credentials') not in ('EPERM', 'ENOENT'):
        raise RuntimeError('private credentials boundary probe failed; render not attempted')
    cli = vf / 'node_modules/hyperframes/dist/cli.js'
    run('lint.log', [str(binaries['node']), str(cli), 'lint'])
    started = time.monotonic()
    run('render.log', [str(binaries['node']), str(cli), 'render', '-o', str(out / 'video.mp4')], timed=True)
    elapsed = time.monotonic() - started
    run('qa.json', [str(args.python.absolute()), str(out / 'qa.py')])
    run('preview.log', [str(binaries['ffmpeg']), '-hide_banner', '-loglevel', 'error', '-i', str(out / 'video.mp4'),
                        '-vf', "select='eq(n,6)+eq(n,18)+eq(n,90)+eq(n,168)',scale=270:480,tile=4x1", '-frames:v', '1', str(out / 'contact-sheet.png')])
    render_log = (out / 'render.log').read_text()
    rss = re.search(r'(\d+)\s+maximum resident set size', render_log)
    result = dict(schema='ceh-fixture-benchmark/1', scope='synthetic fixture approval only',
                  production_approved=False, selected=selected, renderer='hyperframes',
                  hyperframes=json.loads((vf / 'node_modules/hyperframes/package.json').read_text())['version'],
                  wall_seconds=round(elapsed, 3), maximum_resident_set_size_bytes=int(rss[1]) if rss else None,
                  output=str(out / 'video.mp4'), output_bytes=(out / 'video.mp4').stat().st_size,
                  qa=json.loads((out / 'qa.json').read_text()), visual_review='requires independent review',
                  limitations=['Illustrative tone, not narration', 'No approved real catalog capability', 'Single authored fixture, no comparative superiority evidence'])
    (out / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

"""Safety preflights must fail before executing any renderer or creating artifacts."""
import importlib.util
import json
from pathlib import Path
import sys

import pytest


def harness():
    path = Path(__file__).resolve().parents[1] / 'tools/benchmarks/kinetic_type/run.py'
    spec = importlib.util.spec_from_file_location('kinetic_benchmark', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('mode', ['unsupported-renderer', 'missing-sandbox'])
def test_no_execution_before_validated_preflight(tmp_path, monkeypatch, mode):
    module = harness()
    selection = tmp_path / 'selection.json'
    selection.write_text(json.dumps({'selected':[{'renderer':'remotion' if mode == 'unsupported-renderer' else 'hyperframes'}]}))
    output = tmp_path / 'output'
    argv = ['benchmark', '--vf', str(tmp_path / 'vf'), '--selection', str(selection), '--output', str(output)]
    for name in ['node', 'chrome', 'ffmpeg', 'ffprobe', 'python']:
        argv += ['--'+name, '/bin/true']
    monkeypatch.setattr(sys, 'argv', argv)
    monkeypatch.setattr(module.shutil, 'which', lambda _: None)
    def forbidden(*args, **kwargs):
        pytest.fail('subprocess started before required sandbox preflight')
    monkeypatch.setattr(module.subprocess, 'run', forbidden)
    with pytest.raises(SystemExit):
        module.main()
    assert not output.exists()

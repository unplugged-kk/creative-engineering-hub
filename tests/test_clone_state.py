"""CLI inspection distinguishes object-only clones from edited working checkouts."""
import subprocess

from ceh.store import Registry
from conftest import SKILL_REPO, make_repo


def test_no_checkout_local_copy_is_not_modified(ceh, run_ceh):
    upstream = make_repo(ceh['tmp'] / 'upstream', SKILL_REPO)
    local = ceh['tmp'] / 'local' / 'object-copy'
    subprocess.run(['git', 'clone', '--quiet', '--no-checkout', f'file://{upstream}', str(local)], check=True)
    code, rec, err = run_ceh('add', f'file://{upstream}')
    assert code == 0, err
    state = Registry().get(rec['id'])['local']
    assert state['modified'] is False
    assert state['state'][str(local)]['uncommitted_count'] == 0
    assert state['state'][str(local)]['checkout'] == 'object-only'
    code, _, err = run_ceh('inspect', rec['id'])
    assert code == 0, err
    assert Registry().get(rec['id'])['local']['modified'] is False


def test_real_checkout_deletions_and_edits_remain_modified(ceh, run_ceh):
    upstream = make_repo(ceh['tmp'] / 'upstream', SKILL_REPO)
    local = ceh['tmp'] / 'local' / 'working-copy'
    subprocess.run(['git', 'clone', '--quiet', f'file://{upstream}', str(local)], check=True)
    (local / 'README.md').unlink()
    (local / 'SKILL.md').write_text('user edits\n')
    code, rec, err = run_ceh('add', f'file://{upstream}')
    assert code == 0, err
    state = Registry().get(rec['id'])['local']
    assert state['modified'] is True
    assert state['state'][str(local)]['uncommitted_count'] == 2


def test_object_only_copy_untracked_work_is_preserved(ceh, run_ceh):
    upstream = make_repo(ceh['tmp'] / 'upstream', SKILL_REPO)
    local = ceh['tmp'] / 'local' / 'object-copy'
    subprocess.run(['git', 'clone', '--quiet', '--no-checkout', f'file://{upstream}', str(local)], check=True)
    (local / 'user-note.txt').write_text('do not lose me\n')
    code, rec, err = run_ceh('add', f'file://{upstream}')
    assert code == 0, err
    state = Registry().get(rec['id'])['local']
    assert state['modified'] is True
    assert state['state'][str(local)]['uncommitted_count'] == 1
    assert (local / 'user-note.txt').read_text() == 'do not lose me\n'

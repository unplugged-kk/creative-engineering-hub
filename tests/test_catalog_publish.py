import json

from ceh.catalog import digest, validate_catalog
from ceh.catalog_publish import skill_digest
from ceh.store import Registry
from conftest import SKILL_REPO, make_repo


def test_export_does_not_ratify_historical_production(ceh, run_ceh):
    up = make_repo(ceh['tmp'] / 'up' / 'kit', SKILL_REPO)
    _, rec, _ = run_ceh('add', f'file://{up}')
    reg = Registry()
    rec = reg.get(rec['id'])
    rec['status'] = 'PRODUCTION'
    reg.save(rec)
    code, result, err = run_ceh('catalog', 'export')
    assert code == 0, err
    doc = json.loads((ceh['root'] / 'integrations/video-factory/catalog-v2.json').read_text())
    assert not validate_catalog(doc)
    assert doc['entries'] == [] and result['entries'] == 0
    assert reg.get(rec['id'])['status'] == 'PRODUCTION'


def test_guidance_digest_binds_bytes_but_not_release_envelope(tmp_path):
    (tmp_path / 'SKILL.md').write_text('Original guidance')
    meta = tmp_path / 'skill.yaml'
    meta.write_text('name: demo\nversion: 1.0.0\n')
    before = skill_digest(tmp_path)
    meta.write_text('name: demo\nversion: 1.0.0\ncatalog_release: {entry: {digest: abc}}\n')
    assert skill_digest(tmp_path) == before
    (tmp_path / 'SKILL.md').write_text('Changed guidance')
    assert skill_digest(tmp_path) != before


def test_reviewed_release_exports_without_lifecycle_mutation(ceh, run_ceh):
    import yaml
    from test_catalog import entry as entry_fixture
    from ceh.catalog_publish import export_catalog

    up = make_repo(ceh['tmp'] / 'up' / 'kit', SKILL_REPO)
    _, summary, _ = run_ceh('add', f'file://{up}')
    reg = Registry()
    rec = reg.get(summary['id'])
    item = entry_fixture.__wrapped__()
    rec['status'] = 'PRODUCTION'
    rec['url'] = 'https://example.org/source'
    rec['approval'] = {'by': item['approval']['by'], 'at': item['approval']['at'],
                       'pinned_commit': rec['upstream']['pinned_commit']}
    rec['library_skills'] = [item['id']]
    reg.save(rec)
    legacy = ceh['root'] / 'integrations/video-factory/catalog.json'
    legacy.parent.mkdir(parents=True)
    legacy.write_text(json.dumps({'schema': 'ceh-video-factory-catalog/1', 'entries': [{'id': rec['id']}]}))
    sk = ceh['root'] / 'library/skills' / item['id']
    sk.mkdir()
    (sk / 'SKILL.md').write_text('Original test-only guidance')
    meta = {'name':item['id'], 'version':item['version'],
            'approval':{'status':'APPROVED','production_eligible':True}}
    (sk / 'skill.yaml').write_text(yaml.safe_dump(meta))
    meta['approval'].update({'version':item['version'], 'digest':skill_digest(sk), 'by':rec['approval']['by'], 'at':rec['approval']['at']})
    item['resources'] = [{'id':rec['id'], 'url':'https://example.org/source', 'pinned_commit':rec['upstream']['pinned_commit']}]
    item['skills'] = [{'name':item['id'], 'version':item['version'], 'digest':skill_digest(sk)}]
    meta['approval']['catalog_entry_digest'] = digest(item)
    meta['catalog_release'] = {'entry':item}
    (sk / 'skill.yaml').write_text(yaml.safe_dump(meta))
    destination = ceh['root'] / 'catalog-v2.json'
    assert export_catalog(reg, destination)['entries'] == 1
    assert not validate_catalog(json.loads(destination.read_text()))
    assert reg.get(rec['id'])['status'] == 'PRODUCTION'
    meta['catalog_release']['entry']['workflow']['steps'] = ['Changed after approval']
    (sk / 'skill.yaml').write_text(yaml.safe_dump(meta))
    changed = export_catalog(reg, destination)
    assert changed['entries'] == 0 and 'metadata differs' in changed['excluded'][0]['reason']
    (sk / 'SKILL.md').write_text('Changed after review')
    result = export_catalog(reg, destination)
    assert result['entries'] == 0 and 'bytes differ' in result['excluded'][0]['reason']

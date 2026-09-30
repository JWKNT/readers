"""Refresh existing search paragraphs without changing chapter text or metadata.

Usage: python3 tools/rebuild_search.py [reader-id ...]
Without IDs, include catalog readers and the three retained Liu source readers.
"""
import argparse
import json

import import_earths_past as common
from rebuild_annotations import Fragment

ROOT = common.ROOT


def build(slug):
    folder = ROOT / slug
    path = folder / 'search.json'
    source = path.read_text()
    records = json.loads(source)
    manifest = json.loads((folder / 'manifest.json').read_text())
    assert [row['id'] for row in records] == [c['id'] for c in manifest['chapters']], (slug, 'chapter order')
    changed = 0
    for row in records:
        chapter = json.loads((folder / 'chapters' / (row['id'] + '.json')).read_text())
        tree = Fragment(chapter['html']).root
        paragraphs = {'chapter-title': chapter['title']}
        paragraphs.update({e.get('data-block'): common.norm(common.searchable(e))
                           for e in tree.iter() if e.get('data-block')
                           and not any(x.get('data-block') for x in list(e.iter())[1:])})
        for paragraph in row['paragraphs']:
            assert paragraph['id'] in paragraphs, (slug, row['id'], paragraph['id'])
            value = paragraphs[paragraph['id']]
            changed += paragraph['text'] != value
            paragraph['text'] = value
    if changed:
        common.save(path, records)
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('readers', nargs='*')
    args = parser.parse_args()
    readers = args.readers or [r['id'] for r in json.loads((ROOT / 'library.json').read_text())] + ['three-body-problem', 'dark-forest', 'deaths-end']
    for slug in dict.fromkeys(readers):
        changed = build(slug)
        if changed:
            print(f'{slug}: {changed} search paragraphs refreshed')


if __name__ == '__main__':
    main()

"""Validate the static edition; optionally prove text preservation against a Git ref."""
import argparse
from collections import Counter
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]

class Inspect(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.text, self.ids, self.annotations, self.links = [], [], [], []
        self.block = None
        self.feed(source)

    def handle_data(self, text):
        self.text.append(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'data-block' in attrs:
            self.block = attrs.get('id')
            self.ids.append(self.block)
        if 'data-term' in attrs:
            self.annotations.append((attrs['data-term'], self.block,
                                     attrs.get('data-first'), attrs.get('data-local-first')))
        self.links.extend(attrs[k] for k in ('href', 'src') if attrs.get(k))


def article(source):
    return re.search(r'<article\b[^>]*>(.*?)</article>', source, re.S)[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', help='Git ref whose chapter text and IDs must be preserved')
    args = parser.parse_args()
    baseline = None
    if args.baseline:
        baseline = tarfile.open(fileobj=io.BytesIO(subprocess.check_output(
            ['git', '-C', str(ROOT), 'archive', args.baseline])))
    library = {b['id']: b for b in json.loads((ROOT / 'library.json').read_text())}
    for book in sorted(ROOT.glob('book-*')):
        manifest = json.loads((book / 'manifest.json').read_text())
        glossary = json.loads((book / 'glossary.json').read_text())
        terms = {entry['id']: entry for entry in glossary}
        assert len(terms) == len(glossary), (book, 'duplicate glossary IDs')
        assert manifest['glossaryCount'] == library[book.name]['glossaryCount'] == len(glossary)
        counts, first_flags, first = Counter(), Counter(), {}
        for chapter in manifest['chapters']:
            path = book / 'chapters' / (chapter['id'] + '.json')
            data = json.loads(path.read_text())
            current = Inspect(data['html'])
            static = Inspect(article(path.with_suffix('.html').read_text()))
            assert ''.join(current.text) == ''.join(static.text), (path, 'static text mismatch')
            assert current.ids == static.ids == data['blocks'], (path, 'paragraph mismatch')
            assert len(current.ids) == len(set(current.ids)), (path, 'duplicate paragraph IDs')
            anchors = [{'term': t, 'paragraph': p} for t, p, f, local in current.annotations if local == 'true']
            assert anchors == data['noteAnchors'] == chapter['noteAnchors'], (path, 'anchor mismatch')
            if baseline:
                old = json.loads(baseline.extractfile(str(path.relative_to(ROOT))).read())
                previous = Inspect(old['html'])
                assert ''.join(current.text) == ''.join(previous.text), (path, 'text changed')
                for key in ('blocks', 'words', 'startWords', 'id'):
                    assert data[key] == old[key], (path, key)
            for term, paragraph, flag, local in current.annotations:
                assert term in terms, (path, term)
                counts[term] += 1
                first.setdefault(term, {'chapter': chapter['id'], 'paragraph': paragraph, 'index': chapter['index']})
                first_flags[term] += flag == 'true'
        for entry in glossary:
            tid = entry['id']
            assert counts[tid] == entry['occurrences'], (book, tid, 'count')
            assert first[tid] == entry['first'], (book, tid, 'first location')
            assert first_flags[tid] == 1, (book, tid, 'first flag')
            assert entry['note'].strip() and entry['short'].strip()
            for source in entry['sources']:
                assert urlsplit(source['url']).scheme in ('http', 'https')
        index = (book / 'index.html').read_text()
        assert 'series-links' not in index
        initial = json.loads((book / 'chapters' / (manifest['defaultChapter'] + '.json')).read_text())
        assert ''.join(Inspect(article(index)).text) == ''.join(Inspect(initial['html']).text)
        print(f'{book.name}: {len(glossary)} entries, {len(manifest["chapters"])} chapters, {sum(counts.values())} annotations')
    for path in ROOT.rglob('*.html'):
        for link in Inspect(path.read_text()).links:
            url = urlsplit(link)
            if not url.scheme and not url.netloc and url.path:
                assert (path.parent / unquote(url.path)).exists(), (path, link)
    print('PASS: glossary metadata, paragraph IDs, static text, first appearances, and local links')
    if baseline:
        print('PASS: chapter text preserved against ' + args.baseline)


if __name__ == '__main__':
    main()

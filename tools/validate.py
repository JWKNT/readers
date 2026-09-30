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
from editorial import restore
from import_earths_past import norm, searchable, validate_exclusions
from rebuild_annotations import Fragment
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]

class Inspect(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.text, self.ids, self.annotations, self.links = [], [], [], []
        self.annotation_attrs = []
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
            self.annotation_attrs.append(attrs)
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
    baseline_names = set(baseline.getnames()) if baseline else set()
    for book in (ROOT / name for name in sorted(library)):
        manifest = json.loads((book / 'manifest.json').read_text())
        glossary = json.loads((book / 'glossary.json').read_text())
        validate_exclusions(glossary, manifest['chapters'])
        search_records = json.loads((book / 'search.json').read_text())
        assert [row['id'] for row in search_records] == [c['id'] for c in manifest['chapters']], (book, 'search chapter order')
        search = {row['id']: row for row in search_records}
        terms = {entry['id']: entry for entry in glossary}
        assert len(terms) == len(glossary), (book, 'duplicate glossary IDs')
        assert manifest['glossaryCount'] == library[book.name]['glossaryCount'] == len(glossary)
        counts, first_flags, first = Counter(), Counter(), {}
        chapter_ids = {c['id']: set(c['blocks']) for c in manifest['chapters']}
        for c in manifest['chapters']:
            if 'headingHtml' in c: chapter_ids[c['id']].add('chapter-title')
        integrity_path = ROOT / 'data' / 'earths-past' / (book.name + '-integrity.json')
        if not integrity_path.exists(): integrity_path = ROOT / 'data' / 'wolfe-fiction' / (book.name + '-integrity.json')
        if not integrity_path.exists(): integrity_path = ROOT / 'data' / 'hyperion' / (book.name + '-integrity.json')
        integrity = {c['chapter']: c for c in json.loads(integrity_path.read_text())['chapters']} if integrity_path.exists() else {}
        running_words=0
        for chapter in manifest['chapters']:
            path = book / 'chapters' / (chapter['id'] + '.json')
            data = json.loads(path.read_text())
            assert data['startWords']==chapter['startWords']==running_words,(path,'word offset')
            assert data['words']==chapter['words'],(path,'word metadata')
            if data['kind']!='reference':running_words+=data['words']
            current = Inspect(data['html'])
            tree = Fragment(data['html']).root
            for entry in glossary:
                for row in entry.get('excludeMatches', []):
                    if row['chapter'] != chapter['id']:
                        continue
                    blocks = [e for e in tree.iter() if e.get('data-block') == row['paragraph']]
                    if row['paragraph'] == 'chapter-title':
                        blocks = [Fragment(data.get('headingHtml', data['title'])).root]
                    assert len(blocks) == 1, (path, entry['id'], 'exclusion paragraph')
                    value = ''.join(blocks[0].itertext())
                    assert value.count(row['context']) == 1, (path, entry['id'], 'exclusion context')
                    assert not any(e.get('data-term') == entry['id'] and ''.join(e.itertext()) == row['text'] for e in blocks[0].iter()), (path, entry['id'], 'excluded alias still annotated')
            searchable_blocks = {e.get('data-block'): norm(searchable(e)) for e in tree.iter()
                                 if e.get('data-block') and not any(x.get('data-block') for x in list(e.iter())[1:])}
            rows = search[chapter['id']]['paragraphs']
            if any(row['id'] == 'chapter-title' for row in rows):
                searchable_blocks['chapter-title'] = data['title']
            assert len(rows) == len(searchable_blocks), (path, 'search paragraph count')
            assert {row['id']: row['text'] for row in rows} == searchable_blocks, (path, 'search text or addresses')
            if integrity:
                import hashlib
                normalized = ' '.join(''.join(current.text).split())
                assert hashlib.sha256(normalized.encode()).hexdigest() == integrity[chapter['id']]['textSha256'], (path, 'source text integrity')
            for route in re.findall(r'data-route="([^"]+)"', data['html']):
                parts = route.split('/', 1)
                assert parts[0] in chapter_ids, (path, 'unknown note chapter', route)
                assert len(parts) == 1 or parts[1] in chapter_ids[parts[0]], (path, 'unknown note paragraph', route)
            static = Inspect(article(path.with_suffix('.html').read_text()))
            heading = Inspect('<h1 id="chapter-title" data-block="chapter-title">'+data.get('headingHtml','')+'</h1>')
            static_heading = Inspect('')
            if 'headingHtml' in data:
                assert ''.join(heading.text) == data['title'], (path,'heading text changed')
                source_heading = re.search(r'<h1 id="chapter-title">(.*?)</h1>',path.with_suffix('.html').read_text(),re.S)[1]
                static_heading=Inspect('<h1 id="chapter-title" data-block="chapter-title">'+source_heading+'</h1>')
                assert heading.annotations==static_heading.annotations,(path,'static heading annotations')
                assert ''.join(heading.text)==''.join(static_heading.text),(path,'static heading text')
                assert [{'term':t,'paragraph':p} for t,p,f,local in heading.annotations if local=='true']==data['headingNoteAnchors'],(path,'heading anchors')
            assert ''.join(current.text) == ''.join(static.text), (path, 'static text mismatch')
            assert current.ids == static.ids == data['blocks'], (path, 'paragraph mismatch')
            assert current.annotations == static.annotations, (path, 'static annotations mismatch')
            for attrs in static_heading.annotation_attrs + static.annotation_attrs:
                if attrs.get('data-first') == 'true':
                    entry = terms[attrs['data-term']]
                    assert attrs.get('title') == entry['note'], (path, entry['id'], 'static definition')
                    assert attrs.get('href') == entry['sources'][0]['url'], (path, entry['id'], 'static source')
            assert len(current.ids) == len(set(current.ids)), (path, 'duplicate paragraph IDs')
            anchors = [{'term': t, 'paragraph': p} for t, p, f, local in current.annotations if local == 'true']
            assert anchors == data['noteAnchors'] == chapter['noteAnchors'], (path, 'anchor mismatch')
            if baseline and str(path.relative_to(ROOT)) in baseline_names:
                old = json.loads(baseline.extractfile(str(path.relative_to(ROOT))).read())
                previous = Inspect(old['html'])
                original=Inspect(restore(data['html']))
                old_original=Inspect(restore(old['html']))
                assert ' '.join(''.join(original.text).split()) == ' '.join(''.join(old_original.text).split()), (path, 'unrecorded text changed')
                for key in ('blocks', 'id'):
                    assert data[key] == old[key], (path, key)
                count_words=lambda value:len(re.findall(r"\b[\w’'-]+\b",value))
                expected_words=old['words']+count_words(''.join(current.text))-count_words(''.join(previous.text))
                assert data['words']==expected_words,(path,'word-count delta')
            for term, paragraph, flag, local in heading.annotations + current.annotations:
                assert term in terms, (path, term)
                counts[term] += 1
                first.setdefault(term, {'chapter': chapter['id'], 'paragraph': paragraph, 'index': chapter['index']})
                first_flags[term] += flag == 'true'
        assert running_words==manifest['totalWords']==library[book.name]['totalWords'],(book,'total words')
        for entry in glossary:
            tid = entry['id']
            assert counts[tid] == entry['occurrences'], (book, tid, 'count')
            assert first[tid] == entry['first'], (book, tid, 'first location')
            assert first_flags[tid] == 1, (book, tid, 'first flag')
            assert entry['note'].strip() and entry['short'].strip()
            assert entry['sources'], (book, tid, 'missing external source')
            if entry.get('possible'):
                assert all(entry[k].startswith('Possibly') for k in ('short', 'note')), (book, tid, 'uncertainty qualifier')
            for key in ('short', 'note'):
                # Nero Wolfe is Rex Stout's external literary character, not
                # commentary about Gene Wolfe's intentions.
                assert not re.search(r'(?<!Nero )\b(?:Wolfe|the story|in these books)\b', entry[key], re.I), (book, tid, 'editorial framing')
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
    print('PASS: glossary metadata, paragraph IDs, static/search text, first appearances, and local links')
    if baseline:
        print('PASS: original chapter wording and paragraph IDs preserved against ' + args.baseline + '; only recorded repairs and whitespace changed')


if __name__ == '__main__':
    main()

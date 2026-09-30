"""Rebuild non-Solar-Cycle marginal notes from committed chapter text.

The EPUB importers establish source text and stable addresses. This maintenance
command changes annotations only, so adding notes does not require those EPUBs.
Usage: python3 tools/rebuild_annotations.py [reader-id ...]
Run tools/validate.py --baseline <previous-commit> afterward.
"""
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
import re
import xml.etree.ElementTree as ET

import import_earths_past as common

ROOT = common.ROOT
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
        'link', 'meta', 'param', 'source', 'track', 'wbr'}


class Fragment(HTMLParser):
    """Read the importers' balanced HTML, including HTML-style void elements."""
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = ET.Element('div')
        self.stack = [self.root]
        self.feed(source)
        self.close()
        assert len(self.stack) == 1, 'unclosed HTML element'

    def handle_starttag(self, tag, attrs):
        node = ET.SubElement(self.stack[-1], tag, dict(attrs))
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        ET.SubElement(self.stack[-1], tag, dict(attrs))

    def handle_endtag(self, tag):
        if tag not in VOID:
            assert self.stack[-1].tag == tag, ('unbalanced HTML', tag)
            self.stack.pop()

    def handle_data(self, data):
        common.append_text(self.stack[-1], data)

    def handle_comment(self, data):
        self.stack[-1].append(ET.Comment(data))


def unannotate(parent):
    for child in list(parent):
        unannotate(child)
        if child.tag == 'span' and child.get('data-term') is not None:
            assert child.get('class') == 'word' and len(child) == 0
            index = list(parent).index(child)
            text = (child.text or '') + (child.tail or '')
            if index:
                previous = parent[index - 1]
                previous.tail = (previous.tail or '') + text
            else:
                parent.text = (parent.text or '') + text
            parent.remove(child)


def replace_article(page, markup):
    page, count = re.subn(r'(<article\b[^>]*>).*?(</article>)',
                         lambda match: match[1] + markup + match[2], page,
                         count=1, flags=re.S)
    assert count == 1
    return page


def build(slug):
    dest = ROOT / slug
    paths = [ROOT / 'data' / group / (slug + '.json')
             for group in ('earths-past', 'wolfe-fiction')]
    data_path = next((path for path in paths if path.exists()), None)
    assert data_path is not None, ('unsupported reader', slug)
    entries = json.loads(data_path.read_text())
    assert len({e['id'] for e in entries}) == len(entries), 'duplicate note IDs'
    manifest = json.loads((dest / 'manifest.json').read_text())
    counts, first, documents, chapters, headings = Counter(), {}, {}, {}, {}
    for record in manifest['chapters']:
        cid = record['id']
        chapter = json.loads((dest / 'chapters' / (cid + '.json')).read_text())
        chapters[cid] = chapter
        if chapter['kind'] == 'reference':
            continue  # Original notes and afterwords remain byte-identical.
        tree = Fragment(chapter['html']).root
        before = common.txt(tree)
        unannotate(tree)
        if 'headingHtml' in chapter:
            heading = ET.Element('h1', {'data-block': 'chapter-title'})
            heading.text = chapter['title']
            chapter['headingNoteAnchors'] = common.annotate(heading, entries, counts, first, chapter)
            chapter['headingHtml'] = common.inner(heading)
            headings[cid] = heading
        chapter['noteAnchors'] = common.annotate(tree, entries, counts, first, chapter)
        assert common.txt(tree) == before, (slug, cid, 'text changed')
        chapter['html'] = common.inner(tree)
        documents[cid] = tree
        for key in ('noteAnchors', 'headingHtml', 'headingNoteAnchors'):
            if key in chapter:
                record[key] = chapter[key]
    missing = [entry['id'] for entry in entries if not counts[entry['id']]]
    assert not missing, (slug, 'unmatched notes', missing)
    glossary = [dict({k: v for k, v in entry.items() if k != 'evidence'},
                     occurrences=counts[entry['id']], first=first[entry['id']])
                for entry in entries]
    for cid, tree in documents.items():
        common.save(dest / 'chapters' / (cid + '.json'), chapters[cid])
        path = dest / 'chapters' / (cid + '.html')
        page = replace_article(path.read_text(), common.inner(common.static_tree(tree, glossary)))
        if cid in headings:
            page, count = re.subn(r'(<h1 id="chapter-title">).*?(</h1>)',
                                 lambda match: match[1] + common.inner(common.static_tree(headings[cid], glossary)) + match[2],
                                 page, count=1, flags=re.S)
            assert count == 1
        path.write_text(page)
    manifest['glossaryCount'] = len(glossary)
    common.save(dest / 'manifest.json', manifest)
    common.save(dest / 'glossary.json', glossary)
    initial = manifest['defaultChapter']
    if initial in documents:
        markup = chapters[initial]['html'].replace('src="../../assets/', 'src="../assets/').replace('src="../images/', 'src="images/')
        markup = re.sub(r'href="(section-\d+|source-\d+)\.html', r'href="chapters/\1.html', markup)
        path = dest / 'index.html'
        page = replace_article(path.read_text(), markup)
        if initial in headings:
            page, count = re.subn(r'(<h1 id="chapter-title">).*?(</h1>)',
                                 lambda match: match[1] + chapters[initial]['headingHtml'] + match[2],
                                 page, count=1, flags=re.S)
            assert count == 1
        path.write_text(page)
    return len(glossary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('readers', nargs='*')
    args = parser.parse_args()
    library_path = ROOT / 'library.json'
    library = json.loads(library_path.read_text())
    allowed = {book['id'] for book in library if not book['id'].startswith('book-of-the-')}
    targets = set(args.readers) if args.readers else allowed
    assert targets <= allowed, ('unsupported readers', targets - allowed)
    for book in library:
        if book['id'] in targets:
            book['glossaryCount'] = build(book['id'])
            print(book['id'], book['glossaryCount'], 'notes')
    common.save(library_path, library)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Write the link preview tags into every Readers page.

Discord, Slack, Teams and other apps read these tags, without scripts, when someone shares a
link: a title, a description, the canonical address and the Readers card of the site theme.
The words come from each book's manifest: its title, its author and the chapter title. No text
of a book goes into a preview.

The importers write the pages, so run this after an import or a rebuild:

    python3 tools/link_previews.py

`python3 -m unittest discover -s tools -p "test_link_previews.py"` checks that every page has a complete preview.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://jehlp.net/readers/'
CARD = 'https://jehlp.net/site-theme/v2/cards/readers.png'
ORV = 'https://jehlp.net/site-theme/v2/cards/omniscient-readers-viewpoint.png'

SOCIAL = re.compile(r'\n?<meta\b[^>]*?\b(?:property|name)\s*=\s*"(?:og:|twitter:)[^"]*"[^>]*>', re.S)
CANONICAL = re.compile(r'<link\b[^>]*\brel\s*=\s*"canonical"[^>]*>')


def esc(value):
    return html.escape(str(value), quote=True)


def tags(title, description, url, image=CARD, alt='The Readers symbol'):
    pairs = [
        ('property', 'og:type', 'website'),
        ('property', 'og:site_name', 'jehlp.net'),
        ('property', 'og:title', title),
        ('property', 'og:description', description),
        ('property', 'og:url', url),
        ('property', 'og:image', image),
        ('property', 'og:image:width', 600),
        ('property', 'og:image:height', 600),
        ('property', 'og:image:alt', alt),
        ('name', 'twitter:card', 'summary'),
    ]
    return ''.join(f'<meta {kind}="{key}" content="{esc(value)}">' for kind, key, value in pairs)


def page_title(text):
    m = re.search(r'<title>([\s\S]*?)</title>', text)
    return html.unescape(m.group(1).strip()) if m else ''


def books():
    found = {}
    for manifest in ROOT.glob('*/manifest.json'):
        data = json.loads(manifest.read_text())
        if data.get('title'):
            found[manifest.parent.name] = data
    return found


def library_summary(shelf):
    """The preview of the library page: the number of books and their authors, most books first."""
    authors = {}
    for book in shelf:
        authors[book.get('author', '')] = authors.get(book.get('author', ''), 0) + 1
    names = [a for a, _ in sorted(authors.items(), key=lambda item: -item[1]) if a]
    listed = ', '.join(names[:-1]) + ' and ' + names[-1] if len(names) > 1 else (names[0] if names else 'several authors')
    return 'Readers', f'{len(shelf)} books by {listed}, to read with brief definitions in the margin.', SITE


def describe(path, text, library):
    """Return (title, description, address) for one page, or None for a page that needs none."""
    rel = path.relative_to(ROOT).as_posix()
    parts = rel.split('/')
    if rel == 'index.html':
        return library_summary(json.loads((ROOT / 'library.json').read_text()))
    book = library.get(parts[0])
    if not book:
        return None
    title, author = book['title'], book.get('author', '')
    by = f' by {author}' if author else ''
    folder = SITE + parts[0] + '/'
    if parts[1:] == ['index.html']:
        notes = ', with brief definitions in the margin' if book.get('glossaryCount') else ''
        return title, f'{title}{by}, to read in the browser{notes}.', folder
    if parts[1:] == ['contents.html']:
        return f'Contents · {title}', f'The contents of {title}{by}.', folder + 'contents.html'
    if len(parts) == 3 and parts[1] == 'chapters':
        chapter = re.sub(r'\s*·\s*Readers$', '', page_title(text)) or title
        if chapter == title:
            return title, f'The text of {title}{by}.', SITE + rel
        return f'{chapter} · {title}', f'{chapter}, from {title}{by}.', SITE + rel
    return None


def apply(text, title, description, url, image=CARD, alt='The Readers symbol'):
    end = text.index('</head>')
    head, rest = text[:end], text[end:]
    head = SOCIAL.sub('', head)
    if not re.search(r'<meta\b[^>]*name\s*=\s*"description"', head):
        head = head.replace('<title>', f'<meta name="description" content="{esc(description)}"><title>', 1)
    if not re.search(r'<meta\b[^>]*name\s*=\s*"theme-color"', head):
        head = head.replace('<title>', '<meta name="theme-color" content="#fbfaf7"><title>', 1)
    if not CANONICAL.search(head):
        head = re.sub(r'(<title>[\s\S]*?</title>)', lambda m: m.group(1) + f'<link rel="canonical" href="{esc(url)}">', head, count=1)
    m = CANONICAL.search(head)
    # A page that already names its canonical address, such as a volume of a collection, keeps it.
    url = html.unescape(re.search(r'href\s*=\s*"([^"]+)"', m.group(0)).group(1))
    return head[:m.end()] + tags(title, description, url, image, alt) + head[m.end():] + rest


def pages():
    return sorted(p for p in ROOT.rglob('*.html') if '.git' not in p.parts and 'node_modules' not in p.parts)


def main():
    library, changed = books(), 0
    for path in pages():
        text = path.read_text()
        if 'http-equiv="refresh"' in text:
            # A page that has moved: its preview names the new address and its site.
            canonical = re.search(r'rel="canonical" href="([^"]+)"', text)
            if not canonical:
                continue
            spec = (page_title(text), 'This reader has moved to its own site.', canonical.group(1), ORV if 'omniscient' in canonical.group(1) else CARD, 'The symbol of the new site')
            out = apply(text, *spec)
        else:
            spec = describe(path, text, library)
            if not spec:
                continue
            out = apply(text, *spec)
        if out != text:
            path.write_text(out)
            changed += 1
    print(f'{changed} pages updated')


if __name__ == '__main__':
    main()

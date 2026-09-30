"""Build the static catalog without touching any reader or chapter content.

All importers share this renderer. The library supplies the order and titles;
manifests supply the existing first-chapter links for multi-volume readers.
"""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTHOR_IDS = {'Gene Wolfe': 'wolfe-title', 'Cixin Liu': 'liu-title',
              'Dan Simmons': 'simmons-title'}


def render_library(root=ROOT, library=None):
    if library is None:
        library = json.loads((root / 'library.json').read_text())
    authors = list(dict.fromkeys(book['author'] for book in library))
    groups = []
    for author in authors:
        books = [book for book in library if book['author'] == author]
        heading_id = AUTHOR_IDS.get(author, '-'.join(author.lower().split()) + '-title')
        rows = []
        for book in books:
            if book.get('kind') == 'story':
                continue
            slug = book['id']
            manifest = json.loads((root / slug / 'manifest.json').read_text())
            volumes = [volume for volume in book['volumes'] if volume['chapters']]
            row = (f'<article class="book-entry">\n'
                   f'<h3><a href="{escape(slug)}/">{escape(book["title"])}</a></h3>')
            if len(volumes) > 1:
                row += '\n<ul class="volumes">'
                for volume in volumes:
                    first = next(chapter for chapter in manifest['chapters']
                                 if chapter['volume'] == volume['id'])
                    row += (f'\n<li><a href="{escape(slug)}/#{escape(first["id"])}">'
                            f'{escape(volume["title"])}</a></li>')
                row += '\n</ul>'
            rows.append(row + '\n</article>')
        stories = [book for book in books if book.get('kind') == 'story']
        if stories:
            stories_id = 'stories-title' if author == 'Gene Wolfe' else heading_id + '-stories'
            rows.append(f'<section class="short-stories" aria-labelledby="{stories_id}">\n'
                        f'<h3 id="{stories_id}">Short stories</h3>\n<ul class="story-list">\n' +
                        '\n'.join(f'<li><a href="{escape(book["id"])}/">{escape(book["title"])}</a></li>'
                                  for book in stories) + '\n</ul>\n</section>')
        groups.append(f'<section class="author-group" aria-labelledby="{heading_id}">\n'
                      f'<h2 id="{heading_id}" class="author-heading" tabindex="-1">{escape(author)}</h2>\n'
                      '<div class="author-books">\n' + '\n'.join(rows) + '\n</div>\n</section>')
    navigation = '\n'.join(
        f'<a href="#{AUTHOR_IDS.get(author, "-".join(author.lower().split()) + "-title")}">{escape(author)}</a>'
        for author in authors)
    return '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive">
<title>Readers</title>
<script src="assets/theme/theme.js"></script>
<link rel="stylesheet" href="assets/theme/base.css?v=theme-20260930-dial">
<link rel="stylesheet" href="assets/library.css?v=library-20260930">
<link rel="icon" href="assets/theme/favicons/readers.png">
<script defer src="assets/retire-offline.js"></script>
</head>
<body class="library-page">
<a class="skip-link" href="#catalog">Skip to books</a>
<header class="site-header site-header--identity library-header">
<div class="site-brand">
<img class="site-mark" src="assets/theme/marks/readers.png" width="32" height="32" alt="">
<h1 class="site-title">Readers</h1>
</div>
<nav class="author-nav" aria-label="Authors">
''' + navigation + '''
</nav>
<button class="theme-toggle" data-theme-toggle aria-label="Change theme"></button>
</header>
<main class="library" id="catalog" tabindex="-1">
''' + '\n'.join(groups) + '''
</main>
</body>
</html>
'''


def build_library(root=ROOT, library=None):
    (root / 'index.html').write_text(render_library(root, library))


if __name__ == '__main__':
    build_library()

"""Catalog generation/navigation contracts; rendered QA is recorded separately."""
from html.parser import HTMLParser
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.parse import urlsplit

from library_page import ROOT, build_library, render_library


class Catalog(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.ids, self.styles = [], [], []
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a':
            self.links.append(attrs['href'])
        if tag == 'link' and attrs.get('rel') == 'stylesheet':
            self.styles.append(attrs['href'])


class LibraryPage(unittest.TestCase):
    def setUp(self):
        self.library = json.loads((ROOT / 'library.json').read_text())
        self.page = render_library()
        self.catalog = Catalog(self.page)

    def test_committed_page_is_reproducible(self):
        self.assertEqual(self.page, (ROOT / 'index.html').read_text())
        self.assertEqual(self.page, render_library())

    def test_every_book_and_story_is_linked_once(self):
        for book in self.library:
            self.assertEqual(1, self.catalog.links.count(book['id'] + '/'), book['id'])
        self.assertEqual(73, sum(book.get('kind') == 'story' for book in self.library))
        self.assertEqual(96, sum(not urlsplit(link).scheme and not link.startswith('#') for link in self.catalog.links))

    def test_every_catalog_link_resolves(self):
        self.assertEqual(len(self.catalog.ids), len(set(self.catalog.ids)))
        for link in self.catalog.links:
            url = urlsplit(link)
            if url.scheme:
                self.assertEqual('https://jehlp.net/', link)
                continue
            if not url.path:
                self.assertIn(url.fragment, self.catalog.ids)
            else:
                self.assertTrue((ROOT / url.path / 'index.html').is_file(), link)
                if url.fragment:
                    manifest = json.loads((ROOT / url.path / 'manifest.json').read_text())
                    self.assertIn(url.fragment, [chapter['id'] for chapter in manifest['chapters']])

    def test_volume_start_addresses_are_preserved(self):
        expected = {
            'book-of-the-new-sun': ['shadow-01', 'claw-01', 'sword-01', 'citadel-01', 'urth-01'],
            'book-of-the-long-sun': ['nightside-01', 'lake-01', 'calde-01', 'exodus-01'],
            'book-of-the-short-sun': ['blue-prelude', 'green-prelude', 'return-prelude'],
            'remembrance-of-earths-past': ['three-body-problem-section-06', 'dark-forest-section-05', 'deaths-end-section-07'],
            'hyperion': ['hyperion-prologue', 'fall-epigraph'],
        }
        for slug, chapters in expected.items():
            for chapter in chapters:
                self.assertIn(slug + '/#' + chapter, self.catalog.links)

    def test_independent_masthead_and_no_javascript_catalog(self):
        headings = [(tag, attrs) for tag, attrs in self.catalog.tags if tag == 'h1']
        self.assertEqual(1, len(headings))
        self.assertNotIn('sr-only', headings[0][1].get('class', ''))
        self.assertNotIn('/', self.catalog.links)
        self.assertIn(('nav', {'class': 'author-nav', 'aria-label': 'Authors'}), self.catalog.tags)
        self.assertIn(('main', {'class': 'library', 'id': 'catalog', 'tabindex': '-1'}), self.catalog.tags)
        mark = next(attrs for tag, attrs in self.catalog.tags if tag == 'img')
        self.assertEqual('', mark['alt'])
        self.assertEqual(('32', '32'), (mark['width'], mark['height']))
        self.assertTrue((ROOT / mark['src']).is_file())
        buttons = [attrs for tag, attrs in self.catalog.tags if tag == 'button']
        self.assertEqual(1, len(buttons))
        self.assertIn('data-theme-toggle', buttons[0])

    def test_landing_styles_do_not_load_book_typography(self):
        self.assertEqual(['assets/theme/base.css?v=theme-20261001-utilities',
                          'assets/library.css?v=library-20261001-utilities'], self.catalog.styles)
        for page in ROOT.glob('*/index.html'):
            self.assertNotIn('assets/library.css', page.read_text(), str(page))

    def test_importers_use_the_shared_catalog_renderer(self):
        import import_wolfe_fiction
        import series_readers
        with patch('library_page.build_library') as build:
            import_wolfe_fiction.library_page(self.library)
            build.assert_called_once_with(import_wolfe_fiction.ROOT, self.library)
        with patch('library_page.build_library') as build:
            series_readers.library_page()
            build.assert_called_once_with(series_readers.ROOT)

    def test_mobile_catalog_header_has_explicit_two_row_placement(self):
        css = (ROOT / 'assets/library.css').read_text()
        mobile = css.split('@media (max-width: 48rem) {', 1)[1].split('@media (max-width: 34rem)', 1)[0]
        self.assertIn('.site-header.site-header--identity.library-header {\n    display: grid;', mobile)
        self.assertIn('grid-template-columns: minmax(0, 1fr) auto;', mobile)
        self.assertIn('.library-header > .site-brand { grid-column: 1; grid-row: 1; }', mobile)
        self.assertIn('.library-header > .site-utility-pair { grid-column: 2; grid-row: 1; justify-self: end; }', mobile)
        self.assertIn('.library-header nav.author-nav { grid-column: 1 / -1; grid-row: 2;', mobile)
        self.assertIn('.library-header .author-nav a { min-height: 2.75rem; }', mobile)
        self.assertNotIn('order: 3', mobile)
        # Outside the mobile breakpoint the established desktop flex layout wins.
        desktop = css.split('@media (max-width: 48rem)', 1)[0]
        self.assertNotIn('.site-header.site-header--identity.library-header', desktop)

    def test_shared_mobile_header_overrides_identity_specificity(self):
        css = (ROOT / 'assets/theme/base.css').read_text()
        mobile = css.split('@media (max-width: 42rem) {', 1)[1].split('@media (pointer: coarse)', 1)[0]
        self.assertIn('.site-header, .site-header.site-header--identity { align-items: stretch; flex-flow: column nowrap;', mobile)
        self.assertIn('.site-header nav, .site-header.site-header--identity nav { width: 100%; margin-left: 0;', mobile)
        self.assertIn('.site-header nav > a:not(.site-home)', mobile)
        self.assertIn('min-width: 2.75rem; min-height: 2.75rem;', mobile)
        self.assertIn('.site-header nav > .site-utility-pair, .site-header nav > .theme-toggle { margin-left: auto; }', mobile)


if __name__ == '__main__':
    unittest.main()

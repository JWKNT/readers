"""Native Home links survive static exports, cache refreshes and no-JS readers."""
from pathlib import Path
import re
import unittest

from import_earths_past import static_page as imported_page
from series_readers import static_page as series_page
from library_page import render_library

ROOT = Path(__file__).resolve().parents[1]
HOME = ('<nav class="site-home-dock" aria-label="Site"><a class="site-home" '
        'href="https://jehlp.net/" aria-label="Home · jehlp.net" '
        'title="Home · jehlp.net"><span aria-hidden="true">⌂</span></a></nav>')
THEME_VERSION = 'theme-20260930-home2'


class HomeNavigation(unittest.TestCase):
    def test_every_html_page_has_one_native_home(self):
        pages = list(ROOT.rglob('*.html'))
        self.assertEqual(912, len(pages))
        for page in pages:
            source = page.read_text()
            with self.subTest(page=str(page.relative_to(ROOT))):
                self.assertEqual(1, source.count(HOME))
                self.assertEqual(1, source.count('class="site-home"'))
                self.assertRegex(source, r'<body\b[^>]*>' + re.escape(HOME))

    def test_every_shared_asset_reference_has_current_cache_key(self):
        for page in ROOT.rglob('*.html'):
            source = page.read_text()
            with self.subTest(page=str(page.relative_to(ROOT))):
                refs = re.findall(r'assets/theme/(?:base\.css|theme\.js)([^"\s>]*)', source)
                self.assertTrue(refs)
                self.assertTrue(all(ref == '?v=' + THEME_VERSION for ref in refs))
                if 'assets/reader.js' in source:
                    self.assertIn('assets/reader.js?v=reader-20260930-home', source)

    def test_generated_catalog_and_static_exports_keep_native_home(self):
        pages = [render_library(), imported_page('Test', '<p>Book text</p>', ''),
                 series_page('Test', '<p>Book text</p>', '', [])]
        for source in pages:
            self.assertEqual(1, source.count(HOME))
            self.assertRegex(source, r'<body\b[^>]*>' + re.escape(HOME))
            self.assertIn('assets/theme/base.css?v=' + THEME_VERSION, source)
            self.assertIn('assets/theme/theme.js?v=' + THEME_VERSION, source)

    def test_redirect_generator_keeps_native_home(self):
        source = (ROOT / 'tools/series_readers.py').read_text()
        redirect_template = source[source.index('# Keep every old hash'):]
        self.assertIn(HOME, redirect_template)
        self.assertIn('assets/theme/base.css?v=' + THEME_VERSION, redirect_template)

    def test_numeric_edition_rebuilds_preserve_named_chrome_keys(self):
        source = (ROOT / 'book-of-the-short-sun/index.html').read_text()
        rebuilt = re.sub(r'\?v=\d+', '?v=99', source)
        for asset, version in [('theme/base.css', THEME_VERSION), ('theme/theme.js', THEME_VERSION),
                               ('reader.css', 'layout-20260930-home'), ('reader.js', 'reader-20260930-home')]:
            self.assertIn('assets/' + asset + '?v=' + version, rebuilt)
        self.assertIn('assets/initials/initials.css?v=99', rebuilt)

    def test_mobile_controls_require_enhancement_and_reuse_native_nav(self):
        css = (ROOT / 'assets/reader.css').read_text()
        js = (ROOT / 'assets/reader.js').read_text()
        self.assertIn('.mobile-tools{display:none}', css)
        self.assertIn('.reader-controls-ready .mobile-tools{position:fixed;display:flex;', css)
        self.assertIn('.mobile-tools .site-home-dock{display:contents}', css)
        self.assertIn("document.body.classList.add('reader-controls-ready')", js)
        self.assertIn("tools.insertBefore(dock,$('#search-button'))", js)
        self.assertIn('document.body.prepend(dock)', js)
        self.assertNotIn('cloneNode', js)

    def test_home_icon_and_print_clearance_are_vendored(self):
        css = (ROOT / 'assets/theme/base.css').read_text()
        self.assertTrue((ROOT / 'assets/theme/icons/home.svg').is_file())
        self.assertIn('mask: url("icons/home.svg")', css)
        self.assertIn('min-height: calc(3.5rem + env(safe-area-inset-bottom, 0px))', css)
        self.assertIn('padding: .375rem max(.75rem, env(safe-area-inset-right, 0px))', css)
        self.assertIn('min-width: 44px', css)
        self.assertIn('min-height: 44px', css)
        self.assertIn('body:has(.site-home)::after { display: none; }', css)
        self.assertIn('.site-home-dock, .site-home, .theme-toggle', css)


if __name__ == '__main__':
    unittest.main()

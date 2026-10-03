"""Native header Home links survive exports, cache refreshes and no-JS readers."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

from import_earths_past import static_page as imported_page
from series_readers import static_page as series_page
from library_page import render_library

ROOT = Path(__file__).resolve().parents[1]
HOME = ('<a class="site-home" href="https://jehlp.net/" '
        'aria-label="Home — jehlp.net" title="Home — jehlp.net">'
        '<span aria-hidden="true">✳</span></a>')
THEME_VERSION = 'theme-20260930-header-home'
STYLE_VERSION = 'theme-20261001-utilities'


class Headers(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.headers, self.spans, self.homes = [], [], []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'header':
            self.headers.append(attrs)
        if tag == 'span':
            self.spans.append(attrs)
        if tag == 'a' and attrs.get('class') == 'site-home':
            self.homes.append((self.headers[-1] if self.headers else {},
                               any(span.get('class') == 'site-utility-pair' for span in self.spans)))

    def handle_endtag(self, tag):
        if tag == 'header' and self.headers:
            self.headers.pop()
        if tag == 'span' and self.spans:
            self.spans.pop()


class HomeNavigation(unittest.TestCase):
    def test_every_html_page_has_one_native_header_home(self):
        pages = list(ROOT.rglob('*.html'))
        self.assertEqual(912, len(pages))
        aliases = 0
        for page in pages:
            source = page.read_text()
            with self.subTest(page=str(page.relative_to(ROOT))):
                self.assertEqual(1, source.count(HOME))
                self.assertEqual(1, source.count('class="site-home"'))
                self.assertNotIn('site-home-dock', source)
                homes = Headers(source).homes
                self.assertEqual(1, len(homes))
                header, paired = homes[0]
                classes = header.get('class', '').split()
                self.assertTrue(set(classes) & {'appearance', 'static-header', 'library-header', 'site-utilities'})
                if 'site-utilities' in classes:
                    aliases += 1
                    self.assertIn('data-theme-toggle-slot', header)
                else:
                    self.assertTrue(paired)
                    self.assertIn('<span class="site-utility-pair">' + HOME + '<button', source)
        self.assertEqual(3, aliases)

    def test_every_shared_asset_reference_has_current_cache_key(self):
        for page in ROOT.rglob('*.html'):
            source = page.read_text()
            with self.subTest(page=str(page.relative_to(ROOT))):
                refs = re.findall(r'assets/theme/(base\.css|theme\.js)([^"\s>]*)', source)
                self.assertTrue(refs)
                for asset, ref in refs:
                    version = STYLE_VERSION if asset == 'base.css' else THEME_VERSION
                    if page == ROOT / 'index.html' or asset == 'theme.js':
                        self.assertEqual('?v=' + version, ref)
                    else:
                        self.assertIn(ref, ('?v=' + STYLE_VERSION, '?v=' + THEME_VERSION))
                if 'assets/reader.js' in source:
                    self.assertIn('assets/reader.js?v=reader-20261003-controls', source)

    def test_generated_catalog_and_static_exports_keep_native_header_home(self):
        pages = [render_library(), imported_page('Test', '<p>Book text</p>', ''),
                 series_page('Test', '<p>Book text</p>', '', [])]
        for index, source in enumerate(pages):
            self.assertEqual(1, source.count(HOME))
            self.assertIn('<span class="site-utility-pair">' + HOME + '<button', source)
            self.assertTrue(Headers(source).homes[0][1])
            version = STYLE_VERSION
            self.assertIn('assets/theme/base.css?v=' + version, source)
            self.assertIn('assets/theme/theme.js?v=' + THEME_VERSION, source)

    def test_redirect_generator_keeps_in_flow_header_home(self):
        source = (ROOT / 'tools/series_readers.py').read_text()
        redirect_template = source[source.index('# Keep every old hash'):]
        self.assertIn('<header class="site-utilities" data-theme-toggle-slot>' + HOME + '</header>', redirect_template)
        self.assertIn('assets/theme/base.css?v=' + STYLE_VERSION, redirect_template)
        self.assertNotIn('site-home-dock', redirect_template)

    def test_numeric_edition_rebuilds_preserve_named_chrome_keys(self):
        source = series_page('Test', '<p>Book text</p>', '', [])
        rebuilt = re.sub(r'\?v=\d+', '?v=99', source)
        for asset, version in [('theme/base.css', STYLE_VERSION), ('theme/theme.js', THEME_VERSION),
                               ('reader.css', 'layout-20261001-utilities')]:
            self.assertIn('assets/' + asset + '?v=' + version, rebuilt)
        self.assertIn('assets/initials/initials.css?v=99', rebuilt)

    def test_mobile_toolbar_is_unchanged_and_home_stays_in_header(self):
        css = (ROOT / 'assets/reader.css').read_text()
        js = (ROOT / 'assets/reader.js').read_text()
        self.assertIn('.mobile-tools{position:fixed;display:flex;', css)
        self.assertNotIn('reader-controls-ready', css + js)
        self.assertNotIn('moveHome', js)
        self.assertNotIn('site-home', js)
        self.assertNotIn('.mobile-tools .site-home', css)
        self.assertIn('.appearance{display:flex;align-items:center;gap:.5rem;position:absolute;', css)
        self.assertIn('.static-header .site-utility-pair{position:absolute;top:0;right:0;margin-left:0}', css)
        self.assertNotIn('.static-header .theme-toggle{margin-left:auto}', css)

    def test_narrow_static_headers_wrap_in_flow_without_old_top_spacer(self):
        css = (ROOT / 'assets/reader.css').read_text()
        self.assertIn('@media(max-width:919px){.static-header{position:relative;top:auto;flex-wrap:wrap;', css)
        self.assertIn('column-gap:clamp(.75rem,2.5vw,1.5rem);row-gap:.5rem;margin-top:var(--site-frame-top,24px)', css)
        self.assertIn('.static-header+.static-reading,.static-header+.document{margin-top:2rem}', css)
        base = (ROOT / 'assets/theme/base.css').read_text()
        self.assertIn('.site-utility-pair { display: inline-flex; align-items: center; flex: none;', base)

    def test_home_icon_is_vendored_without_footer_spacing(self):
        css = (ROOT / 'assets/theme/base.css').read_text()
        self.assertTrue((ROOT / 'assets/theme/icons/home-compass.svg').is_file())
        self.assertIn('icons/home-compass.svg', css)
        self.assertNotIn('--site-home-clearance', css)
        self.assertNotIn('body:has(.site-home)::after', css)
        self.assertNotIn('.site-home-dock', css)
        self.assertIn('.site-home', css)
        home_block = css[css.index('a.site-home,'):css.index('.site-utility-pair .theme-toggle')]
        self.assertNotRegex(home_block, r'position:\s*(?:fixed|sticky)')
        self.assertIn('min-width: 44px', home_block)
        self.assertIn('min-height: 44px', home_block)
        self.assertIn('.site-home, .site-utility-pair, .site-utilities, .theme-toggle', css)


if __name__ == '__main__':
    unittest.main()

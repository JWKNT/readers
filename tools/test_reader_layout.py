"""Static regressions for page-local controls and narrow-screen drop capitals.

These assert the CSS contract, not rendered browser behavior. The release notes
record the separate browser review and native-Safari coverage limit.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / 'assets/reader.css').read_text()
STYLE_VERSION = 'layout-20260930'


class ReaderLayout(unittest.TestCase):
    def test_theme_headers_scroll_with_document(self):
        for selector in ('.appearance', '.static-header'):
            rules = re.findall(re.escape(selector) + r'\{([^}]+)\}', CSS)
            positions = [re.search(r'(?:^|;)position:([^;]+)', rule)[1]
                         for rule in rules if re.search(r'(?:^|;)position:', rule)]
            self.assertEqual(['absolute'], positions, selector)
        # The reader's deliberately persistent navigation still works.
        self.assertIn('.mobile-tools{position:fixed;', CSS)
        self.assertIn('.word-popup{position:fixed;', CSS)

    def test_mobile_initial_has_clearance_before_fourth_line(self):
        mobile = re.search(
            r'@media\(max-width:919px\)\{\.note-leaders.*?'
            r'\.chapter-body \.initial\{([^}]+)\}', CSS)[1]
        self.assertEqual('--initial-height:calc(3 * var(--book-leading) * 1em - .6em)', mobile)
        leading = float(re.search(r'--book-leading:([\d.]+)', CSS)[1])
        initial = re.search(r'\.chapter-body \.initial\{([^}]+)\}', CSS)[1]
        top = float(re.search(r'margin:([\d.]+)em', initial)[1])
        contour = float(re.search(r'shape-margin:([\d.]+)em', initial)[1])
        height = 3 * leading - .6
        # Even without margin-box clipping, leave > .2em for subpixel rounding.
        self.assertGreater(3 * leading - (height + top + contour), .2)
        self.assertIn('--initial-height:4.65em;', initial)
        self.assertIn('shape-outside:var(--initial-shape, inset(0)) content-box', initial)
        self.assertIn('width:calc(var(--initial-height)*var(--initial-ratio))', initial)

    def test_every_page_fetches_current_reader_css(self):
        count = 0
        for page in ROOT.rglob('*.html'):
            for href in re.findall(r'href=[\"\']([^\"\']*assets/reader\.css[^\"\']*)', page.read_text()):
                self.assertTrue(href.endswith('?v=' + STYLE_VERSION), str(page))
                count += 1
        self.assertGreater(count, 900)

    def test_static_export_templates_keep_css_version(self):
        for filename in ('import_earths_past.py', 'series_readers.py'):
            source = (ROOT / 'tools' / filename).read_text()
            self.assertNotIn('assets/reader.css?v={EDITION}', source)
            self.assertIn('assets/reader.css?v=' + STYLE_VERSION, source)


if __name__ == '__main__':
    unittest.main()

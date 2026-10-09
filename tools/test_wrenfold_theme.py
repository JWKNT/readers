"""Static contracts for the shared font and folio Home mark."""
from hashlib import sha256
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
THEME = ROOT / 'assets/theme'


class WrenfoldTheme(unittest.TestCase):
    def test_exact_approved_font_and_license_bundle(self):
        font = THEME / 'fonts/WrenfoldText-Regular.woff2'
        self.assertEqual('826f6c238521bfbf98d897a8f81810a78ed2d6571fec0ef86d0d51edba0212be', sha256(font.read_bytes()).hexdigest())
        for name in ('OFL-1.1.txt', 'Noto-Debian-copyright.txt', 'Wrenfold-README.txt'):
            self.assertTrue((THEME / 'fonts' / name).is_file(), name)

    def test_reading_uses_wrenfold_and_interface_keeps_original_fonts(self):
        base = (THEME / 'base.css').read_text()
        reader = (ROOT / 'assets/reader.css').read_text()
        library = (ROOT / 'assets/library.css').read_text()
        self.assertIn('font-family: "Wrenfold Text";', base)
        self.assertIn('url("fonts/WrenfoldText-Regular.woff2")', base)
        self.assertIn('--reading: "Wrenfold Text",', base)
        self.assertIn('--serif: Georgia, "Times New Roman", serif;', base)
        self.assertIn('--display: "Palatino Linotype", Palatino,', base)
        self.assertIn('--ui: var(--serif);', base)
        self.assertIn('--book-reading:var(--reading,"Wrenfold Text",', reader)
        self.assertIn('--book-serif:Georgia,"Times New Roman",serif;', reader)
        self.assertIn('var(--book-size)/var(--book-leading) var(--book-reading)', reader)
        self.assertIn('--regal:"Palatino Linotype",Palatino,', reader)
        self.assertIn('--serif: Georgia, "Times New Roman", serif;', library)
        self.assertIn('--display: "Palatino Linotype", Palatino,', library)
        self.assertIn('code, kbd, pre, samp { font-family: var(--mono); }', base)
        self.assertIn('"Noto Serif CJK JP"', base)

    def test_folio_svg_and_legacy_aliases_are_exact(self):
        for name in ('home-folio-scroll.svg', 'home-compass.svg', 'home.svg', 'home-emblem.svg'):
            self.assertEqual('ff757b439e901db80d320d5fd1422edb63525b0ff46e235ab2dd5c52b2dad55f', sha256((THEME / 'icons' / name).read_bytes()).hexdigest(), name)
        self.assertIn('icons/home-folio-scroll.svg', (THEME / 'base.css').read_text())


if __name__ == '__main__':
    unittest.main()

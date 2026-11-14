"""Every Readers page has a complete link preview.

    python3 -m unittest discover -s tools -p "test_link_previews.py"
"""
import re
import unittest

from link_previews import ROOT, pages

KEYS = ['og:type', 'og:site_name', 'og:title', 'og:description', 'og:url', 'og:image', 'og:image:alt']


class LinkPreviews(unittest.TestCase):
    def test_every_page_has_a_preview(self):
        checked = 0
        for path in pages():
            text = path.read_text()
            head = text[:text.index('</head>')]
            name = path.relative_to(ROOT).as_posix()
            for key in KEYS:
                self.assertRegex(head, rf'<meta property="{re.escape(key)}" content="[^"]+">', f'{name} {key}')
            self.assertIn('<meta name="twitter:card" content="summary">', head, name)
            url = re.search(r'property="og:url" content="([^"]+)"', head).group(1)
            self.assertEqual(url, re.search(r'rel="canonical" href="([^"]+)"', head).group(1), name)
            self.assertRegex(re.search(r'property="og:image" content="([^"]+)"', head).group(1), r'^https://jehlp\.net/site-theme/v2/cards/[a-z-]+\.png$', name)
            checked += 1
        self.assertGreater(checked, 800)


if __name__ == '__main__':
    unittest.main()

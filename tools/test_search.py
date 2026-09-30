"""Search snippets retain line boundaries without splitting inline words."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from import_earths_past import norm, searchable
from rebuild_annotations import Fragment
import rebuild_search


class SearchText(unittest.TestCase):
    def plain(self, markup):
        return norm(searchable(Fragment(markup).root))

    def test_line_break_is_word_boundary(self):
        self.assertEqual('dreamed of the city', self.plain('dreamed<br>of the city'))
        self.assertEqual('me. Dr. S:', self.plain('me.<br><strong>Dr. S:</strong>'))

    def test_inline_nodes_are_not_word_boundaries(self):
        self.assertEqual('midshipmen', self.plain('mid<span class="text-fix">s</span>hipmen'))
        self.assertEqual('Words, not spaces.', self.plain('<em>Words</em>, not <span class="word">spaces</span>.'))

    def test_nested_and_repeated_breaks(self):
        self.assertEqual('first second third', self.plain('first<em><br>second<br></em><br>third'))

    def test_rebuild_preserves_schema_ids_and_chapter_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); folder = root/'book'; (folder/'chapters').mkdir(parents=True)
            chapter = {'id':'one', 'title':'Chapter', 'html':'<p data-block="p-1">dreamed<br>of <em>a</em> city.</p>'}
            (folder/'manifest.json').write_text(json.dumps({'chapters':[{'id':'one'}]}))
            cp = folder/'chapters/one.json'; cp.write_text(json.dumps(chapter)); original = cp.read_bytes()
            record = [{'id':'one','kind':'chapter','paragraphs':[{'id':'chapter-title','text':'Chapter'},{'id':'p-1','text':'dreamedof a city.'}]}]
            sp = folder/'search.json'; sp.write_text(json.dumps(record))
            with patch.object(rebuild_search, 'ROOT', root):
                self.assertEqual(1, rebuild_search.build('book'))
                first = sp.read_bytes()
                self.assertEqual(0, rebuild_search.build('book'))
                self.assertEqual(first, sp.read_bytes())
            record[0]['paragraphs'][1]['text'] = 'dreamed of a city.'
            self.assertEqual(record, json.loads(sp.read_text()))
            self.assertEqual(original, cp.read_bytes())

    def test_stale_paragraph_fails_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); folder = root/'book'; (folder/'chapters').mkdir(parents=True)
            (folder/'manifest.json').write_text(json.dumps({'chapters':[{'id':'one'}]}))
            (folder/'chapters/one.json').write_text(json.dumps({'id':'one','title':'Chapter','html':'<p data-block="p-1">Text</p>'}))
            sp = folder/'search.json'; sp.write_text(json.dumps([{'id':'one','paragraphs':[{'id':'missing','text':'Text'}]}])); original = sp.read_bytes()
            with patch.object(rebuild_search, 'ROOT', root), self.assertRaises(AssertionError):
                rebuild_search.build('book')
            self.assertEqual(original, sp.read_bytes())


if __name__ == '__main__':
    unittest.main()

"""Focused regression tests for annotations-only maintenance."""
from collections import Counter
import unittest

import import_earths_past as common
from rebuild_annotations import Fragment, unannotate, replace_article


class RebuildAnnotationsTests(unittest.TestCase):
    def test_unwrap_preserves_exact_text_and_source_markup(self):
        source = '<p id="p-001" data-block="p-001">A &amp; <em>rare <span class="word" data-term="term">word</span> here</em>.<sup><a href="source-1.html#p-001">1</a></sup><span class="source-note">Original note</span><br><img alt="square" src="glyph.jpg"></p>'
        tree = Fragment(source).root
        before = common.txt(tree)
        unannotate(tree)
        self.assertEqual(common.txt(tree), before)
        self.assertFalse(any(e.get('data-term') for e in tree.iter()))
        self.assertEqual(tree.find('.//a').get('href'), 'source-1.html#p-001')
        self.assertEqual(tree.find('.//span').text, 'Original note')
        self.assertEqual(tree.find('.//img').get('alt'), 'square')

    def test_unwrap_adjacent_notes_keeps_tails(self):
        tree = Fragment('<p><span class="word" data-term="x">one</span> <span class="word" data-term="y">two</span>!</p>').root
        unannotate(tree)
        self.assertEqual(common.inner(tree), '<p>one two!</p>')

    def test_annotations_preserve_original_notes_and_links(self):
        tree = Fragment('<p id="p-001" data-block="p-001">tarn <a href="#note">tarn</a><span class="source-note">tarn</span><sup>tarn</sup></p>').root
        entry = {'id': 'tarn', 'term': 'tarn', 'aliases': []}
        counts, first = Counter(), {}
        anchors = common.annotate(tree, [entry], counts, first, {'id': 'story', 'index': 0})
        self.assertEqual(counts['tarn'], 1)
        self.assertEqual(anchors, [{'term': 'tarn', 'paragraph': 'p-001'}])
        self.assertEqual(first['tarn'], {'chapter': 'story', 'paragraph': 'p-001', 'index': 0})

    def test_article_replacement_preserves_surrounding_document(self):
        source = '<header>keep</header><article class="chapter-body">old</article><footer>keep</footer>'
        self.assertEqual(replace_article(source, 'new'), source.replace('>old<', '>new<'))


if __name__ == '__main__':
    unittest.main()

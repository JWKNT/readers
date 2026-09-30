"""Focused regression tests for annotations-only maintenance."""
from collections import Counter
import unittest

import import_earths_past as common
from rebuild_annotations import Fragment, unannotate, replace_article, annotate_correction_runs


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

    def test_unwrap_preserves_nested_repairs_and_interleaved_markup(self):
        source = '<p><em>Before</em> <span class="word" data-term="x">for<span class="text-fix" data-correction="fix-1" data-original="o">e</span>ver <i>and</i> more</span> after <b>end</b>.</p>'
        tree = Fragment(source).root
        before = common.txt(tree)
        repair = tree.find('.//span[@class="text-fix"]')
        italic = tree.find('.//i')
        unannotate(tree)
        self.assertEqual(common.txt(tree), before)
        self.assertEqual(common.inner(tree), source.replace('<span class="word" data-term="x">', '').replace(' more</span>', ' more'))
        self.assertIs(tree.find('.//span[@class="text-fix"]'), repair)
        self.assertIs(tree.find('.//i'), italic)
        self.assertEqual(repair.attrib, {'class': 'text-fix', 'data-correction': 'fix-1', 'data-original': 'o'})
        self.assertEqual(repair.tail, 'ver ')
        self.assertEqual(italic.tail, ' more after ')

    def test_unwrap_leading_note_keeps_initial_and_empty_repair(self):
        source = '<p data-block="p-001"><span class="word" data-term="x"><span class="initial"><span class="initial-letter">T</span><img src="t.svg" alt=""></span>he<span class="text-fix" data-correction="fix-2" data-original="!"></span></span> rest.</p>'
        tree = Fragment(source).root
        initial = tree.find('.//span[@class="initial"]')
        repair = tree.find('.//span[@class="text-fix"]')
        before = common.txt(tree)
        unannotate(tree)
        self.assertEqual(common.txt(tree), before)
        self.assertIs(tree.find('./p/span[@class="initial"]'), initial)
        self.assertEqual(initial.tail, 'he')
        self.assertIs(tree.find('./p/span[@class="text-fix"]'), repair)
        self.assertEqual(repair.get('data-original'), '!')
        self.assertEqual(repair.tail, ' rest.')
        self.assertIsNone(repair.text)
        once = common.inner(tree)
        unannotate(tree)
        self.assertEqual(common.inner(tree), once)

    def test_unwrap_nested_annotation_inside_correction_keeps_original(self):
        tree = Fragment('<p><span class="word" data-term="outer">A<span class="text-fix" data-correction="fix-3" data-original="&lt;&amp;&quot;"><span class="word" data-term="inner">B</span>C</span>D</span>E</p>').root
        before = common.txt(tree)
        unannotate(tree)
        self.assertEqual(common.txt(tree), before)
        self.assertFalse(any(e.get('data-term') for e in tree.iter()))
        repair = tree.find('./p/span')
        self.assertEqual(repair.get('data-original'), '<&"')
        self.assertEqual(repair.text, 'BC')
        self.assertEqual(repair.tail, 'DE')
        self.assertEqual(tree.find('./p').text, 'A')

    def test_annotations_preserve_original_notes_and_links(self):
        tree = Fragment('<p id="p-001" data-block="p-001">tarn <a href="#note">tarn</a><span class="source-note">tarn</span><sup>tarn</sup></p>').root
        entry = {'id': 'tarn', 'term': 'tarn', 'aliases': []}
        counts, first = Counter(), {}
        anchors = common.annotate(tree, [entry], counts, first, {'id': 'story', 'index': 0})
        self.assertEqual(counts['tarn'], 1)
        self.assertEqual(anchors, [{'term': 'tarn', 'paragraph': 'p-001'}])
        self.assertEqual(first['tarn'], {'chapter': 'story', 'paragraph': 'p-001', 'index': 0})

    def test_rebuild_keeps_a_corrected_name_annotated_and_recounts_it(self):
        from editorial import restore, text
        source='<p id="p-002" data-block="p-002"><span class="word" data-term="old-id" data-first="false">Aquin<span class="text-fix" data-correction="v16-test" data-original="u">a</span>s</span> and Aquinas.</p>'
        entries=[{'id':'aquinas','term':'Aquinas','aliases':[]}]
        tree=Fragment(source).root
        regex,_=common.matcher(entries)
        unannotate(tree,preserve=regex)
        counts,first=Counter(),{}
        common.annotate(tree,entries,counts,first,{'id':'fall-34','index':10})
        result=common.inner(tree)
        self.assertEqual(text(result),'Aquinas and Aquinas.')
        self.assertEqual(text(restore(result)),'Aquinus and Aquinas.')
        self.assertEqual(counts,{'aquinas':2})
        self.assertEqual(first['aquinas'],{'chapter':'fall-34','paragraph':'p-002','index':10})
        self.assertNotIn('old-id',result)
        self.assertEqual(result.count('data-first="true"'),1)
        unannotate(tree,preserve=regex)
        common.annotate(tree,entries,Counter(),{}, {'id':'fall-34','index':10})
        self.assertEqual(common.inner(tree),result)

    def correction_run_fixture(self, source, entries):
        from editorial import restore, text
        tree = Fragment(source).root
        visible, original = text(source), text(restore(source))
        regex, lookup = common.matcher(entries)
        unannotate(tree, preserve=regex)
        annotate_correction_runs(tree, regex, lookup)
        counts, first = Counter(), {}
        common.annotate(tree, entries, counts, first, {'id': 'test', 'index': 0})
        result = common.inner(tree)
        self.assertEqual(text(result), visible)
        self.assertEqual(text(restore(result)), original)
        unannotate(tree, preserve=regex)
        annotate_correction_runs(tree, regex, lookup)
        repeated = Counter()
        common.annotate(tree, entries, repeated, {}, {'id': 'test', 'index': 0})
        self.assertEqual(common.inner(tree), result)
        self.assertEqual(repeated, counts)
        return tree, counts, first

    def test_new_annotation_crosses_inserted_letter(self):
        source = '<p id="p-001" data-block="p-001">Very ab<span class="text-fix" data-correction="insert" data-original="">s</span>truse, indeed.</p>'
        tree, counts, first = self.correction_run_fixture(source, [{'id': 'abstruse', 'term': 'abstruse'}])
        self.assertEqual(counts, {'abstruse': 1})
        self.assertEqual(first['abstruse']['paragraph'], 'p-001')
        word = tree.find('.//span[@data-term="abstruse"]')
        self.assertEqual(common.txt(word), 'abstruse')
        self.assertEqual(word.find('span').get('data-correction'), 'insert')

    def test_new_annotation_crosses_empty_deleted_letter_repairs(self):
        source = '<p id="p-001" data-block="p-001">The Og<span class="text-fix" data-correction="name" data-original="a"></span>la<span class="text-fix" data-correction="name" data-original="l"></span>la Sioux and others.</p>'
        tree, counts, _ = self.correction_run_fixture(source, [{'id': 'oglala', 'term': 'Oglala Sioux'}])
        self.assertEqual(counts, {'oglala': 1})
        self.assertEqual(len(tree.findall('.//span[@data-correction="name"]')), 2)

    def test_correction_runs_respect_notes_links_and_initials(self):
        repair = 'ab<span class="text-fix" data-original="">s</span>truse'
        source = '<p id="p-001" data-block="p-001"><a href="#note">'+repair+'</a><span class="source-note">'+repair+'</span><span class="initial">'+repair+'</span></p>'
        _, counts, _ = self.correction_run_fixture(source, [{'id': 'abstruse', 'term': 'abstruse'}])
        self.assertEqual(counts, {})

    def test_correction_runs_do_not_split_repair_or_bridge_emphasis(self):
        source = '<p id="p-001" data-block="p-001"><span class="text-fix" data-original="very ab">very abs</span>truse and ab<em>s</em>truse.</p>'
        _, counts, _ = self.correction_run_fixture(source, [{'id': 'abstruse', 'term': 'abstruse'}])
        self.assertEqual(counts, {})

    def test_multiple_correction_run_matches_keep_order_and_tails(self):
        source = '<p id="p-001" data-block="p-001">ab<span class="text-fix" data-original="">s</span>truse; ab<span class="text-fix" data-original="">s</span>truse!</p>'
        tree, counts, _ = self.correction_run_fixture(source, [{'id': 'abstruse', 'term': 'abstruse'}])
        self.assertEqual(counts, {'abstruse': 2})
        self.assertEqual(len(tree.findall('.//span[@data-first="true"]')), 1)

    def test_article_replacement_preserves_surrounding_document(self):
        source = '<header>keep</header><article class="chapter-body">old</article><footer>keep</footer>'
        self.assertEqual(replace_article(source, 'new'), source.replace('>old<', '>new<'))


if __name__ == '__main__':
    unittest.main()

"""Ambiguous aliases skip only explicit, context-guarded occurrences."""
from collections import Counter
import copy
import unittest

import import_earths_past as common
from rebuild_annotations import Fragment, unannotate


class ContextualAnnotations(unittest.TestCase):
    def entry(self):
        return {'id':'brown','term':'Charles Brown','aliases':['Brown'],
                'excludeMatches':[{'chapter':'one','paragraph':'p-1','text':'Brown',
                                   'context':'Brown robe','reason':'A color, not a surname.'}]}

    def annotate(self, source, entry=None, chapter='one'):
        tree = Fragment(source).root
        counts, first = Counter(), {}
        anchors = common.annotate(tree, [entry or self.entry()], counts, first,
                                  {'id':chapter,'index':0})
        return tree, counts, first, anchors

    def test_alias_exclusion_preserves_text_and_moves_first(self):
        source = '<p data-block="p-1">Brown robe.</p><p data-block="p-2">Brown met Charles Brown.</p>'
        tree, counts, first, anchors = self.annotate(source)
        self.assertEqual(common.txt(Fragment(source).root), common.txt(tree))
        self.assertEqual(2, counts['brown'])
        self.assertEqual({'chapter':'one','paragraph':'p-2','index':0}, first['brown'])
        self.assertEqual([{'term':'brown','paragraph':'p-2'}], anchors)
        self.assertFalse(any(e.get('data-term') for e in tree[0].iter()))

    def test_maintenance_rebuild_is_idempotent(self):
        tree, _, _, _ = self.annotate('<p data-block="p-1">Brown robe.</p><p data-block="p-2">Brown.</p>')
        once = common.inner(tree)
        unannotate(tree)
        common.annotate(tree, [self.entry()], Counter(), {}, {'id':'one','index':0})
        self.assertEqual(once, common.inner(tree))

    def test_exclusion_is_chapter_specific(self):
        _, counts, _, _ = self.annotate('<p data-block="p-1">Brown robe.</p>', chapter='two')
        self.assertEqual(1, counts['brown'])

    def test_stale_context_or_duplicate_alias_fails_before_annotation(self):
        for source in ('<p data-block="p-1">Brown coat.</p>',
                       '<p data-block="p-1">Brown robe. Brown.</p>',
                       '<p data-block="p-2">Brown robe.</p>'):
            tree = Fragment(source).root; before = common.inner(tree)
            with self.assertRaises(AssertionError):
                common.annotate(tree, [self.entry()], Counter(), {}, {'id':'one','index':0})
            self.assertEqual(before, common.inner(tree))

    def test_heading_and_body_exclusions_are_separate(self):
        heading = Fragment('<h1 data-block="chapter-title">Brown</h1>').root[0]
        counts = Counter()
        common.annotate(heading, [self.entry()], counts, {}, {'id':'one','index':0})
        self.assertEqual(1, counts['brown'])
        entry = copy.deepcopy(self.entry())
        entry['excludeMatches'][0].update(paragraph='chapter-title',context='Brown')
        heading = Fragment('<h1 data-block="chapter-title">Brown</h1>').root[0]
        counts = Counter()
        common.annotate(heading, [entry], counts, {}, {'id':'one','index':0})
        self.assertEqual(0, counts['brown'])
        _, counts, _, _ = self.annotate('<p data-block="p-1">Brown.</p>', entry)
        self.assertEqual(1, counts['brown'])

    def test_preserved_repair_exclusion_fails_without_silent_wrong_anchor(self):
        source = '<p data-block="p-1"><span class="word" data-term="brown">Br<span class="text-fix" data-original="0">o</span>wn</span> robe.</p>'
        with self.assertRaisesRegex(AssertionError, 'excluded match crosses a preserved repair'):
            self.annotate(source)

    def test_stale_exclusion_address_rejected(self):
        chapters = [{'id':'one','kind':'chapter','blocks':['p-1']},
                    {'id':'ref','kind':'reference','blocks':['p-1']}]
        common.validate_exclusions([self.entry()], chapters)
        for changes in ({'chapter':'missing'}, {'paragraph':'p-2'}, {'chapter':'ref'},
                        {'text':'robe'}, {'count':0}):
            entry = self.entry(); entry['excludeMatches'][0].update(changes)
            with self.assertRaises(AssertionError):
                common.validate_exclusions([entry], chapters)


if __name__ == '__main__':
    unittest.main()

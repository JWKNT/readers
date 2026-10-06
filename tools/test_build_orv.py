"""Check ORV alignment gates, documented source ordering, and draft exports."""
import copy
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

import build_orv as builder
from validate import Inspect, article


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False))


class OrvBuilder(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory(prefix='orv-build-test-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.data = self.root / 'data/orv'
        for directory in ('source', 'target'):
            (self.data / directory).mkdir(parents=True)
        (self.root / 'book-of-the-short-sun').mkdir()
        shutil.copy(builder.ROOT / 'book-of-the-short-sun/index.html',
                    self.root / 'book-of-the-short-sun/index.html')
        save(self.root / 'library.json', [])
        self.manifest = {'schemaVersion': 1, 'source': {'sha256': '0' * 64, 'pages': 3}, 'chapters': []}
        self.sources, self.targets = {}, {}
        for number in (1, 2, 3):
            cid = f'chapter-{number:03d}'
            rows = [dict(id='p-001', lineId=cid + ':p-001', type='prose', source='한국 이야기', pages=[number]),
                    dict(id='p-002', lineId=cid + ':p-002', type='system', source='[이야기 시작]', pages=[number]),
                    dict(id='p-003', lineId=cid + ':p-003', type='scene-break', source='* * *', pages=[number])]
            for row in rows:
                row['sourceHash'] = builder.digest(row['source'])
            canonical = json.dumps({'label': str(number), 'title': '시작',
                                    'rows': [(row['id'], row['type'], row['source']) for row in rows]},
                                   ensure_ascii=False, separators=(',', ':'))
            record = dict(id=cid, number=number, labelSource=str(number), titleSource='시작',
                          kind='chapter', volume='novel', volumeTitle='Novel',
                          pageStart=number, pageEnd=number, rowCount=len(rows), sourceHash=builder.digest(canonical))
            self.manifest['chapters'].append(record)
            self.sources[cid] = record | {'rows': rows}
            self.targets[cid] = dict(id=cid, sourceHash=record['sourceHash'], title='The Beginning', status='mt-draft',
                                    review={'alignment': True, 'accuracy': False, 'prose': False}, rows=[
                                        dict(id='p-001', text='This is a long enough narrative opening.', status='mt-draft', notes=''),
                                        dict(id='p-002', text='[The story begins.]\n[Choose <a & b>.]', status='mt-draft', notes=''),
                                        dict(id='p-003', text='* * *', status='mt-draft', notes='')])
        self.store_sources()

    def store_sources(self):
        save(self.data / 'source-manifest.json', self.manifest)
        for cid, source in self.sources.items():
            save(self.data / 'source' / (cid + '.json'), source)

    def store_target(self, cid, target=None):
        save(self.data / 'target' / (cid + '.json'), target or self.targets[cid])

    def pending(self, cid):
        target = copy.deepcopy(self.targets[cid])
        target.update(title='', status='untranslated')
        for row in target['rows']:
            row.update(text='', status='untranslated')
        return target

    def validate(self, target):
        return builder.validate_target(self.manifest['chapters'][0], self.sources['chapter-001'], target)

    def test_progressive_build_skips_partial_units_and_preserves_text(self):
        self.store_target('chapter-001')
        pending = self.pending('chapter-002')
        pending['title'] = 'The Beginning'
        pending['rows'][0] = copy.deepcopy(self.targets['chapter-002']['rows'][0])
        self.store_target('chapter-002', pending)
        self.store_target('chapter-003')
        manifest = builder.build(self.root)
        self.assertEqual(['chapter-001'], [chapter['id'] for chapter in manifest['chapters']])
        translation = manifest['translation']
        self.assertFalse(translation['complete'])
        self.assertEqual(['chapter-003'], translation['completeTargetsAwaitingEarlierChapters'])
        destination = self.root / builder.SLUG
        data = json.loads((destination / 'chapters/chapter-001.json').read_text())
        current = Inspect(data['html'])
        static = Inspect(article((destination / 'chapters/chapter-001.html').read_text()))
        self.assertEqual(''.join(current.text), ''.join(static.text))
        self.assertEqual(current.ids, static.ids)
        self.assertEqual(['p-001', 'p-002', 'p-003'], current.ids)
        self.assertIn('data-set="shadow"', data['html'])
        self.assertIn('&lt;a &amp; b&gt;', data['html'])
        index = (destination / 'index.html').read_text()
        self.assertEqual(''.join(current.text), ''.join(Inspect(article(index)).text))
        self.assertIn('Translation draft. 1 of 3 source sections are available.', index)
        self.assertNotIn('series-switch', index)
        self.assertIn(f'../assets/reader.js?v=orv-{builder.EDITION}', index)
        self.assertEqual(builder.EDITION, manifest['editionVersion'])
        search = json.loads((destination / 'search.json').read_text())[0]['paragraphs']
        self.assertEqual('[The story begins.] [Choose <a & b>.]', search[2]['text'])
        self.assertEqual([], json.loads((self.root / 'library.json').read_text()))
        self.assertFalse((destination / 'chapters/chapter-002.json').exists())
        with self.assertRaisesRegex(builder.BuildError, 'incomplete translation'):
            builder.build(self.root, require_complete=True)

    def test_complete_build_and_catalog_opt_in(self):
        for cid in self.targets:
            self.store_target(cid)
        manifest = builder.build(self.root, require_complete=True, update_library=True)
        self.assertTrue(manifest['translation']['complete'])
        self.assertEqual(1, len(json.loads((self.root / 'library.json').read_text())))
        self.assertIn('Sing Shong', (self.root / 'index.html').read_text())

    def test_local_source_qualification_keeps_prose_and_external_notes(self):
        for cid in self.targets:
            self.store_target(cid)
        local = {'id': 'local-story', 'kind': 'source-qualification', 'term': 'story',
                 'short': 'Printed source wording.', 'sourceLabel': 'Supplied Korean PDF, page 1',
                 'note': 'The source wording is preserved. Source: supplied Korean PDF, page 1.',
                 'includeChapters': ['chapter-001'], 'sources': [],
                 'evidence': {'sourceHash': 'private-fixture-hash', 'source': '한국 이야기'}}
        linked = {'id': 'linked-narrative', 'term': 'narrative', 'short': 'External fixture.',
                  'note': 'External reference fixture.', 'includeChapters': ['chapter-001'],
                  'sources': [{'url': 'https://example.invalid/fixture', 'label': 'Fixture'}]}
        save(self.data / 'annotations.json', [local, linked])
        builder.build(self.root, require_complete=True)
        destination = self.root / builder.SLUG
        glossary = json.loads((destination / 'glossary.json').read_text())
        public_local = next(item for item in glossary if item['id'] == local['id'])
        self.assertEqual([], public_local['sources'])
        self.assertEqual(local['sourceLabel'], public_local['sourceLabel'])
        self.assertNotIn('evidence', public_local)
        self.assertNotIn('private-fixture-hash', (destination / 'glossary.json').read_text())
        data = json.loads((destination / 'chapters/chapter-001.json').read_text())
        static = article((destination / 'chapters/chapter-001.html').read_text())
        self.assertEqual(''.join(Inspect(data['html']).text), ''.join(Inspect(static).text))
        self.assertIn('class="static-word"', static)
        self.assertIn('tabindex="0"', static)
        self.assertIn('aria-label="story. The source wording is preserved.', static)
        self.assertIn('href="https://example.invalid/fixture"', static)
        self.assertIn('rel="noopener noreferrer"', static)
        self.assertNotIn('data-term="local-story"', (destination / 'chapters/chapter-002.html').read_text())
        before = builder.make_tree(self.sources['chapter-001'], self.targets['chapter-001'])
        counts, first = __import__('collections').Counter(), {}
        chapter = {'id': 'chapter-001', 'index': 0, 'kind': 'chapter', 'blocks': ['p-001', 'p-002', 'p-003']}
        builder.common.annotate(before, [linked], counts, first, chapter)
        self.assertEqual(builder.common.inner(builder.common.static_tree(before, [linked])),
                         builder.common.inner(builder.static_note_tree(before, [linked])))

    def test_empty_note_sources_require_explicit_local_qualification_and_label(self):
        note = {'id': 'bad-local', 'term': 'story', 'short': 'Fixture.',
                'note': 'Source wording fixture.', 'sources': []}
        save(self.data / 'annotations.json', [note])
        with self.assertRaisesRegex(builder.BuildError, 'no external source'):
            builder.load_notes(self.data)
        note['kind'] = 'source-qualification'
        save(self.data / 'annotations.json', [note])
        with self.assertRaisesRegex(builder.BuildError, 'local source label: empty English text'):
            builder.load_notes(self.data)
        note['sourceLabel'] = '한국 원문'
        save(self.data / 'annotations.json', [note])
        with self.assertRaisesRegex(builder.BuildError, 'local source label: untranslated Korean text'):
            builder.load_notes(self.data)
        note['sourceLabel'] = 'Supplied Korean PDF, page 1'
        note['sources'] = [{'label': 'Missing URL'}]
        save(self.data / 'annotations.json', [note])
        with self.assertRaisesRegex(builder.BuildError, 'invalid source URL'):
            builder.load_notes(self.data)

    def test_wordplay_annotation_scope_preserves_other_uses_and_original_text(self):
        for cid in self.targets:
            self.store_target(cid)
        note = {'id': 'scoped-story', 'term': 'story', 'short': 'Synthetic fixture.',
                'note': 'Synthetic wordplay fixture only.', 'includeChapters': ['chapter-001'],
                'sources': [{'url': 'https://example.invalid/fixture', 'label': 'Fixture'}]}
        save(self.data / 'annotations.json', [note])
        manifest = builder.build(self.root, require_complete=True)
        destination = self.root / builder.SLUG
        glossary = json.loads((destination / 'glossary.json').read_text())
        self.assertEqual(glossary[0]['occurrences'], 1)
        self.assertEqual(glossary[0]['first']['chapter'], 'chapter-001')
        for number, record in enumerate(manifest['chapters'], 1):
            chapter = json.loads((destination / 'chapters' / f"{record['id']}.json").read_text())
            self.assertEqual('data-term="scoped-story"' in chapter['html'], number == 1)
            self.assertIn('[The story begins.]', ''.join(Inspect(chapter['html']).text))
        note['includeChapters'] = ['unknown']
        save(self.data / 'annotations.json', [note])
        with self.assertRaisesRegex(builder.BuildError, 'unknown chapter scope'):
            builder.build(self.root)

    def test_pending_target_is_valid_but_structural_errors_are_rejected(self):
        pending = self.pending('chapter-001')
        self.validate(pending)
        modifiers = {
            'missing row': lambda target: target['rows'].pop(),
            'duplicate row': lambda target: target['rows'].__setitem__(1, copy.deepcopy(target['rows'][0])),
            'reordered rows': lambda target: target['rows'].reverse(),
            'unknown row': lambda target: target['rows'][1].__setitem__('id', 'p-004'),
            'bad source hash': lambda target: target.__setitem__('sourceHash', '1' * 64),
            'invalid row text': lambda target: target['rows'][0].__setitem__('text', None),
            'invalid row status': lambda target: target['rows'][0].__setitem__('status', 'pending'),
        }
        for name, modifier in modifiers.items():
            with self.subTest(name=name):
                target = copy.deepcopy(pending)
                modifier(target)
                with self.assertRaises(builder.BuildError):
                    self.validate(target)

    def test_completed_target_rejects_missing_text_and_false_review_metadata(self):
        modifiers = {
            'empty text': lambda target: target['rows'][0].__setitem__('text', ''),
            'untranslated Korean': lambda target: target['rows'][0].__setitem__('text', 'This is 한국'),
            'alignment unchecked': lambda target: target['review'].__setitem__('alignment', False),
            'accuracy unchecked': lambda target: target.__setitem__('status', 'accuracy-reviewed'),
            'scene break changed': lambda target: target['rows'][2].__setitem__('text', '***'),
            'placeholder': lambda target: target['rows'][0].__setitem__('text', 'TODO: translate'),
            'status mismatch': lambda target: target['rows'][0].__setitem__('status', 'untranslated'),
        }
        for name, modifier in modifiers.items():
            with self.subTest(name=name):
                target = copy.deepcopy(self.targets['chapter-001'])
                modifier(target)
                with self.assertRaises(builder.BuildError):
                    self.validate(target)

    def test_source_attested_crying_emoticon_survives_the_english_gate(self):
        self.sources['chapter-001']['rows'][0]['source'] = '「현재 수정 중입니다. ㅠㅠ」'
        target = copy.deepcopy(self.targets['chapter-001'])
        target['rows'][0]['text'] = '「Currently revising. ㅠㅠ」'
        self.validate(target)
        self.assertEqual('「Currently revising. ㅠㅠ」', target['rows'][0]['text'])

        rejected = ('Currently revising. ㅠㅠ ㅠㅠ', 'Currently 수정. ㅠㅠ',
                    'Currently revising. ㅠㅠㅠ', 'Currently revising. 한국ㅠㅠ',
                    'Currently revising. ㅜㅜ', 'Currently revising. ㅠㅠ한국')
        for text in rejected:
            with self.subTest(text=text):
                target['rows'][0]['text'] = text
                with self.assertRaisesRegex(builder.BuildError, 'untranslated Korean text'):
                    self.validate(target)

        target['rows'][0]['text'] = '「Currently revising. ㅠㅠ」'
        self.sources['chapter-001']['rows'][0]['source'] = '현재 수정 중입니다.'
        with self.assertRaisesRegex(builder.BuildError, 'untranslated Korean text'):
            self.validate(target)
        self.sources['chapter-001']['rows'][0]['source'] += ' ㅠㅠㅠ'
        with self.assertRaisesRegex(builder.BuildError, 'untranslated Korean text'):
            self.validate(target)

        self.sources['chapter-001']['rows'][0]['source'] = '현재 수정 중입니다. ㅠㅠ'
        target['title'] = 'The Beginning ㅠㅠ'
        with self.assertRaisesRegex(builder.BuildError, 'title: untranslated Korean text'):
            self.validate(target)

    def prose_target(self, cid):
        target = copy.deepcopy(self.targets[cid])
        target['status'] = 'prose-reviewed'
        target['review'].update(accuracy=True, prose=True)
        for row in target['rows']:
            row['status'] = 'prose-reviewed'
        return target

    def held_accuracy_target(self):
        target = copy.deepcopy(self.targets['chapter-002'])
        target['status'] = 'accuracy-reviewed'
        target['review']['accuracy'] = True
        for row in target['rows']:
            row['status'] = 'accuracy-reviewed'
        target['title'] = '아직 검토 중'
        target['rows'][0]['text'] = 'TODO: finish reviewing'
        target['rows'][1]['text'] = '[As expected, ■■■의 ■■■······.]'
        return target

    def test_prose_prefix_skips_held_english_but_checks_eligible_targets_after_gap(self):
        self.store_target('chapter-001', self.prose_target('chapter-001'))
        held = self.held_accuracy_target()
        held['title'] = 'The Beginning'
        held['rows'][0]['text'] = 'This is a long enough narrative opening.'
        self.store_target('chapter-002', held)
        self.store_target('chapter-003', self.prose_target('chapter-003'))
        manifest = builder.build(self.root, minimum_status='prose-reviewed')
        self.assertEqual(['chapter-001'], [chapter['id'] for chapter in manifest['chapters']])
        self.assertEqual(['chapter-002', 'chapter-003'], manifest['translation']['completeTargetsAwaitingEarlierChapters'])
        destination = self.root / builder.SLUG
        self.assertFalse((destination / 'chapters/chapter-002.json').exists())
        self.assertNotIn('■■■의', (destination / 'index.html').read_text())

        published_manifest = destination / 'manifest.json'
        before = published_manifest.read_bytes()
        eligible = self.prose_target('chapter-003')
        eligible['rows'][1]['text'] = '[As expected, ■■■의 ■■■······.]'
        self.store_target('chapter-003', eligible)
        with self.assertRaisesRegex(builder.BuildError, 'chapter-003/p-002: untranslated Korean'):
            builder.build(self.root, minimum_status='prose-reviewed')
        self.assertEqual(before, published_manifest.read_bytes())

    def test_below_minimum_target_still_requires_structure_source_and_status(self):
        self.store_target('chapter-001', self.prose_target('chapter-001'))
        changes = {
            'missing row': ('target row IDs', lambda target: target['rows'].pop()),
            'bad source hash': ('target source hash mismatch', lambda target: target.__setitem__('sourceHash', '1' * 64)),
            'invalid row text': ('invalid row text', lambda target: target['rows'][0].__setitem__('text', None)),
            'invalid row status': ('invalid row status', lambda target: target['rows'][0].__setitem__('status', 'pending')),
            'false accuracy flag': ('accuracy review status mismatch', lambda target: target['review'].__setitem__('accuracy', False)),
            'status mismatch': ('chapter status does not match', lambda target: target.__setitem__('status', 'mt-draft')),
            'changed scene break': ('source scene break changed', lambda target: target['rows'][2].__setitem__('text', '***')),
        }
        for name, (message, change) in changes.items():
            with self.subTest(name=name):
                target = self.held_accuracy_target()
                change(target)
                self.store_target('chapter-002', target)
                with self.assertRaisesRegex(builder.BuildError, message):
                    builder.build(self.root, minimum_status='prose-reviewed')

    def test_target_english_remains_strict_when_it_meets_the_selected_minimum(self):
        self.store_target('chapter-001', self.prose_target('chapter-001'))
        target = self.held_accuracy_target()
        target['title'] = 'The Beginning'
        target['rows'][0]['text'] = 'This is a long enough narrative opening.'
        self.store_target('chapter-002', target)
        with self.assertRaisesRegex(builder.BuildError, 'chapter-002/p-002: untranslated Korean'):
            builder.build(self.root, minimum_status='accuracy-reviewed')

    def test_reader_verified_status_requires_prose_review(self):
        target = copy.deepcopy(self.targets['chapter-001'])
        target['status'] = 'reader-verified'
        for row in target['rows']:
            row['status'] = 'reader-verified'
        target['review'].update(accuracy=True, prose=True)
        self.validate(target)
        target['review']['prose'] = False
        with self.assertRaises(builder.BuildError):
            self.validate(target)

    def test_unknown_target_rejected_before_generated_files_change(self):
        self.store_target('chapter-001')
        builder.build(self.root)
        path = self.root / builder.SLUG / 'manifest.json'
        before = path.read_bytes()
        save(self.data / 'target/unknown.json', self.pending('chapter-002'))
        with self.assertRaisesRegex(builder.BuildError, 'unknown target chapters'):
            builder.build(self.root)
        self.assertEqual(before, path.read_bytes())

    def test_changed_source_rows_and_headings_rejected(self):
        source = self.sources['chapter-001']
        for field, value in (('source', '수정'), ('titleSource', '수정')):
            with self.subTest(field=field):
                changed = copy.deepcopy(source)
                if field == 'source':
                    changed['rows'][0]['source'] = value
                else:
                    changed[field] = value
                save(self.data / 'source/chapter-001.json', changed)
                with self.assertRaises(builder.BuildError):
                    builder.validate_sources(self.data)
        self.store_sources()

    def test_documented_numbered_reading_order_permits_pdf_page_inversion(self):
        self.manifest['chapters'][1]['pageStart'] = self.manifest['chapters'][1]['pageEnd'] = 3
        self.manifest['chapters'][2]['pageStart'] = self.manifest['chapters'][2]['pageEnd'] = 2
        for chapter in self.manifest['chapters']:
            self.sources[chapter['id']].update(pageStart=chapter['pageStart'], pageEnd=chapter['pageEnd'])
            for row in self.sources[chapter['id']]['rows']:
                row['pages'] = [chapter['pageStart']]
        self.store_sources()
        with self.assertRaisesRegex(builder.BuildError, 'no documented reading-order repair'):
            builder.validate_sources(self.data)
        self.manifest.update(readingOrderBasis='numbered-source-headings',
                             orderingRepairs=[{'reason': 'The numbered headings correct the PDF chapter order.'}])
        for index, chapter in enumerate(self.manifest['chapters']):
            chapter['readingIndex'] = index
        self.store_sources()
        manifest, _ = builder.validate_sources(self.data)
        self.assertEqual([1, 3, 2], [chapter['pageStart'] for chapter in manifest['chapters']])
        self.manifest['chapters'].reverse()
        self.store_sources()
        with self.assertRaisesRegex(builder.BuildError, 'readingIndex'):
            builder.validate_sources(self.data)

    def test_page_ranges_outside_pdf_rejected(self):
        self.manifest['chapters'][0]['pageEnd'] = 4
        self.store_sources()
        with self.assertRaisesRegex(builder.BuildError, 'page range is invalid'):
            builder.validate_sources(self.data)

    def test_supplementary_material_remains_in_source_chronology(self):
        self.manifest['chapters'][0].update(kind='reference', volume='supplementary', volumeTitle='Author’s notes')
        self.manifest['chapters'][2].update(kind='reference', volume='supplementary', volumeTitle='Author’s notes')
        for chapter in self.manifest['chapters']:
            self.sources[chapter['id']].update(kind=chapter['kind'])
            self.store_target(chapter['id'])
        self.store_sources()
        manifest = builder.build(self.root)
        self.assertEqual(['supplementary', 'novel', 'supplementary-2'], [chapter['volume'] for chapter in manifest['chapters']])
        for cid in ('chapter-001', 'chapter-003'):
            data = json.loads((self.root / builder.SLUG / 'chapters' / (cid + '.json')).read_text())
            self.assertNotIn('initial-image', data['html'])


if __name__ == '__main__':
    unittest.main()

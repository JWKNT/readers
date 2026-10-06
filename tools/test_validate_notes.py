import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from validate import Inspect, published_html, validate_static_note


class StaticNoteValidationTests(unittest.TestCase):
    def test_public_reader_links_remain_in_scope_without_revision_proofs(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            paths = ['index.html', 'reader/index.html', 'reader/chapters/chapter.html',
                     'data/revisions/render-proof/chapter.html']
            for path in paths:
                destination = root / path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text('<a href="missing.html">Missing</a>')
            observed = {str(path.relative_to(root)) for path in published_html(root, {'reader': {}})}
            self.assertEqual(observed, set(paths[:3]))

    def test_external_note_still_requires_its_exact_source(self):
        entry = {'id': 'external', 'note': 'Reference note.',
                 'sources': [{'url': 'https://example.invalid/reference'}]}
        attrs = {'title': entry['note'], 'href': entry['sources'][0]['url']}
        validate_static_note(attrs, 'a', entry, 'fixture')
        attrs['href'] = 'https://example.invalid/wrong'
        with self.assertRaisesRegex(AssertionError, 'static source'):
            validate_static_note(attrs, 'a', entry, 'fixture')

    def test_local_note_requires_a_label_and_keyboard_access_without_a_url(self):
        entry = {'id': 'local', 'kind': 'source-qualification', 'sources': [],
                 'sourceLabel': 'Supplied PDF, page 1', 'note': 'Printed wording.'}
        markup = '<span data-term="local" title="Printed wording." tabindex="0" aria-label="Word. Printed wording.">Word</span>'
        parsed = Inspect(markup)
        attrs, tag = parsed.annotation_attrs[0], parsed.annotation_tags[0]
        validate_static_note(attrs, tag, entry, 'fixture')
        for changes in [{'href': 'https://example.invalid/unwanted'}, {'tabindex': '-1'},
                        {'aria-label': 'Word.'}]:
            with self.subTest(changes=changes), self.assertRaises(AssertionError):
                validate_static_note(attrs | changes, tag, entry, 'fixture')
        with self.assertRaisesRegex(AssertionError, 'local source label'):
            validate_static_note(attrs, tag, entry | {'sourceLabel': ''}, 'fixture')
        with self.assertRaisesRegex(AssertionError, 'local note URL'):
            validate_static_note(attrs, 'a', entry, 'fixture')


if __name__ == '__main__':
    unittest.main()

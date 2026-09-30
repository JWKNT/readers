"""Preserve anthology boundaries, source text and semantic reading structures."""
import hashlib
import json
import unittest

from editorial import restore, text
from import_wolfe_fiction import ROOT
from rebuild_annotations import Fragment


def read(path): return json.loads(path.read_text())
def digest(markup): return hashlib.sha256(' '.join(text(markup).split()).encode()).hexdigest()


class StrangeTravelersIntegrity(unittest.TestCase):
    def test_distinct_stories_and_duplicates(self):
        provenance=read(ROOT/'data/wolfe-fiction/strange-travelers-catalog.json')
        catalog=read(ROOT/'data/wolfe-fiction/catalog.json')
        imported=[entry['id'] for entry in catalog if entry['source']=='strange-travelers']
        self.assertEqual(13,len(imported))
        self.assertEqual(set(provenance['newReaders']),set(imported))
        self.assertEqual(15,len(imported)+len(provenance['duplicates']))
        for duplicate in provenance['duplicates']:
            record=next(entry for entry in catalog if entry['id']==duplicate['reader'])
            self.assertEqual('best',record['source'])

    def test_source_text_recoverable_and_dropcaps_present(self):
        catalog=read(ROOT/'data/wolfe-fiction/catalog.json')
        for story in (entry for entry in catalog if entry['source']=='strange-travelers'):
            report=read(ROOT/'data/wolfe-fiction'/(story['id']+'-integrity.json'))
            self.assertEqual([],report['unmatchedGlossaryEntries'],story['id'])
            for chapter in report['chapters']:
                data=read(ROOT/story['id']/'chapters'/(chapter['chapter']+'.json'))
                self.assertEqual(chapter['sourceTextSha256'],digest(restore(data['html'])),story['id'])
                self.assertEqual(chapter['textSha256'],digest(data['html']),story['id'])
                tree=Fragment(data['html']).root
                initials=[e for e in tree.iter() if e.get('class')=='initial']
                self.assertEqual(0 if data['kind']=='reference' else 1,len(initials),story['id'])

    def test_sections_epigraph_and_source_note(self):
        useful=read(ROOT/'useful-phrases/chapters/story.json')
        self.assertEqual(['I. Show Me Something Better','II. The Three Visitors','III. The Hidden Page'],[s['title'] for s in useful['sections']])
        contents=Fragment((ROOT/'useful-phrases/contents.html').read_text()).root
        links={e.get('href') for e in contents.iter('a')}
        for section in useful['sections']:
            self.assertIn('chapters/story.html#'+section['paragraph'],links)
        planets=Fragment(read(ROOT/'no-planets-strike/chapters/story.json')['html']).root
        epigraphs=[e for e in planets.iter('p') if 'epigraph' in e.get('class','')]
        self.assertEqual(2,len(epigraphs))
        self.assertEqual(6,len(list(epigraphs[0].iter('br'))))
        self.assertIn('Hamlet',''.join(epigraphs[1].itertext()))
        self.assertFalse(any('initial'==e.get('class') for p in epigraphs for e in p.iter()))
        koshchei=read(ROOT/'the-death-of-koshchei-the-deathless/manifest.json')
        self.assertEqual([('story','chapter'),('author-note','reference')],[(c['id'],c['kind']) for c in koshchei['chapters']])
        note=read(ROOT/'the-death-of-koshchei-the-deathless/chapters/author-note.json')
        self.assertIn('The Red Fairy Book',text(note['html']))


if __name__=='__main__': unittest.main()

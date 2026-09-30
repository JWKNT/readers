"""Check the series migration against its retained source readers and EPUB hashes."""
import copy
import hashlib
import json
from pathlib import Path
import unittest

from editorial import restore, text
from series_readers import ROOT, LIU_BOOKS, LIU_ID
from rebuild_annotations import Fragment


def read(path): return json.loads(path.read_text())
def digest(markup): return hashlib.sha256(' '.join(text(markup).split()).encode()).hexdigest()


class SeriesIntegrity(unittest.TestCase):
    def test_hyperion_contents_separates_frame_chapters_and_tales(self):
        manifest=read(ROOT/'hyperion/manifest.json')
        for chapter in manifest['chapters']:
            if not chapter.get('navigationSections'):continue
            self.assertEqual('Chapter '+chapter['label'],chapter['title'])
            source=read(ROOT/'hyperion/chapters'/(chapter['id']+'.json'))
            tree=Fragment(source['html']).root
            for section in chapter['navigationSections']:
                heading=next(e for e in tree.iter('h2') if e.get('id')==section['paragraph'])
                self.assertGreater(chapter['blocks'].index(section['paragraph']),0)
                self.assertIn(section['title'].split(':')[0].upper(),''.join(heading.itertext()))
        contents=Fragment((ROOT/'hyperion/contents.html').read_text()).root
        self.assertEqual([],list(contents.iter('ol')))
        lists=[e for e in contents.iter('ul') if e.get('class')=='contents-list']
        fall=lists[1]
        parts=[e for e in fall if e.get('class')=='contents-part']
        self.assertEqual([15,15,15],[len(e.find('ul')) for e in parts])
        direct=[e.find('a').text for e in fall if e.find('a') is not None]
        self.assertEqual(['Epigraph','Epilogue','Dedication'],direct)

    def test_contents_only_links_within_each_series(self):
        for slug in (LIU_ID,'hyperion'):
            self.assertNotIn('series-switch',(ROOT/slug/'index.html').read_text(),slug)

    def test_liu_prose_paragraphs_and_notes_unchanged(self):
        dest=ROOT/LIU_ID
        manifest=read(dest/'manifest.json')
        current={c['id']:c for c in manifest['chapters']}
        notes={e['id']:e for e in read(dest/'glossary.json')}
        offset=0;all_ids=[];total=0
        for slug in LIU_BOOKS:
            source=read(ROOT/slug/'manifest.json')
            prefix=slug+'-'
            total+=source['totalWords']
            for old in source['chapters']:
                cid=prefix+old['id'];all_ids.append(cid)
                original=read(ROOT/slug/'chapters'/(old['id']+'.json'))
                derived=read(dest/'chapters'/(cid+'.json'))
                self.assertEqual(text(original['html']),text(derived['html']),cid)
                self.assertEqual(original['blocks'],derived['blocks'],cid)
                self.assertEqual(original['words'],derived['words'],cid)
                self.assertEqual(original['noteAnchors'],[a|{'term':a['term'].removeprefix(prefix)} for a in derived['noteAnchors']],cid)
                self.assertEqual(current[cid]['sourceChapter'],old['id'])
            for old in read(ROOT/slug/'glossary.json'):
                new=copy.deepcopy(notes[prefix+old['id']])
                new['id']=new['id'].removeprefix(prefix)
                new['first']['chapter']=new['first']['chapter'].removeprefix(prefix)
                new['first']['index']-=offset
                self.assertEqual(old,new,old['id'])
            for image in (ROOT/slug/'images').glob('*'):
                copied=dest/'images'/(slug+'-'+image.name)
                if copied.exists():self.assertEqual(image.read_bytes(),copied.read_bytes())
            offset+=len(source['chapters'])
        self.assertEqual(all_ids,list(current))
        self.assertEqual(total,manifest['totalWords'])

    def test_hyperion_source_text_recoverable(self):
        report=read(ROOT/'data/hyperion/hyperion-integrity.json')
        self.assertEqual(57,len(report['chapters']))
        self.assertEqual([],report['unmatchedGlossaryEntries'])
        for chapter in report['chapters']:
            data=read(ROOT/'hyperion/chapters'/(chapter['chapter']+'.json'))
            self.assertEqual(chapter['textSha256'],digest(data['html']),chapter['chapter'])
            self.assertEqual(chapter['sourceTextSha256'],digest(restore(data['html'])),chapter['chapter'])


if __name__=='__main__':unittest.main()

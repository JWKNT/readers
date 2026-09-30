import unittest
from collections import Counter
from rebuild_solar_annotations import add_new,recount,unwrap_removed,Fragment,common

class SolarMaintenanceTests(unittest.TestCase):
    def entry(self,id,term,aliases=None):return {'id':id,'term':term,'aliases':aliases or []}
    def test_retains_original_anchor_by_id_not_spelling(self):
        tree=Fragment('<p data-block="p-001"><span class="word" data-term="ash" data-first="true" data-local-first="true">ASH</span> ash Ash anchor</p>').root
        original=next(e for e in tree.iter()if e.get('data-term'))
        add_new(tree,[self.entry('anchor','anchor')]);counts=Counter();first={}
        anchors=recount(tree,{'ash','anchor'},counts,first,{'id':'c','index':0})
        self.assertIs(next(e for e in tree.iter()if e.get('data-term')),original)
        self.assertEqual(counts,{'ash':1,'anchor':1});self.assertEqual(len(anchors),2)
    def test_correction_span_is_preserved(self):
        tree=Fragment('<p data-block="p-001">ab<span data-original="" data-correction="r1">s</span>truse</p>').root
        repair=next(e for e in tree.iter()if e.get('data-original')is not None)
        add_new(tree,[self.entry('abstruse','abstruse')])
        self.assertIn(repair,list(tree.iter()));self.assertEqual(repair.attrib,{'data-original':'','data-correction':'r1'})
        self.assertEqual(common.txt(tree),'abstruse')
        self.assertEqual(sum(e.get('data-term')=='abstruse'for e in tree.iter()),1)
    def test_initial_and_source_notes_are_protected(self):
        tree=Fragment('<p data-block="p-001"><span class="initial"><span class="initial-letter">A</span></span>sh <span class="source-note">anchor</span> anchor</p>').root
        add_new(tree,[self.entry('ash','Ash'),self.entry('anchor','anchor')])
        self.assertEqual([e.get('data-term')for e in tree.iter()if e.get('data-term')],['anchor'])
    def test_removal_preserves_nested_repairs(self):
        tree=Fragment('<p data-block="p-001">A <span class="word" data-term="old">a<span data-original="x">b</span>c</span> end</p>').root
        before=common.txt(tree);repair=next(e for e in tree.iter()if e.get('data-original'))
        unwrap_removed(tree,{'old'});self.assertEqual(common.txt(tree),before);self.assertIn(repair,list(tree.iter()))
        self.assertFalse(any(e.get('data-term')for e in tree.iter()))
    def test_new_alias_can_be_first_without_losing_old_anchor(self):
        tree=Fragment('<p data-block="p-001">calot <span class="word" data-term="calotte">calotte</span></p>').root
        add_new(tree,[self.entry('calotte','calot')]);counts=Counter();first={}
        recount(tree,{'calotte'},counts,first,{'id':'c','index':1})
        words=[e for e in tree.iter()if e.get('data-term')]
        self.assertEqual([e.get('data-first')for e in words],['true','false']);self.assertEqual(counts['calotte'],2)
    def test_repeat_addition_does_not_nest_or_duplicate(self):
        tree=Fragment('<p data-block="p-001">anchor anchor</p>').root
        entries=[self.entry('anchor','anchor')];add_new(tree,entries);first=common.inner(tree);add_new(tree,entries)
        self.assertEqual(common.inner(tree),first)


class TargetedAnchorTests(unittest.TestCase):
    def rule(self):return {'paragraph':'p-001','old_id':'pampas','old_text':'pampas','replacement_id':'pampas-grass','replacement_text':'pampas grass'}
    def test_targeted_replacement_leaves_other_anchors(self):
        from rebuild_solar_annotations import apply_anchor_corrections
        tree=Fragment('<p data-block="p-001"><span class="word" data-term="pampas">pampas</span> grass</p><p data-block="p-002"><span class="word" data-term="pampas">pampas</span></p>').root
        before=common.txt(tree);apply_anchor_corrections(tree,[self.rule()]);add_new(tree,[{'id':'pampas-grass','term':'pampas grass'}])
        self.assertEqual(common.txt(tree),before)
        self.assertEqual([e.get('data-term')for e in tree.iter()if e.get('data-term')],['pampas-grass','pampas'])
        apply_anchor_corrections(tree,[self.rule()])
    def test_unrelated_phrase_in_same_paragraph_does_not_satisfy_target(self):
        from rebuild_solar_annotations import apply_anchor_corrections
        tree=Fragment('<p data-block="p-001"><span class="word" data-term="pampas">pampas</span> reeds; pampas grass</p>').root
        with self.assertRaises(AssertionError):apply_anchor_corrections(tree,[self.rule()])

    def test_stale_target_fails(self):
        from rebuild_solar_annotations import apply_anchor_corrections
        tree=Fragment('<p data-block="p-001">pampas grass</p>').root
        with self.assertRaises(AssertionError):apply_anchor_corrections(tree,[self.rule()])

class SolarBuildTests(unittest.TestCase):
    def test_unmatched_addition_fails_without_output_writes(self):
        import tempfile,json,pathlib,hashlib
        from rebuild_solar_annotations import build
        with tempfile.TemporaryDirectory() as temp:
            root=pathlib.Path(temp);slug='book-of-the-new-sun';dest=root/slug
            (dest/'chapters').mkdir(parents=True);(root/'data/solar-cycle').mkdir(parents=True)
            entry={'id':'old','term':'old','aliases':[],'short':'Old.','note':'Old.','sources':[{'url':'https://example.org/old','label':'Example'}]}
            chapter={'id':'c','index':0,'kind':'chapter','title':'Chapter','html':'<p data-block="p-001"><span class="word" data-term="old" data-first="true" data-local-first="true">old</span> present</p>','noteAnchors':[{'term':'old','paragraph':'p-001'}]}
            glossary=[dict(entry,occurrences=1,first={'chapter':'c','paragraph':'p-001','index':0})]
            common.save(dest/'glossary.json',glossary)
            common.save(dest/'manifest.json',{'defaultChapter':'c','chapters':[{'id':'c'}],'glossaryCount':1})
            common.save(dest/'chapters/c.json',chapter)
            (dest/'chapters/c.html').write_text('<article>'+chapter['html']+'</article>')
            (dest/'index.html').write_text('<article>'+chapter['html']+'</article>')
            additions=[dict(entry,id='present',term='present'),dict(entry,id='missing',term='missing')]
            common.save(root/'data/solar-cycle'/(slug+'.json'),[entry]+additions)
            hashes=lambda:{str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in dest.rglob('*')if p.is_file()}
            before=hashes()
            with self.assertRaises(AssertionError):build(slug,root)
            self.assertEqual(hashes(),before)
            common.save(root/'data/solar-cycle'/(slug+'.json'),[entry])
            self.assertEqual(build(slug,root),1)
            self.assertEqual(hashes(),before)

class SolarFailureAtomicityTests(unittest.TestCase):
    def fixture(self,root,body,rules=None,static=True):
        import json
        slug='book-of-the-long-sun';dest=root/slug
        (dest/'chapters').mkdir(parents=True);(root/'data/solar-cycle').mkdir(parents=True)
        old={'id':'pampa','term':'pampas','short':'Grassland.','note':'Grassland.','sources':[{'url':'https://example.org/pampa','label':'Example'}]}
        new=dict(old,id='pampas-grass',term='pampas grass')
        common.save(root/'data/solar-cycle'/(slug+'.json'),[old,new])
        common.save(dest/'glossary.json',[old])
        common.save(dest/'manifest.json',{'chapters':[{'id':'c'}],'defaultChapter':'c','glossaryCount':1})
        common.save(dest/'chapters/c.json',{'id':'c','index':0,'kind':'chapter','html':body,'noteAnchors':[]})
        if static:(dest/'chapters/c.html').write_text('<article>old</article>')
        (dest/'index.html').write_text('<article>old</article>')
        if rules:common.save(root/'data/solar-cycle/anchor-corrections.json',{slug:rules})
        return slug,dest
    def hashes(self,root):
        import hashlib
        return {str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in root.rglob('*')if p.is_file()}
    def test_replacement_in_wrong_paragraph_fails_before_writes(self):
        import tempfile,pathlib
        from rebuild_solar_annotations import build
        with tempfile.TemporaryDirectory()as temp:
            root=pathlib.Path(temp)
            body='<p data-block="p-001"><span class="word" data-term="pampa">pampas</span> reeds</p><p data-block="p-002">pampas grass</p><p data-block="p-003"><span class="word" data-term="pampa">pampas</span></p>'
            rule={'chapter':'c','paragraph':'p-001','old_id':'pampa','old_text':'pampas','replacement_id':'pampas-grass','replacement_text':'pampas grass'}
            slug,dest=self.fixture(root,body,[rule]);before=self.hashes(root)
            with self.assertRaises(AssertionError):build(slug,root)
            self.assertEqual(self.hashes(root),before)
    def test_removal_in_appendix_preserves_prose(self):
        import tempfile,pathlib,json
        from rebuild_solar_annotations import build
        with tempfile.TemporaryDirectory()as temp:
            root=pathlib.Path(temp)
            body='<p data-block="p-001"><span class="word" data-term="pampa" data-first="true" data-local-first="true">pampas</span> reeds</p>'
            slug,dest=self.fixture(root,body)
            common.save(root/'data/solar-cycle'/(slug+'.json'),[])
            chapter=json.loads((dest/'chapters/c.json').read_text());chapter['kind']='appendix'
            common.save(dest/'chapters/c.json',chapter)
            self.assertEqual(build(slug,root),0)
            after=json.loads((dest/'chapters/c.json').read_text())
            self.assertEqual(common.txt(Fragment(after['html']).root),'pampas reeds')
            self.assertNotIn('data-term',after['html'])

    def test_missing_static_fails_before_json_writes(self):
        import tempfile,pathlib
        from rebuild_solar_annotations import build
        with tempfile.TemporaryDirectory()as temp:
            root=pathlib.Path(temp)
            body='<p data-block="p-001"><span class="word" data-term="pampa">pampas</span> and pampas grass</p>'
            slug,dest=self.fixture(root,body,static=False);before=self.hashes(root)
            with self.assertRaises(FileNotFoundError):build(slug,root)
            self.assertEqual(self.hashes(root),before)

if __name__=='__main__':unittest.main()

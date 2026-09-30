"""Incremental Solar annotation maintenance; preserve established anchors by ID."""
import copy,json,re
from collections import Counter
import xml.etree.ElementTree as ET
from rebuild_annotations import Fragment,annotate_correction_runs,replace_article
import import_earths_past as common


def add_new(tree, entries):
    """Match new definitions only, never rematching an established annotation."""
    if not entries:return
    regex,lookup=common.matcher(entries)
    annotate_correction_runs(tree,regex,lookup)
    def parts(text):
        last=0;out=[]
        for m in regex.finditer(text):
            out.append(text[last:m.start()]);e=ET.Element('span',{'class':'word','data-term':lookup[m[0].lower()]['id']});e.text=m[0];out.append(e);last=m.end()
        out.append(text[last:]);return out
    def walk(e,block=None):
        block=e.get('data-block',block)
        if e.get('data-term') or e.tag in ('a','sup','script','style') or any(s in e.get('class','')for s in ('initial','source-note','source-address')):return
        children=list(e)
        if block and e.text:
            text=e.text;e.text='';index=0
            for p in parts(text):
                if isinstance(p,str):
                    if index:e[index-1].tail=(e[index-1].tail or '')+p
                    else:e.text+=p
                else:e.insert(index,p);index+=1
        for child in children:
            walk(child,block)
            if block and child.tail:
                text=child.tail;child.tail='';prev=child
                for p in parts(text):
                    if isinstance(p,str):prev.tail=(prev.tail or '')+p
                    else:e.insert(list(e).index(prev)+1,p);prev=p
    walk(tree)


def recount(tree,known,counts,first,ch):
    local=set();anchors=[]
    def walk(e,block=None):
        block=e.get('data-block',block)
        tid=e.get('data-term')
        if tid:
            assert tid in known,('unknown retained note',tid)
            assert block,('unaddressed note',tid)
            fresh=counts[tid]==0;here=tid not in local
            e.set('data-first',str(fresh).lower());e.set('data-local-first',str(here).lower())
            counts[tid]+=1
            if fresh:first[tid]={'chapter':ch['id'],'paragraph':block,'index':ch['index']}
            if here:anchors.append({'term':tid,'paragraph':block});local.add(tid)
            return
        for child in e:walk(child,block)
    walk(tree);return anchors


def unwrap_removed(parent,removed):
    for child in list(parent):
        unwrap_removed(child,removed)
        if child.get('data-term')not in removed:continue
        index=list(parent).index(child)
        if index:parent[index-1].tail=(parent[index-1].tail or '')+(child.text or '')
        else:parent.text=(parent.text or '')+(child.text or '')
        children=list(child);parent.remove(child)
        for n,node in enumerate(children):parent.insert(index+n,node)
        if children:children[-1].tail=(children[-1].tail or '')+(child.tail or '')
        elif index:parent[index-1].tail=(parent[index-1].tail or '')+(child.tail or '')
        else:parent.text=(parent.text or '')+(child.tail or '')


def text_offsets(tree):
    positions = {}
    offset = 0
    def walk(node):
        nonlocal offset
        start = offset
        offset += len(node.text or '')
        for child in node:
            walk(child)
            offset += len(child.tail or '')
        positions[node] = (start, offset)
    walk(tree)
    return positions


def apply_anchor_corrections(tree, rules):
    """Unwrap only explicitly reviewed old matches, with stale-target guards."""
    applied = []
    for rule in rules:
        blocks = [e for e in tree.iter() if e.get('data-block') == rule['paragraph']]
        assert len(blocks) == 1, ('anchor correction paragraph missing', rule)
        block = blocks[0]
        offsets = text_offsets(block)
        matches = [e for e in block.iter() if e.get('data-term') == rule['old_id']
                   and common.txt(e) == rule['old_text']]
        if not matches:
            replacements = [e for e in block.iter()
                            if e.get('data-term') == rule['replacement_id']
                            and common.txt(e) == rule['replacement_text']
                            and (rule.get('text_offset') is None or offsets[e][0] == rule['text_offset'])]
            assert len(replacements) == rule.get('count', 1), ('stale anchor correction', rule)
            continue
        assert len(matches) == rule.get('count', 1), ('ambiguous anchor correction', rule)
        starts = [offsets[e][0] for e in matches]
        for start in starts:
            assert rule.get('text_offset', start) == start, ('anchor offset changed', rule)
            assert common.txt(block)[start:start+len(rule['replacement_text'])] == rule['replacement_text'], ('anchor phrase changed', rule)
        for match in matches:
            # A temporary unique ID lets the tested unwrapping routine preserve
            # every nested repair and tail without touching sibling matches.
            match.set('data-term', '__reviewed_anchor_removal__')
        unwrap_removed(block, {'__reviewed_anchor_removal__'})
        applied.append(dict(rule, _starts=starts))
    return applied


def definition(entry):return {k:v for k,v in entry.items()if k not in ('first','occurrences','evidence')}


def build(slug,root=None):
    root=root or common.ROOT;dest=root/slug
    entries=json.loads((root/'data/solar-cycle'/(slug+'.json')).read_text())
    old=json.loads((dest/'glossary.json').read_text())
    assert len({e['id']for e in entries})==len(entries)
    rules_path=root/'data/solar-cycle/anchor-corrections.json'
    known_ids={e['id']for e in entries}
    rules=[r for r in (json.loads(rules_path.read_text()).get(slug,[]) if rules_path.exists() else []) if r['replacement_id']in known_ids]
    pending_rule=False
    for rule in rules:
        probe=json.loads((dest/'chapters'/(rule['chapter']+'.json')).read_text())
        pending_rule=bool(apply_anchor_corrections(Fragment(probe['html']).root,[rule])) or pending_rule
    if not pending_rule and [definition(e)for e in entries]==[definition(e)for e in old]:return len(old)
    oldids={e['id']for e in old};known={e['id']for e in entries};removed=oldids-known
    added=[e for e in entries if e['id']not in oldids]
    for e in entries:
        if e['id']in {r['replacement_id']for r in rules} and e not in added:added.append(e)
    oldmap={e['id']:e for e in old}
    for e in entries:
        if e['id']not in oldmap:continue
        prior=oldmap[e['id']];oldforms={prior['term'],*prior.get('aliases',[])}
        forms=[x for x in [e['term'],*e.get('aliases',[])]if x not in oldforms]
        if forms:added.append(dict(e,term=forms[0],aliases=forms[1:]))
    changed={e['id']for e in entries if e['id']in oldids and definition(e)!=definition(next(x for x in old if x['id']==e['id']))}
    manifest=json.loads((dest/'manifest.json').read_text());counts=Counter();first={};documents={};chapter_updates={}
    for record in manifest['chapters']:
        cid=record['id'];path=dest/'chapters'/(cid+'.json');ch=json.loads(path.read_text());original=copy.deepcopy(ch);tree=Fragment(ch['html']).root
        before=common.txt(tree)
        protected=lambda node:[(e.tag,dict(e.attrib),common.txt(e))for e in node.iter()if e.get('data-original')is not None or 'initial' in e.get('class','')]
        protected_before=protected(tree)
        retained_nodes=[e for e in tree.iter()if e.get('data-term')not in removed and e.get('data-term')]
        chapter_rules=[r for r in rules if r['chapter']==cid]
        applied=apply_anchor_corrections(tree,chapter_rules)
        retained_nodes=[e for e in retained_nodes if e in list(tree.iter())]
        oldnodes=[(e.get('data-term'),common.txt(e))for e in retained_nodes]
        unwrap_removed(tree,removed)
        if ch['kind']in ('chapter','prelude','epilogue') or (slug=='book-of-the-long-sun' and cid=='exodus-my-defense'):
            add_new(tree,added)
        for rule in applied:
            block=next(e for e in tree.iter()if e.get('data-block')==rule['paragraph'])
            replacements=[e for e in block.iter()if e.get('data-term')==rule['replacement_id'] and common.txt(e)==rule['replacement_text']]
            offsets=text_offsets(block)
            assert sorted(offsets[e][0]for e in replacements)==sorted(rule['_starts']), ('anchor replacement failed',rule)
        anchors=recount(tree,known,counts,first,ch)
        assert common.txt(tree)==before,(slug,cid,'text changed')
        assert protected(tree)==protected_before,(slug,cid,'repair or initial changed')
        retained=[(e.get('data-term'),common.txt(e))for e in tree.iter()if e in retained_nodes]
        assert retained==oldnodes,(slug,cid,'existing anchor changed')
        original_terms=[(e.get('data-term'),common.txt(e),e.get('data-first'),e.get('data-local-first'))for e in Fragment(original['html']).root.iter()if e.get('data-term')]
        current_terms=[(e.get('data-term'),common.txt(e),e.get('data-first'),e.get('data-local-first'))for e in tree.iter()if e.get('data-term')]
        if original_terms!=current_terms:
            ch['html']=common.inner(tree);ch['noteAnchors']=anchors;record['noteAnchors']=anchors
        static_update=bool(ch!=original or any(e.get('data-first')=='true' and e.get('data-term')in changed for e in tree.iter()))
        if ch!=original:chapter_updates[path]=ch
        if static_update:documents[cid]=(tree,ch)
    assert all(counts[e['id']]for e in entries),('unmatched', [e['id']for e in entries if not counts[e['id']]])
    glossary=[dict(definition(e),occurrences=counts[e['id']],first=first[e['id']])for e in entries]
    serialize=lambda value:json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    outputs={path:serialize(ch)for path,ch in chapter_updates.items()}
    for cid,(tree,ch)in documents.items():
        path=dest/'chapters'/(cid+'.html');outputs[path]=replace_article(path.read_text(),common.inner(common.static_tree(tree,glossary)))
    initial=manifest['defaultChapter']
    if initial in documents:
        path=dest/'index.html';tree,ch=documents[initial];markup=ch['html'].replace('src="../../assets/','src="../assets/').replace('src="../images/','src="images/')
        outputs[path]=replace_article(path.read_text(),markup)
    manifest['glossaryCount']=len(glossary)
    outputs[dest/'manifest.json']=serialize(manifest);outputs[dest/'glossary.json']=serialize(glossary)
    # Parsing, matching, exact-target checks and static rendering must all finish
    # before the first write. A bad input cannot leave half-rendered outputs.
    for path,content in outputs.items():path.write_text(content)
    return len(glossary)


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('readers',nargs='+',choices=['book-of-the-new-sun','book-of-the-long-sun','book-of-the-short-sun'])
    args=parser.parse_args()
    library_path=common.ROOT/'library.json';library=json.loads(library_path.read_text())
    for slug in args.readers:
        count=build(slug)
        for book in library:
            if book['id']==slug:book['glossaryCount']=count
        print(slug,count,'notes')
    # Preserve even the file bytes when there are no editorial changes.
    if library!=json.loads(library_path.read_text()):common.save(library_path,library)


if __name__=='__main__':main()

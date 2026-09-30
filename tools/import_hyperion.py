"""Build the two-volume Hyperion reader from the owner's supplied EPUBs.

Usage: python3 tools/import_hyperion.py --hyperion PATH --fall PATH
Only publisher packaging and chapter-heading images duplicated by navigation
are omitted. Poetry, internal headings, special punctuation and equations stay.
"""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from zipfile import ZipFile

import import_earths_past as common
from import_earths_past import tag, txt, norm, inner, append_text, save
from reader_ornaments import decorate, generate
from series_readers import write_reader, library_page

ROOT = common.ROOT
DATA = ROOT/'data/hyperion'
TALES = ('The Priest’s Tale', 'The Soldier’s Tale', 'The Poet’s Tale',
         'The Scholar’s Tale', 'The Detective’s Tale', 'The Consul’s Tale')
TALE_SUBTITLES = ('The Man Who Cried God', 'The War Lovers', 'Hyperion Cantos',
                 'The River Lethe’s Taste Is Bitter', 'The Long Good-Bye', 'Remembering Siri')
GLYPHS = {
    'L06':'double backslash', 'L05':'double slash', 'L09':'triple slash',
    'L08':'double downward chevron', 'L07':'slash',
    '001':'square root of G h-bar divided by c cubed',
    '002':'square root of G h-bar divided by c to the fifth power',
    '003':'square root of G h-bar divided by c cubed',
    '004':'square root of G h-bar divided by c to the fifth power',
}


def clean(source, archive, epigraph=False):
    name, cls = tag(source), source.get('class','')
    if name in ('script','style'): return None
    if name=='a' and not txt(source): return None  # print-page anchors
    if name=='img' and '_line' in source.get('src',''): return None
    if name=='p' and cls=='section': name='h2'
    classes=[]
    if name=='p': classes.append('prose')
    if cls: classes.append('hyp-'+cls)
    if name=='p' and cls in ('nonindent','extract','extract0'): classes.append('noindent')
    if name=='span' and cls=='small': classes.append('small-caps')
    out=ET.Element(name, {'class':' '.join(classes)} if classes else {})
    out.text=source.text
    for child in source:
        item=clean(child,archive,epigraph)
        if item is not None:
            if epigraph and item.tag=='span' and 'hyp-small' in item.get('class',''):
                append_text(out,item.text or '')
                for grand in list(item):out.append(grand)
            else:out.append(item)
        append_text(out,child.tail or '')
    if name=='img':
        filename=Path(source.get('src')).name
        code=re.search(r'_epub_(.*?)_r1',filename)[1]
        assert code in GLYPHS, ('unreviewed inline image', filename)
        dest=ROOT/'hyperion/images';dest.mkdir(parents=True,exist_ok=True)
        (dest/filename).write_bytes(archive.read('OEBPS/images/'+filename))
        out.set('src','../images/'+filename)
        out.set('alt',GLYPHS[code])
        out.set('class','hyperion-glyph '+('hyperion-formula' if code.isdigit() else 'hyperion-punctuation'))
    return out


def add_initial(tree, family):
    # Open narration, rather than quoted poetry or a source heading.
    for p in tree.iter('p'):
        if 'hyp-bl_' in p.get('class','') or len(norm(txt(p)))<24:continue
        if not re.match(r'[\s“‘"—]*[A-Z]',p.text or ''):continue
        wrapper=ET.Element('div');wrapper.append(p)
        common.initial(wrapper,family)
        return


def plans(archive, volume):
    names=archive.namelist()
    def filename(code):return next(n for n in names if '_'+code+'_' in n and n.endswith('.htm'))
    if volume=='hyperion':
        return [('hyperion-prologue','Prologue','',filename('prl'),'')]+[
            (f'hyperion-{i:02}',f'Chapter {i}',str(i),filename(f'c{i:02}'),'') for i in range(1,7)
        ]+[('hyperion-epilogue','Epilogue','',filename('epl'),''),('hyperion-dedication','Dedication','',filename('ded'),'')]
    return [('fall-epigraph','Epigraph','',filename('col2'),'')]+[(f'fall-{i:02}',f'Chapter {i}',str(i),filename(f'c{i:02}'),('Part One' if i<=15 else 'Part Two' if i<=30 else 'Part Three')) for i in range(1,46)]+[
        ('fall-epilogue','Epilogue','',filename('epl'),''),('fall-dedication','Dedication','',filename('ded'),'')]


def merged_entries():
    """Share identical referents while retaining conflicting authoring IDs safely."""
    combined=[];by_id={};maps={}
    for volume,file in [('hyperion','hyperion.json'),('fall','the-fall-of-hyperion.json')]:
        path=DATA/file
        entries=json.loads(path.read_text()) if path.exists() else []
        maps[volume]=[]
        for source in entries:
            entry=copy.deepcopy(source)
            current=by_id.get(entry['id'])
            if current and current['term'].casefold()==entry['term'].casefold():
                current['aliases']=sorted(set(current.get('aliases',[])+entry.get('aliases',[])))
                for row in entry.get('excludeMatches', []):
                    if row not in current.setdefault('excludeMatches', []):
                        current['excludeMatches'].append(row)
                maps[volume].append(current)
                continue
            if current:entry['id']=volume+'-'+entry['id']
            combined.append(entry);by_id[entry['id']]=entry;maps[volume].append(entry)
    return combined, maps


def build(paths):
    DATA.mkdir(parents=True,exist_ok=True)
    entries,_=merged_entries()
    chapters,documents,integrity=[],{},[]
    source_files={}
    for volume,path in paths.items():
        source_files[volume]=dict(file=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        with ZipFile(path) as archive:
            for cid,title,label,filename,part in plans(archive,volume):
                body=next(e for e in ET.fromstring(archive.read(filename)).iter() if tag(e)=='body')
                selected=list(body)
                epigraph=cid=='fall-epigraph'
                dedication=cid.endswith('-dedication')
                if not (epigraph or dedication):
                    assert tag(selected[0])=='h1',filename
                    selected=selected[1:]
                source_text=norm(''.join(txt(e) for e in selected))
                tree=ET.Element('div')
                for source in selected:
                    item=clean(source,archive,epigraph)
                    if item is not None:tree.append(item)
                assert norm(txt(tree))==source_text,(filename,'conversion changed source text')
                blocks=[]
                for e in tree.iter():
                    if e.tag in ('p','h2','h3') and (norm(txt(e)) or len(e)):
                        pid=f'p-{len(blocks)+1:03}';blocks.append(pid)
                        e.set('id',pid);e.set('data-block',pid)
                record=dict(id=cid,title=title,label=label,volume=volume,
                    volumeTitle='Hyperion' if volume=='hyperion' else 'The Fall of Hyperion',
                    partTitle=part,kind='reference' if dedication else 'chapter',index=len(chapters),layout='prose',blocks=blocks,
                    sections=[dict(title=norm(txt(e)),paragraph=e.get('data-block')) for e in tree.iter('h2')],
                    words=len(re.findall(r"\b[\w’'-]+\b",txt(tree))))
                record['unnumberedToc'] = True
                record['navigationSections'] = [dict(title=TALES[int(label)-1]+': '+TALE_SUBTITLES[int(label)-1],paragraph=e['paragraph']) for e in record['sections']] if label and volume=='hyperion' else []
                if not (epigraph or dedication):
                    add_initial(tree,'shadow' if volume=='hyperion' else 'urth')
                    decorate(tree,'hyperion' if volume=='hyperion' else 'the-fall-of-hyperion',tailpiece=True)
                documents[cid]=tree;chapters.append(record)
                integrity.append(dict(chapter=cid,source=volume,file=filename,sourceTextSha256=hashlib.sha256(source_text.encode()).hexdigest(),textSha256=hashlib.sha256(norm(txt(tree)).encode()).hexdigest(),blocks=len(blocks)))
    common.validate_exclusions(entries, chapters)
    counts,first=Counter(),{}
    for record in chapters:
        tree=documents[record['id']]
        record['noteAnchors']=common.annotate(tree,entries,counts,first,record) if record['kind']!='reference' else []
        record['html']=inner(tree)
        assert hashlib.sha256(norm(txt(tree)).encode()).hexdigest()==next(r['textSha256'] for r in integrity if r['chapter']==record['id'])
    glossary=[{k:v for k,v in e.items() if k!='evidence'}|dict(occurrences=counts[e['id']],first=first[e['id']]) for e in entries if counts[e['id']]]
    unmatched=[e['id'] for e in entries if not counts[e['id']]]
    book=write_reader('hyperion','Hyperion','Dan Simmons',chapters,glossary,[
        dict(id='hyperion',title='Hyperion',chapters=8,referenceTitle='Dedication'),dict(id='fall',title='The Fall of Hyperion',chapters=47,referenceTitle='Dedication')],['hyperion.css'])
    save(DATA/'hyperion-integrity.json',dict(book='hyperion',sourceFiles=source_files,chapters=integrity,unmatchedGlossaryEntries=unmatched,notePolicy='External referents only; uncertain identifications begin Possibly.'))
    library=json.loads((ROOT/'library.json').read_text());library=[b for b in library if b['id']!='hyperion']+[book]
    save(ROOT/'library.json',library)
    from editorial import apply
    apply({'hyperion'})
    library_page()
    print('Hyperion:',len(chapters),'chapters;',len(glossary),'notes;',book['totalWords'],'words; unmatched:',unmatched)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hyperion',required=True,type=Path)
    parser.add_argument('--fall',required=True,type=Path)
    args=parser.parse_args()
    generate()
    build({'hyperion':args.hyperion,'fall':args.fall})

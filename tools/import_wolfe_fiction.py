"""Build standalone readers from three supplied EPUBs; originals stay outside Git.

Usage: python3 tools/import_wolfe_fiction.py --best PATH --endangered PATH --fifth-head PATH
Catalog and researched notes live in data/wolfe-fiction. The mislabeled Island
EPUB is deliberately not an input. Anthology notes are separate reference sections.
"""
import argparse
from collections import Counter
import copy
import hashlib
import html
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from zipfile import ZipFile

import import_earths_past as common
from import_earths_past import tag, txt, norm, save, inner, append_text

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/wolfe-fiction'
EDITION = 15


def body(z, filename):
    return list(next(e for e in ET.fromstring(z.read(filename)).iter() if tag(e) == 'body'))


def trim(items):
    items = list(items)
    while items and not norm(txt(items[0])) and not any(tag(e) == 'img' for e in items[0].iter()): items.pop(0)
    while items and not norm(txt(items[-1])) and not any(tag(e) == 'img' for e in items[-1].iter()): items.pop()
    return items


def best_parts(z, filename):
    items = body(z, filename)
    heading = next(i for i,e in enumerate(items) if tag(e) == 'h2')
    afterword = next(i for i,e in enumerate(items) if norm(txt(e)) in ('AFTERWORD','AUTHOR’S NOTE'))
    end = next(i for i,e in enumerate(items) if 'OceanofPDF.com' == norm(txt(e)))
    main = trim(items[heading+1:afterword])
    note = trim(items[afterword+1:end])
    # The final decorative publisher flourish belongs to the story ending.
    return main, note


def clean(source, edition):
    """Map source semantics, not its fonts. Neutral conversion spans are unwrapped."""
    name, cls = tag(source), source.get('class', '')
    if name in ('script','style'): return None
    if name == 'a': name = 'span'  # source contents links and fictional email stay text
    if name == 'span':
        if cls in ('i','italic'): name = 'em'
        elif cls in ('b','b1'): name = 'strong'
    if name == 'i': name = 'em'
    if name == 'b': name = 'strong'
    if edition == 'best' and (name == 'big' or name == 'div' and cls in ('calibre6','calibre_9','calibre_10')):
        name = 'span'  # PDF-era drop-cap wrappers otherwise create invalid p > div
    if edition == 'endangered' and name == 'div':
        if cls in ('title-chapter','title-section'): name = 'h2'
        elif cls.startswith('p') and cls != 'p-blanc': name = 'p'
    out = ET.Element(name)
    classes = []
    if tag(source)=='a' and '@' in txt(source):classes.append('source-address')
    if name == 'p':
        classes.append('prose')
        if edition == 'best' and any(tag(e)=='big' for e in source.iter()): classes.append('source-section-opening')
        if edition == 'best':
            if cls in ('calibre_1','calibre_4','calibre_6','calibre_7'): classes.append('center')
            elif cls == 'calibre_12': classes.append('right')
            elif cls == 'calibre_13': classes.append('hanging')
            elif cls == 'calibre_2': classes.append('noindent')
            if cls in ('calibre_','calibre_4','calibre_6','calibre_7'): classes.append('source-spaced')
        elif edition == 'endangered':
            if cls == 'p': classes.append('noindent')
            if cls == 'p-d': classes.append('right')
            if cls in ('p-blocktext','p-c-br-blocktext'): classes.append('inset')
            if cls == 'p-c-br-blocktext': classes.append('center')
        elif cls == 'calibre2': classes.append('center')
    if name == 'div' and cls in ('calibre_5','p-blanc'): classes.append('source-space')
    if name == 'div' and cls in ('blocktext','author-blocktext'): classes.append('blocktext')
    if edition == 'endangered' and cls in ('author-blocktext','illustype_fullpage_image'): classes.append('center')
    if name == 'sup' or cls == 'calibre14' and edition == 'best': out.tag = 'sup'
    if cls == 'calibre7' and edition == 'endangered': out.tag = 'sub'
    if classes: out.set('class', ' '.join(classes))
    for attr in ('src','alt','colspan','rowspan'):
        if source.get(attr) is not None: out.set(attr,source.get(attr))
    out.text = (source.text or '').replace('\xa0',' ')
    for child in source:
        item = clean(child,edition)
        if item is not None:
            if item.tag == 'span' and not item.attrib:
                append_text(out,item.text or '')
                for grand in list(item): out.append(grand)
            else: out.append(item)
        append_text(out,(child.tail or '').replace('\xa0',' '))
    # Unwrapping conversion spans can join spaces to a following newline.
    out.text = re.sub(r'[ \t]+\n', '\n', out.text or '')
    for child in out:
        if child.tail: child.tail = re.sub(r'[ \t]+\n', '\n', child.tail)
    if out.tag=='div' and norm(txt(out)) and not any(e.tag in ('p','div','h2','h3','blockquote','ul','ol','table') for e in list(out.iter())[1:]):
        out.tag='p';out.set('class',out.get('class','')+' prose noindent')
        if any(e.tag=='br' for e in out):out.set('class',out.get('class','')+' verse')
    return out


def records_for(spec, archives):
    if spec['source'] == 'best':
        main,note = best_parts(archives['best'],spec['files'][0])
        return [('story',spec['title'],'chapter','best',[(spec['files'][0],main)]),
                ('author-note','Author’s note' if spec['files'][0]=='index_split_038.html' else 'Afterword','reference','best',[(spec['files'][0],note)])]
    if spec['source'] == 'endangered':
        parts = []
        for i,fn in enumerate(spec['files']):
            chapter = body(archives['endangered'],fn)[0]
            parts.append((fn,list(chapter)[1:] if i == 0 else list(chapter)))
        return [('story',spec['title'],'chapter','endangered',parts)]
    a = body(archives['fifth-head'],'index_split_000.html')
    b = body(archives['fifth-head'],'index_split_001.html')
    c = body(archives['fifth-head'],'index_split_002.html')
    # These source files divide by size, not novella. Bounds were checked against
    # headings, epigraphs and the uninterrupted final/initial narrative paragraphs.
    assert norm(txt(a[550])) == '“A STORY,”'
    assert norm(txt(b[571])) == 'V. R. T.'
    assert norm(txt(b[567])).startswith('The mist was burning away.')
    main,note = best_parts(archives['best'],'index_split_010.html')
    return [('fifth-head','The Fifth Head of Cerberus','chapter','best',[('index_split_010.html',main)]),
            ('a-story','“A Story,” by John V. Marsch','chapter','fifth-head',
             [('index_split_000.html',a[552:-1]),('index_split_001.html',b[:568])]),
            ('vrt','V. R. T.','chapter','fifth-head',
             [('index_split_001.html',b[572:-1]),('index_split_002.html',c[:-1])]),
            ('author-note','Afterword to The Fifth Head of Cerberus','reference','best',[('index_split_010.html',note)])]


def mark_epigraphs(tree, record, source, slug):
    # Epigraphs remain complete and annotatable, but do not receive drop capitals.
    if record == 'fifth-head': count = 2
    elif record == 'a-story': count = 10  # nine verse lines and attribution
    elif record == 'vrt': count = 2
    elif record == 'story' and slug == 'the-eyeflash-miracles': count = 2
    elif record == 'story' and slug in {'and-when-they-appear','the-death-of-dr-island','the-hero-as-werwolf','hour-of-trust','game-in-the-popes-head'}:
        count={'and-when-they-appear':2,'the-death-of-dr-island':9,'the-hero-as-werwolf':6,'hour-of-trust':3,'game-in-the-popes-head':4}[slug]
    elif record == 'story' and slug == 'silhouette':
        for e in list(tree.iter('p'))[:4]:e.set('class',e.get('class','')+' epigraph')
        return
    else: return
    meaningful = [e for e in tree.iter('p') if norm(txt(e))]
    for e in meaningful[:count]:
        e.set('class',e.get('class','')+' epigraph')
        if len(e) and e[0].tag=='br' and not norm(e.text or ''):
            first=e[0];e.text=(e.text or '')+(first.tail or '');e.remove(first)
        # The anthology encodes verse line endings as long runs of nonbreaking spaces.
        for x in list(e.iter()):
            if x.text and re.search(r' {4,}', x.text):
                lines = re.split(r' {4,}',x.text)
                if sum(bool(line.strip()) for line in lines)<2:
                    x.text=re.sub(r' {4,}', ' ',x.text)
                    continue
                x.text=lines[0]
                for i,line in enumerate(lines[1:]):
                    br=ET.Element('br');br.tail=' '+line;x.insert(i,br)
    for e in tree.iter():
        if e.tag=='blockquote' and all('epigraph' in p.get('class','') for p in e.iter('p') if norm(txt(p))):
            e.tag='div';e.set('class','epigraph-container' if e in tree else 'epigraph-inner')


def format_transcript(tree, slug):
    if slug != 'from-the-notebook-of-dr-stein': return
    # Retain paragraph addresses, but let each speaker turn flow at reader width.
    for p in tree.iter('p'):
        value=inner(p)
        if not any(label in txt(p) for label in ('Dr. S','DW:','Nurse Johnson:')):continue
        def reflow_break(match):
            following=value[match.end():].lstrip()
            turn=re.match(r'(?:<strong>)?(?:Dr\. (?:Stein|S)|DW)(?:</strong>)?:',following)
            return match[0] if turn else match[1]
        value=re.sub(r'<br>(\s*)', reflow_break, value)
        value=re.sub(r'(^|<br>\s*)(Dr\. Stein:|Dr\. S:|DW:)',r'\1<strong>\2</strong>',value)
        value=re.sub(r'(?<!>)(Dr\. Stein:|Dr\. S:|DW:|Nurse Johnson:)',r'<strong>\1</strong>',value)
        value=value.replace(' <strong>Nurse Johnson:</strong>',' <br><strong>Nurse Johnson:</strong>')
        parsed=ET.fromstring('<p>'+value.replace('<br>','<br/>')+'</p>')
        p.text=parsed.text
        for child in list(p):p.remove(child)
        for child in parsed:p.append(child)
        p.set('class',p.get('class','')+' transcript')


def join_source_fragments(tree, slug, chapter):
    """Reflow confirmed OCR paragraph splits while retaining each old address."""
    if slug!='the-fifth-head-of-cerberus':return
    groups={'a-story':[['p-123','p-124'],['p-127','p-128']],
            'vrt':[['p-188','p-189'],['p-401','p-402'],['p-786','p-787'],
                   ['p-034','p-035','p-036'],['p-468','p-469','p-470'],
                   ['p-489','p-490'],['p-540','p-541'],['p-584','p-585'],['p-606','p-607']]}.get(chapter,[])
    claimed={pid for group in groups for pid in group}
    children=list(tree)
    for i,e in enumerate(children[:-1]):
        if e.tag=='p' and norm(txt(e)) in ('Q:','A:') and e.get('id') not in claimed:
            following=children[i+1]
            if following.tag=='p' and following.get('id') not in claimed and norm(txt(following)) not in ('Q:','A:'):
                groups.append([e.get('id'),following.get('id')])
                claimed.update((e.get('id'),following.get('id')))
    by_id={e.get('id'):e for e in tree if e.get('id')}
    for group in groups:
        nodes=[by_id[pid] for pid in group]
        start=list(tree).index(nodes[0])
        assert list(tree)[start:start+len(nodes)]==nodes,(slug,chapter,group)
        transcript=bool(re.match(r'^[AQ]:',norm(txt(nodes[0]))))
        wrapper=ET.Element('div',{'class':'continued-passage'+(' transcript' if transcript else '')})
        for i,e in enumerate(nodes):
            tree.remove(e);e.tag='span';e.set('class',e.get('class','')+' paragraph-fragment')
            wrapper.append(e)
            if i+1<len(nodes):
                space=ET.SubElement(wrapper,'span',{'class':'text-fix','data-correction':f'layout-{chapter}-{group[0]}-{i}','data-original':''})
                space.text=' '
        tree.insert(start,wrapper)


def add_initial(tree, family):
    # Top-level narration is preferred to epigraphs; epistolary stories may begin
    # inside a blockquote. Use a temporary view containing only eligible paragraphs.
    eligible = [e for e in tree if e.tag == 'p' and 'epigraph' not in e.get('class','') and len(norm(txt(e))) >= 24]
    if not eligible:
        eligible = [e for e in tree.iter('p') if 'epigraph' not in e.get('class','') and len(norm(txt(e))) >= 24]
    if eligible:
        view=ET.Element('div');view.append(eligible[0]);common.initial(view,family)


def static_page(title,content,nav,depth=2):
    common.EDITION=EDITION
    return common.static_page(title,content,nav,depth).replace('earths-past.css','wolfe-fiction.css')


def build(spec, archives, source_info):
    from reader_ornaments import decorate
    slug,title=spec['id'],spec['title'];dest=ROOT/slug;(dest/'chapters').mkdir(parents=True,exist_ok=True)
    records=[];documents={};headings={};integrity=[];corrections=[]
    for i,(cid,ctitle,kind,source,parts) in enumerate(records_for(spec,archives)):
        tree=ET.Element('div'); raw=''
        for filename,items in parts:
            for original in items:
                raw += txt(original)
                item=clean(original,source)
                if item is not None:tree.append(item)
        assert norm(txt(tree))==norm(raw),(slug,cid,'conversion changed text')
        source_hash=hashlib.sha256(norm(raw).encode()).hexdigest()
        # Empty conversion paragraphs only contribute whitespace, but preserve it
        # in the tree so both the source hash and generated fallback stay auditable.
        for e in tree.iter('img'):
            old=e.get('src','');name=Path(old).name
            if source=='endangered' or name=='00004.jpg':
                e.tag='span';e.attrib.clear();e.set('class','scene-divider')
            else:
                (dest/'images').mkdir(exist_ok=True)
                fn=(Path(parts[0][0]).parent/old).as_posix()
                (dest/'images'/name).write_bytes(archives[source].read(fn))
                e.set('src','../images/'+name);e.set('class','source-glyph')
                e.set('alt','one third' if name=='00005.jpg' else 'square')
        mark_epigraphs(tree,cid,source,slug)
        if kind!='reference':format_transcript(tree,slug)
        if slug=='the-woman-who-loved-the-centaur-pholus':
            for e in tree.iter('p'):
                if 'inset' in e.get('class','') or any(x.tag=='br' for x in e):e.set('class',e.get('class','')+' verse')
        section_openings=[e for e in tree if 'source-section-opening' in e.get('class','')]
        for e in section_openings[1:]:
            divider=ET.Element('div');ET.SubElement(divider,'span',{'class':'scene-divider'})
            tree.insert(list(tree).index(e),divider)
        # A verified spelling repair retains the original bytes in authoring metadata.
        for e in list(tree.iter()):
            if e.text and 'C�apek' in e.text:
                before,after=e.text.split('C�apek',1);e.text=before
                repair=ET.Element('span',{'class':'text-fix','data-original':'C�apek'})
                repair.text='Čapek';repair.tail=after;e.insert(0,repair)
                corrections.append({'chapter':cid,'original':'C�apek','replacement':'Čapek','source':'https://www.britannica.com/biography/Karel-Capek'})
        blocks=[]
        for e in tree.iter():
            if e.tag in ('p','h2','h3','table') and (norm(txt(e)) or any(tag(x)=='img' for x in e.iter())):
                pid=f'p-{len(blocks)+1:03d}';blocks.append(pid);e.set('id',pid);e.set('data-block',pid)
        join_source_fragments(tree,slug,cid)
        if slug=='the-fifth-head-of-cerberus' and cid=='vrt':
            for e in tree.iter('p'):
                if re.match(r'^[AQ]:',norm(txt(e))):e.set('class',e.get('class','')+' transcript')
        verse_ids={
            'the-woman-the-unicorn-loved':{'p-005','p-038','p-150','p-185','p-196','p-215'},
            'in-the-house-of-gingerbread':{'p-150'},'silhouette':{'p-096','p-098'}
        }.get(slug,set()) if cid=='story' else set()
        for e in tree.iter('p'):
            if e.get('id') in verse_ids:e.set('class',e.get('class','')+' verse')
            if slug=='the-hero-as-werwolf' and cid=='author-note':
                if e.get('id')=='p-002':e.set('class',e.get('class','')+' verse')
                if e.get('id')=='p-003':e.set('class',e.get('class','')+' right')
            if slug=='the-woman-who-loved-the-centaur-pholus' and cid=='story' and e.get('id') in ('p-019','p-020'):
                e.set('class',e.get('class','')+' verse-line')
            if slug=='the-tree-is-my-hat' and cid=='story' and e.get('id') in ('p-061','p-063'):
                assert e[0].tag=='em'
                e[0].text=(e.text or '')+(e[0].text or '');e.text=''
            if slug=='the-death-of-dr-island' and cid=='story' and e.get('id')=='p-005':
                e.set('class',e.get('class','')+' stanza-start')
            if slug=='the-death-of-dr-island' and cid=='story' and e.get('id')=='p-687':
                for em in e.iter('em'):
                    if em.text=='Patrão.”':em.text='Patrão.';em.tail='”'+(em.tail or '')
        if slug=='the-woman-the-unicorn-loved':
            for e in tree.iter('p'):
                if e.get('id')=='p-005' and e.text and 'spares, Who' in e.text:
                    first,last=e.text.split('spares, ',1);e.text=first+'spares, '
                    line=ET.Element('br');line.tail=last;e.insert(0,line)
                    e.set('class',e.get('class','')+' verse')
        if slug=='the-detective-of-dreams' and cid=='story':
            e=next(p for p in tree.iter('p') if p.get('id')=='p-145')
            first,second=e.text.split('“You have this experience each night?”')
            e.text=first
            ET.SubElement(e,'span',{'class':'dialogue-turn'}).text='“You have this experience each night?”'+second
        sections=[{'title':norm(txt(e)),'paragraph':e.get('data-block')} for e in tree.iter('h2') if e.get('data-block')]
        r=dict(id=cid,title=ctitle,volume='sources' if kind=='reference' else 'text',volumeTitle='Supplementary material' if kind=='reference' else title,number=i+1,label=('I','II','III')[i] if spec['kind']=='book' and kind=='chapter' else '',kind=kind,index=i,layout='prose',blocks=blocks,sections=sections)
        records.append(r);documents[cid]=tree
        integrity.append(dict(chapter=cid,source=source,files=[f for f,items in parts],sourceTextSha256=source_hash,textSha256=hashlib.sha256(norm(txt(tree)).encode()).hexdigest(),blocks=len(blocks)))
        if kind!='reference':
            add_initial(tree,spec['initial'])
            decorate(tree,slug,tailpiece=not any('scene-divider' in e.get('class','') for e in tree.iter()))
    entries_path=DATA/(slug+'.json');entries=json.loads(entries_path.read_text()) if entries_path.exists() else []
    counts,first=Counter(),{}
    for r in records:
        heading=ET.Element('h1',{'data-block':'chapter-title'});heading.text=r['title']
        headings[r['id']]=heading
        r['headingNoteAnchors']=common.annotate(heading,entries,counts,first,r) if r['kind']!='reference' else []
        r['headingHtml']=inner(heading)
        r['noteAnchors']=common.annotate(documents[r['id']],entries,counts,first,r) if r['kind']!='reference' else []
        assert hashlib.sha256(norm(txt(documents[r['id']])).encode()).hexdigest()==next(x['textSha256'] for x in integrity if x['chapter']==r['id']), (slug,r['id'],'annotation or decoration changed text')
    glossary=[]
    for e in entries:
        if counts[e['id']]:
            item={k:v for k,v in e.items() if k!='evidence'};item.update(occurrences=counts[e['id']],first=first[e['id']]);glossary.append(item)
    missing=[e['id'] for e in entries if not counts[e['id']]]
    total=0;search=[]
    for r in records:
        tree=documents[r['id']];r['words']=len(re.findall(r"\b[\w’'-]+\b",txt(tree)));r['startWords']=total
        if r['kind']!='reference':total+=r['words']
        search.append({k:r[k] for k in ('id','index','title','volume','kind')}|{'paragraphs':[{'id':'chapter-title','text':r['title']}]+[{'id':e.get('data-block'),'text':norm(txt(e))} for e in tree.iter() if e.get('data-block') and not any(x.get('data-block') for x in list(e.iter())[1:])]})
        save(dest/'chapters'/(r['id']+'.json'),r|{'html':inner(tree)})
        nav='<a href="../../">Readers</a><a href="../index.html#'+r['id']+'">Reader</a><a href="../contents.html">Contents</a>'
        if r['index']>0:nav+=f'<a href="{records[r["index"]-1]["id"]}.html">Previous</a>'
        if r['index']+1<len(records):nav+=f'<a href="{records[r["index"]+1]["id"]}.html">Next</a>'
        page=static_page(r['title'],inner(common.static_tree(tree,glossary)),nav)
        page=page.replace('<h1>'+html.escape(r['title'])+'</h1>','<h1 id="chapter-title">'+inner(common.static_tree(headings[r['id']],glossary))+'</h1>')
        (dest/'chapters'/(r['id']+'.html')).write_text(page)
    volumes=[dict(id='text',title=title,chapters=sum(r['kind']=='chapter' for r in records))]
    if any(r['kind']=='reference' for r in records):volumes.append(dict(id='sources',title='Supplementary material',chapters=0,referenceTitle='Afterword'))
    manifest=dict(schema=1,id=slug,title=title,author='Gene Wolfe',volumes=volumes,totalWords=total,defaultChapter=records[0]['id'],glossaryCount=len(glossary),correctionCount=len(corrections),editionVersion=EDITION,chapters=records)
    save(dest/'manifest.json',manifest);save(dest/'glossary.json',glossary);save(dest/'search.json',search)
    template=(ROOT/'book-of-the-short-sun/index.html').read_text()
    template=template.replace('The Book of the Short Sun',html.escape(title)).replace('data-book="book-of-the-short-sun"',f'data-book="{slug}" data-fiction="{spec["kind"]}"')
    template=re.sub(r'<article\b[^>]*>.*?</article>',lambda m:'<article class="chapter-body" id="chapter-body">'+inner(documents[records[0]['id']])+'</article>',template,flags=re.S)
    template=re.sub(r'<h1 id="chapter-title">.*?</h1>',lambda m:'<h1 id="chapter-title">'+records[0]['headingHtml']+'</h1>',template)
    template=re.sub(r'<nav aria-label="Books" class="series-switch">.*?</nav>','',template)
    template=template.replace('chapters/blue-prelude.html','chapters/'+records[0]['id']+'.html')
    template=re.sub(r'\?v=\d+',f'?v={EDITION}',template)
    template=template.replace('</head>',f'<link rel="stylesheet" href="../assets/wolfe-fiction.css?v={EDITION}"></head>')
    start,end=template.index('<article'),template.index('</article>')
    chunk=template[start:end].replace('src="../../assets/','src="../assets/').replace('src="../images/','src="images/')
    template=template[:start]+chunk+template[end:]
    (dest/'index.html').write_text(template)
    links='<ol>'+''.join(f'<li><a href="chapters/{r["id"]}.html">{html.escape(r["title"])}</a></li>' for r in records)+'</ol>'
    (dest/'contents.html').write_text(static_page(title,links,'<a href="../">Readers</a><a href="index.html">Reader</a>',depth=1))
    save(DATA/(slug+'-integrity.json'),dict(book=slug,sourceFiles={s:source_info[s] for s in set(x['source'] for x in integrity)},chapters=integrity,corrections=corrections,unmatchedGlossaryEntries=missing,notePolicy='External referents only. Supplied afterwords are separate reference sections.'))
    print(slug,len(glossary),'notes;',total,'words;', 'unmatched '+str(missing) if missing else '')
    return {k:manifest[k] for k in ('id','title','author','volumes','glossaryCount','totalWords')}|{'kind':spec['kind']}


def library_page(library):
    path=ROOT/'index.html';text=path.read_text()
    # Keep the established Sun and Liu presentation. New works are independent links.
    text=re.sub(r'<div id="additional-wolfe">.*?</div><!-- additional-wolfe -->','',text,flags=re.S)
    works=[b for b in library if b.get('kind')=='book']
    stories=[b for b in library if b.get('kind')=='story']
    extra='<div id="additional-wolfe">'+''.join(f'<article><h3><a href="{b["id"]}/">{html.escape(b["title"])}</a></h3></article>' for b in works)
    extra+='<section class="short-stories" aria-labelledby="stories-title"><h3 id="stories-title">Short stories</h3><ul class="story-list">'
    extra+=''.join(f'<li><a href="{b["id"]}/">{html.escape(b["title"])}</a></li>' for b in stories)
    extra+='</ul></section></div><!-- additional-wolfe -->'
    text=text.replace('</section><section class="author-group"',extra+'</section><section class="author-group"',1)
    text=re.sub(r'\?v=\d+',f'?v={EDITION}',text)
    if 'wolfe-fiction.css' not in text:text=text.replace('</head>',f'<link rel="stylesheet" href="assets/wolfe-fiction.css?v={EDITION}"></head>')
    path.write_text(text)


def main():
    p=argparse.ArgumentParser()
    for key in ('best','endangered','fifth-head'):p.add_argument('--'+key,required=True,type=Path)
    args=p.parse_args();paths={'best':args.best,'endangered':args.endangered,'fifth-head':args.fifth_head}
    archives={k:ZipFile(v) for k,v in paths.items()}
    source_info={k:{'file':v.name,'sha256':hashlib.sha256(v.read_bytes()).hexdigest()} for k,v in paths.items()}
    catalog=json.loads((DATA/'catalog.json').read_text())
    additions=[build(s,archives,source_info) for s in catalog]
    library=json.loads((ROOT/'library.json').read_text());ids={x['id'] for x in additions}
    existing=[b for b in library if b['id'] not in ids]
    library=[b for b in existing if b['author']=='Gene Wolfe']+additions+[b for b in existing if b['author']!='Gene Wolfe']
    save(ROOT/'library.json',library);library_page(library)
    from editorial import apply
    apply(ids)


if __name__=='__main__':main()

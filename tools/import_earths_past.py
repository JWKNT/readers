"""Build three readers from a user-supplied omnibus EPUB (not stored in this repo).

Usage: python3 tools/import_earths_past.py /path/to/omnibus.epub
Edit the three data/earths-past/*.json files to maintain external-reference notes.
Only source headings duplicated by the reader, packaging, and adverts are omitted.
"""
from collections import Counter
import copy
import hashlib
import html
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
EDITION = 15
BOOKS = [('three-body-problem', 'The Three-Body Problem', 1, 'shadow'),
         ('dark-forest', 'The Dark Forest', 2, 'claw'),
         ('deaths-end', 'Death’s End', 3, 'sword')]
NS = '{http://www.w3.org/1999/xhtml}'

def tag(e): return e.tag.rsplit('}', 1)[-1]
def txt(e): return ''.join(e.itertext())
def norm(s): return ' '.join(s.split())
def save(p, obj): p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
def serial(e): return ET.tostring(e, encoding='unicode', method='html')
def inner(e): return html.escape(e.text or '') + ''.join(serial(x) for x in e)

def append_text(parent, s):
    if len(parent): parent[-1].tail = (parent[-1].tail or '') + s
    else: parent.text = (parent.text or '') + s

def clean(source, booknum):
    """Unwrap conversion spans; preserve semantic runs and source anchor IDs."""
    name = tag(source)
    if name in ('script', 'style'): return None
    out = ET.Element(name)
    classes = source.get('class', '').split()
    if classes: out.set('class', ' '.join('ep%d-%s' % (booknum, c) for c in classes if c != 'koboSpan'))
    for key in ('id', 'href', 'src', 'alt', 'colspan', 'rowspan', 'title'):
        val = source.get(key)
        if val is not None and not (key == 'id' and val.startswith('kobo.')): out.set(key, val)
    out.text = source.text
    for child in source:
        item = clean(child, booknum)
        if item is not None:
            if tag(child) == 'span' and (child.get('class') == 'koboSpan' or not item.attrib):
                append_text(out, item.text or '')
                for grand in list(item): out.append(grand)
            else: out.append(item)
        append_text(out, child.tail or '')
    out.tail = None
    return out


def plan(toc, number):
    records, volume, vtitle = [], 'opening', 'Opening'
    for row in toc:
        fn = Path(row['source']).name
        if not fn.startswith('B%d' % number): continue
        n = int(fn[2:5])
        title = row['title'].replace('\u00ad', '')
        if title.startswith('Part '):
            volume = 'part-' + str(sum(r.get('divider', False) for r in records) + 1)
            vtitle = title
            records.append({'divider': True, 'volume': volume, 'volumeTitle': vtitle})
            continue
        if title in ('Welcome Page', 'Contents') or title.startswith('Book '): continue
        reference = (number == 1 and (n == 3 or n >= 43)) or (number == 2 and n in (4,28)) or (number == 3 and (n in (5,6) or n >= 88))
        if reference:
            records.append(dict(source=fn, id='source-'+str(n).zfill(2), title=title, volume='sources', volumeTitle='Supplementary material', kind='reference'))
        else:
            records.append(dict(source=fn, id='section-'+str(n).zfill(2), title=re.sub(r'^Chapter \d+\. ', '', title), volume=volume, volumeTitle=vtitle, kind='chapter'))
    narrative = [r for r in records if not r.get('divider') and r['kind'] == 'chapter']
    refs = [r for r in records if not r.get('divider') and r['kind'] == 'reference']
    return narrative + refs


def selected_elements(z, record, booknum):
    root = ET.fromstring(z.read('OEBPS/Text/' + record['source']))
    body = next(e for e in root.iter() if e.get('id') == 'book-inner')
    children = list(body)
    # Reader chapter headings reproduce the source heading, once.
    while children:
        e = children[0]; cl = e.get('class', '')
        if tag(e) in ('h1','h2') or cl in ('CN','CT__1 KBHeading','CT KBHeading') or norm(txt(e)).replace('\u00ad','') == record['title']:
            children.pop(0)
        elif not txt(e).strip() and not any(tag(x)=='img' for x in e.iter()): children.pop(0)
        else: break
    if record['source'] == 'B3087.html':
        cut = next(i for i,e in enumerate(children) if 'We hope you enjoyed this book' in txt(e))
        children = children[:cut]
    return children


def initial(tree, family):
    for p in tree.iter('p'):
        if any(c in p.get('class','') for c in ('ep1-DL','ep2-p0','source-note')) or len(norm(txt(p))) < 24: continue
        for e in p.iter():
            if e.tag not in ('p','span','em','i'): continue
            s = e.text or ''
            m = re.match(r'([\s“‘"\u2014]*)([A-Z])', s)
            if not m: continue
            letter = m[2]
            e.text = m[1]
            cap = ET.Element('span', {'class':'initial', 'data-letter':letter, 'data-set':family})
            ET.SubElement(cap, 'span', {'class':'initial-letter'}).text = letter
            ET.SubElement(cap, 'img', {'alt':'', 'aria-hidden':'true', 'class':'initial-image', 'decoding':'sync', 'src':f'../../assets/initials/{family}/{letter}.svg'})
            cap.tail = s[m.end():]
            e.insert(0, cap)
            p.set('class', p.get('class','') + ' chapter-opening')
            return


def matcher(entries):
    aliases = {}
    for item in entries:
        for term in [item['term']] + item.get('aliases', []): aliases.setdefault(term, item)
    alternatives = sorted(aliases, key=len, reverse=True)
    if not alternatives: return None, aliases
    # Scientific vocabulary is case-insensitive; proper names retain capitalization.
    patterns = [re.escape(x) if x[0].isupper() else '(?i:'+re.escape(x)+')' for x in alternatives]
    regex = re.compile(r'(?<![\w])(?:'+'|'.join(patterns)+r')(?![\w])')
    lookup = {k.lower():v for k,v in aliases.items()}
    return regex, lookup


def annotate(tree, entries, counts, first, ch):
    regex, lookup = matcher(entries)
    if regex is None: return []
    local, anchors = set(), []
    def register(word, item, block):
        tid=item['id'];fresh,here=counts[tid]==0,tid not in local
        word.set('class','word');word.set('data-term',tid)
        word.set('data-first',str(fresh).lower());word.set('data-local-first',str(here).lower())
        counts[tid]+=1
        if fresh:first[tid]={'chapter':ch['id'],'paragraph':block,'index':ch['index']}
        if here:anchors.append({'term':tid,'paragraph':block});local.add(tid)
    def fragments(s, block):
        last, out = 0, []
        for m in regex.finditer(s):
            out.append(s[last:m.start()]); item = lookup[m[0].lower()]; tid = item['id']
            word = ET.Element('span');word.text=m[0]
            register(word,item,block);out.append(word)
            last = m.end()
        out.append(s[last:]); return out
    def walk(e, block=None):
        block = e.get('data-block', block)
        if e.get('class')=='word' and e.get('data-term') and block:
            # Annotation maintenance can retain a word around correction spans.
            # Recount its complete visible spelling while preserving those spans.
            value=txt(e);assert regex.fullmatch(value),('stale preserved annotation',value)
            register(e,lookup[value.lower()],block)
            return
        if e.tag in ('a','sup','script','style') or any(x in e.get('class','') for x in ('initial', 'source-note', 'source-address')): return
        children = list(e)
        if block and e.text:
            content = fragments(e.text, block); e.text = ''; at=0
            for x in content:
                if isinstance(x,str):
                    if at: e[at-1].tail = (e[at-1].tail or '') + x
                    else: e.text += x
                else: e.insert(at,x);at+=1
        for child in children:
            walk(child, block)
            if block and child.tail:
                content = fragments(child.tail, block); child.tail=''; previous=child
                for x in content:
                    if isinstance(x,str): previous.tail = (previous.tail or '') + x
                    else:
                        e.insert(list(e).index(previous)+1,x);previous=x
    walk(tree)
    return anchors


def static_tree(tree, glossary):
    result = copy.deepcopy(tree); lookup = {x['id']:x for x in glossary}
    for e in result.iter():
        if e.get('data-first') == 'true':
            item = lookup[e.get('data-term')]; e.tag='a';e.set('class','static-word')
            e.set('href',item['sources'][0]['url']);e.set('title',item['note']);e.set('target','_blank');e.set('rel','noopener noreferrer')
    return result


def static_page(title, content, nav, depth=2, volume=''):
    prefix='../'*depth
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow,noarchive"><title>{html.escape(title)} · Readers</title><link rel="icon" href="{prefix}assets/theme/favicons/readers.png"><script src="{prefix}assets/theme/theme.js"></script><link rel="stylesheet" href="{prefix}assets/theme/base.css?v=theme-20260930-dial"><link rel="stylesheet" href="{prefix}assets/reader.css?v={EDITION}"><link rel="stylesheet" href="{prefix}assets/initials/initials.css?v={EDITION}"><link rel="stylesheet" href="{prefix}assets/earths-past.css?v={EDITION}"></head><body class="static-page" data-dropcaps="true" data-paragraphs="indented"><header class="static-header">{nav}<button class="theme-toggle" data-theme-toggle aria-label="Change theme"></button></header><main class="reading static-reading"><header class="chapter-heading"><h1>{html.escape(title)}</h1></header><article class="chapter-body" data-volume="{volume}">{content}</article></main></body></html>'''


def build(z, toc, spec):
    slug,title,num,family=spec; dest=ROOT/slug; (dest/'chapters').mkdir(parents=True,exist_ok=True)
    records=plan(toc,num); maps={}; documents={}; sources=[]
    for i,r in enumerate(records):
        r.update(index=i,number=i+1,label=str(i+1) if num == 1 and r['kind'] != 'reference' else '—',layout='prose',sections=[])
        original=selected_elements(z,r,num); tree=ET.Element('div')
        for e in original:
            child=clean(e,num)
            if child is not None: tree.append(child)
        assert norm(txt(tree))==norm(''.join(txt(e) for e in original)), (r['source'],'conversion changed text')
        source_text=norm(txt(tree)); source_hash=hashlib.sha256(source_text.encode()).hexdigest()
        blocks=[]
        for e in tree.iter():
            if e.tag in ('p','h1','h2','h3','h4','table') and not (e.tag=='p' and not txt(e).strip() and not list(e)):
                pid='p-%03d'%(len(blocks)+1);blocks.append(pid)
                for x in e.iter():
                    sid=x.get('id')
                    if sid: maps[(r['source'],sid)]=(r['id'],pid)
                e.set('id',pid);e.set('data-block',pid)
                classes=e.get('class','')
                if e.tag=='p': e.set('class','prose '+classes)
                if any('ep2-'+x in classes for x in ('p34','p34a')) or ('Translator’s Note:' in txt(e) and num==3):
                    e.set('class',e.get('class','')+' source-note')
        # Source heading anchors lead to the first retained block.
        raw=ET.fromstring(z.read('OEBPS/Text/'+r['source']))
        for e in raw.iter():
            sid=e.get('id')
            if sid and not sid.startswith('kobo.'): maps.setdefault((r['source'],sid),(r['id'],blocks[0] if blocks else ''))
        r['blocks']=blocks
        documents[r['id']]=tree
        sources.append({'chapter':r['id'],'source':r['source'],'textSha256':source_hash,'blocks':len(blocks)})
    counts,first=Counter(),{}
    sourcepath=ROOT/'data'/'earths-past'/(slug+'.json')
    entries=json.loads(sourcepath.read_text()) if sourcepath.exists() else []
    refs={r['source']:r for r in records}
    for r in records:
        tree=documents[r['id']]
        for e in tree.iter():
            if 'id' in e.attrib and 'data-block' not in e.attrib: del e.attrib['id']
            if e.tag=='img':
                old=e.get('src','');filename=Path(old).name
                if filename=='line.jpg':
                    e.tag='span';e.attrib.clear();e.set('class','scene-divider');e.set('role','separator')
                else:
                    (dest/'images').mkdir(exist_ok=True);(dest/'images'/filename).write_bytes(z.read('OEBPS/Images/'+filename));e.set('src','../images/'+filename)
                    if filename.startswith('chi'): e.set('class','source-glyph')
            if e.tag=='a' and e.get('href'):
                old=e.get('href');url=urlsplit(old)
                if not url.scheme and not url.netloc:
                    fn=Path(unquote(url.path)).name if url.path else r['source']
                    target=maps.get((fn,unquote(url.fragment)))
                    if target is None and fn in refs: target=(refs[fn]['id'],'')
                    if target:
                        cid,pid=target;e.set('href',cid+'.html'+('#'+pid if pid else ''));e.set('data-route',cid+('/'+pid if pid else ''))
                    else:
                        # Packaging links (contents/cover) become navigation to this book.
                        e.set('href','../contents.html')
        if r['kind']!='reference':
            from reader_ornaments import decorate
            initial(tree,family)
            decorate(tree,slug)
        r['noteAnchors']=annotate(tree,entries,counts,first,r) if r['kind']!='reference' else []
        assert hashlib.sha256(norm(txt(tree)).encode()).hexdigest()==next(x['textSha256'] for x in sources if x['chapter']==r['id']),(r['source'],'annotation changed text')
    glossary=[]
    for e in entries:
        if counts[e['id']]:
            item={k:v for k,v in e.items() if k!='evidence'};item.update(occurrences=counts[e['id']],first=first[e['id']]);glossary.append(item)
    missing=[e['id'] for e in entries if not counts[e['id']]]
    total=0;search=[]
    for r in records:
        tree=documents[r['id']];r['words']=len(re.findall(r"\b[\w’'-]+\b",txt(tree)));r['startWords']=total
        if r['kind']!='reference':total+=r['words']
        search.append({k:r[k] for k in ('id','index','title','volume','kind')}|{'paragraphs':[{'id':e.get('data-block'),'text':norm(txt(e))} for e in tree.iter() if e.get('data-block') and not any(x.get('data-block') for x in list(e.iter())[1:])]})
        data={k:v for k,v in r.items() if k!='source'}|{'html':inner(tree)}
        save(dest/'chapters'/(r['id']+'.json'),data)
        nav=f'<a href="../index.html#{r["id"]}">Book</a><a href="../contents.html">Contents</a>'
        if r['index']>0:nav+=f'<a href="{records[r["index"]-1]["id"]}.html">Previous</a>'
        if r['index']+1<len(records):nav+=f'<a href="{records[r["index"]+1]["id"]}.html">Next</a>'
        (dest/'chapters'/(r['id']+'.html')).write_text(static_page(r['title'],inner(static_tree(tree,glossary)),nav,volume=r['volume']))
    volumes=[]
    for r in records:
        if not any(v['id']==r['volume'] for v in volumes):volumes.append({'id':r['volume'],'title':r['volumeTitle'],'chapters':sum(x['volume']==r['volume'] and x['kind']!='reference' for x in records),'referenceTitle':'Supplementary material'})
    manifest=dict(schema=1,id=slug,title=title,author='Cixin Liu',volumes=volumes,totalWords=total,defaultChapter=records[0]['id'],glossaryCount=len(glossary),correctionCount=0,editionVersion=EDITION,chapters=[{k:v for k,v in r.items() if k!='source'} for r in records])
    save(dest/'manifest.json',manifest);save(dest/'glossary.json',glossary);save(dest/'search.json',search)
    template=(ROOT/'book-of-the-short-sun'/'index.html').read_text()
    template=template.replace('The Book of the Short Sun',title).replace('data-book="book-of-the-short-sun"',f'data-book="{slug}"')
    template=re.sub(r'<article\b[^>]*>.*?</article>',lambda m:'<article class="chapter-body" id="chapter-body">'+inner(documents[records[0]['id']])+'</article>',template,flags=re.S)
    template=re.sub(r'<h1 id="chapter-title">.*?</h1>',lambda m:'<h1 id="chapter-title">'+html.escape(records[0]['title'])+'</h1>',template)
    template=re.sub(r'<nav aria-label="Books" class="series-switch">.*?</nav>','',template)
    template=template.replace('chapters/blue-prelude.html','chapters/'+records[0]['id']+'.html')
    template=re.sub(r'\?v=\d+',f'?v={EDITION}',template)
    template=template.replace('</head>',f'<link rel="stylesheet" href="../assets/earths-past.css?v={EDITION}"></head>')
    # Static initial screen uses paths relative to the book, including original notes.
    start,end=template.index('<article'),template.index('</article>')
    chunk=template[start:end].replace('src="../../assets/','src="../assets/').replace('src="../images/','src="images/')
    chunk=re.sub(r'href="(section-\d+|source-\d+)\.html',r'href="chapters/\1.html',chunk)
    template=template[:start]+chunk+template[end:]
    (dest/'index.html').write_text(template)
    links=''.join(f'<h2>{html.escape(v["title"])}</h2><ol>'+''.join(f'<li><a href="chapters/{r["id"]}.html">{html.escape(r["title"])}</a></li>' for r in records if r['volume']==v['id'])+'</ol>' for v in volumes)
    (dest/'contents.html').write_text(static_page(title,links,'<a href="../">Readers</a><a href="index.html">Book</a>',depth=1))
    report={'book':slug,'source':Path(sys.argv[1]).name,'sourceSha256':hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest(),'chapters':sources,'unmatchedGlossaryEntries':missing,'notePolicy':'External referents only; original translator notes retained separately.'}
    save(ROOT/'data'/'earths-past'/(slug+'-integrity.json'),report)
    print(slug,len(records),'sections;',len(glossary),'references;',total,'words; unmatched',missing)
    return {k:manifest[k] for k in ('id','title','author','volumes','glossaryCount','totalWords')}


def source_css(z):
    out=['/* Source semantics only: typography and color come from Readers. */']
    for num,fn in enumerate(('stylesheet1.css','style2.css','style3.css'),1):
        path=next(x for x in z.namelist() if x.endswith('/'+fn))
        text=z.read(path).decode()
        for selector,body in re.findall(r'([^{}]+)\{([^{}]+)\}',text):
            selector=selector.strip()
            if not re.fullmatch(r'(?:p|span|h[1-6])?\.[\w-]+',selector):continue
            styles=[]
            for k,v in re.findall(r'([\w-]+)\s*:\s*([^;]+)',body):
                if k in ('text-align','text-indent','font-style','font-weight','font-variant','vertical-align') or k.startswith('margin'):
                    styles.append(k+':'+v.strip())
                    if k=='text-align' and v.strip() in ('center','right'):styles.append('text-align-last:'+v.strip())
            if styles:
                name,cl=selector.split('.');out.append(f'.chapter-body {name}.ep{num}-{cl}'+'{'+ ';'.join(styles)+'}')
    out.append('''
.chapter-body .source-note{font-size:.85em;line-height:1.6;text-indent:0;margin-top:1.3em}
.chapter-body img.source-glyph{display:inline;width:auto;height:1em;margin:0;vertical-align:baseline}
.chapter-body table{width:100%;border-collapse:collapse;font-size:.85em;line-height:1.5;margin:1.5em 0}
.chapter-body td,.chapter-body th{padding:.4em .6em;border-bottom:1px solid var(--line);text-align:left}
.chapter-body .scene-divider{display:block;border:0;width:3em;margin:2em auto;border-top:1px solid currentColor;opacity:.25}
.source-divider-text{position:absolute;width:1px;height:1px;padding:0;overflow:hidden;clip-path:inset(50%);white-space:pre}
.chapter-body .chapter-opening{text-indent:0!important}
.chapter-body .ep1-ePub-SUP,.chapter-body .ep2-t5,.chapter-body .ep2-t10,.chapter-body .ep2-t15,.chapter-body .ep3-t5{font-size:.7em;vertical-align:super;line-height:0}
.chapter-body .ep1-ePub-I,.chapter-body .ep1-ePub-Sans-I{font-style:italic}
.chapter-body .ep1-ePub-B{font-weight:600}
.chapter-body .ep1-ePub-SC{font-variant:small-caps}
.library .author-group{margin-top:5rem}
.library .author-heading{font:700 36px/1.2 var(--regal);margin:0 0 46px}
.library h3{font:700 27px/1.2 var(--regal);margin:0 0 8px}
.library .cycle-title{font-size:15px;color:var(--muted);margin:-24px 0 30px}
.toc details[data-volume="sources"] a{display:block}
''')
    (ROOT/'assets'/'earths-past.css').write_text('\n'.join(out).rstrip()+'\n')

if __name__=='__main__':
    with ZipFile(sys.argv[1]) as z:
        n=ET.fromstring(z.read('OEBPS/toc.ncx'));ns={'n':'http://www.daisy.org/z3986/2005/ncx/'}
        toc=[{'title':e.find('n:navLabel/n:text',ns).text,'source':e.find('n:content',ns).get('src').split('#')[0]} for e in n.findall('.//n:navPoint',ns)]
        (ROOT/'data'/'earths-past').mkdir(parents=True,exist_ok=True)
        books=[build(z,toc,s) for s in BOOKS]
        source_css(z)
    library=json.loads((ROOT/'library.json').read_text());library=[b for b in library if b['id'] not in {s[0] for s in BOOKS}]+books;save(ROOT/'library.json',library)
    from editorial import apply
    apply({s[0] for s in BOOKS})
    from series_readers import group_liu, library_page
    group_liu()
    library_page()

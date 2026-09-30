"""Publish multi-volume readers and preserve the original Liu reader addresses.

The Liu assembly is bookkeeping: original prose, notes, images and paragraph IDs
are retained. Its authored sources remain in data/earths-past and the three
original reader directories. Run after an annotation or source-text rebuild.
"""
import copy
import hashlib
import html
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import import_earths_past as common
from rebuild_annotations import Fragment

ROOT = common.ROOT
EDITION = 16
LIU_ID = 'remembrance-of-earths-past'
LIU_BOOKS = ('three-body-problem', 'dark-forest', 'deaths-end')


def searchable(node):
    """A verse line break is a word boundary in a plain-text search snippet."""
    return (node.text or '') + ''.join((' ' if child.tag=='br' else searchable(child)) + (child.tail or '') for child in node)


def static_page(title, content, nav, styles, heading=None, volume=''):
    links = ''.join(f'<link rel="stylesheet" href="../../assets/{s}?v={EDITION}">' for s in styles)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow,noarchive"><title>{html.escape(title)} · Readers</title><link rel="icon" href="../../assets/theme/favicons/readers.png"><script src="../../assets/theme/theme.js"></script><link rel="stylesheet" href="../../assets/theme/base.css"><link rel="stylesheet" href="../../assets/reader.css?v={EDITION}"><link rel="stylesheet" href="../../assets/initials/initials.css?v={EDITION}">{links}</head><body class="static-page" data-dropcaps="true" data-paragraphs="indented"><header class="static-header">{nav}<button class="theme-toggle" data-theme-toggle aria-label="Change theme"></button></header><main class="reading static-reading"><header class="chapter-heading"><h1 id="chapter-title">{heading or html.escape(title)}</h1></header><article class="chapter-body" data-volume="{volume}">{content}</article></main></body></html>'''


def write_reader(slug, title, author, chapters, glossary, volumes, styles):
    dest = ROOT / slug
    (dest / 'chapters').mkdir(parents=True, exist_ok=True)
    total, search = 0, []
    for i, data in enumerate(chapters):
        data.update(index=i, number=i+1, startWords=total)
        if data['kind'] != 'reference': total += data['words']
        tree = Fragment(data['html']).root
        search.append({k: data[k] for k in ('id', 'index', 'title', 'volume', 'kind')} | {
            'paragraphs': [{'id': 'chapter-title', 'text': data['title']}] + [
                {'id': e.get('data-block'), 'text': common.norm(searchable(e) if slug=='hyperion' else common.txt(e))}
                for e in tree.iter() if e.get('data-block') and not any(x.get('data-block') for x in list(e.iter())[1:])]})
        common.save(dest / 'chapters' / (data['id']+'.json'), data)
        nav = f'<a href="../index.html#{data["id"]}">Reader</a><a href="../contents.html">Contents</a>'
        if i: nav += f'<a href="{chapters[i-1]["id"]}.html">Previous</a>'
        if i+1 < len(chapters): nav += f'<a href="{chapters[i+1]["id"]}.html">Next</a>'
        heading = None
        if 'headingHtml' in data:
            heading = common.inner(common.static_tree(Fragment(data['headingHtml']).root, glossary))
        page = static_page(data['title'], common.inner(common.static_tree(tree, glossary)), nav, styles, heading, data['volume'])
        (dest / 'chapters' / (data['id']+'.html')).write_text(page)
    records = [{k:v for k,v in c.items() if k != 'html'} for c in chapters]
    manifest = dict(schema=1, id=slug, title=title, author=author, volumes=volumes,
                    totalWords=total, defaultChapter=chapters[0]['id'], glossaryCount=len(glossary),
                    correctionCount=0, editionVersion=EDITION, chapters=records)
    common.save(dest / 'manifest.json', manifest)
    common.save(dest / 'glossary.json', glossary)
    common.save(dest / 'search.json', search)
    template = (ROOT / 'book-of-the-short-sun/index.html').read_text()
    template = template.replace('The Book of the Short Sun', html.escape(title)).replace('data-book="book-of-the-short-sun"', f'data-book="{slug}"')
    template = re.sub(r'<nav aria-label="Books" class="series-switch">.*?</nav>', '', template, flags=re.S)
    opening = chapters[0]['html'].replace('src="../../assets/', 'src="../assets/').replace('src="../images/', 'src="images/')
    opening = opening.replace('src="../../three-body-problem/', 'src="../three-body-problem/').replace('src="../../dark-forest/', 'src="../dark-forest/').replace('src="../../deaths-end/', 'src="../deaths-end/')
    opening = re.sub(r'href="([^"/]+)\.html', r'href="chapters/\1.html', opening)
    template = re.sub(r'<article\b[^>]*>.*?</article>', lambda m: '<article class="chapter-body" id="chapter-body">'+opening+'</article>', template, flags=re.S)
    template = re.sub(r'<h1 id="chapter-title">.*?</h1>', lambda m: '<h1 id="chapter-title">'+chapters[0].get('headingHtml',html.escape(chapters[0]['title']))+'</h1>', template)
    template = template.replace('chapters/blue-prelude.html', 'chapters/'+chapters[0]['id']+'.html')
    template = re.sub(r'\?v=\d+', f'?v={EDITION}', template)
    template = template.replace('</head>', ''.join(f'<link rel="stylesheet" href="../assets/{s}?v={EDITION}">' for s in styles)+f'<link rel="canonical" href="https://jehlp.net/readers/{slug}/"></head>')
    (dest / 'index.html').write_text(template)
    groups=[]
    for volume in volumes:
        group='<h2>'+html.escape(volume['title'])+'</h2><ol>';last_part=''
        for chapter in (c for c in chapters if c['volume']==volume['id']):
            part=chapter.get('partTitle','') if chapter['kind']!='reference' else 'Supplementary material'
            if part and part!=last_part:
                group+='</ol><h3>'+html.escape(part)+'</h3><ol>';last_part=part
            group+=f'<li><a href="chapters/{chapter["id"]}.html">{html.escape(chapter["title"])}</a></li>'
        groups.append(group+'</ol>')
    links=''.join(groups).replace('<ol></ol>','')
    contents = static_page(title, links, '<a href="../">Readers</a><a href="index.html">Reader</a>', styles).replace('../../assets/', '../assets/')
    (dest / 'contents.html').write_text(contents)
    return {k:manifest[k] for k in ('id','title','author','volumes','glossaryCount','totalWords')} | {'kind':'series'}


def group_liu():
    chapters, glossary, volumes, integrity = [], [], [], []
    for slug in LIU_BOOKS:
        folder = ROOT / slug
        manifest = json.loads((folder / 'manifest.json').read_text())
        prefix = slug+'-'
        volumes.append(dict(id=slug, title=manifest['title'], chapters=sum(c['kind']!='reference' for c in manifest['chapters']), referenceTitle='Supplementary material'))
        by_id = {c['id']: prefix+c['id'] for c in manifest['chapters']}
        chapter_offset = len(chapters)
        for entry in json.loads((folder / 'glossary.json').read_text()):
            item = copy.deepcopy(entry)
            item['id'] = prefix+item['id']
            item['first']['chapter'] = by_id[item['first']['chapter']]
            item['first']['index'] += chapter_offset
            glossary.append(item)
        for record in manifest['chapters']:
            data = json.loads((folder/'chapters'/(record['id']+'.json')).read_text())
            original_html = data['html']
            tree = Fragment(original_html).root
            for e in tree.iter():
                if e.get('data-term'): e.set('data-term', prefix+e.get('data-term'))
                if e.get('data-route'):
                    route=e.get('data-route');cid,sep,pid=route.partition('/')
                    e.set('data-route',by_id[cid]+sep+pid)
                if e.get('href'):
                    href=e.get('href');file,sep,anchor=href.partition('#')
                    if file.endswith('.html') and file[:-5] in by_id:e.set('href',by_id[file[:-5]]+'.html'+sep+anchor)
                if e.get('src','').startswith('../images/'):
                    filename=e.get('src')[10:]
                    target=ROOT/LIU_ID/'images';target.mkdir(parents=True,exist_ok=True)
                    (target/(slug+'-'+filename)).write_bytes((folder/'images'/filename).read_bytes())
                    e.set('src','../images/'+slug+'-'+filename)
            assert common.txt(tree) == common.txt(Fragment(original_html).root)
            data.update(id=by_id[record['id']],volume=slug,volumeTitle=manifest['title'],html=common.inner(tree),sourceReader=slug,sourceChapter=record['id'])
            data['partTitle']=record['volumeTitle'] if record['volume'].startswith('part-') else ''
            data['noteAnchors'] = [a|{'term':prefix+a['term']} for a in data['noteAnchors']]
            chapters.append(data)
            integrity.append(dict(chapter=data['id'],sourceReader=slug,sourceChapter=record['id'],textSha256=hashlib.sha256(common.norm(common.txt(tree)).encode()).hexdigest(),blocks=len(data['blocks'])))
        title=html.escape(manifest['title'])
        # Keep every old hash and the source-wording query when entering the series.
        (folder/'index.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow,noarchive"><title>{title} · Remembrance of Earth’s Past</title><link rel="canonical" href="https://jehlp.net/readers/{LIU_ID}/"><script defer src="../assets/series-redirect.js?v={EDITION}"></script><link rel="stylesheet" href="../assets/theme/base.css"><link rel="stylesheet" href="../assets/reader.css?v={EDITION}"></head><body data-series="{LIU_ID}" data-prefix="{prefix}" data-first="{manifest['defaultChapter']}"><main class="document"><h1>{title}</h1><p><a href="../{LIU_ID}/#{prefix}{manifest['defaultChapter']}">Read in Remembrance of Earth’s Past</a></p><p><a href="contents.html">Plain HTML contents</a></p></main></body></html>''')
    book=write_reader(LIU_ID, 'Remembrance of Earth’s Past', 'Cixin Liu', chapters, glossary, volumes, ['earths-past.css'])
    common.save(ROOT/'data/earths-past'/(LIU_ID+'-integrity.json'),dict(book=LIU_ID,chapters=integrity,notePolicy='Assembly only: prose and external-reference notes are unchanged.'))
    library=json.loads((ROOT/'library.json').read_text())
    library=[b for b in library if b['id'] not in {*LIU_BOOKS,LIU_ID}]+[book]
    library.sort(key=lambda b:{'Gene Wolfe':0,'Cixin Liu':1,'Dan Simmons':2}.get(b['author'],3))
    common.save(ROOT/'library.json',library)
    return book


def library_page():
    path=ROOT/'index.html';page=path.read_text()
    liu='<section class="author-group" aria-labelledby="liu-title"><h2 class="author-heading" id="liu-title">Cixin Liu</h2><article><h3><a href="remembrance-of-earths-past/">Remembrance of Earth’s Past</a></h3><p class="volumes">'
    for slug in LIU_BOOKS:
        m=json.loads((ROOT/slug/'manifest.json').read_text())
        liu+=f'<a href="{LIU_ID}/#{slug}-{m["defaultChapter"]}">{html.escape(m["title"])}</a><br>'
    liu=liu.removesuffix('<br>')+'</p></article></section>'
    page=re.sub(r'<section class="author-group" aria-labelledby="liu-title">.*?</section>',lambda m:liu,page,flags=re.S)
    page=re.sub(r'<section class="author-group" aria-labelledby="simmons-title">.*?</section>','',page,flags=re.S)
    if (ROOT/'hyperion/manifest.json').exists():
        page=page.replace('</main>','<section class="author-group" aria-labelledby="simmons-title"><h2 class="author-heading" id="simmons-title">Dan Simmons</h2><article><h3><a href="hyperion/">Hyperion</a></h3><p class="volumes"><a href="hyperion/#hyperion-prologue">Hyperion</a><br><a href="hyperion/#fall-epigraph">The Fall of Hyperion</a></p></article></section></main>')
    path.write_text(re.sub(r'\?v=\d+',f'?v={EDITION}',page))


if __name__=='__main__':
    group_liu()
    library_page()

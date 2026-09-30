"""Apply reviewed, paragraph-addressed transcription repairs without moving links.

The authored ledger is replayable after an EPUB import. Original text remains in
text-fix spans for ?wording=source and for baseline verification.
"""
from collections import defaultdict
from difflib import SequenceMatcher
from html import escape, unescape
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / 'data/editorial-corrections.json'
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}


class Runs(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source, self.stack, self.runs = source, [], []
        self.lines = [0]
        self.lines.extend(m.end() for m in re.finditer('\n', source))
        self.feed(source)

    def position(self):
        line, column = self.getpos()
        return self.lines[line-1] + column

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in VOID:
            self.stack.append((tag, attrs.get('data-block') or (self.stack[-1][1] if self.stack else None)))

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_startendtag(self, tag, attrs):
        pass

    def add(self, raw, value):
        self.runs.append((self.position(), self.position()+len(raw), value, self.stack[-1][1] if self.stack else None))

    def handle_data(self, value):
        self.add(value, value)

    def handle_entityref(self, name):
        self.add('&'+name+';', unescape('&'+name+';'))

    def handle_charref(self, name):
        self.add('&#'+name+';', unescape('&#'+name+';'))


def text(source):
    return ''.join(run[2] for run in Runs(source).runs)


def restore(source):
    source=re.sub(r'<span class="text-fix" data-correction="[^"]+" data-original="([^"]*)">[^<]*</span>',
                  lambda m: escape(unescape(m[1]),quote=False),source)
    if 'data-correction=' not in source:return source
    class OriginalSpans(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=False)
            self.lines=[0]+[m.end() for m in re.finditer('\n',source)]
            self.spans=[];self.patches=[];self.feed(source)

        def position(self):
            line,column=self.getpos();return self.lines[line-1]+column

        def handle_starttag(self, tag, attrs):
            if tag=='span':self.spans.append((self.position(),dict(attrs)))

        def handle_endtag(self, tag):
            if tag=='span':
                start,attrs=self.spans.pop()
                if attrs.get('data-correction') and 'data-original' in attrs:
                    self.patches.append((start,self.position()+len('</span>'),escape(attrs['data-original'],quote=False)))

    patches=OriginalSpans().patches
    # Notes may be regenerated inside a repaired fragment. Restore the entire
    # fragment, including nested annotation markup, without losing its original.
    selected=[];end=-1
    for patch in sorted(patches,key=lambda p:(p[0],-p[1])):
        if patch[0]>=end:selected.append(patch);end=patch[1]
    for start,end,value in reversed(selected):source=source[:start]+value+source[end:]
    return source


def repair(source, entry):
    def visible_initial_quote(value):
        # An inserted opening quote must sit beside the ornamental initial,
        # rather than inside its visually hidden accessible letter.
        return re.sub(r'(<span class="initial"[^>]*><span class="initial-letter">)(<span class="text-fix"[^>]*data-original=""[^>]*>[“‘]</span>)',
                      lambda m:m[2].replace('class="text-fix"','class="text-fix opening-quote"')+m[1],value)
    marker = 'data-correction="'+entry['id']+'"'
    if marker in source:
        return visible_initial_quote(source)
    runs = [r for r in Runs(source).runs if r[3] == entry['paragraph']]
    current = ''.join(r[2] for r in runs)
    before, after = entry['before'], entry['after']
    assert before != after and current.count(before) == 1, (entry['id'], entry['book'], entry['chapter'], entry['paragraph'], 'ambiguous or missing correction', before)
    base = current.index(before)
    edits = []
    # A fragment may cross italics, a decorated initial, or annotation markup.
    # Change only differing characters; leave every surrounding element in place.
    for op, a, b, c, d in SequenceMatcher(None, before, after, autojunk=False).get_opcodes():
        if op != 'equal': edits.append((base+a, base+b, after[c:d]))
    replacements = defaultdict(list)
    offsets, at = [], 0
    for run in runs:
        offsets.append((at, at+len(run[2]), run)); at += len(run[2])
    for start, end, replacement in edits:
        if start == end:
            candidates = [(a,b,r) for a,b,r in offsets if a <= start < b]
            if not candidates: candidates = [offsets[-1]]
            a,b,run = candidates[0]
            replacements[run].append((start-a,start-a,replacement))
        else:
            first = True
            for a,b,run in offsets:
                if a < end and b > start:
                    replacements[run].append((max(start,a)-a,min(end,b)-a,replacement if first else ''))
                    first = False
    patches = []
    for run, changes in replacements.items():
        pos = 0; chunks = []
        for start,end,replacement in sorted(changes):
            chunks.append(escape(run[2][pos:start], quote=False))
            original = run[2][start:end]
            chunks.append('<span class="text-fix" data-correction="'+entry['id']+'" data-original="'+escape(original,quote=True)+'">'+escape(replacement,quote=False)+'</span>')
            pos = end
        chunks.append(escape(run[2][pos:],quote=False))
        patches.append((run[0],run[1],''.join(chunks)))
    result = source
    for start,end,replacement in sorted(patches, reverse=True):
        result = result[:start]+replacement+result[end:]
    result = visible_initial_quote(result)
    expected = current.replace(before,after,1)
    assert ''.join(r[2] for r in Runs(result).runs if r[3]==entry['paragraph']) == expected, entry['id']
    assert text(restore(result)) == text(restore(source)), (entry['id'],'source recovery')
    return result


def save(path, data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def format_existing(source, book, chapter):
    # The source cast list accidentally runs two people into one paragraph.
    # A line break leaves its long-established paragraph address intact.
    if book=='book-of-the-short-sun' and chapter=='blue-reference':
        def split_names(match):
            value=match[0]
            if 'data-editorial-break' in value:return value
            needle='fig, a mercenary'
            if needle in value:
                value=value.replace(needle,'<br data-editorial-break="pehla-pig">'+needle,1)
            return value
        source=re.sub(r'<p\b[^>]*\bid="p-076"[^>]*>.*?</p>',split_names,source,flags=re.S)
    return source


def apply(books=None):
    if not LEDGER.exists(): return
    ledger = json.loads(LEDGER.read_text())
    grouped = defaultdict(lambda:defaultdict(list))
    for row in ledger:
        if books is None or row['book'] in books:
            grouped[row['book']][row['chapter']].append(row)
    library = json.loads((ROOT/'library.json').read_text())
    for book, chapters in grouped.items():
        folder=ROOT/book;manifest=json.loads((folder/'manifest.json').read_text())
        edition=max(15,manifest.get('editionVersion',15))
        for rows in chapters.values():
            for entry in rows:
                revision=re.match(r'v(\d+)-',entry['id'])
                if revision:edition=max(edition,int(revision[1]))
        search=json.loads((folder/'search.json').read_text()); search_by_id={s['id']:s for s in search}
        integrity_path=next((ROOT/'data'/family/(book+'-integrity.json') for family in ('wolfe-fiction','earths-past','hyperion') if (ROOT/'data'/family/(book+'-integrity.json')).exists()),None)
        integrity=json.loads(integrity_path.read_text()) if integrity_path else None
        total=0
        for chapter in manifest['chapters']:
            path=folder/'chapters'/(chapter['id']+'.json');data=json.loads(path.read_text());old_words=data['words']
            if chapter['id'] in chapters:
                before_html=data['html']
                plain=path.with_suffix('.html');static=plain.read_text()
                data['html']=format_existing(data['html'],book,chapter['id'])
                static=format_existing(static,book,chapter['id'])
                for entry in chapters[chapter['id']]:
                    data['html']=repair(data['html'],entry);static=repair(static,entry)
                plain.write_text(static)
                # Add only the word-count delta: older editions use their own
                # tokenization convention, which unrelated paragraphs retain.
                words=lambda s:len(re.findall(r"\b[\w’'-]+\b",text(s)))
                data['words']=old_words+words(data['html'])-words(before_html)
                data['editorialVersion']=edition
                paragraph_text=defaultdict(str)
                for _,_,value,pid in Runs(data['html']).runs:
                    if pid:paragraph_text[pid]+=value
                if book=='hyperion':
                    from rebuild_annotations import Fragment
                    from series_readers import searchable
                    paragraph_text={e.get('data-block'):searchable(e) for e in Fragment(data['html']).root.iter() if e.get('data-block')}
                for p in search_by_id[data['id']]['paragraphs']:
                    if p['id'] in paragraph_text:p['text']=' '.join(paragraph_text[p['id']].split())
                if integrity:
                    row=next(r for r in integrity['chapters'] if r['chapter']==data['id'])
                    row.setdefault('preEditorialTextSha256',row['textSha256'])
                    row['textSha256']=hashlib.sha256(' '.join(text(data['html']).split()).encode()).hexdigest()
                if chapter['id']==manifest['defaultChapter']:
                    index=folder/'index.html';value=index.read_text()
                    for entry in chapters[chapter['id']]:value=repair(value,entry)
                    index.write_text(value)
            data['startWords']=total
            chapter['words']=data['words'];chapter['startWords']=total
            if data['kind']!='reference':total+=data['words']
            save(path,data)
        manifest['totalWords']=total;manifest['editionVersion']=edition
        count=sum(len(rows) for rows in chapters.values())
        manifest['editorialCorrectionCount']=count
        index=folder/'index.html'
        index.write_text(re.sub(r'\?v=\d+', f'?v={edition}', index.read_text()))
        save(folder/'manifest.json',manifest);save(folder/'search.json',search)
        if integrity:
            integrity['editorialCorrections']=[e for rows in chapters.values() for e in rows]
            save(integrity_path,integrity)
        for b in library:
            if b['id']==book:b['totalWords']=total
        print(book,count,'reviewed repairs')
    save(ROOT/'library.json',library)


if __name__=='__main__':
    apply()

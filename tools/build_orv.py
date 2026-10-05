"""Build the ORV reader from aligned Korean source and English target rows.

Usage: python3 tools/build_orv.py
       python3 tools/build_orv.py --require-complete --update-library

The default build contains the complete chronological target prefix. It marks
the edition as a translation draft and reports the remaining source chapters.
The source text stays in data/orv and is never included in reader output.
"""
import argparse
import copy
from collections import Counter
import hashlib
import html
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import import_earths_past as common
from library_page import build_library
from series_readers import chapter_contents, static_page


ROOT = Path(__file__).resolve().parents[1]
SLUG = 'omniscient-readers-viewpoint'
TITLE = 'Omniscient Reader’s Viewpoint'
AUTHOR = 'Sing Shong'
EDITION = 21
STAGES = ('mt-draft', 'accuracy-reviewed', 'prose-reviewed', 'reader-verified')
TARGET_STAGES = ('untranslated',) + STAGES
IDENTIFIER = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
SHA256 = re.compile(r'[0-9a-f]{64}\Z')
HANGUL = re.compile(r'[\u1100-\u11ff\u3130-\u318f\ua960-\ua97f\uac00-\ud7af\ud7b0-\ud7ff]')
PLACEHOLDER = re.compile(r'^\s*(?:TODO|TBD|TRANSLATION PENDING|UNTRANSLATED|\[\[PLACEHOLDER\]\])(?:\s*[:.]|\s*$)', re.I)


class BuildError(ValueError):
    """Invalid or incomplete authoring data."""


def require(condition, message):
    if not condition:
        raise BuildError(message)


def load(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError) as error:
        raise BuildError(f'{path}: {error}') from error


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def valid_hash(value):
    return isinstance(value, str) and SHA256.fullmatch(value)


def english_text(value, location):
    require(nonempty(value), f'{location}: empty English text')
    require(not HANGUL.search(value), f'{location}: untranslated Korean text')
    require('\ufffd' not in value, f'{location}: replacement character')
    require(not PLACEHOLDER.search(value), f'{location}: translation placeholder')


def validate_sources(data):
    manifest = load(data / 'source-manifest.json')
    require(isinstance(manifest, dict) and manifest.get('schemaVersion') == 1,
            'source-manifest.json: unsupported schema')
    chapters = manifest.get('chapters')
    require(isinstance(chapters, list) and chapters, 'source manifest has no chapters')
    require(all(isinstance(chapter, dict) for chapter in chapters), 'source manifest has invalid chapter records')
    source_info = manifest.get('source', {})
    require(isinstance(source_info, dict) and valid_hash(source_info.get('sha256')),
            'source manifest has no valid PDF hash')
    require(isinstance(source_info.get('pages'), int) and source_info['pages'] > 0,
            'source manifest has no valid PDF page count')
    ids = [chapter.get('id') for chapter in chapters]
    require(all(isinstance(cid, str) and IDENTIFIER.fullmatch(cid) for cid in ids),
            'source manifest has an invalid chapter ID')
    require(len(ids) == len(set(ids)), 'source manifest has duplicate chapter IDs')
    unknown = {path.stem for path in (data / 'source').glob('*.json')} - set(ids)
    require(not unknown, f'unknown source chapters: {sorted(unknown)}')
    if any('readingIndex' in chapter for chapter in chapters):
        indices = [chapter.get('readingIndex') for chapter in chapters]
        require(all(isinstance(index, int) for index in indices)
                and indices == list(range(indices[0], indices[0] + len(indices)))
                and indices[0] in (0, 1), 'source manifest readingIndex values are missing, duplicated, or reordered')
    numbered_order = manifest.get('readingOrderBasis') == 'numbered-source-headings'
    ordering_repairs = manifest.get('orderingRepairs')
    documented_repairs = isinstance(ordering_repairs, (list, dict)) and bool(ordering_repairs)
    if numbered_order:
        numbers = [int(chapter['id'].removeprefix('chapter-')) for chapter in chapters
                   if re.fullmatch(r'chapter-\d+', chapter['id'])]
        require(numbers == sorted(set(numbers)), 'source manifest numbered chapter order is invalid')
    sources = {}
    previous_page = 0
    for chapter in chapters:
        cid = chapter['id']
        require(chapter.get('kind') in ('chapter', 'reference'), f'{cid}: invalid chapter kind')
        require(nonempty(chapter.get('volume')) and IDENTIFIER.fullmatch(chapter['volume']),
                f'{cid}: invalid volume ID')
        require(nonempty(chapter.get('volumeTitle')), f'{cid}: missing volume title')
        require(valid_hash(chapter.get('sourceHash')), f'{cid}: invalid source hash')
        start, end = chapter.get('pageStart'), chapter.get('pageEnd')
        require(isinstance(start, int) and isinstance(end, int) and 1 <= start <= end <= source_info['pages'],
                f'{cid}: source page range is invalid')
        if start < previous_page:
            require(numbered_order and documented_repairs,
                    f'{cid}: source page inversion has no documented reading-order repair')
        previous_page = start
        source = load(data / 'source' / (cid + '.json'))
        require(isinstance(source, dict) and source.get('id') == cid, f'{cid}: source ID mismatch')
        require(source.get('sourceHash') == chapter['sourceHash'], f'{cid}: source hash mismatch')
        rows = source.get('rows')
        require(isinstance(rows, list) and rows, f'{cid}: no source rows')
        require(all(isinstance(row, dict) for row in rows), f'{cid}: invalid source rows')
        require(len(rows) == chapter.get('rowCount'), f'{cid}: source row count mismatch')
        row_ids = [row.get('id') for row in rows]
        expected = [f'p-{i:03d}' for i in range(1, len(rows) + 1)]
        require(row_ids == expected, f'{cid}: missing, duplicate, unknown, or reordered source row IDs')
        for row in rows:
            location = f'{cid}/{row["id"]}'
            require(row.get('lineId') == cid + ':' + row['id'], f'{location}: source line ID mismatch')
            require(row.get('type') in ('prose', 'system', 'scene-break'), f'{location}: invalid source type')
            require(nonempty(row.get('source')), f'{location}: empty source')
            require(valid_hash(row.get('sourceHash')), f'{location}: invalid row source hash')
            require(digest(row['source']) == row['sourceHash'], f'{location}: changed source row')
            require(isinstance(row.get('pages'), list) and row['pages']
                    and all(isinstance(page, int) and start <= page <= end for page in row['pages']),
                    f'{location}: invalid source page list')
        canonical = json.dumps({'label': source.get('labelSource'), 'title': source.get('titleSource'),
                                'rows': [(row['id'], row['type'], row['source']) for row in rows]},
                               ensure_ascii=False, separators=(',', ':'))
        require(digest(canonical) == chapter['sourceHash'], f'{cid}: changed source chapter')
        sources[cid] = source
    return manifest, sources


def validate_target(chapter, source, target, *, check_english=True):
    cid = chapter['id']
    require(isinstance(target, dict) and target.get('id') == cid, f'{cid}: target ID mismatch')
    require(target.get('sourceHash') == chapter['sourceHash'], f'{cid}: target source hash mismatch')
    require(isinstance(target.get('title'), str), f'{cid}: invalid target title')
    require(target.get('status') in TARGET_STAGES, f'{cid}: invalid target status')
    review = target.get('review', {})
    require(isinstance(review, dict) and review.get('alignment') is True,
            f'{cid}: alignment has not been checked')
    if target['status'] in STAGES[1:]:
        require(review.get('accuracy') is True, f'{cid}: accuracy review status mismatch')
    if target['status'] in STAGES[2:]:
        require(review.get('prose') is True, f'{cid}: prose review status mismatch')
    rows = target.get('rows')
    require(isinstance(rows, list), f'{cid}: no target rows')
    require(all(isinstance(row, dict) for row in rows), f'{cid}: invalid target rows')
    require([row.get('id') for row in rows] == [row['id'] for row in source['rows']],
            f'{cid}: missing, duplicate, unknown, or reordered target row IDs')
    for original, row in zip(source['rows'], rows):
        location = f'{cid}/{row["id"]}'
        require(row.get('status') in TARGET_STAGES, f'{location}: invalid row status')
        require(isinstance(row.get('text'), str), f'{location}: invalid row text')
        if row['status'] == 'untranslated':
            if check_english and row['text'].strip():
                english_text(row['text'], location)
            continue
        if check_english:
            english_text(row.get('text'), location)
        if check_english and original['type'] != 'scene-break' and HANGUL.search(original['source']):
            require(row['text'].strip() != original['source'].strip(), f'{location}: unchanged Korean source')
        if original['type'] == 'scene-break':
            require(common.norm(row['text']) == common.norm(original['source']),
                    f'{location}: source scene break changed')
    lowest_stage = min((row['status'] for row in rows), key=TARGET_STAGES.index)
    require(target['status'] == lowest_stage, f'{cid}: chapter status does not match its least-reviewed row')
    if target['status'] != 'untranslated' or target['title'].strip():
        if check_english:
            english_text(target['title'], f'{cid}: title')
        if chapter.get('editorialTitle'):
            require(target['title'] == chapter['editorialTitle'], f'{cid}: editorial title mismatch')
    return target


def select_targets(data, manifest, sources, require_complete=False, minimum_status='mt-draft'):
    chapters = manifest['chapters']
    by_id = {chapter['id']: chapter for chapter in chapters}
    present = {path.stem: path for path in (data / 'target').glob('*.json')}
    require(not (set(present) - set(by_id)), f'unknown target chapters: {sorted(set(present) - set(by_id))}')
    targets = {cid: validate_target(by_id[cid], sources[cid], load(path), check_english=False)
               for cid, path in present.items()}
    for cid, target in targets.items():
        if TARGET_STAGES.index(target['status']) >= TARGET_STAGES.index(minimum_status):
            validate_target(by_id[cid], sources[cid], target)
    prefix = []
    for chapter in chapters:
        if (chapter['id'] not in targets or TARGET_STAGES.index(targets[chapter['id']]['status'])
                < TARGET_STAGES.index(minimum_status)):
            break
        prefix.append(chapter)
    require(prefix, 'the first source chapter has no complete English target')
    if require_complete:
        missing = [chapter['id'] for chapter in chapters
                   if chapter['id'] not in targets or TARGET_STAGES.index(targets[chapter['id']]['status'])
                   < TARGET_STAGES.index(minimum_status)]
        require(not missing, f'incomplete translation: {len(missing)} missing chapters, starting with {missing[:5]}')
    return prefix, targets


def make_tree(source, target):
    tree = ET.Element('div')
    for original, translated in zip(source['rows'], target['rows']):
        classes = 'prose'
        if original['type'] == 'system':
            classes += ' noindent'
        elif original['type'] == 'scene-break':
            classes += ' center scene-break'
        paragraph = ET.SubElement(tree, 'p', {'id': original['id'], 'data-block': original['id'], 'class': classes})
        lines = translated['text'].split('\n')
        paragraph.text = lines[0]
        for line in lines[1:]:
            ET.SubElement(paragraph, 'br').tail = line
    # Use the established initial alphabet, and skip system panels and scene breaks.
    if source.get('kind') != 'reference':
        for first in tree:
            if ('noindent' in first.get('class', '') or 'scene-break' in first.get('class', '')
                    or len(common.norm(common.txt(first))) < 24):
                continue
            view = ET.Element('div')
            view.append(first)
            common.initial(view, 'shadow')
            if first.find('.//span[@class="initial"]') is not None:
                break
    return tree


def load_notes(data):
    path = data / 'annotations.json'
    if not path.exists():
        return []
    entries = load(path)
    require(isinstance(entries, list), 'annotations.json: expected a list')
    require(all(isinstance(entry, dict) for entry in entries), 'annotations.json: invalid entries')
    ids = [entry.get('id') for entry in entries]
    require(len(ids) == len(set(ids)), 'annotations.json: duplicate note IDs')
    for entry in entries:
        require(nonempty(entry.get('id')), 'annotation has no ID')
        for key in ('term', 'short', 'note'):
            english_text(entry.get(key), f'annotation {entry["id"]}: {key}')
        require(isinstance(entry.get('sources'), list),
                f'annotation {entry["id"]}: invalid sources list')
        if not entry['sources']:
            require(entry.get('kind') == 'source-qualification',
                    f'annotation {entry["id"]}: no external source')
            english_text(entry.get('sourceLabel'), f'annotation {entry["id"]}: local source label')
        require(all(isinstance(source, dict) and isinstance(source.get('url'), str)
                    and re.match(r'https?://', source['url']) for source in entry['sources']),
                f'annotation {entry["id"]}: invalid source URL')
        if 'includeChapters' in entry:
            scope = entry['includeChapters']
            require(isinstance(scope, list) and scope
                    and all(isinstance(cid, str) and IDENTIFIER.fullmatch(cid) for cid in scope)
                    and len(scope) == len(set(scope)), f'annotation {entry["id"]}: invalid chapter scope')
    return entries


def static_note_tree(tree, glossary):
    """Keep linked notes unchanged; expose local qualifications without a URL."""
    result = copy.deepcopy(tree)
    lookup = {entry['id']: entry for entry in glossary}
    for element in result.iter():
        if element.get('data-first') != 'true':
            continue
        entry = lookup[element.get('data-term')]
        element.set('class', 'static-word')
        if entry.get('sources'):
            element.tag = 'a'
            element.set('href', entry['sources'][0]['url'])
            element.set('title', entry['note'])
            element.set('target', '_blank')
            element.set('rel', 'noopener noreferrer')
        else:
            element.tag = 'span'
            element.set('title', entry['note'])
            element.set('tabindex', '0')
            element.set('aria-label', common.txt(element) + '. ' + entry['note'])
    return result


def status_text(translation):
    prefix = 'Translation draft' if not translation['complete'] or translation['status'] not in STAGES[2:] else 'Translation reviewed'
    return (f'{prefix}. {translation["availableChapters"]} of '
            f'{translation["sourceChapters"]} source sections are available.')


def add_status(page, translation):
    status = '<p class="quiet translation-status">' + html.escape(status_text(translation)) + '</p>'
    return page.replace('<header class="chapter-heading">', status + '<header class="chapter-heading">', 1)


def build(root=ROOT, data=None, require_complete=False, update_library=False, minimum_status='mt-draft'):
    data = Path(data or root / 'data/orv')
    root = Path(root)
    source_manifest, sources = validate_sources(data)
    selected, targets = select_targets(data, source_manifest, sources, require_complete, minimum_status)
    entries = load_notes(data)
    for entry in entries:
        require(set(entry.get('includeChapters', [])) <= set(sources),
                f'annotation {entry["id"]}: unknown chapter scope')
    chapters, trees, headings, integrity = [], {}, {}, []
    total = 0
    volume_runs = Counter()
    previous_source_volume = None
    generated_volume = None
    for index, original in enumerate(selected):
        cid, target = original['id'], targets[original['id']]
        if original['volume'] != previous_source_volume:
            volume_runs[original['volume']] += 1
            run = volume_runs[original['volume']]
            generated_volume = original['volume'] + (f'-{run}' if run > 1 else '')
            previous_source_volume = original['volume']
        tree = make_tree(sources[cid], target)
        words = len(re.findall(r"\b[\w’'-]+\b", common.searchable(tree)))
        record = dict(id=cid, title=target['title'], volume=generated_volume, sourceVolume=original['volume'],
                      volumeTitle=original['volumeTitle'], number=original.get('number', index + 1),
                      label=str(original.get('number', index + 1)) if original['kind'] != 'reference' and original.get('number') != 0 else '',
                      kind=original['kind'], index=index, layout='prose', blocks=[row['id'] for row in sources[cid]['rows']],
                      sections=[], words=words, startWords=total, translationStatus=target['status'],
                      sourceHash=original['sourceHash'], sourcePages=[original['pageStart'], original['pageEnd']])
        if original.get('number') == 0:
            record['unnumberedToc'] = True
        if original['kind'] != 'reference':
            total += words
        chapters.append(record)
        trees[cid] = tree
        heading = ET.Element('h1', {'data-block': 'chapter-title'})
        heading.text = target['title']
        headings[cid] = heading
        integrity.append(dict(chapter=cid, sourceHash=original['sourceHash'],
                              textSha256=digest(common.norm(common.txt(tree))), blocks=len(record['blocks']),
                              rowIds=record['blocks'], rowSourceHashes=[row['sourceHash'] for row in sources[cid]['rows']]))
    common.validate_exclusions(entries, chapters)
    counts, first = Counter(), {}
    for record in chapters:
        cid = record['id']
        applicable_entries = [entry for entry in entries
                              if 'includeChapters' not in entry or cid in entry['includeChapters']]
        record['headingNoteAnchors'] = common.annotate(headings[cid], applicable_entries, counts, first, record) if record['kind'] != 'reference' else []
        record['headingHtml'] = common.inner(headings[cid])
        record['noteAnchors'] = common.annotate(trees[cid], applicable_entries, counts, first, record) if record['kind'] != 'reference' else []
        require(digest(common.norm(common.txt(trees[cid]))) == integrity[record['index']]['textSha256'],
                f'{cid}: annotation changed target text')
    glossary = [{key: value for key, value in entry.items() if key != 'evidence'}
                | {'occurrences': counts[entry['id']], 'first': first[entry['id']]}
                for entry in entries if counts[entry['id']]]
    complete = len(selected) == len(source_manifest['chapters'])
    stage = min((targets[chapter['id']]['status'] for chapter in selected), key=STAGES.index)
    translation = dict(sourceLanguage='ko', targetLanguage='en', status=stage, complete=complete,
                       availableChapters=len(selected), sourceChapters=len(source_manifest['chapters']),
                       availableNarrativeChapters=sum(chapter['kind'] != 'reference' for chapter in selected),
                       sourceNarrativeChapters=sum(chapter['kind'] != 'reference' for chapter in source_manifest['chapters']),
                       sourceSha256=source_manifest['source']['sha256'],
                       pendingChapters=[chapter['id'] for chapter in source_manifest['chapters'][len(selected):]],
                       completeTargetsAwaitingEarlierChapters=[chapter['id'] for chapter in source_manifest['chapters'][len(selected):]
                                                              if chapter['id'] in targets and targets[chapter['id']]['status'] != 'untranslated'])
    volumes = []
    for record in chapters:
        if not any(volume['id'] == record['volume'] for volume in volumes):
            volumes.append(dict(id=record['volume'], title=record['volumeTitle'],
                                chapters=sum(chapter['volume'] == record['volume'] and chapter['kind'] != 'reference' for chapter in chapters),
                                referenceTitle='Supplementary material'))
    manifest = dict(schema=1, id=SLUG, title=TITLE, author=AUTHOR, volumes=volumes,
                    totalWords=total, defaultChapter=chapters[0]['id'], glossaryCount=len(glossary),
                    correctionCount=0, editionVersion=EDITION, translation=translation, chapters=chapters)
    search = []
    for record in chapters:
        search.append({key: record[key] for key in ('id', 'index', 'title', 'volume', 'kind')} | {
            'paragraphs': [{'id': 'chapter-title', 'text': record['title']}] + [
                {'id': row.get('data-block'), 'text': common.norm(common.searchable(row))}
                for row in trees[record['id']] if row.get('data-block')]})
    template = (root / 'book-of-the-short-sun/index.html').read_text()
    library = load(root / 'library.json') if update_library else None
    destination = root / SLUG
    former_manifest = load(destination / 'manifest.json') if (destination / 'manifest.json').exists() else {}
    former_ids = {record['id'] for record in former_manifest.get('chapters', [])}
    # Complete validation above precedes every generated-file mutation.
    (destination / 'chapters').mkdir(parents=True, exist_ok=True)
    for index, record in enumerate(chapters):
        cid, tree = record['id'], trees[record['id']]
        write_json(destination / 'chapters' / (cid + '.json'), record | {'html': common.inner(tree)})
        nav = f'<a href="../../">Readers</a><a href="../index.html#{cid}">Reader</a><a href="../contents.html">Contents</a>'
        if index:
            nav += f'<a href="{chapters[index - 1]["id"]}.html">Previous</a>'
        if index + 1 < len(chapters):
            nav += f'<a href="{chapters[index + 1]["id"]}.html">Next</a>'
        heading = common.inner(static_note_tree(headings[cid], glossary))
        page = static_page(record['title'], common.inner(static_note_tree(tree, glossary)), nav, [], heading, record['volume'])
        (destination / 'chapters' / (cid + '.html')).write_text(add_status(page, translation))
    for filename, value in (('manifest.json', manifest), ('glossary.json', glossary), ('search.json', search)):
        write_json(destination / filename, value)
    template = template.replace('The Book of the Short Sun', html.escape(TITLE))
    template = template.replace('data-book="book-of-the-short-sun"', f'data-book="{SLUG}"')
    template = re.sub(r'<nav aria-label="Books" class="series-switch">.*?</nav>', '', template, flags=re.S)
    opening = common.inner(trees[chapters[0]['id']]).replace('src="../../assets/', 'src="../assets/')
    template = re.sub(r'<article\b[^>]*>.*?</article>',
                      lambda match: '<article class="chapter-body" id="chapter-body">' + opening + '</article>', template, flags=re.S)
    template = re.sub(r'<h1 id="chapter-title">.*?</h1>',
                      lambda match: '<h1 id="chapter-title">' + chapters[0]['headingHtml'] + '</h1>', template, flags=re.S)
    template = template.replace('chapters/blue-prelude.html', 'chapters/' + chapters[0]['id'] + '.html')
    template = re.sub(r'\?v=\d+', f'?v={EDITION}', template)
    (destination / 'index.html').write_text(add_status(template, translation))
    contents = ''.join(chapter_contents(chapters, volume) for volume in volumes)
    page = static_page(TITLE, contents, '<a href="../">Readers</a><a href="index.html">Reader</a>', []).replace('../../assets/', '../assets/')
    (destination / 'contents.html').write_text(add_status(page, translation))
    write_json(data / 'reader-integrity.json', dict(book=SLUG, source=source_manifest['source'],
               translation=translation, chapters=integrity,
               unmatchedGlossaryEntries=[entry['id'] for entry in entries if not counts[entry['id']]]))
    # Remove only former ORV chapter outputs after a valid shorter build.
    retained = {record['id'] for record in chapters}
    for cid in former_ids - retained:
        for suffix in ('.json', '.html'):
            path = destination / 'chapters' / (cid + suffix)
            if path.exists():
                path.unlink()
    book = {key: manifest[key] for key in ('id', 'title', 'author', 'volumes', 'glossaryCount', 'totalWords')}
    book.update(kind='book', translation=translation)
    if update_library:
        existing = next((index for index, item in enumerate(library) if item['id'] == SLUG), len(library))
        library = [item for item in library if item['id'] != SLUG]
        library.insert(min(existing, len(library)), book)
        write_json(root / 'library.json', library)
        build_library(root, library)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT, help='Readers repository directory')
    parser.add_argument('--data-dir', type=Path, help='ORV authoring data directory')
    parser.add_argument('--require-complete', action='store_true', help='Require targets for every source chapter')
    parser.add_argument('--update-library', action='store_true', help='Add or update the catalog entry')
    parser.add_argument('--minimum-status', choices=STAGES, default='mt-draft',
                        help='Render only chapters that have reached this review stage')
    args = parser.parse_args()
    try:
        manifest = build(args.root, args.data_dir, args.require_complete, args.update_library, args.minimum_status)
    except (BuildError, AssertionError, OSError) as error:
        parser.error(str(error))
    print(f'{SLUG}: {status_text(manifest["translation"])} {manifest["totalWords"]} words, '
          f'{manifest["glossaryCount"]} notes.')


if __name__ == '__main__':
    main()

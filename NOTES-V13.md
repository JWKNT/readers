# Version 13 — individual fiction readers

2026-09-30. Base release: `854c40b`.

## Scope and source selection

67 total readers: the six existing Sun/Liu readers, one complete-work reader for
The Fifth Head of Cerberus, and 60 distinct short-story readers. The new works
contain 408,369 narrative words and 94 sections including 31 optional afterwords.
Each reader has its own search index, glossary, source-linked static HTML, and
stable paragraph addresses. No anthology reader pages are created.

The 30 Best stories exclude its first Fifth Head novella as a separate reader.
The 30 remaining Endangered stories exclude A Cabin on the Coast, Kevin Malone,
The God and His Man, and The Detective of Dreams, which use the Best versions.
The Rose and the Nightingale joins source c33 and c34: the outer frame and inner
tale remain one work. House of Ancestors and Procreation retain their internal
sections. The incorrectly named Island EPUB contains another author's trilogy
and is wholly excluded at the owner's request.

Source headings repeated by the reader, empty conversion packaging, advertisements,
and the injected conversion-site footer are omitted. The Best afterwords are
separate reference sections, preserved without marginal annotations. The source
fraction and seven checkbox glyphs remain byte-identical, with meaningful alt text.

## Fifth Head source quality

The standalone EPUB is an OCR conversion. Its first novella omits 14 substantial
passages where its source has lone bullets. Comparison found those passages in
the supplied Best version, which is therefore used for the first novella.
The standalone files split by length rather than novella; verified boundaries
produce The Fifth Head of Cerberus, “A Story,” by John V. Marsch, and V. R. T.

The latter two novellas contain 10 and 34 lone bullets respectively. No second
supplied copy exists to establish whether these mark similar omissions; their
text is preserved as supplied, without invented repairs. Repeated tape dialogue
in V. R. T. is intentional and retained. Karel C�apek is repaired to Karel Čapek,
with the original in `data-original` and source metadata. This edition does not
claim a verified critical text for those two OCR sections.

## Margins and ornaments

386 externally sourced notes: 58 in Fifth Head, 155 in the Best stories, and
173 in the remaining Endangered stories. Sources cover language, historical
terms, science, religions, namesakes and other literature. Uncertain connections
start with “Possibly” in both the short and full note. No fictional biographies
or assertions about authorial intentions are supplied. Westwind receives no
forced notes merely to produce a quota.

Representative distinctions include the New Deal NRA in Parkroads, D’Annunzio's
Gioconda, Thoreau’s The Atlantides, Dunsany’s Sombelenë, Baum’s Nome King,
Arab/Egyptian titles and deities, gligua in Molina, and diakka in Andrew Jackson
Davis. Rex Stout's Nero Wolfe is an external fictional character; the validation
rule distinguishes that proper name from commentary about Gene Wolfe.

Title-only references such as Hyle and Peritonitis now work as normal marginal
notes. Their first appearances and search anchors use `chapter-title`. Original
epigraphs retain their role; decorated initials begin narration. Fictional email
addresses remain text and do not consume a name's first reference occurrence.

64 original small monochrome SVGs give each new work and Liu novel its own mark.
Source asterisks, bullets, image dividers and Best section-opening capitals
determine internal breaks. Original separator text remains hidden for exact
source comparison. A quiet end ornament serves stories without a source divider.
The 12 existing Sun ornaments and all 312 historical initials are unchanged.

## Validation

- `python3 tools/validate.py --baseline 854c40b`: passed across all 67 readers.
  Checks source hashes, metadata/counts, first occurrences, title notes, paragraph
  IDs, static equivalents, uncertainty wording, routes and local assets. Every
  existing Sun/Liu chapter retains exact text, word counts, offsets and IDs.
- Independent source review checked all 30 Best boundaries and afterwords, all
  30 Endangered texts and nested sections, and all three Fifth Head boundaries.
  Fixed malformed source drop-cap wrappers and the Eyeflash epigraph initial.
- `node --check assets/reader.js` and whitespace checks passed. The theme's 22
  existing behavior tests passed; no shared theme runtime changed.
- All 64 SVGs are distinct and valid; small paper/charcoal proofs reviewed.
  The decorator preserves text/attributes and is idempotent.
- Browser review at 1440px and 390px covered paper/charcoal, the alphabetical
  library, long titles, desktop title definitions, mobile touch definitions,
  search-to-paragraph navigation, contents dismissal/focus return, original
  HTML fallback, the corrected Eyeflash initial and Liu scene ornaments.
  Fixed the end ornament's inherited left alignment and static-header wrapping.
- External-source checks found no confirmed 404/410 links. Some museums and
  dictionaries block automated requests; some Gutenberg requests timed out.
  These are not reported as successful HTTP checks. Research evidence and
  context review remain in the authored note data.
- Native 200% browser text zoom and print preview were not exposed by this
  preview surface; neither is claimed as a completed browser check.

Public deployment verification is performed after the release commit; the
source commit is available in the repository history.

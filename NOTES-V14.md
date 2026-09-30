# Version 14 — expanded external-reference notes

2026-09-30. Audit baseline: `89b41da`.

## Scope and first research batch

The audit covers the three Liu novels, The Fifth Head of Cerberus, and all
60 standalone stories. New Sun, Long Sun, and Short Sun are excluded. The full
scope comprises 64 readers and 181 narrative sections; the 42 original reference
sections, including translator material and afterwords, are left unchanged.
This is an incremental research release, not a claim that the full audit is done.

The first batch adds 45 notes to 15 readers, supported by 40 distinct external
source URLs. Examples include ephemeris, armillary spheres, Möbius strip,
choralcelo, pochette, specula, hysteresis, ululant, stridulations, bordels,
keypunching, and indefectible. The source-linked short-gloss/full-definition
style is preserved. Context evidence is retained in authored annotation data;
interpretations of fictional events are omitted from definitions.

## Maintenance and preservation

`tools/rebuild_annotations.py` rebuilds annotations from the committed chapter
HTML using the existing importer’s matching and source-link rendering. It
requires no original EPUB, never rebuilds Solar Cycle readers, and does not
rewrite reference chapters or search indexes. Original inline footnotes and
translator notes retain the importer’s annotation exclusions.

Before adding notes, rebuilding all 64 readers twice produced byte-identical
tracked files. Four focused regression tests cover text/tail preservation,
original footnotes and links, annotation anchors, and static-page wrappers.

## Verification

- `python3 tools/validate.py --baseline 89b41da`: passed for all 67 readers,
  including exact chapter text, stable paragraph IDs, word counts and offsets,
  source integrity hashes, annotation occurrences, first appearances, and
  source-linked static HTML
- `python3 -m unittest discover -s tools -p 'test_rebuild_annotations.py'`:
  four tests passed
- `node --check assets/reader.js` and `git diff --check`: passed
- No shared reader CSS or runtime behavior changes

Further research batches and final coverage findings will be recorded here.

## Second research batch

Added 126 further notes to 35 readers. The cumulative enrichment is now 171
notes across 45 readers, supported by 158 distinct external source URLs.
Coverage includes Fifth Head vocabulary, meteorite mineralogy and structures,
naval history, musical and nautical terms, textile techniques, folklore,
foreign-language expressions, and uncommon descriptive vocabulary.

Context review distinguishes aigrettes as birds rather than plume ornaments,
gorget as an officer’s badge, and pricket as a candleholder. The ecliptic-plane
definition explicitly states its conventional astronomical meaning. Fractal
and muzhiks were omitted because their immediate prose already explains them;
Silhouette’s apparent “tegs” was rejected as an OCR trap.

All baseline-preservation and annotation checks and four regression tests pass
again for this batch. Solar Cycle, source-integrity, search, and reference
section files are unchanged.

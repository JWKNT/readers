# Reader typography and contextual annotation audit

2026-09-30. Baseline: `b7f9ac2`.

## Scope and results

This fresh pass covers all 79 catalog readers, 618 chapter/reference files and
2,754,839 incoming narrative words. All 3,817 incoming brief/full definitions
and their first rendered contexts were screened: 1,924 Solar Cycle, 1,027 other
Wolfe, and 866 Liu/Hyperion entries. The 79 original Liu author/translator notes
were checked to avoid duplicating them. Full-corpus character, punctuation,
spacing and OCR-pattern inventories were followed by contextual checks, selected
adjacent-paragraph reading and independent source research.

The release contains:

- 186 high-confidence, paragraph-addressed transcription repairs
- 44 selective new annotations, 15 definition/alias refinements, two misleading
  notes removed, and one duplicate consolidated; 3,858 final glossary entries
- Twelve search paragraphs repaired so verse, headings and transcript lines do
  not join words across visible line breaks
- An existing opening quotation mark made visible beside Beech Hill's drop
  capital, plus complete annotation targets across older Fifth Head repairs

The detailed reader-by-reader outcomes, changed definitions, exact repairs,
anchor movements and deferred typography are in
`data/annotation-audit-second-pass.json`.

## Editorial decisions

Repairs include 84 instances of the weapon misspelling `needier`, repeated
corruptions of established names, stray OCR letters and punctuation, fused words,
reversed or omitted quotation marks, and the digit in `Cald6 Bison`. The five Liu
repairs are authored against the retained Dark Forest source reader, then
assembled into Remembrance of Earth's Past. Every new repair uses a `v18-` ID
and retains its exact original text in `data-original`; `?wording=source` remains
available. No global quotation/dash normalization or design change was made.

Thirty-three uncertain missing sentence stops and one ambiguous `butťcould`
recovery remain untouched. The original EPUBs were not newly available for
collation: accepted repairs rely on unambiguous local grammar, repeated canonical
spellings and source-export evidence, rather than a claim of critical-edition
authority. Intentional dialect, unusual capitalization such as `midShipmen`,
invented vocabulary, and unresolved damaged readings remain.

Contextual annotation improvements include:

- Hyperion's Gulliver note now describes the Houyhnhnms voyage actually invoked
- Maui identifies the explicitly named Hawaiian island; de Kooning is qualified
  where the referent is uncertain; Hegira includes its general exodus sense
- Albedo's ordinary optical definition and the disavowed Cicero namesake note
  are removed; the two Bosch entries become one shared reference
- The color adjective in `Brown robe` and four fictional-city Buckminster
  occurrences are excluded, leaving the genuine historical/map references
- Palatine's possible hill reference, narthex's multiple attested senses, and
  the brief senses of anacreontic, proscenium and palinode are corrected
- Newly earlier coruscated and repaired Loganstone references receive the
  established notes; pard is consolidated under pardal

New notes include the Amelie Gravereaux rose, Mount Kaf, contextual weapon and
river vocabulary, string theory, nuclear magnetic resonance, accretion discs,
Verne's Propeller Island, and selected nautical/classical vocabulary. Terms with
insufficient exact-form evidence, including canjiah and shabbäbi, were withheld.
Cross-reader terms were never copied without checking their actual sense.

## Maintenance and verification

Non-Solar `excludeMatches` rules live with their authored entries. They require
an existing chapter/paragraph, an exact term or alias, a positive occurrence
count and unique surrounding context. Stale rules fail before annotation output
writes. The shared matcher is used by reimports and annotations-only rebuilds.

The Solar ledger also permits a narrowly scoped insertion with `old_id: null`:
the Loganstone rule checks one exact paragraph, spelling and character offset,
then retains the old later anchor. It does not globally rematch the definition.

`tools/rebuild_search.py` refreshes existing search records without changing
chapter content, schema or paragraph order. Importers, series assembly and
editorial maintenance share the same line-break-aware extraction. The validator
now checks every search paragraph against the rendered text.

Verification passed against the final content:

- 67 Python tests and four Node tests, JavaScript syntax and whitespace checks
- Full baseline validator, including static/search text, annotations, first
  appearances, word counts, original-note routes and local links
- Independent exact comparison of all 747 catalog/retained-source chapter files
  and 90,461 block records: only ledger-listed visible changes; exact underlying
  source and semantic structure; stable IDs; all prior repair spans retained
- Complete editorial, annotation, Solar, search and catalog replays; repeated
  outputs are byte-identical
- Actual generated first contexts checked for all new entries and relocated
  annotations; the five wrong Hyperion matches are absent

Live desktop/narrow-screen rendering and exact-commit deployment are checked as
part of publication. Native phone/Safari and print rendering are not claimed.
This is systematic screening and targeted research, not an uninterrupted new
close reading of every word, universal recertification of every old source URL,
or proof that every literary allusion has been found.

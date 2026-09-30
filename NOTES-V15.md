# Version 15 — transcription and typography

2026-09-30. Text audit baseline: `89b41da`. Release integrates the newer annotation commits
`c2acc84`, `8a29770` and `6a18472`, preserving their 340 additional notes.

## Editorial pass

335 paragraph-scoped repairs across 44 readers and 98 chapters:

- Long Sun: 104; Short Sun: 48; New Sun: 8.
- Fifth Head: 75; other new short-story readers: 99.
- Death’s End: 1. The other two Liu readers needed no wording changes.

The owner explicitly preferred reasonable correction of malformed EPUB text to
literal preservation of probable transcription errors. Repairs include broken or
fused words, OCR letter substitutions, missing apostrophes and quotation marks,
duplicated punctuation, and locally inferable omissions. A few examples are
`lightshoneonlyfitfully`, `sketclwnap`, `slirine ofScylla’s`, `Isn��t`, and the
detached initials in `Iknow` and `T his`. The alternate supplied Fifth Head text
corroborates *owed* for *owned* in the sentence about debts. The Hopkins epigraph
uses *havens* and the first stanza's full stop, checked against the poem.

Every repair has its exact original fragment, replacement, address and rationale
in `data/editorial-corrections.json`. Nineteen are explicitly marked probable.
`tools/editorial.py` replays these repairs after import, preserves inline emphasis
and annotation elements, and synchronizes static pages, initial fallbacks, search
text, word counts, offsets and integrity hashes. Original fragments remain in
`data-original`; the existing `?wording=source` view restores them.

Intentional forms remain, including Forlesen's name variations and invented time
unit, the child's misspelled invitation, the phonetic dialect in Seven American
Nights, and *Maser* in The God and His Man. Uncertain readings such as *quartanary*,
*tuber*, *anipotence* and *laggling* remain. Missing stretches of Fifth Head have
not been invented. A few damaged Long Sun sentence fragments still cannot be
reliably reconstructed; this is a corrective reading edition, not a critical text.

## Prose and verse presentation

- Five additional Best epigraph groups and the Silhouette opening extract have
  explicit epigraph styling. Ornamented initials stay at the start of narration.
  Poetry retains its lines and stanza breaks without source padding becoming
  extra blank lines.
- Dr. Stein's transcript reflows at the reader width, keeps speaker turns apart,
  and uses consistent labels. Fifth Head's split transcript labels and words
  rejoin visually while blank replies and all original fragment addresses remain.
- Restored verse roles in Pholus, Unicorn, Gingerbread and Silhouette; the two
  adjacent Pholus verse lines form one stanza. Source centering remains where
  meaningful.
- Email initials in The Tree Is My Hat join their italic text. Detective of
  Dreams' merged speaker turn becomes a separate line, corroborated by the
  duplicate story in Endangered Species. Every existing paragraph ID is retained.
- Consecutive OCR bullet markers share one visual divider; their source markers
  remain available for comparison. The existing ornaments and alphabets are unchanged.

## Validation

- `python3 tools/validate.py --baseline 89b41da`: all 67 readers / 547 chapters
  pass restored original wording, paragraph IDs, static equivalents, annotations,
  local links, word-count deltas, offsets and total-word checks.
- Independent review checked 63,636 searchable paragraphs and 223 source-integrity
  hashes. Reapplying the final correction ledger twice in a temporary copy changed
  none of the 1,202 files checked. Focused checks cover corrections crossing
  initials, italics, annotation spans and HTML entities.
- Generated fiction markup has balanced tags and no block elements inside
  paragraphs. Whitespace checks pass. The shared theme's 22 tests pass.
- The merge retains all 64 authored-note files byte-for-byte and all 2,393
  published glossary entries from `6a18472`. The full validator also passes
  against that baseline, and all 223 chapter integrity hashes match. Annotation maintenance now preserves nested
  correction spans; seven regression tests pass, with a separate text/repair
  preservation check across all 223 non-Solar reader chapters.
- Browser review at 1440px paper and 390px charcoal covers the corrected Hopkins
  epigraph/initial, mobile transcript reflow, retained paragraph anchors, search
  for a repaired word, search-to-paragraph navigation and source-wording recovery.
  A blank answer initially merged with the next transcript label was found and
  fixed. No horizontal overflow or broken images in the reviewed states.
- Native 200% text enlargement and print preview were not exposed by the preview
  surface; neither is claimed as completed visual validation.

Public deployment verification follows the release commit.

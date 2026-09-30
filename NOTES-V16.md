# Version 16 — Hyperion and series readers

2026-09-30. Initial baseline: `337d71b`; final integration baseline: `4559554`.

## Reader organization

- Hyperion and The Fall of Hyperion share `/hyperion/`, two volume groups,
  chapter navigation, continuous progress, and edition-wide search. The reader
  contains 54 narrative chapters, the Fall opening epigraph, and two optional
  dedications: 57 sections and 352,735 narrative/epigraph words.
- Remembrance of Earth’s Past now shares one reader at
  `/remembrance-of-earths-past/`. All three books, their part headings and their
  supplementary material remain separately identifiable. This is assembly only:
  all 129 source chapters, 12,884 paragraph addresses and 350 existing notes are
  preserved, with book prefixes added to the combined chapter and note IDs.
- The three former Liu entry URLs forward into the corresponding volume while
  retaining paragraph hashes and query parameters, including `wording=source`.
  Original plain HTML routes remain available. Authored note files and original
  text assets remain the assembly inputs.
- Endangered Species is the same source edition already imported. All 34 stories
  are represented: 30 independent readers and four duplicate stories already
  present from Best. The two source files of The Tale of the Rose and the
  Nightingale remain one story; internal story sections are not extra books.

## Research and text

The two Hyperion research files contain 174 and 135 authored entries. Twelve
shared referents are merged, producing 297 distinct notes in the combined reader.
These cover Keats and other literature, music, art, Greek mythology, religious
terms, Zen teachers, historical names, real geography, science, and uncommon
vocabulary. Sources favor original literature, museums, universities, religious
texts, scientific institutions and dictionaries. Notes identify external meanings;
uncertain namesakes begin “Possibly.” Invented terms without a useful external
referent are omitted, including a speculative Schrödinger explanation for Schrön.
Sources and occurrence evidence are stored with the authored entries.

Fourteen additional external notes are spread across seven Endangered stories.
They include river-nymph vocabulary, an APS journal, German academic terminology,
Soviet terms, historic media and real Alaskan communities. Existing definitions
are unchanged.

The correction ledger gains 39 entries: 15 in Hyperion, 21 in Fall, and three
quotation repairs in Endangered stories. Examples include Schwarzschild, Loewe,
Muses nine, abstruse, archaic, Aquinas, pro tem and several scrambled character
names. The Ming interview’s stray closing quote is marked probable. This brings
the full ledger to 374. Every repair retains its original fragment and address.
Deliberately deteriorating diary text, dialect, archaic verse, invented words and
the source’s historical claim about Keats’s age remain intact. OneWhose is a
source line break, not a transcription error; it remains two displayed lines and
is searchable as “One Whose.”

## Typography and artwork

The new reader preserves the six internal Tale headings, diary dates, italic
passages, poetry lines and stanza spacing. The Fall epigraph receives separate
quotation and attribution styles, with no narrative initial. The two volumes use
the approved Shadow and Urth alphabets and two original pen-drawn ornaments: a
thorned hourglass and a lyre with a falling star. Existing artwork is unchanged.

All 209 occurrences of source inline punctuation and equation images are retained
using their original nine image assets. They remain inline, receive accessible
descriptions, and stay legible in paper and charcoal modes. Print-page anchors and
heading images duplicated by chapter/part navigation are omitted. The three Fall
part images were inspected and contain only the part numbers and decorative rules.

## Maintenance and validation

- `tools/import_hyperion.py` builds from the two supplied EPUBs and replays the
  correction ledger. `tools/series_readers.py` assembles the Liu trilogy from its
  retained source readers. Neither EPUB is committed.
- Annotation maintenance recognizes complete corrected names while preserving
  nested correction spans, and recomputes first appearances and counts. It can
  update both new series without requiring the source EPUBs.
- All 66 readers / 604 sections pass the full validator against the baseline:
  original wording recovery, paragraph IDs, static equivalents, local links,
  notes, word counts and offsets. All 57 Hyperion sections match source hashes
  when documented corrections are restored. There are 2,763 notes overall.
- Eight annotation regression tests, three series-integrity tests and 25 theme
  tests pass. Syntax and whitespace checks pass. An independent source audit
  verified the Liu migration, Hyperion boundaries, all inline images and repeated
  builds. The final corrected import is byte-identical to the maintenance output;
  repeated Liu assembly is identical across 277 checked files.
- Browser review covers 1440px paper and 390px charcoal reading, inline equations,
  external-note popups, source-wording recovery, combined mobile contents and
  Escape focus return. A whole-edition search crosses from Hyperion into Fall
  and finds the line-broken Keats epitaph. Old Liu links retain the exact paragraph
  and original-wording query. Reviewed states have no horizontal overflow or
  broken images. Unrelated Sun links inherited by the mobile contents template
  were found and removed from both new combined readers.
- Native 200% text enlargement and print preview were not available in the
  browser surface; neither is claimed as completed visual validation.

The independent annotation audit at `4559554` was integrated before release. Its
authored additions and contextual revisions remain intact, including the three
Liu note files, which are copied into the combined reader without further research
or definition edits. The duplicate Odysseus proposal was omitted in favor of the
already-published Odysseus’s wax note.

Public deployment and file verification follow the release commit.

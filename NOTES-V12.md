# Readers v12 — 30 September 2026

Adds separate readers for Cixin Liu’s The Three-Body Problem, The Dark Forest,
and Death’s End. The library groups them under Remembrance of Earth’s Past.

## External references

| Reader | Notes | Marked occurrences | Reading sections | Supplementary sections |
|---|---:|---:|---:|---:|
| The Three-Body Problem | 89 | 499 | 35 | 5 |
| The Dark Forest | 59 | 177 | 8 | 2 |
| Death’s End | 76 | 333 | 75 | 4 |

The 224 notes explain external history, science, literature, art, language, or
vocabulary. They do not explain fictional characters, plot, or invented technology.
Tentative identifications begin “Possibly” in both the margin and the full note.
Original translator notes are retained separately and linked from their original
callouts. Inherited Sun glossaries and prose are unchanged.

Sources include museum collections, universities, NASA/ESA, CERN, national
archives, original literary works, publishers, and dictionaries. Each annotation
links to its sources. Ambiguous matches were checked in prose context: Planck’s
constant and the Planck satellite are separate; nanotechnology is distinct from
nanomaterials; the figurative “strong force of alienation” is not a physics match.
Translator-note-only names are excluded from the generated margins. The possible
Bester title echo and Newton namesake in Death’s End are qualified explicitly.

## Source conversion

The importer consumes the supplied omnibus EPUB; source files are not committed.
All 129 retained sections match the source text after whitespace normalization,
both before and after annotation. Narrative order and paragraph structure remain
intact. Chapter headings are presented once, while part dividers become contents
headings. Cover, welcome, duplicate contents, and publisher advertising are omitted.
Illustrations, emphasis, scene breaks, tables, original note callouts, and copyright
pages remain available. Character lists, era tables, notes, and postscripts appear
under Supplementary material. Table search indexes leaf blocks to avoid duplicate
results. The two exceptionally long Dark Forest sections retain their source
boundaries; each is loaded independently.

The authored notes are in `data/earths-past/`. Integrity reports hold source and
retained-text hashes. Rebuild with `tools/import_earths_past.py`; validate all six
readers with `python3 tools/validate.py --baseline 478de81`.

## Ornamental initials

Replaced 182 Long/Short Sun initials with seven complete historical alphabets:
Eileen (Nightside), Elzevier (Lake), Carrick (Caldé), Rothenburg (Exodus), Nouveau
Drop Caps (Blue), Acorn (Green), and Morris (Return). These provide actual engraved
foliage, interlace, and pen ornament rather than generic framed letters. The 130
New Sun SVGs, corresponding shape rules, and metrics are unchanged. Liu readers
reuse the approved Shadow, Claw, and Sword alphabets without modifying them.

CTAN provenance, source hashes, and LPPL notices accompany the assets. The rebuild
is deterministic. All seven alphabets were inspected A–Z and at reading size in
paper and charcoal. Edition URLs refresh the updated styles and initials for
existing browser sessions; the retired offline worker remains retired.

## Validation

- All six readers pass glossary counts, occurrence/first-appearance metadata,
  paragraph IDs, static-versus-interactive text, local files, and note-route checks.
- Existing 324 Sun sections preserve their prose and paragraph addresses against
  commit `478de81`; new sections pass retained-source hash checks.
- Independent conversion review checked all 129 new sections, original link
  fragments, and images. Duplicate table search results were corrected.
- Browser QA covered desktop and 390px mobile layouts, paper/dark themes,
  original footnote navigation, contents dialogs, search, keyboard definition
  activation, and representative Long/Short Sun initials. No horizontal overflow
  or failed images was observed. The two largest Dark Forest sections loaded
  and searched successfully.
- A source-link check caught three moved/retired endpoints; these were replaced
  with working primary-source pages or source packs. Some external sites reject
  automated HEAD requests; those responses are not treated as broken pages.
- JavaScript syntax, Python compilation, and `git diff --check` pass.

Release scope is JWKNT/readers only, main branch / repository-root GitHub Pages.
The pre-release revision is `478de819901d7251d467f80cd1a89cc11caa9876`.

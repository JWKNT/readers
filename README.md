# Books — local setup and hosting

This directory is a complete static website. It contains New Sun (including Urth),
Long Sun (four novels), Short Sun (three novels), and Cixin Liu’s Remembrance of
Earth’s Past trilogy (one reader), Dan Simmons’s Hyperion and The Fall of Hyperion
(one reader), The Fifth Head of Cerberus, and 73 individual short stories. No package installation,
build service, database, or account is required.

## Local test

With this folder at `~/Desktop/bin/readers`, run:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory "$HOME/Desktop/bin"
```

Open `http://127.0.0.1:8000/readers/`.

The book addresses are:

- `/readers/book-of-the-new-sun/`
- `/readers/book-of-the-long-sun/`
- `/readers/book-of-the-short-sun/`
- `/readers/remembrance-of-earths-past/`
- `/readers/hyperion/`
- `/readers/the-fifth-head-of-cerberus/`

The library links to every standalone story; `data/wolfe-fiction/catalog.json`
is the complete title and route inventory.
The supplied Strange Travelers adds thirteen individual story readers. Its two
duplicates, Bed and Breakfast and And When They Appear, retain their existing
Best of Gene Wolfe readers and afterwords. `data/wolfe-fiction/strange-travelers-catalog.json`
records the complete anthology mapping and retained source material.
The original `three-body-problem`, `dark-forest`, and `deaths-end` reader URLs
forward into the combined trilogy, preserving chapter/paragraph hashes and queries.
Their plain HTML chapters remain available at their original addresses.

Use an HTTP server rather than opening index.html directly. If instead you serve
this directory itself, the addresses have no initial `/readers` component.
Ctrl+C stops the server.

## Replacing an earlier version

Move the old directory aside before extracting this version; do not overlay it.
Otherwise obsolete pages will remain on disk. Hard-reload an old browser tab once.
The small retirement script only retires the earlier Readers offline worker and
its specifically named caches. It does not erase personal notes previously stored
by older versions. This version does not read or write those notes.

## Navigation

The left margin contains contents and current-page progress. The right margin
contains search and brief vocabulary notes. Hover an underlined word or its
marginal label for the full definition and source. Keyboard focus also opens it;
touch devices use a tap. Escape closes an open definition or dialog.

On narrow screens, Contents and Search move to the lower edge. Search defaults to the current chapter; its scope can be
expanded explicitly. Search and first-appearance annotations are independent for
each reader.

A chapter address uses `#chapter-id`; a paragraph address uses
`#chapter-id/paragraph-id`. The bare book address starts at the beginning.
There is no remembered reading position or account. Theme preference is inherited
from the original site. Original named-character lists, where supplied, remain
optional under each volume's “Names in the text”; these may contain spoilers.
The Liu novels keep original notes, character lists, era tables, and postscripts
in “Supplementary material.” Original footnote links also work within chapters.

## Plain HTML

Each book's `contents.html` links to complete ordinary HTML chapters. These remain
readable without JavaScript. The interactive version loads one chapter at a time;
search loads the selected book's search index only when needed.

## Files

`assets/` contains shared styles, scripts, decorative SVG illustrations, and the
original theme. Each book directory contains index.html, contents.html, chapter
JSON/HTML, manifest.json, glossary.json, and search.json. Vocabulary is stored as
short marginal glosses, full definitions, and independent source links. No
reference-guide files, font programs, editorial section, or audit pages are included.

This is a static export. A reproducible, source-specific importer for the supplied
Liu omnibus lives in `tools/import_earths_past.py`; it is not a general EPUB application. Typography changes
can be made in assets/reader.css. Preserve chapter/paragraph IDs when editing text.
Documented corrections retain their original strings in `data-original` attributes;
adding `?wording=source` before a chapter hash displays that wording.
Reviewed transcription repairs live in `data/editorial-corrections.json`; run
`python3 tools/editorial.py` to replay them after editing an older export. The EPUB
importers invoke this step automatically. Version 15 adds 335 repairs and restores
verse, epigraph, transcript and inline-emphasis formatting; see `NOTES-V15.md`.

To maintain annotations in the non-Solar-Cycle readers, edit the corresponding
JSON in `data/earths-past/`, `data/wolfe-fiction/`, or `data/hyperion/`, then run
`python3 tools/rebuild_annotations.py reader-id` (omit the ID to rebuild all).
This annotations-only rebuild uses the committed chapter text, requires no EPUB,
and leaves original notes, supplementary sections, and source metadata untouched.
Verify with `python3 tools/validate.py --baseline <previous-commit>` and
`python3 -m unittest discover -s tools -p "test_rebuild_annotations.py"`.
The unlinked `data/annotation-audit.json` records the 2026-09-30 audit scope,
chapter-by-chapter outcomes, and editorial corrections; `NOTES-ANNOTATION-AUDIT.md`
explains the method and verification.

To import only Strange Travelers, leaving the other source editions intact:

```sh
python3 tools/import_wolfe_fiction.py --strange-travelers /path/to/strange-travelers.epub
```

The importer also accepts repeated `--only story-slug` options. It preserves the
three named sections of Useful Phrases, poetry and epigraphs, inset letters and
diary entries, boxed notices, and Koshchei’s optional source note. Blank-line scene
boundaries use thirteen distinct original ornaments; drop capitals reuse the
approved historical alphabets. The supplied story files contain no inline images.
See [NOTES-STRANGE-TRAVELERS.md](NOTES-STRANGE-TRAVELERS.md) for the 255 new notes,
48 reversible transcription repairs, source boundaries and release checks.
The separate [Hyperion contents correction](NOTES-HYPERION-CONTENTS.md) restores
numbered chapters with indented jumps to the embedded Tales.

## Hosting

For a repository served at `/readers/`, put the contents of this directory in its
root. For a larger site, retain readers as a subdirectory. All local links are
relative. Keep `.nojekyll` when using GitHub Pages. The GitHub repository is https://github.com/JWKNT/readers. GitHub Pages serves
`main` from the repository root at https://jehlp.net/readers/.

The package contains complete copyrighted book texts. Keep it local or behind
actual access control unless you have permission to publish them. The noindex tags
are not access control. See NOTICE.md for content and artwork credits.

## Version 7

The unlinked `NOTES.md` records accepted typography decisions and annotation
research. It is plain Markdown, not an editorial section or an audit application.
Tentative references say “Possibly” in the definition itself. Short marginal glosses
remain separate from the full hover text. All earlier paragraph addresses are kept.

## Version 8

Expanded annotation coverage and corrected contextual glosses are documented in
`NOTES.md`. The individual readers retain chapter navigation and progress without
links to the other series. Verify the edition with `python3 tools/validate.py`;
add `--baseline 4dac1a4` to check preservation of the original chapter text.

## Version 10

The external-reference re-audit adds 318 series-specific notes and revises 41
existing entries, for 1,175 notes across the three readers. The margins explain
external meanings and possible namesakes, with “Possibly” in both short and full
notes where the connection is tentative. Research decisions and validation are
recorded in `NOTES-V10.md`. Original prose and paragraph addresses are preserved.

## Version 11

A further external-reference sweep adds 268 series-specific notes and revises 19
existing entries, bringing the total to 1,443. It expands saints, names, language
roots, historical vocabulary, and other externally attested references. Tentative
connections begin “Possibly”; prose and paragraph addresses are preserved.
[NOTES-V11.md](NOTES-V11.md) records the research and validation.

## Version 12

Adds three separate readers for The Three-Body Problem, The Dark Forest, and
Death’s End, with independent search and external-reference margins. The original
translator footnotes and illustrations remain available; packaging and publisher
adverts are omitted. Authored annotations are in `data/earths-past/*.json`; rebuild
with `python3 tools/import_earths_past.py /path/to/supplied-omnibus.epub`.
The EPUB is not stored in this repository. Text-integrity hashes record the retained
source text before annotation.

Long and Short Sun now use seven historical ornamental alphabets. New Sun’s five
approved alphabets remain unchanged. See `assets/initials/NOTICE.md` for artwork
provenance, licenses, and the deterministic rebuild command.

## Version 13

Adds The Fifth Head of Cerberus as one reader with three novella sections, plus
60 distinct short-story readers from the supplied Best and Endangered Species
EPUBs. Four duplicated stories appear once, using the Best text and afterword;
the first Fifth Head novella is incorporated into the full book. The mislabeled
Island EPUB is excluded entirely. The library lists stories alphabetically,
without anthology pages. Supplied afterwords remain optional reference sections.

There are 386 external-reference notes in the new readers. Relevant titles can
also carry notes, with the same keyboard, touch, margin and static-link behavior.
Each new work and each Liu novel has its own original thematic SVG ornament.

Rebuild from the supplied EPUBs (which are not stored here):

```sh
python3 tools/reader_ornaments.py
python3 tools/import_wolfe_fiction.py --best /path/to/best.epub --endangered /path/to/endangered.epub --fifth-head /path/to/fifth-head.epub
python3 tools/import_earths_past.py /path/to/earths-past.epub
python3 tools/validate.py --baseline 854c40b
```

Authored notes, catalog and source-integrity records live in `data/wolfe-fiction`.
See [NOTES-V13.md](NOTES-V13.md) for source-quality limitations and validation.

## Version 16

Hyperion and The Fall of Hyperion share one reader, contents and search, with
separate volume ornaments and external-reference margins. Supplied poetry,
diary sections, unusual inline punctuation and mathematical images are retained.
Remembrance of Earth’s Past is assembled into the same multi-volume structure;
its existing text and definitions are unchanged. Endangered Species already has
all 34 stories represented across its 30 distinct pages and four shared duplicates.

```sh
python3 tools/import_hyperion.py --hyperion /path/to/hyperion.epub --fall /path/to/fall.epub
python3 tools/series_readers.py
python3 tools/test_series_readers.py
python3 tools/validate.py --baseline 337d71b
```

`tools/series_readers.py` assembles the Liu trilogy from its retained source
readers. The Liu importer and annotation-maintenance command invoke it
automatically. If replaying editorial repairs against a retained Liu source,
run the assembly afterward. See [NOTES-V16.md](NOTES-V16.md) for this release.

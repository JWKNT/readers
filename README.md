# Books — local setup and hosting

This directory is a complete static website. It contains New Sun (including Urth),
Long Sun (four novels), and Short Sun (three novels). No package installation,
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
each of the three series.

A chapter address uses `#chapter-id`; a paragraph address uses
`#chapter-id/paragraph-id`. The bare book address starts at the beginning.
There is no remembered reading position or account. Theme preference is inherited
from the original site. Original named-character lists, where supplied, remain
optional under each volume's “Names in the text”; these may contain spoilers.

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

This is a finished static export, not an EPUB import application. Typography changes
can be made in assets/reader.css. Preserve chapter/paragraph IDs when editing text.
Documented corrections retain their original strings in `data-original` attributes;
adding `?wording=source` before a chapter hash displays that wording.

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

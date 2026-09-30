# Header Home navigation — 2026-09-30

All 912 HTML pages include one native, accessible Home link to
`https://jehlp.net/`. On the 909 pages with an existing appearance control,
Home and the theme button form one no-wrap header pair. The three redirect
aliases have a minimal, in-flow utilities header. Home remains usable without
JavaScript and scrolls away with its header.

The shared emblem and 44px target are vendored locally. Existing Readers
colors, typography, page-bound appearance position and book content remain
unchanged. Narrow plain-chapter headers wrap in normal document flow, with
matching top spacing so they cannot cover the chapter heading. The original Contents/Search mobile toolbar is restored with no
Home integration. The earlier floating dock, footer strip, body spacer and
focused-field scroll handler are removed.

Catalog, static export and redirect generators retain the native header
markup. Named cache versions survive numeric edition rebuilds. Prose,
annotations, paragraph IDs, search data and source records are unchanged.

## Checks

- 52 Python tests cover the edition plus eight header Home/export/cache contracts
- Four Node source-contract tests check header positioning, unchanged mobile
  toolbar behavior and removal of the footer/scroll behavior
- Full edition validation uses `python3 tools/validate.py --baseline b81c90a`
- All HTML content is compared byte-for-byte with the baseline after removing
  only added Home/header-pair markup and asset cache-key changes
- JavaScript syntax and `git diff --check` are checked before publication

Source and contract tests do not claim rendered browser or native iOS Safari
coverage. The header design is reviewed separately before publication.

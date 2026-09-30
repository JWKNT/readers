# Persistent Home navigation — 2026-09-30

Every one of the 912 HTML pages includes one native, accessible Home link to
`https://jehlp.net/` immediately after the opening body tag. This includes the
catalog, enhanced readers, plain chapters, contents, documentation and redirects.
The shared theme's house icon, 44px target, keyboard outline, safe-area offsets
and print hiding are vendored locally; existing Readers typography is preserved.

On narrow enhanced readers, the existing Home navigation moves between Contents
and Search in the bottom toolbar. Desktop restores that same element to its
standalone fixed corner. The toolbar is enabled only after reader JavaScript
wires it, leaving the standalone native Home visible without JavaScript. There
is no second Home or extra toolbar. Appearance controls still scroll with the
page.

The catalog/static export/redirect generators retain the native markup. The
shared theme, reader stylesheet and reader script have named cache versions,
which numeric edition rebuilds preserve. Prose, annotations, paragraph IDs,
search data, source records and all other page content are unchanged.

## Checks

- 51 Python tests pass, including seven new Home/export/cache regressions
- Four Node DOM unit tests cover desktop, mobile, repeated breakpoint changes
  and absent optional controls: `node --test tools/test_home_navigation.cjs`
- `python3 tools/validate.py --baseline b81c90a` passes all edition checks
- All 912 HTML pages match the baseline byte-for-byte after removing only the
  new Home markup and cache-key changes; no JSON data changed
- Both JavaScript syntax checks and `git diff --check` pass

These are source and DOM contract checks. They do not claim rendered browser
or native iOS Safari coverage; deployed browser review is performed separately.

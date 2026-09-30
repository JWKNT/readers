# Hyperion contents correction

2026-09-30. Baseline: 71dc166.

The source EPUB identifies Chapters 1–6, with each Tale beginning later inside
its numbered chapter. The original conversion used the Tale's role as the chapter
title and its subtitle as a second link, incorrectly splitting one heading across
two destinations. Parent links and chapter headings now use Chapter 1–6; indented
links give the complete Tale heading and jump directly to its original paragraph.

Both volumes use consistent single-label rows. Parts contain their chapter lists;
Fall's Epilogue sits outside Part Three. Each dedication is one secondary link,
without a redundant same-name disclosure. The plain HTML contents has the same
hierarchy and does not add misleading list numbers to Prologue or Epigraph.

All 57 chapter bodies, paragraph addresses, word counts, annotation anchors and
297 glossary entries are byte-preserved. Full baseline validation passes, as do
12 reader tests and JavaScript syntax/whitespace checks. A source audit confirmed
both embedded Tale boundaries and Fall's 15/15/15 chapter groups. Browser checks
cover desktop paper and 390px charcoal contents, Tale navigation, dialog close,
Escape focus return, and no horizontal overflow. Native enlarged-text and print
preview were not available. The existing Sun navigation contract remains intact.

# Readers mobile layout correction — 2026-09-30

- The interactive appearance header and plain-HTML navigation header were fixed
  to the viewport. Both are now document-positioned, so the theme control keeps
  its top-of-page location and scrolls away with the book instead of covering prose.
  Shared theme CSS, icons, persistence, accessibility and other sites are unchanged.
- Narrow-screen decorated initials now derive their height from three text lines,
  with room for the top inset, contour expansion and fractional-pixel clearance.
  The previous 4.65em artwork plus .16em top inset ended only .05em before the
  fourth line (at the reader's 1.62 leading). The supplied iOS Safari screenshot
  showed that fourth line still indented; Chromium did not reproduce the extra
  indent. The revised geometry does not depend on such a tight rounding boundary.
  The letter-specific shapes and aspect ratios are retained; the desktop and
  print sizes remain 4.65em.
- All reader stylesheet URLs have a new layout cache key, including the plain
  HTML pages and export templates. No prose, annotations, correction records,
  artwork, navigation targets or reader data were changed.

## Checks

- 37 Python unit tests pass, including four new CSS-contract regressions.
- Full `tools/validate.py --baseline c72917f` passes.
- Byte comparison confirms all 912 HTML edits change only the reader stylesheet
  cache key; every body is untouched.
- `git diff --check` passes.

The CSS-contract tests are not browser rendering tests. Browser review is
recorded separately after deployment; native iOS Safari is not available in this
execution environment, so the supplied screenshots are the Safari evidence.

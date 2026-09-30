# Solar Cycle annotation sources

The initial 1,443 definitions were migrated without changing their wording from
the published version-11 Solar Cycle glossaries at commit `97d6dcf`. Subsequent
reviewed additions and corrections are recorded in the annotation audit log. The original
repository is a static export and does not contain a Solar EPUB importer or a
separate earlier authoring dataset. See `NOTES-V11.md` for the research policy and
provenance. Only derived `occurrences` and `first` fields are omitted here.

Maintenance uses `python3 tools/rebuild_solar_annotations.py reader-id`, where the
ID is `book-of-the-new-sun`, `book-of-the-long-sun`, or
`book-of-the-short-sun`. This deliberately differs from the non-Solar rebuild:

- Existing annotation nodes are retained by ID, including their exact spellings,
  capital-only name decisions, formatting and reversible transcription repairs.
- Only new entries and newly added term/alias spellings are matched in unoccupied
  narrative text. A new spelling may legitimately become an entry’s first
  occurrence; its resulting first context must be reviewed.
- Definition/source edits refresh the corresponding static source links.
- Removing a definition unwraps only its annotation nodes, preserving their text
  and nested correction spans. Editing/removing an alias does not delete old
  anchors automatically. Any such targeted removal needs a separately reviewed
  change; a blanket rematch is intentionally unsupported. The reviewed
  `anchor-corrections.json` ledger guards those changes by chapter, paragraph,
  old ID and exact text, and fails on stale or ambiguous targets.
- A ledger row with `old_id: null` inserts one reviewed missing anchor at an
  exact paragraph and character offset. This supports newly repaired spellings
  such as Loganstone while retaining the original later anchor and avoiding a
  global rematch. Apply the editorial ledger before this annotation rebuild.
- New Sun’s five appendixes and the Long/Short Sun proper-name lists receive no
  new notes. Long Sun’s fictional “My Defense” and “Afterward” and Short Sun’s
  narrative “Afterword” remain eligible narrative material.

An unchanged migrated source produces no file writes. The migration was checked
byte-for-byte across all 667 Solar files. Independent recounting also reproduced
all 1,443 original note counts, first positions and chapter anchor lists exactly.
Run the unit tests and `python3 tools/validate.py --baseline previous-commit` after
changes, and separately verify exact visible text, addresses, decorative initials
and every `data-original` correction node. A successful general validator does
not replace contextual review of new first occurrences.

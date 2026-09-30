# Three further reader audits

2026-09-30. Baseline: `856785a`.

## Results

Three distinct passes produce 75 reversible, paragraph-addressed repair records,
12 new glossary entries, and six existing-entry refinements. Four false annotation
matches are removed; no complete glossary entry is removed. The final catalog has
3,870 notes. The exact edits, evidence, reader/chapter coverage and deferred
candidates are recorded in `data/annotation-audit-further-passes.json`.

### 1. Residual typography and source collation

Fresh character, lexical and residual-pattern inventories cover all 79 readers
and 618 chapter/reference files. Seven official publisher opening excerpts were
collated against 1,262 corresponding blocks, comprising 46,762 lexical tokens.
The original supplied EPUBs were not newly available. Publisher excerpts can
also contain defects; their bad joins and genuine edition differences were not
copied into the reader.

The 75 repair records have two deliberately distinct evidence levels:

- 28 have exact official publisher witnesses: 26 Long Sun, one Short Sun and
  one New Sun. They restore missing stops and interrupted-thought delimiters,
  missing letters, and corrupt readings such as `someone eke`, `well-toed`,
  `Proloctor` and `city’specifically`
- 40 New Sun apostrophe-to-dash repairs have individually reviewed, decisive
  paired-aside syntax. Seven further records repair eight `diem` occurrences
  where explicit plural antecedents require the object pronoun `them`.
  These 47 records do **not** claim an exact external witness

The latter cases received a separate independent contextual review. An observed
corruption mechanism did not authorize blanket replacement. Eighty unpaired or
ambiguous New Sun delimiter candidates remain untouched, as does the separate
uncertain `seating` reading. The Latin phrase `carpe diem` and valid `fo’c’sle`
are preserved. One of the earlier 34 formal deferrals is now source-resolved;
33 remain. The separately flagged `Proloctor` is also resolved by its exact
publisher context. Original text remains recoverable with `?wording=source`.

### 2. Annotation accuracy and ambiguous aliases

All 3,858 incoming brief/full definitions and first-context excerpts were
screened. The fresh inventory contains 54,977 rendered spans, including 15 in
headings; this is an inventory count, not a claim that every later paragraph was
close-read. Focused work additionally covers 143 cross-volume first contexts,
480 spans for 91 selected polysemous entries, and 63 New Sun `armiger` spans.

- Hyperion: the sailing-vessel note no longer attaches to `he barks`
- Hyperion: the biblical Abraham note excludes both Abraham Lincoln matches
- Hyperion: the Francis Bacon surname alias no longer annotates breakfast;
  the full philosopher reference remains
- Rachmaninoff: the note now distinguishes the opening Prelude from the later
  Second Piano Concerto
- New Sun: `calotte` retains its architectural meaning and adds the independently
  attested skull-vault sense required by a later passage

The two exclusions are exact chapter/paragraph/context rules. No other matches
are globally suppressed. Existing first anchors for these five entries stay put.
Unproved alternative senses and speculative alias removals remain withheld.

### 3. Missed vocabulary, named objects and direct references

The fresh discovery pass inventories every eligible block in all 562 narrative
sections, including preludes, epilogues and the narrative afterwords. It screens
unfamiliar word forms and selected named-reference, emphasis and quotation-cue
contexts, compares existing full terms and aliases across volumes, and reviews
all 79 original Liu notes to avoid duplication.

New entries cover `sikinnis`, `hobilers`, `pilani`, `thalamegii`, `crotaline`,
`maté` in two separate readers, `syrette`, `thermite`, `qipao`, `geta`, and the
explicit Genesis 37:9 quotation. Opened dictionary, primary-text, museum and
institutional sources support each. No plot interpretation is imposed.

Plain `flechette/flechettes` aliases are added to Hyperion's existing accented
entry, giving it the correctly earlier first at `hyperion-02/p-213` and three
additional valid matches. `maté` deliberately gains no unaccented `mate` alias.
`Geta` is defined without claiming that the character wears it; the prose says
she does not. The unusual `thalamegii` spelling is preserved.

The incoming catalog total is 2,754,838 words. The annotation-eligible total is
2,751,340; New Sun's five excluded appendixes contribute the 3,498-word difference.
Discovery inventories are not equivalent to uninterrupted close reading. Names,
emphases and the broad low-frequency inventory were selectively reviewed.

## Verification and limits

Local verification passes:

- 67 Python tests, four Node tests, JavaScript syntax and whitespace checks
- Full baseline validation of text, search, counts, firsts, original notes and links
- Independent exact preservation across 747 catalog/retained-source chapter files
  and 90,461 blocks: only the 75 ledger-listed changes in 72 blocks; underlying
  source, semantic structure, paragraph IDs and prior repairs preserved
- Complete editorial, non-Solar/Solar annotation, search and catalog maintenance
  replay; repeated output byte-identical
- Actual generated first contexts checked for all 12 additions and the relocated
  flechette note; all four false matches absent
- Shared CSS, runtime, catalog HTML, home links, mobile headers and theme unchanged

Exact-commit Pages deployment, live file equivalence and selected cloud-browser
checks are verified during publication. Native phone/Safari and print rendering
are not claimed. Existing external URLs were selectively reopened, not universally
recertified.

The yield is narrowing: the annotation passes found a small useful set after the
previous 1,206-note enrichment and 44-note follow-on. Fresh primary collation still
uncovered typography that token scans missed. Further repairs need new evidence
or genuinely new review methods; repeating the same scan does not establish an
edition's completeness, and uncertain text is not changed to reach a quota.

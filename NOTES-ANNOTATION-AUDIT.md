# Non-Solar-Cycle annotation audit

2026-09-30. Annotation research/count baseline: `89b41da`.
Final annotation-only preservation baseline: `337d71b`.

## Scope and first research batch

The audit covers the three Liu novels, The Fifth Head of Cerberus, and all
60 standalone stories. New Sun, Long Sun, and Short Sun are excluded. The full
scope comprises 64 readers and 181 narrative sections; the 42 original reference
sections, including translator material and afterwords, are left unchanged.
This is an incremental research release, not a claim that the full audit is done.

The first batch adds 45 notes to 15 readers, supported by 40 distinct external
source URLs. Examples include ephemeris, armillary spheres, Möbius strip,
choralcelo, pochette, specula, hysteresis, ululant, stridulations, bordels,
keypunching, and indefectible. The source-linked short-gloss/full-definition
style is preserved. Context evidence is retained in authored annotation data;
interpretations of fictional events are omitted from definitions.

## Maintenance and preservation

`tools/rebuild_annotations.py` rebuilds annotations from the committed chapter
HTML using the existing importer’s matching and source-link rendering. It
requires no original EPUB, never rebuilds Solar Cycle readers, and does not
rewrite reference chapters or search indexes. Original inline footnotes and
translator notes retain the importer’s annotation exclusions.

Before adding notes, rebuilding all 64 readers twice produced byte-identical
tracked files. Four focused regression tests cover text/tail preservation,
original footnotes and links, annotation anchors, and static-page wrappers.

## Verification

- `python3 tools/validate.py --baseline 89b41da`: passed for all 67 readers,
  including exact chapter text, stable paragraph IDs, word counts and offsets,
  source integrity hashes, annotation occurrences, first appearances, and
  source-linked static HTML
- `python3 -m unittest discover -s tools -p 'test_rebuild_annotations.py'`:
  four tests passed
- `node --check assets/reader.js` and `git diff --check`: passed
- No shared reader CSS or runtime behavior changes

Further research batches and final coverage findings will be recorded here.

## Second research batch

Added 126 further notes to 35 readers. The cumulative enrichment is now 171
notes across 45 readers, supported by 158 distinct external source URLs.
Coverage includes Fifth Head vocabulary, meteorite mineralogy and structures,
naval history, musical and nautical terms, textile techniques, folklore,
foreign-language expressions, and uncommon descriptive vocabulary.

Context review distinguishes aigrettes as birds rather than plume ornaments,
gorget as an officer’s badge, and pricket as a candleholder. The ecliptic-plane
definition explicitly states its conventional astronomical meaning. Fractal
and muzhiks were omitted because their immediate prose already explains them;
Silhouette’s apparent “tegs” was rejected as an OCR trap.

All baseline-preservation and annotation checks and four regression tests pass
again for this batch. Solar Cycle, source-integrity, search, and reference
section files are unchanged.

## Third research batch

The cumulative enrichment reaches 340 notes across 63 readers, using
323 distinct external source URLs. This batch includes primary-source grounding
for the Harlow effect and Kirlian photography; verified Hopkins, Tennyson, Luke,
and Hamlet references; historical textiles, musical instruments, naval rigging,
architecture, classical terminology, and further science and foreign vocabulary.

Context checks keep distinct the two Darwins in Pholus: Erasmus, the poet and
grandfather, and Charles, associated with the Beagle and natural selection.
Fifth Head’s pallets are beds, radiogram is a wireless message, and areaway is
a passage between building wings. Dendritic was withheld rather than inventing
a prehistoric era from a dictionary adjective. Possible name-play and quotation
echoes retain “Possibly” in both note lengths.

A live cloud-browser check of The Cat confirmed the new margin glosses, full
definition/source popup, and close/focus-return behavior in the existing visual
style. Exact text, IDs, counts, source metadata and original reference material
continue to pass the baseline checks. Full chapter coverage records are being
reconciled with the researchers’ documented systematic-sweep methods.

## Completed baseline-corpus audit

All 64 non-Solar-Cycle readers present at `89b41da` received a complete lexical
and named-reference inventory, comparison with existing notes, targeted
contextual review, and independently opened supporting sources. This covers
181 narrative sections originally comprising 930,940 narrative words. The final
annotation-only delta preserves the incoming corrected text (930,949 words)
and all 42 original reference sections exactly against `337d71b`. The chapter-by-chapter outcomes and rejections are recorded
in the unlinked `data/annotation-audit.json`. This method does not claim a new
line-by-line close reading or discovery of every subtle allusion.

The final addition count for this corpus is 400, using 384 distinct source URLs.
63 readers gained notes. On the Train received no forced additions: its Great
Circle reference was already covered and no other supported rare reference
earned a marginal entry. The 79 original Liu author/translator footnotes were
reviewed to avoid duplicating their explanations.

A second contextual review corrected seven existing entries and removed one:

- The Cat: removed the ordinary “triumphantly joyful” exultant gloss, which
  misleadingly annotated occurrences of a fictional social rank
- Our Neighbour: sere now covers the actual description of a person
- The Map: nones includes historically attested midday usage, consistent with
  the dialogue, alongside the original ninth-hour office
- Rose and Nightingale: the brief Gharib/Ajib note identifies both as figures,
  rather than labeling the antagonist a hero
- And When They Appear: Saint Wilfrid’s name corrected from Wilfred; the
  Father Eddi note now links directly to Kipling’s poem and its publication notes
- Death’s End: removed artist/author-name aliases from the Starry Night and
  Maelstrom title entries; linked the latter directly to the museum’s story page
- Death’s End: clerical script’s pre-Han origins and Han usage distinguished

The new achondrite brief gloss was also tightened to specify chondrules.
This produces 400 additions and one removal, a net increase of 399 notes.

Repeated names that later label fictional spacecraft, such as Sirius, Newton,
and Einstein, retain valid first-reference definitions. Later inactive token
matches remain grouped in occurrence metadata; no fictional biographies or
claims about naming intent were added.

Final local verification passed: full baseline validation across all 67 readers,
seven regression tests, an idempotent annotations-only rebuild, protected-file
checks, JavaScript syntax, and whitespace checks. Remote commit and deployment
verification follow publication.

## Integration with transcription and typography changes

Before the closing annotation commit, remote main advanced to `337d71b`,
containing the separately authorized Version 15 corrections and formatting.
Those incoming edits were retained in full. Only authored annotation changes
and this audit record were replayed; stale generated chapters were not restored.
The incoming annotation-maintenance tool preserves nested correction spans and
passed its seven regression tests.

Two baselines are intentionally distinguished:

- The three earlier annotation batches preserved exact text against `89b41da`
- The final annotation-only delta preserves all 223 incoming non-Solar chapter
  texts, original-repair strings, paragraph IDs, word counts and offsets exactly
  against `337d71b`; incoming Solar Cycle, reference, search, integrity and
  typography files remain unchanged

`tools/validate.py --baseline 337d71b` passes across all 67 readers. A stricter
comparison of visible text and repair attributes also passed for every non-Solar
chapter. The annotation audit log has a distinct name so it does not compete
with the edition-numbered release notes.

## Hyperion and The Fall of Hyperion

The incoming series reader received a bounded lexical/reference audit across
all 55 narrative sections (352,735 words), with both dedications excluded.
The combined 297-note glossary and all aliases were checked before additions.
Duplicate cross-volume vocabulary and repeated quotation openings were merged,
then actual first visible contexts were reviewed across both books. Detailed
coverage is in `data/annotation-audit-hyperion.json`.

The audit adds 221 notes, corrects or refines 13 original entries, and removes
two misleading surname glosses: Magritte as the painter and Aspic as food.
The resulting series glossary has 516 entries. Strong additions include verified
poem openings, map projections, poetic meter, clinical and scientific terms,
church architecture, historical references, and uncommon contextual vocabulary.
New-note source URLs total 223. Nimbus was withheld where its first occurrence names
a fictional plant; King Tut was omitted as a low-value familiar nickname.

Paired-reference glosses now cover both referents rather than labeling one as
the other. Somme is first the river in a 1415 context, not the 1916 battle.
Oort-cloud, cislunar and ecliptic wording avoids forcing an Earth-only referent
on fictional systems. Bar mitzvah replaces an unhelpful partial-word match.

A narrow maintenance fix annotates complete words or phrases crossing existing
repair spans. It preserves every visible character, `data-original` value,
correction marker and paragraph address; it does not bridge arbitrary emphasis,
links, original notes or initials, and does not split a repair. Five regression
cases cover insertions, deletions, protected spans, partial repairs and repeated
matches. Full validation and strict 57-file text/repair comparisons passed.

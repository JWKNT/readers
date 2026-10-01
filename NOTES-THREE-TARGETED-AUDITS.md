# Three targeted reader audits

2026-10-01. Baseline: `0451fc5`.

## Results

Three further, distinct passes produce three reversible transcription repairs,
five new source-identification notes, and five existing-note improvements. No
complete entry or existing match is removed. All 79 catalog readers are covered
by fresh screening; the final catalog has 3,875 notes and 55,001 annotated spans.
Exact changes, source URLs, coverage and negative decisions are recorded in
`data/annotation-audit-targeted-passes.json`.

### 1. Unresolved readings and new source collation

A new long-phrase repetition screen covers all 618 chapter/reference files.
279 candidate windows in 242 blocks were reviewed without automatic deletion.
Seven additional official publisher excerpts were collated against 936 local
blocks and 31,850 lexical tokens. These cover new material from Green, Urth,
Bluesberry Jam, Three-Body, Dark Forest, Hyperion and Fall; they do not repeat
the seven excerpts collated in the preceding audit.

None of the publisher differences justifies a new novel-source repair. Several
excerpts themselves contain OCR defects, word joins or typographic variants.
They are not copied into the readers. Green, Three-Body and Fall agree lexically
through their collated ranges.

The three accepted, independently reviewed mechanical repairs are:

- Fifth Head: `After that lie only sang` becomes `After that he only sang`
- Short Sun: `Babbie and I and going` becomes `Babbie and I are going`
- Urth: the stray stop in `puts the Stars to. Flight` is removed

The first two have decisive local syntax. The third is also corroborated by the
quoted FitzGerald poem, not by a newly collated edition of Wolfe's novel. All use
`v20-` repair IDs and retain original characters in `data-original` for
`?wording=source`. No broad punctuation or spelling normalization is introduced.

All 33 formal deferrals and 80 ambiguous New Sun delimiters remain untouched.
A newly detected repeated clause at `shadow-06/p-071` is also withheld pending
an independent edition witness.

### 2. Annotation edge cases

The fresh inventory covers 3,870 incoming definitions and 54,990 spans. Targeted
review tests materially different aliases, a new 36-entry/425-span polysemy set,
strong factual claims and all 15 title spans. The overlapping screening sets are
not summed as if they were unique close-read passages.

Long Sun's `gammadion` note now includes a single gamma-shaped ornament as well
as the assembled cross. The later prose explicitly distinguishes four pieces
from the cross. The Century Dictionary and a Cleveland Museum textile record
support the additional sense; all 24 matches and the original first stay put.

Several attractive changes were rejected. In particular, the plural `balusters`
can mean a balustrade, so its existing note was not incorrectly narrowed. No
surname alias is removed merely because it later names a fictional person or
place; the actual reference and the note's wording determine the decision.

### 3. Overlooked direct references

Fresh phrase-cue screening covers all 562 annotation-eligible sections and
2,751,380 current words. 356 flagged context excerpts were screened, with
selected adjacent verse and quotation passages checked against primary texts.
The five new notes identify:

- FitzGerald's opening Rubáiyát stanza in Urth
- The paraphrased gate-of-Hell inscription from Dante's Inferno III
- The Wodhull/Euripides quotation in Fifth Head
- The Pope/Iliad IX couplet in The Woman the Unicorn Loved
- Keats's July 1818 prose-letter self-description, “five feet high,” in Hyperion

David's `fourfold head` is preserved: the source has `triple-head`, but the next
paragraph makes the changed count a joke. The uncertain `dog. With` punctuation
is not silently rewritten. Hyperion's description of Keats's prose as verse is
also left in the fiction; the note supplies the original source.

Four existing notes improve their source or matching precision: Bacon now points
to Novum Organum I.43; Adam's dream connects to the earlier quotation from the
same Bailey letter; the shorter street-quarrel quotation joins the existing
Keats letter note; and the Enoch Arden note begins at the excerpt's actual opening.
The Adam's-dream first moves to `hyperion-03/p-084`; Tennyson moves from `p-520`
to `p-516`. The superior-beings first remains `hyperion-05/p-788`.

## Verification and limits

Local release checks pass:

- 67 Python tests, four Node tests, JavaScript syntax and whitespace checks
- Full baseline validator for text, search, counts, firsts, original notes and links
- Exact comparison of 747 retained/catalog chapter files and 90,461 blocks:
  only the three ledger-listed visible changes; source, semantic structure,
  paragraph IDs and every previous repair preserved
- All generated new/refined entries, actual first targets and unchanged glossary
  entries verified; eleven additional valid spans, no removed spans
- Complete editorial, annotation, Solar, search and catalog replay; repeated
  output byte-identical
- Independent comparison of all 912 HTML documents and 454 protected files;
  source text, structure, original links, navigation and theme controls preserved
- Shared CSS, reader runtime, landing-page HTML, home controls, mobile headers
  and theme byte-identical; only existing edition metadata advances

Independent preservation/replay review also passes. Exact-commit Pages deployment,
deployed file equivalence and selected live cloud-browser reading checks form the
final publication checks. Native phone/Safari and print rendering are not claimed.
Existing external sources were selectively reopened, not universally recertified.

The yield is diminishing. New primary-source work still identifies useful exact
references, but another broad lexical scan would mostly repeat previous work.
These passes do not establish a complete critical edition or identify every
possible literary allusion. Uncertain text is not changed to reach a quota.

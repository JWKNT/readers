# Strange Travelers readers

2026-09-30. Initial baseline: 9c80028 (the separately released Hyperion contents repair).
Final integration baseline: 200397e, preserving the concurrent shared-theme rollout.

## Scope and source treatment

The supplied Strange Travelers EPUB contains fifteen stories. Thirteen are new
standalone readers; Bed and Breakfast and And When They Appear retain their
existing Best of Gene Wolfe readers and optional afterwords. There is no anthology
reader. The library now contains 73 independent short stories and 79 readers total.
The source EPUB remains outside Git.

The new material has fourteen sections: thirteen story texts and the bracketed
Koshchei source note, which remains a separate optional reference. The import
preserves the A Tale of Old Russia subtitle, No Planets Strike's Hamlet epigraph,
Useful Phrases' three internal headings, song and verse lines, letters, diary
entries and boxed notices. Source blank-line scene breaks receive distinct
story-specific ornaments. Thirteen original SVG drawings reuse the established
pen-line style, and opening initials use the approved historical alphabets.
There are no narrative image assets in these source files.

All retained source prose was independently compared with the EPUB before any
recorded corrections; normalized text matched exactly. Publisher packaging,
collection-level dedication and copyright material are omitted. The complete
fifteen-story mapping is in data/wolfe-fiction/strange-travelers-catalog.json.

## Research and correction policy

Margins identify external words, sources, people, places and historical or cultural
references. They omit explanations of the invented world and invented languages.
Uncertain connections start “Possibly” in both short and full descriptions. Every
note includes external sources and an occurrence record in the authored JSON.
The final build adds 255 external-reference notes. Coverage includes Russian and
Senegalese folklore, traditional songs, Latin poetry, literary quotations, real
geography, historical names, brands, scientific terms and unusual vocabulary.
Ambiguous title coincidences and unsupported name guesses are omitted.

The correction ledger adds 48 repairs, including Balts, snowshoes, musical bass,
misspelled recurring names, missing punctuation and fused compounds. Two small
dialect-adjacent repairs are marked probable. Every original fragment remains
recoverable through the source-wording query; intentional dialect, variant song
lyrics and the grammatical “those who had had dropped” remain intact. The new
stories contain 96,580 narrative words after corrections.

The importer reapplies annotation matching after corrections. The Balts entry
recognizes its source typo Baits so all four occurrences—including the corrected
first appearance—retain complete word annotations and source restoration.

## Maintenance and validation

The importer supports --strange-travelers and repeated --only arguments, allowing
this source to be rebuilt without rewriting earlier books. It also produces
canonical reader URLs, search indexes and standalone HTML with real section links.
Source hashes, stable paragraph addresses and reversible corrections support
subsequent annotation-only maintenance.

Initial validation: all thirteen source texts match the supplied edition;
original duplicate routes are untouched; three anthology-specific integrity tests
pass. Desktop paper review covers epigraph, subtitle, initial and source-note
presentation. At 390px in charcoal, Useful Phrases' contents opens, its section
link navigates to the proper heading and closes the dialog, and the centered
notice stays within the page without horizontal overflow.

Final validation passes for all 79 readers / 618 sections and 3,018 notes, with
exact prior-text recovery against 200397e, stable paragraph addresses, static
equivalents, search indexes, links, annotation counts and source hashes. Fifteen
reader tests and 25 theme tests pass, as do syntax and whitespace checks. All
authored note data is present in the generated glossaries without definition or
source loss. A complete corrected source reimport reproduces all 108 checked files
byte-for-byte. An independent audit checked all 1,565 files in the original
66 reader folders against 200397e, with no changes, and separately reconstructed
all fourteen new sections directly from the EPUB. It verified every authored
note, annotation flag, correction ID, static text and local route. Public
verification follows the release commit.

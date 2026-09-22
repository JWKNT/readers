# External-reference re-audit — version 10

The margins explain external words, namesakes, languages, history, mythology, and natural history. They do not identify fictional characters or explain the plot. Possible derivations and namesakes begin with “Possibly” in both the brief gloss and the full definition. A dictionary meaning is distinguished from a proposed connection.

Lexicon Urthus and Gate of Horn, Book of Silk supplied research leads. Accepted notes were checked against independently linked dictionaries, classical texts, scholarly studies, church traditions, museum collections, and botanical or zoological references. The notes use original concise wording. Neither supplied guide nor extracted reference text is included in the site.

## Scope and counts

| Series | Before | Added | Existing entries revised | After |
|---|---:|---:|---:|---:|
| New Sun | 454 | 154 | 27 | 608 |
| Long Sun | 182 | 78 | 2 | 260 |
| Short Sun | 221 | 86 | 12 | 307 |

There are 1,175 series-specific notes, with 318 additions and 41 revisions to existing entries. A reference appearing in multiple series is counted separately in each. Revised entries include definition corrections, uncertainty wording, and a few missed inflection/spelling aliases. All 324 chapters retain their reading text and paragraph addresses.

## Editorial checks

- Expanded New Sun saints and religious names, classical mythology, Latin names and place roots, obsolete clothing, arms, natural history, and uncommon vocabulary. Saints’ legendary biographies are presented as traditions; the notes do not claim a proven fictional identity.
- Expanded Long and Short Sun botanical and zoological names, Arabic, Hindi, Urdu, Dutch, Italian, Irish, Swahili, Turkish, Finnish, and classical-language references. Shared references are added to each series only after checking actual prose occurrences.
- Corrected misleading guide leads: Siyuf is plural swords; Qarya is Arabic; Torda has an attested old Swedish razorbill sense; Rimah is plausibly Arabic spears. Used prose spellings such as Exmoor and Ushujaa.
- Context review refined saros (ancient 3,600-year period and eclipse cycle), mensal (table and church revenues), notule (possible noctule bat and French brief note), nizam (Ottoman soldier and Hyderabad ruler), clarion (trumpet and ringing voice), and mizzen (mast and sail).
- Replaced the weak Barbatus saint connection with the external Latin meaning and a carefully described Augustine passage; qualified the Moly herb connection. Removed interpretive wording from dimber and chrasmologic.
- Shiprock, inhumi, and the other in-world-only entries removed in version 9 remain excluded. Unverified or mismatched leads such as Wichote, Toter, and a supposed cavalry sense of bacele were not turned into assertions. Canna in Short Sun is dialect for cannot and was not annotated with the plant definition.

## Validation

`python3 tools/validate.py --baseline 4dac1a4` checks chapter text preservation, paragraph IDs, annotation and first-appearance counts, manifest/library agreement, JSON/plain-HTML agreement, local links, static source targets and tooltips, external-source presence, and uncertainty qualifiers. `git diff --check` checks whitespace.

First-occurrence paragraphs were reviewed for every addition across the three readers. Browser checks covered the new Katharine and Siyuf popups at desktop size, Pajarocu at 390px without horizontal overflow, source links, Escape dismissal, and theme switching. No browser console errors were observed. The reading layout and runtime are unchanged.

## Added references

These are first locations within each series. The first linked source is listed here; entries may have additional sources in the glossary.

### New Sun

- **Abdiesus** — Possibly Saint Abdiesus, a Persian Christian martyr. First: `shadow-13/p-024`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n23/mode/2up?q=Abdiesus).
- **Herena** — Possibly Saint Herena, an African martyr. First: `urth-28/p-037`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n107/mode/2up?q=Herena).
- **Guasacht** — Possibly Saint Guasacht, an early Irish bishop. First: `citadel-19/p-028`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n152/mode/2up?q=Guasacht).
- **Pia** — Possibly Saint Pia, an early African martyr. First: `sword-28/p-027`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n232/mode/2up?q=Pia).
- **Zama** — Possibly Saint Zama, an early bishop of Bologna. First: `urth-31/p-036`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n295/mode/2up?q=Zama).
- **Becan** — Possibly Becan, an early Irish monastic name. First: `sword-14/p-044`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n64/mode/2up?q=Becan).
- **Barnoch** — Possibly Saint Barrog, the hermit associated with Barry Island. First: `claw-01/p-015`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n61/mode/2up?q=Barnoch).
- **Cyby** — Possibly Saint Cybi, associated with Holyhead. First: `shadow-06/p-016`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n94/mode/2up?q=Cyby).
- **Piaton** — Possibly Saint Piaton, missionary and martyr at Tournai. First: `sword-25/p-010`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n242/mode/2up?q=Piaton).
- **Llibio** — Possibly Saint Llibio, remembered in Anglesey. First: `sword-31/p-004`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n188/mode/2up?q=Llibio).
- **Ouen** — Possibly Saint Ouen, seventh-century bishop of Rouen. First: `shadow-26/p-029`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n56/mode/2up?q=Ouen).
- **Eskil** — Possibly Saint Eskil, a missionary to Sweden. First: `urth-35/p-019`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n118/mode/2up?q=Eskil).
- **Lomer** — Possibly Saint Lomer, a sixth-century French abbot. First: `claw-15/p-003`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n189/mode/2up?q=Lomer).
- **Eusebia** — Possibly Saint Eusebia, a martyr remembered at Bergamo. First: `claw-01/p-002`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n122/mode/2up?q=Eusebia).
- **Severa** — Possibly Saint Severa, an abbess at Trier. First: `sword-14/p-018`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n264/mode/2up?q=Severa).
- **Thais** — Possibly Saint Thaïs, an Egyptian penitent. First: `urth-44/p-027`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n274/mode/2up?q=Thais).
- **Merryn** — Possibly Saint Merinus or Merryn, an Irish monastic saint. First: `claw-30/p-031`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n216/mode/2up?q=Merryn).
- **Stachys** — Possibly Stachys, named in Paul’s Epistle to the Romans. First: `claw-01/p-001`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n270/mode/2up?q=Stachys).
- **Jader** — Possibly Saint Jader, an African bishop sent to the mines. First: `sword-03/p-030`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n222/mode/2up?q=Jader).
- **Chuniald** — Possibly Saint Chuniald, a companion of Rupert of Salzburg. First: `claw-10/p-046`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n86/mode/2up?q=Chuniald).
- **Jurmin** — Possibly Saint Jurmin, an East Anglian prince. First: `sword-09/p-009`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n180/mode/2up?q=Jurmin).
- **Nennoc** — Possibly Saint Nennoc, an abbess of Brittany. First: `citadel-07/p-021`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n222/mode/2up?q=Nennoc).
- **Modan** — Possibly Saint Modan, a Scottish monastic saint. First: `urth-11/p-034`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n218/mode/2up?q=Modan).
- **Leocadia** — Possibly Saint Leocadia, a martyr of Toledo. First: `claw-15/p-010`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n187/mode/2up?q=Leocadia).
- **Marcellina** — Possibly Saint Marcellina, sister of Ambrose of Milan. First: `shadow-12/p-020`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n199/mode/2up?q=Marcellina).
- **Talarican** — Possibly Saint Talarican, a missionary bishop in Scotland. First: `shadow-14/p-049`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n273/mode/2up?q=Talarican).
- **Werenfrid** — Possibly Saint Werenfrid, a missionary among the Frisians. First: `shadow-33/p-011`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n292/mode/2up?q=Werenfrid).
- **Manahen** — Possibly Manahen, a prophet and teacher at Antioch. First: `claw-29/p-026`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n198/mode/2up?q=Manahen).
- **Barbea** — Possibly Saint Barbea, a martyr of Edessa. First: `shadow-09/p-008`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n60/mode/2up?q=Barbea).
- **Ibar** — Possibly Saint Ibar, an early Irish missionary. First: `citadel-18/p-016`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n162/mode/2up?q=Ibar).
- **Lactan** — Possibly Saint Lactan, an Irish monastic founder. First: `citadel-19/p-038`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n183/mode/2up?q=Lactan).
- **Loman** — Possibly Saint Loman, bishop of Trim. First: `shadow-06/p-094`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n189/mode/2up?q=Loman).
- **Maruthas** — Possibly Saint Maruthas, a bishop active in Persian Christianity. First: `shadow-13/p-037`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n206/mode/2up?q=Maruthas).
- **Nilammon** — Possibly Saint Nilammon, an Egyptian recluse. First: `shadow-05/p-045`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n225/mode/2up?q=Nilammon).
- **Sebald** — Possibly Saint Sebald, a hermit honored at Nuremberg. First: `claw-02/p-009`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n261/mode/2up?q=Sebald).
- **Solange** — Possibly Saint Solange, a French shepherdess and martyr. First: `claw-24/p-078`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n269/mode/2up?q=Solange).
- **Cinnia** — Possibly Saint Cinnia, an Irish princess and nun. First: `urth-29/p-005`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n86/mode/2up?q=Cinnia).
- **Ceallach** — Possibly Saint Ceallach, an early bishop of Killala. First: `urth-33/p-040`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n83/mode/2up?q=Ceallach).
- **Abban** — Possibly Abban, the name of early Irish abbots. First: `shadow-25/p-014`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n23/mode/2up?q=Abban).
- **Hadrian** — Possibly Saint Hadrian, a soldier-martyr of Nicomedia. First: `shadow-11/p-003`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n153/mode/2up?q=Hadrian).
- **Fausta** — Possibly Saint Fausta, a young martyr of Cyzicus. First: `citadel-07/p-009`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n128/mode/2up?q=Fausta).
- **Eusignius** — Possibly Saint Eusignius, a veteran soldier and martyr. First: `shadow-03/p-020`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n123/mode/2up?q=Eusignius).
- **Epicharis** — Possibly Saint Epicharis, an early Christian martyr. First: `citadel-10/p-032`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n116/mode/2up?q=Epicharis).
- **Decuman** — Possibly Saint Decuman, a Welsh hermit in Somerset. First: `sword-21/p-024`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n100/mode/2up?q=Decuman).
- **Bregwyn** — Possibly Saint Bregwin, an archbishop of Canterbury. First: `urth-29/p-005`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n73/mode/2up?q=Bregwyn).
- **Winnoc** — Possibly Saint Winnoc, an abbot honored in Flanders. First: `citadel-12/p-001`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n294/mode/2up?q=Winnoc).
- **Abundantius** — Possibly Saint Abundantius, a deacon-martyr of Rome. First: `sword-21/p-016`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n24/mode/2up?q=Abundantius).
- **Chad** — Possibly Saint Chad, a seventh-century English bishop. First: `claw-01/p-001`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n84/mode/2up?q=Chad).
- **Gildas** — Possibly Gildas, author of On the Ruin of Britain. First: `shadow-11/p-008`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n147/mode/2up?q=Gildas).
- **Odo** — Possibly Saint Odo, a reforming abbot of Cluny. First: `shadow-03/p-008`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n226/mode/2up?q=Odo).
- **Jovinian** — Possibly Saint Jovinian, a Christian lector and martyr. First: `shadow-29/p-024`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n176/mode/2up?q=Jovinian).
- **Hormisdas** — Possibly Pope Hormisdas, who reconciled Rome and Constantinople. First: `citadel-35/p-065`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n160/mode/2up?q=Hormisdas).
- **Mamas** — Possibly Saint Mamas, a martyr honored in Cappadocia. First: `citadel-26/p-017`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n197/mode/2up?q=Mamas).
- **Phocas** — Possibly Saint Phocas, a bishop-martyr of Sinope. First: `claw-15/p-010`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n241/mode/2up?q=Phocas).
- **Mannea** — Possibly Saint Mannea, remembered with her family. First: `citadel-14/p-030`. [Source](https://lapide.org/baronius_caesar/De_Martyrologio_Romano.html).
- **Thea** — Possibly Saint Thea, a martyr of Gaza. First: `shadow-01/p-049`. [Source](https://nominis.cef.fr/contenus/saint/9902/Saintes-Th%C3%A9a-et-Meuris.html).
- **Gundulf** — Possibly a Germanic name formed from “battle” and “wolf.” First: `citadel-07/p-002`. [Source](https://dmnes.org/name/Gundulf).
- **Erblon** — Possibly Saint Hermeland, also known as Herbland. First: `citadel-19/p-028`. [Source](https://gertrude.paysdelaloire.fr/dossier/IM53008252).
- **Domnina** — Possibly Saint Domnina of Syria, a fifth-century ascetic. First: `shadow-20/p-025`. [Source](https://www.oca.org/saints/lives/2009/03/01/100632-saint-domnina-the-younger-of-syria).
- **Ava** — Possibly Saint Ava, a nun of Denain. First: `citadel-10/p-052`. [Source](https://nominis.cef.fr/contenus/saint/2156/Sainte-Ava.html).
- **Hunna** — Possibly Saint Hunna, remembered for washing for the poor. First: `citadel-04/p-037`. [Source](https://www.catholic.org/saints/saint.php?saint_id=3823).
- **Racho** — Possibly Saint Racho, a bishop of Autun. First: `shadow-05/p-020`. [Source](https://www.catholic.org/saints/saint.php?saint_id=4549).
- **Beuzec** — Possibly Budoc, a Breton saint whose name survives as Beuzec. First: `claw-13/p-043`. [Source](https://www.fondation-patrimoine.org/les-projets/eglise-saint-budoc-a-beuzec-cap-sizun/100540).
- **Mamillian** — Possibly Saint Mamillian, a bishop of Palermo. First: `citadel-23/p-013`. [Source](https://drjohnhutchisonhall.com/saints-pre-schism-rome/15-september/).
- **Mesrop** — Possibly Mesrop Mashtots, creator of the Armenian alphabet. First: `citadel-19/p-038`. [Source](https://www.iranicaonline.org/articles/mesrop-mastoc%CA%BF/).
- **Katharine** — Possibly Saint Catherine of Alexandria, associated with the wheel. First: `shadow-04/p-004`. [Source](https://www.metmuseum.org/art/collection/search/468353).
- **Hermas** — Possibly Hermas, author of The Shepherd. First: `shadow-06/p-094`. [Source](https://www.newadvent.org/fathers/0201.htm).
- **Famulimus** — Possibly from Latin famulus: a servant or attendant. First: `sword-33/p-017`. [Source](https://en.wiktionary.org/wiki/famulus#Latin).
- **Famulorum** — Possibly Latin: “of the servants.” First: `urth-40/p-016`. [Source](https://en.wiktionary.org/wiki/famulus#Latin).
- **Gurgustii** — Possibly from Latin gurgustium: a hut or hovel. First: `urth-29/p-021`. [Source](https://en.wiktionary.org/wiki/gurgustium#Latin).
- **Vici** — Possibly Latin vici: villages or neighborhoods. First: `urth-29/p-005`. [Source](https://cld.bbaw.de/lemma/lat/vicus).
- **Liti** — Possibly from Latin litus: a shore or beach. First: `urth-28/p-014`. [Source](https://cld.bbaw.de/lemma/lat/litus).
- **Os** — Possibly Latin os: a mouth or opening. First: `urth-29/p-042`. [Source](https://cld.bbaw.de/lemma/lat/os).
- **Fluminis** — Possibly Latin: “of a river.” First: `urth-30/p-016`. [Source](https://cld.bbaw.de/lemma/lat/flumen).
- **Noctua** — Possibly Latin noctua: an owl. First: `claw-17/p-026`. [Source](https://cld.bbaw.de/lemma/lat/noctua).
- **Quiesco** — Possibly Latin quiesco: “I rest” or “I am still.” First: `claw-13/p-046`. [Source](https://cld.bbaw.de/lemma/lat/quiesco).
- **Pestis** — Possibly Latin pestis: plague, ruin, or destruction. First: `urth-33/p-019`. [Source](https://cld.bbaw.de/lemma/lat/pestis).
- **Carina** — Possibly Latin carina: a ship’s keel. First: `claw-24/p-185`. [Source](https://cld.bbaw.de/lemma/lat/carina).
- **Silva** — Possibly Latin silva: a wood or forest. First: `citadel-23/p-003`. [Source](https://cld.bbaw.de/lemma/lat/silva).
- **Miles** — Possibly Latin miles: a soldier. First: `citadel-06/p-006`. [Source](https://en.wiktionary.org/wiki/miles#Latin).
- **Domnicellae** — Possibly related to the Latin ancestor of “damsel.” First: `shadow-18/p-042`. [Source](https://en.wiktionary.org/wiki/Reconstruction:Latin/domnicella).
- **avern** — Possibly Avernus, the lake associated with an entrance to the underworld. First: `shadow-17/p-028`. [Source](https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Aabo%3Aphi%2C0690%2C003%3A6).
- **Abaia** — Possibly Abaia, a great magical eel in Melanesian tradition. First: `shadow-12/p-088`. [Source](https://www.globalgreyebooks.com/online-ebooks/roland-b-dixon_oceanic-mythology_complete-text.html).
- **Samru** — Possibly the Simurgh, a mythical bird of Iranian tradition. First: `claw-06/p-009`. [Source](https://www.iranicaonline.org/articles/simorg/).
- **Orithyia** — Possibly Oreithyia, the Athenian princess carried off by the north wind. First: `sword-11/p-072`. [Source](https://www.theoi.com/Nymphe/NympheOreithyia1.html).
- **Alcyone** — Possibly Alcyone, transformed with Ceyx into a sea bird. First: `urth-30/p-056`. [Source](https://www.theoi.com/Text/OvidMetamorphoses11.html).
- **Ceryx** — Possibly Keryx, the herald associated with the Eleusinian mysteries. First: `urth-30/p-016`. [Source](https://www.theoi.com/Olympios/HermesFamily.html).
- **Dis** — Possibly Dis, the Roman god of the underworld. First: `sword-25/p-002`. [Source](https://www.theoi.com/Khthonios/Haides.html).
- **Skuld** — Possibly Skuld, one of the Norse Norns. First: `claw-10/p-019`. [Source](https://sacred-texts.com/neu/pre/pre04.htm).
- **Cephissus** — Possibly Cephissus, a Greek river and river-god. First: `claw-28/p-008`. [Source](https://www.theoi.com/Potamos/PotamosKephisos1.html).
- **amaranthine** — Unfading; also a reddish-purple color. First: `claw-08/p-051`. [Source](https://www.merriam-webster.com/dictionary/amaranthine).
- **simar** — A flowing robe or light shift. First: `shadow-29/p-002`. [Source](https://www.merriam-webster.com/dictionary/simar).
- **lucivee** — A regional name for the Canada lynx. First: `citadel-26/p-010`. [Source](https://www.merriam-webster.com/dictionary/lucivee).
- **sanbenito** — A penitential garment of the Inquisition. First: `sword-06/p-001`. [Source](https://www.merriam-webster.com/dictionary/sanbenito).
- **paduasoy** — A ribbed silk fabric. First: `shadow-16/p-042`. [Source](https://www.merriam-webster.com/dictionary/paduasoy).
- **rosolio** — A sweet, flavored cordial. First: `sword-04/p-052`. [Source](https://www.merriam-webster.com/dictionary/rosolio).
- **gegenschein** — A faint glow opposite the Sun. First: `sword-17/p-032`. [Source](https://www.merriam-webster.com/dictionary/gegenschein).
- **coryphaeus** — A chorus leader. First: `citadel-22/p-008`. [Source](https://www.merriam-webster.com/dictionary/coryphaeus).
- **palinode** — A poem retracting an earlier poem. First: `urth-31/p-016`. [Source](https://www.merriam-webster.com/dictionary/palinode).
- **oriflamme** — A battle banner or rallying symbol. First: `shadow-17/p-041`. [Source](https://www.merriam-webster.com/dictionary/oriflamme).
- **saros** — An ancient 3,600-year period; also an eclipse cycle. First: `shadow-02/p-011`. [Source](https://www.tertullian.org/rpearse/eusebius_chron/resources/berossos_and_manetho.pdf).
- **narthex** — The entrance area of a church. First: `citadel-15/p-003`. [Source](https://www.merriam-webster.com/dictionary/narthex).
- **pursuivant** — A junior heraldic officer. First: `shadow-07/p-107`. [Source](https://www.merriam-webster.com/dictionary/pursuivant).
- **palmer** — A pilgrim to the Holy Land. First: `shadow-17/p-053`. [Source](https://www.merriam-webster.com/dictionary/palmer).
- **paphian** — Of Paphos; an old term for a sex worker. First: `shadow-09/p-029`. [Source](https://www.merriam-webster.com/dictionary/paphian).
- **oread** — A mountain nymph. First: `claw-30/p-029`. [Source](https://www.merriam-webster.com/dictionary/oread).
- **mensal** — Church property supporting a religious household. First: `shadow-18/p-015`. [Source](https://www.dsl.ac.uk/entry/snd/mensal).
- **midinette** — A Parisian seamstress or shopgirl. First: `sword-06/p-001`. [Source](https://www.merriam-webster.com/dictionary/midinette).
- **lazulite** — An azure-blue phosphate mineral. First: `claw-01/p-003`. [Source](https://www.merriam-webster.com/dictionary/lazulite).
- **lanugo** — Fine, downy body hair. First: `urth-31/p-028`. [Source](https://www.merriam-webster.com/dictionary/lanugo).
- **lambrequin** — A helmet scarf or decorative valance. First: `shadow-16/p-002`. [Source](https://www.merriam-webster.com/dictionary/lambrequin).
- **hyalite** — A glasslike form of opal. First: `urth-33/p-003`. [Source](https://www.merriam-webster.com/dictionary/hyalite).
- **heteroclite** — Irregular or unconventional. First: `urth-48/p-004`. [Source](https://www.merriam-webster.com/dictionary/heteroclite).
- **hexaemeron** — The six days of Creation. First: `claw-08/p-035`. [Source](https://www.merriam-webster.com/dictionary/hexaemeron).
- **gamboge** — A yellow pigment from tree resin. First: `shadow-27/p-015`. [Source](https://www.merriam-webster.com/dictionary/gamboge).
- **archimage** — A great magician. First: `shadow-19/p-072`. [Source](https://www.merriam-webster.com/dictionary/archimage).
- **aubade** — A dawn song or poem. First: `sword-05/p-044`. [Source](https://www.merriam-webster.com/dictionary/aubade).
- **barghest** — An ominous spectral dog or goblin. First: `sword-07/p-038`. [Source](https://www.merriam-webster.com/dictionary/barghest).
- **beryl** — The mineral of emerald and aquamarine. First: `sword-14/p-005`. [Source](https://www.merriam-webster.com/dictionary/beryl).
- **chatoyant** — Shimmering like a cat’s eye. First: `sword-09/p-032`. [Source](https://www.merriam-webster.com/dictionary/chatoyant).
- **cordwain** — Cordovan leather. First: `shadow-06/p-081`. [Source](https://www.merriam-webster.com/dictionary/cordwain).
- **dux** — Latin: a leader or commander. First: `urth-46/p-062`. [Source](https://www.merriam-webster.com/dictionary/dux).
- **fearnought** — A thick, shaggy woolen cloth. First: `shadow-23/p-062`. [Source](https://www.merriam-webster.com/dictionary/fearnought).
- **lansquenet** — A German mercenary foot soldier. First: `shadow-16/p-041`. [Source](https://www.merriam-webster.com/dictionary/lansquenet).
- **monstrance** — A vessel displaying the Eucharist. First: `sword-26/p-018`. [Source](https://www.merriam-webster.com/dictionary/monstrance).
- **noctilucent** — Glowing or visible at night. First: `claw-06/p-016`. [Source](https://www.merriam-webster.com/dictionary/noctilucent).
- **perischii** — People whose shadows turn all around them. First: `sword-05/p-026`. [Source](https://www.merriam-webster.com/dictionary/periscii).
- **mandragora** — Mandrake, a plant of magical folklore. First: `citadel-35/p-003`. [Source](https://www.merriam-webster.com/dictionary/mandrake).
- **hypethral** — Open to the sky. First: `claw-19/p-037`. [Source](https://www.merriam-webster.com/dictionary/hypaethral).
- **burginot** — Possibly burgonet, a Renaissance helmet. First: `shadow-35/p-002`. [Source](https://www.merriam-webster.com/dictionary/burgonet).
- **haubergeon** — A short medieval coat of mail. First: `citadel-19/p-007`. [Source](https://www.merriam-webster.com/dictionary/habergeon).
- **chrisos** — Possibly Greek chrysos: gold. First: `shadow-03/p-023`. [Source](https://atlas.perseus.tufts.edu/dictionaries/entry/urn%3Acite2%3Ascaife-viewer%3Adictionaries.v1%3Alsj-n114972/).
- **aes** — Latin: copper, bronze, or money. First: `shadow-16/p-042`. [Source](https://atlas.perseus.tufts.edu/dictionaries/entry/urn%3Acite2%3Ascaife-viewer%3Adictionary-entries.atlas_v1%3Alat.ls.perseus-eng2-n1359/).
- **dimarchi** — Possibly dimachae: cavalry fighting on foot. First: `shadow-03/p-042`. [Source](https://www.mediterranees.net/civilisation/Rich/Articles/Armee_romaine/Armee/Dimachae.html).
- **vingtner** — Possibly vintenar: leader of twenty soldiers. First: `claw-01/p-019`. [Source](https://livrepository.liverpool.ac.uk/3173890/1/692831.pdf).
- **thiasus** — A religious company in ancient Greece. First: `claw-11/p-048`. [Source](https://www.treccani.it/vocabolario/tiaso/).
- **graisle** — An old French battle trumpet. First: `shadow-27/p-029`. [Source](https://anglo-norman.net/entry/greille_1).
- **teratornis** — An extinct giant soaring bird. First: `shadow-35/p-053`. [Source](https://tarpits.org/stories/meet-teratorn-largest-bird-found-la-brea-tar-pits).
- **jelab** — A North African hooded robe. First: `shadow-16/p-051`. [Source](https://www.dictionary.com/browse/djellaba).
- **schiavoni** — Adriatic Slavs; Venetian mercenary troops. First: `citadel-19/p-010`. [Source](https://www.treccani.it/vocabolario/schiavone/).
- **batardeau** — A small auxiliary knife. First: `urth-41/p-013`. [Source](https://www.cnrtl.fr/definition/b%C3%A2tardeaux).
- **atrox** — Possibly Panthera atrox, the American lion. First: `shadow-25/p-036`. [Source](https://tarpits.org/stories/meet-biggest-big-cat-tar-pits-american-lion).
- **khaibit** — An Egyptian term for the shadow. First: `shadow-07/p-080`. [Source](https://sacred-texts.com/egy/ebod/ebodintr.htm).
- **phrontiserion** — Possibly phrontisterion: a place for thought. First: `urth-37/p-050`. [Source](https://assets.cambridge.org/97805211/72561/excerpt/9780521172561_excerpt.pdf).
- **notule** — Possibly the noctule bat; also French for a brief note. First: `claw-13/p-018`. [Source](https://www.bats.org.uk/about-bats/what-are-bats/uk-bats/noctule).
- **nigrescent** — Darkening or tending toward black. First: `shadow-10/p-034`. [Source](https://webstersdictionary1828.com/Dictionary/nigrescent).
- **vates** — Latin: a seer, prophet, or poet. First: `urth-35/p-021`. [Source](https://alatius.com/ls/index.php?l=vates).
- **harena** — Latin: sand or an arena. First: `sword-01/p-024`. [Source](https://alatius.com/ls/index.php?l=harena).
- **spado** — Latin: a eunuch. First: `urth-13/p-050`. [Source](https://alatius.com/ls/index.php?l=spado).
- **fulgurator** — An interpreter of lightning omens. First: `shadow-07/p-066`. [Source](https://alatius.com/ls/index.php?l=fulguratorem).
- **fuscina** — Latin: a trident. First: `edition-part0152/p-002`. [Source](https://archli.com/dictionary/lewis-short-latin-dictionary/fuscina-150145).
- **hastarii** — Possibly Latin hasta: spear or lance. First: `claw-14/p-027`. [Source](https://atlas.perseus.tufts.edu/dictionaries/entry/urn%3Acite2%3Ascaife-viewer%3Adictionary-entries.atlas_v1%3Alat.ls.perseus-eng2-n20273/).
- **Scylla** — A many-headed sea monster of Greek myth. First: `claw-04/p-030`. [Source](https://www.theoi.com/Pontios/Skylla.html).
- **theophany** — A visible appearance of a deity. First: `sword-27/p-018`. [Source](https://www.merriam-webster.com/dictionary/theophany).

Revised existing entries: thecla, nacre, coruscant, lazaretto, clarion, dorcas, thaumaturgist, mizzen, burgundofara, eata, gurloes, ymar, rudesind, hildegrin, agilus, trudo, pega, anskar, declan, odilo, drotte, hethor, arctother, capulus, inire, terminus-est, barbatus.

### Long Sun

- **Mamelta** — Possibly Saint Mamelta, a Persian martyr. First: `lake-09/p-206`. [Source](https://www.oca.org/saints/lives/2012/10/05/102881-martyr-memelchtha-of-persia).
- **Siyuf** — Possibly Arabic siyūf, swords. First: `calde-epilogue/p-004`. [Source](https://fada.birzeit.edu/jspui/bitstream/20.500.11889/4947/1/spokenarabicofeg00willuoft.pdf).
- **Saba** — Possibly Arabic ṣabā, the east wind. First: `calde-10/p-002`. [Source](https://www.rekhtadictionary.com/meaning-of-sabaa).
- **Sirka** — Possibly Persian and Urdu sirka, vinegar. First: `exodus-05/p-039`. [Source](https://www.rekhtadictionary.com/meaning-of-sirka).
- **Abanja** — Possibly Arabic banj, an anesthetic. First: `exodus-09/p-247`. [Source](https://kutub.nur.nu/Arabic-Language/Hans-Wehr.pdf).
- **Hadale** — Possibly Arabic hadīl, a dove’s cooing. First: `exodus-09/p-221`. [Source](https://brill.com/display/book/9789004499287/BP000005.xml?language=en).
- **Hossaan** — Possibly Arabic ḥiṣān, a horse or stallion. First: `exodus-02/p-160`. [Source](https://dictionary.reverso.net/english-arabic/horse).
- **Matar** — Possibly Arabic maṭar, rain. First: `exodus-14/p-380`. [Source](https://www.lisaanmasry.org/online/word.php?cn=3&id=7775&ui=).
- **Lijam** — Possibly Arabic lijām, a bridle. First: `exodus-14/p-481`. [Source](https://eprints.soas.ac.uk/28940/1/10673184.pdf).
- **gleacaiocht** — Irish gleacaíocht: wrestling, fighting, or gymnastics. First: `exodus-12/p-137`. [Source](https://www.teanglann.ie/en/fgb/gleaca%C3%ADocht).
- **achates** — A faithful companion, from Virgil’s Achates. First: `lake-07/p-041`. [Source](https://www.merriam-webster.com/dictionary/achates).
- **Lemur** — A Madagascan primate; its name derives from Latin spirits of the dead. First: `nightside-09/p-250`. [Source](https://www.merriam-webster.com/dictionary/lemur).
- **Ermine** — A stoat, especially in its white winter coat. First: `nightside-04/p-070`. [Source](https://www.merriam-webster.com/dictionary/ermine).
- **Titi** — A small South American monkey; also a name for certain trees. First: `exodus-06/p-275`. [Source](https://www.merriam-webster.com/dictionary/titi).
- **Mattak** — Whale skin and attached blubber eaten in Greenland. First: `calde-06/p-358`. [Source](https://visitgreenland.com/activities/greenlandic-gastronomy-a-taste-of-greenland/).
- **Yapok** — A water opossum of South America. First: `calde-05/p-022`. [Source](https://www.merriam-webster.com/dictionary/yapok).
- **Gurnard** — A sea robin; the name is related to grunting. First: `nightside-03/p-197`. [Source](https://www.merriam-webster.com/dictionary/gurnard).
- **Brocket** — A small deer with unbranched antlers. First: `calde-09/p-267`. [Source](https://www.merriam-webster.com/dictionary/brocket).
- **Caddis** — A caddisfly or its aquatic larva. First: `nightside-06/p-076`. [Source](https://www.merriam-webster.com/dictionary/caddis).
- **Bongo** — An African forest antelope with white stripes. First: `exodus-11/p-147`. [Source](https://www.merriam-webster.com/dictionary/bongo).
- **Loach** — A small freshwater fish related to carp. First: `nightside-10/p-143`. [Source](https://www.merriam-webster.com/dictionary/loach).
- **Liana** — A woody climbing vine of tropical forests. First: `calde-06/p-296`. [Source](https://www.merriam-webster.com/dictionary/liana).
- **Kingcup** — A name for marsh marigold and related buttercups. First: `calde-05/p-021`. [Source](https://www.merriam-webster.com/dictionary/kingcup).
- **Arolla** — The Swiss stone pine. First: `lake-05/p-195`. [Source](https://www.merriam-webster.com/dictionary/arolla).
- **Feist** — A dialect word for a small dog. First: `exodus-14/p-133`. [Source](https://www.merriam-webster.com/dictionary/feist).
- **Marmot** — A large burrowing rodent of the squirrel family. First: `calde-05/p-023`. [Source](https://www.merriam-webster.com/dictionary/marmot).
- **Scup** — An Atlantic porgy with a Narragansett-derived name. First: `calde-01/p-172`. [Source](https://www.merriam-webster.com/dictionary/scup).
- **Skink** — A usually small lizard of the family Scincidae. First: `calde-06/p-173`. [Source](https://www.merriam-webster.com/dictionary/skink).
- **Civet** — A slender carnivorous mammal; also its musky secretion. First: `calde-02/p-357`. [Source](https://www.merriam-webster.com/dictionary/civet).
- **Nizam** — An Ottoman regular soldier; also the title of Hyderabad’s rulers. First: `exodus-14/p-156`. [Source](https://www.gw.uni-jena.de/phifakmedia/93797/rocchi-ottoman-turkish-loanwords-in-egyptian-and-syro-lebanese-palestinian-arabic.pdf?nonactive=1&suffix=pdf).
- **Moly** — Possibly the magical herb in the Odyssey. First: `calde-03/p-023`. [Source](https://www.merriam-webster.com/dictionary/moly).
- **catachrest** — Possibly catachresis, an unusual or improper use of a word. First: `nightside-02/p-021`. [Source](https://www.merriam-webster.com/dictionary/catachresis).
- **Sard** — A brownish red variety of chalcedony. First: `calde-05/p-225`. [Source](https://www.merriam-webster.com/dictionary/sard).
- **Catamitus** — The Latin form of Ganymede. First: `nightside-06/p-031`. [Source](https://www.merriam-webster.com/dictionary/catamite).
- **bandeau** — A band worn around the head or across the breasts. First: `calde-03/p-126`. [Source](https://www.merriam-webster.com/dictionary/bandeau).
- **Aster** — A flowering plant whose name is Greek for star. First: `calde-03/p-193`. [Source](https://www.merriam-webster.com/dictionary/aster).
- **Cassava** — Manioc, a tropical crop grown for its starchy roots. First: `calde-04/p-006`. [Source](https://www.merriam-webster.com/dictionary/cassava).
- **Kerria** — An Asian flowering shrub named for William Kerr. First: `exodus-16/p-338`. [Source](https://www.merriam-webster.com/dictionary/kerria).
- **Elodia** — Possibly Elodea, a genus of aquatic plants. First: `calde-03/p-484`. [Source](https://www.merriam-webster.com/dictionary/elodea).
- **Bittersweet** — A name for woody vines, including a poisonous nightshade. First: `lake-10/p-054`. [Source](https://www.merriam-webster.com/dictionary/bittersweet).
- **Orchid** — A flowering plant of the family Orchidaceae. First: `nightside-03/p-217`. [Source](https://www.merriam-webster.com/dictionary/orchid).
- **Slate** — A fine-grained metamorphic rock that splits into sheets. First: `exodus-10/p-014`. [Source](https://www.merriam-webster.com/dictionary/slate).
- **karbaj** — Possibly kurbash, a hide whip. First: `exodus-02/p-247`. [Source](https://www.merriam-webster.com/dictionary/kurbash).
- **Ah Lah** — Possibly Allah, the Arabic name for God. First: `calde-01/p-044`. [Source](https://www.merriam-webster.com/dictionary/Allah).
- **Vulpes** — Latin for a fox. First: `lake-06/p-099`. [Source](https://atlas.perseus.tufts.edu/dictionaries/entry/urn%3Acite2%3Ascaife-viewer%3Adictionary-entries.atlas_v1%3Alat.ls.perseus-eng2-n51431/).
- **Aquila** — Latin for an eagle, also a Roman legion’s standard. First: `lake-04/p-223`. [Source](https://atlas.perseus.tufts.edu/dictionaries/entry/urn%3Acite2%3Ascaife-viewer%3Adictionary-entries.atlas_v1%3Alat.ls.perseus-eng2-n3282/).
- **Thetis** — A Greek sea goddess and the mother of Achilles. First: `calde-03/p-014`. [Source](https://www.theoi.com/Pontios/NereisThetis.html).
- **Fulmar** — A cold-water seabird related to petrels. First: `lake-10/p-054`. [Source](https://www.merriam-webster.com/dictionary/fulmar).
- **Goldcrest** — A tiny kinglet with a bright yellow crown. First: `nightside-01/p-028`. [Source](https://www.merriam-webster.com/dictionary/goldcrest).
- **Shrike** — A predatory songbird that often impales its prey. First: `exodus-03/p-021`. [Source](https://www.merriam-webster.com/dictionary/shrike).
- **Pard** — An old word for a leopard. First: `nightside-08/p-178`. [Source](https://www.merriam-webster.com/dictionary/pard).
- **Eft** — A newt, especially in its land-dwelling stage. First: `calde-06/p-331`. [Source](https://www.merriam-webster.com/dictionary/eft).
- **Hart** — A mature male red deer. First: `calde-03/p-193`. [Source](https://www.merriam-webster.com/dictionary/hart).
- **Serval** — An African wildcat with long legs and large ears. First: `exodus-10/p-188`. [Source](https://www.merriam-webster.com/dictionary/serval).
- **Bison** — Large wild cattle with a shoulder hump. First: `calde-04/p-176`. [Source](https://www.merriam-webster.com/dictionary/bison).
- **Mandrill** — A large African monkey with a brightly colored muzzle. First: `calde-03/p-482`. [Source](https://www.merriam-webster.com/dictionary/mandrill).
- **Bellflower** — A flowering plant of the genus Campanula. First: `lake-05/p-195`. [Source](https://www.merriam-webster.com/dictionary/bellflower).
- **Dahlia** — A flowering plant named for the botanist Anders Dahl. First: `lake-11/p-062`. [Source](https://www.merriam-webster.com/dictionary/dahlia).
- **Chamomile** — An aromatic plant of the daisy family. First: `exodus-07/p-028`. [Source](https://www.merriam-webster.com/dictionary/chamomile).
- **Mockorange** — A name for shrubs of the genus Philadelphus. First: `calde-05/p-326`. [Source](https://www.merriam-webster.com/dictionary/mock%20orange).
- **narthex** — The entrance vestibule of a church. First: `calde-02/p-018`. [Source](https://www.merriam-webster.com/dictionary/narthex).
- **yataghan** — A Turkish sword with a curved blade and no handguard. First: `calde-06/p-136`. [Source](https://www.merriam-webster.com/dictionary/yataghan).
- **skiagraph** — A shadow-picture, especially a radiograph. First: `lake-02/p-001`. [Source](https://truthbook.com/urantia-book-viewer-core/1924-Websters-Dictionary-Edition/LETTER-S.pdf).
- **Kalan** — A name for the sea otter. First: `nightside-03/p-197`. [Source](https://portals.iucn.org/library/efiles/documents/1990-009.pdf).
- **Pricklythrift** — A cushion-forming plant with pointed leaves. First: `lake-12/p-006`. [Source](https://www.csu.org/water-wise-plants/prickly-thrift).
- **Moorgrass** — Possibly moor-grass, a tufted grass with purple flower clusters. First: `nightside-10/p-145`. [Source](https://www.rhs.org.uk/plants/11169/molinia-caerulea/details).
- **Aquifolia** — Possibly Oregon grapeholly, Mahonia aquifolium. First: `nightside-01/p-171`. [Source](https://woodyplants.cals.cornell.edu/plant/150).
- **Nemesis** — The Greek goddess of retribution. First: `calde-05/p-124`. [Source](https://www.merriam-webster.com/dictionary/nemesis).
- **Exmoor** — Possibly the Exmoor pony, a native British breed. First: `lake-12/p-006`. [Source](https://www.exmoor-nationalpark.gov.uk/nature-and-landscape/our-habitats-and-wildlife/exmoor-ponies).
- **Rimah** — Possibly Arabic rimāḥ, spears. First: `exodus-14/p-452`. [Source](https://www.rekhtadictionary.com/meaning-of-rimaah).
- **Boraz** — Possibly Arabic burāz, excrement. First: `exodus-11/p-214`. [Source](https://resources.lingualism.com/levantine-arabic/the-human-body-and-describing-people-2/).
- **marhaba** — An Arabic greeting meaning welcome. First: `exodus-05/p-037`. [Source](https://www.rekhtadictionary.com/meaning-of-marhabaa).
- **sellaria** — Latin for a sitting room furnished with seats. First: `nightside-09/p-038`. [Source](https://www.alatius.com/ls/index.php?met=up&ord=sellae).
- **ausculator** — Possibly Latin auscultator, a listener. First: `nightside-10/p-073`. [Source](https://www.latin-is-simple.com/en/vocabulary/noun/3002/).
- **Sedes** — Latin for a seat, throne, or dwelling place. First: `lake-06/p-308`. [Source](https://atlas.perseus.tufts.edu/dictionaries/entry/urn%3Acite2%3Ascaife-viewer%3Adictionary-entries.atlas_v1%3Alat.ls.perseus-eng2-n43306/).
- **Hackum** — Old cant for a bullying fighter or bravo. First: `lake-05/p-132`. [Source](https://vulgar.pangyre.org/h/).
- **calotte** — A shallow, cap-shaped dome. First: `nightside-03/p-109`. [Source](https://en.wikipedia.org/wiki/Dome#Saucer_dome).
- **clarion** — A shrill trumpet; also clear and ringing. First: `exodus-16/p-256`. [Source](https://www.merriam-webster.com/dictionary/clarion).

Revised existing entries: chrasmologic, dimber.

### Short Sun

- **Bello** — Italian: beautiful or handsome. First: `green-12/p-007`. [Source](https://www.treccani.it/vocabolario/bello/).
- **Vivo** — Italian: alive, lively, or vivid. First: `green-12/p-007`. [Source](https://www.treccani.it/vocabolario/vivo/).
- **Turco** — Italian: Turkish, or a Turk. First: `green-03/p-002`. [Source](https://www.treccani.it/vocabolario/turco1/).
- **Zitta** — Italian: silent or quiet. First: `green-01/p-206`. [Source](https://www.treccani.it/vocabolario/zitto/).
- **Marzo** — Italian: March, the month. First: `green-14/p-119`. [Source](https://www.treccani.it/vocabolario/marzo/).
- **Corpo** — Italian: a body or organized group. First: `green-01/p-167`. [Source](https://www.treccani.it/vocabolario/corpo/).
- **Uscita** — Italian: an exit or departure. First: `green-16/p-073`. [Source](https://www.treccani.it/vocabolario/uscita/).
- **Urbanita** — Possibly Italian urbanità: civility or refined manners. First: `green-15/p-136`. [Source](https://www.treccani.it/vocabolario/urbanita/).
- **Solenno** — Possibly Italian solenne: solemn or stately. First: `green-03/p-034`. [Source](https://www.treccani.it/vocabolario/solenne/).
- **Salica** — Possibly Salic: relating to the laws of the Salian Franks. First: `green-02/p-038`. [Source](https://www.treccani.it/vocabolario/salico/).
- **Ugolo** — Possibly Italian ugola: the uvula. First: `green-14/p-184`. [Source](https://www.treccani.it/vocabolario/ugola/).
- **Bruna** — Italian: dark or brown. First: `green-11/p-050`. [Source](https://www.treccani.it/vocabolario/bruno/).
- **Atteno** — Possibly Italian attento: attentive or careful. First: `green-01/p-046`. [Source](https://www.treccani.it/vocabolario/attento/).
- **Mysire** — Anglo-Norman: my lord. First: `return-03/p-019`. [Source](https://anglo-norman.net/entry/misire).
- **Rechtor** — Possibly Dutch rechter: a judge. First: `return-07/p-046`. [Source](https://anw.ivdnt.org/article/rechter).
- **Ziek** — Dutch: sick or ill. First: `return-01/p-198`. [Source](https://dictionary.cambridge.org/dictionary/dutch-english/ziek).
- **Legaro** — Possibly Italian legare: to bind or tie. First: `green-17/p-247`. [Source](https://www.treccani.it/vocabolario/legare1/).
- **Chaku** — Hindi: a knife. First: `green-11/p-108`. [Source](https://www.collinsdictionary.com/us/dictionary/hindi-english/चाकू).
- **Somvar** — Hindi: Monday. First: `blue-01/p-081`. [Source](https://www.collinsdictionary.com/dictionary/hindi-english/सोमवार).
- **Nauvan** — Hindi: ninth. First: `blue-01/p-081`. [Source](https://www.collinsdictionary.com/dictionary/hindi-english/नौवाँ).
- **Bala** — Possibly Hindi bālā: a girl or young woman. First: `green-24/p-109`. [Source](https://www.hindwi.org/hindi-dictionary/meaning-of-baalaa).
- **Shauk** — Possibly shauq: desire or enthusiasm. First: `green-24/p-115`. [Source](https://www.rekhtadictionary.com/meaning-of-shauq).
- **Bahar** — Possibly Persian bahār: springtime or flourishing beauty. First: `blue-12/p-034`. [Source](https://www.rekhtadictionary.com/meaning-of-bahaar?lang=ur).
- **Thody** — Possibly Hindi thoṛī: a little or scanty. First: `green-11/p-118`. [Source](https://www.rekhta.org/urdudictionary?keyword=tho.dii).
- **Nadar** — Possibly nādār: poor or without possessions. First: `green-24/p-290`. [Source](https://www.rekhtadictionary.com/meaning-of-naadaar).
- **Maliki** — Possibly Swahili maliki: a ruler or sovereign. First: `green-24/p-052`. [Source](https://www.maktaba.org/download/file/1589/Swahili-english_dictionary_Arthur_cornwallis_madan.pdf).
- **Ushujaa** — Swahili: courage or heroism. First: `green-08/p-009`. [Source](https://upload.wikimedia.org/wikipedia/commons/f/f5/Swahili-English_dictionary_%28IA_swahilienglishdi00madarich%29.pdf).
- **Tuz** — Turkish: salt. First: `blue-16/p-022`. [Source](https://dictionary.cambridge.org/us/dictionary/english-turkish/salt).
- **miralaly** — Possibly Ottoman Turkish miralay: colonel. First: `green-24/p-035`. [Source](https://kelime.com/kelime/miralay/63335e36101dea5b8e1bdbd2-63335e36bafb252dfda5ecda/os).
- **Yksin** — Finnish: alone. First: `blue-14/p-088`. [Source](https://www.suomisanakirja.fi/yksin).
- **Advocaat** — Dutch: an advocate or lawyer. First: `return-11/p-022`. [Source](https://dictionary.cambridge.org/dictionary/dutch-english/advocaat).
- **sellaria** — Latin: a sitting room. First: `blue-11/p-130`. [Source](https://www.alatius.com/ls/index.php?met=up&ord=sellae).
- **Pajarocu** — Possibly the pájaro Cú, a bird of Mexican folklore. First: `blue-01/p-215`. [Source](https://www.coreknowledge.org/wp-content/uploads/2016/11/Birds-Through-the-Seasons.pdf).
- **Flannan** — Possibly Saint Flannan of Killaloe. First: `return-04/p-094`. [Source](https://www.clarelibrary.ie/eolas/coclare/people/saint_flannan.htm).
- **Morphia** — Possibly Morpheus, the shaper of human figures in dreams. First: `return-01/p-030`. [Source](https://www.theoi.com/Text/OvidMetamorphoses11.html).
- **Teras** — Possibly Malay teras: heartwood or an essential core. First: `green-15/p-002`. [Source](https://prpm.dbp.gov.my/Cari1?d=72508&keyword=teras).
- **Torda** — Possibly Swedish torda: a razorbill. First: `green-prelude/p-007`. [Source](https://runeberg.org/ordboksv/2/0560.html).
- **Han** — Possibly the Han dynasty of China. First: `blue-01/p-015`. [Source](https://www.metmuseum.org/TOAH/hd/hand/hd_hand.htm).
- **Qarya** — Arabic: a village. First: `green-24/p-028`. [Source](https://www.lisaanmasry.org/online/word.php?cn=2&id=10353&ui=).
- **Vent** — Dutch: a fellow or chap. First: `return-09/p-170`. [Source](https://www.dbnl.org/tekst/weil004nede14_01/weil004nede14_01_2557.php).
- **Versregal** — Possibly Dutch versregel: a line of poetry. First: `return-07/p-108`. [Source](https://uitmuntend.de/woordenboek/versregel).
- **kandij** — Dutch: rock candy or crystallized sugar. First: `return-09/p-048`. [Source](https://www.ensie.nl/etymologisch-woordenboek/kandij).
- **Volanta** — Possibly Italian volante: a steering wheel. First: `green-15/p-087`. [Source](https://www.treccani.it/vocabolario/volante2/).
- **Comus** — Greek personification of revelry and merrymaking. First: `green-19/p-018`. [Source](https://www.theoi.com/Georgikos/SatyrosKomos.html).
- **Alpaca** — An Andean camel relative bred for its soft fleece. First: `return-02/p-277`. [Source](https://nationalzoo.si.edu/animals/alpaca).
- **Amberjack** — A large marine fish of the jack family. First: `blue-01/p-173`. [Source](https://www.fisheries.noaa.gov/species/greater-amberjack).
- **Antbear** — Another name for a giant anteater or an aardvark. First: `return-02/p-277`. [Source](https://www.collinsdictionary.com/dictionary/english/ant-bear).
- **Judastree** — A small tree with pink flowers and heart-shaped leaves. First: `green-24/p-125`. [Source](https://www.rhs.org.uk/plants/24283/cercis-siliquastrum/details).
- **M’to** — Possibly Swahili mto: a river. First: `return-16/p-299`. [Source](https://swahili-dictionary.com/swahili-english/mto_mto).
- **Beled** — Possibly Arabic balad: a town or country. First: `blue-04/p-196`. [Source](https://www.qdl.qa/en/archive/81055/vdc_100085185904.0x0000c2).
- **Zeehra** — Possibly Arabic zahrāʾ: bright or radiant. First: `blue-13/p-103`. [Source](https://www.rekhta.org/urdudictionary?keyword=zahraa).
- **Cilinia** — Possibly Saint Cilinia, mother of Remigius of Reims. First: `return-17/p-365`. [Source](https://www.katolsk.no/biografier/historisk/celilaon).
- **Tigridia** — Possibly Saint Tigridia, abbess of Oña. First: `return-19/p-118`. [Source](https://www.archiburgos.es/2016/11/22/tras-mas-de-un-siglo-vuelve-la-fiesta-de-santa-tigridia-a-ona/).
- **Oxlip** — A primrose relative with pale yellow flower clusters. First: `return-12/p-183`. [Source](https://www.rhs.org.uk/plants/13747/primula-elatior-pr/details).
- **Cowslip** — A spring wildflower with drooping yellow flowers. First: `return-17/p-025`. [Source](https://www.woodlandtrust.org.uk/trees-woods-and-wildlife/plants/wild-flowers/cowslip/).
- **Sweetbay** — Bay laurel, an evergreen tree with aromatic leaves. First: `return-20/p-031`. [Source](https://www.rhs.org.uk/plants/bay-tree/growing-guide).
- **Madrone** — An evergreen Arbutus tree with peeling bark. First: `return-20/p-031`. [Source](https://research.fs.usda.gov/silvics/pacific-madrone).
- **Gadwall** — A dabbling duck with a white wing patch. First: `blue-01/p-263`. [Source](https://www.allaboutbirds.org/guide/Gadwall/overview).
- **Grig** — An old word for a cricket or a merry person. First: `green-13/p-158`. [Source](https://www.dictionary.com/browse/grig).
- **Sealily** — A stalked crinoid, a marine animal with feathery arms. First: `blue-01/p-233`. [Source](https://ocean.si.edu/through-time/sea-lilies).
- **Heleno** — Possibly the Esperanto form of Helen. First: `green-02/p-090`. [Source](https://www.majstro.com/dictionaries/English-Greek/Helen).
- **Poliso** — Possibly Greek polis: a city-state. First: `green-02/p-109`. [Source](https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.04.0009%3Achapter%3D5%3Asection%3D1).
- **Urbasecundus** — Possibly Latin urbs and secundus: second city. First: `blue-02/p-012`. [Source](https://www.alatius.com/ls/index.php?met=up&ord=secundus).
- **Aspis** — Greek: a round shield; also an asp. First: `green-09/p-157`. [Source](https://atlas.perseus.tufts.edu/lemma/15794/).
- **Karn** — Possibly Sanskrit karṇa: an ear; also the epic hero Karna. First: `green-24/p-115`. [Source](https://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/MWScanpdf/mw0256-karkakhaNDa.pdf).
- **Merryn** — Possibly Saint Merinus or Merryn, an Irish monastic saint. First: `return-13/p-094`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n216/mode/2up?q=Merryn).
- **mizzen** — A mast behind the mainmast, or its sail. First: `return-13/p-203`. [Source](https://www.merriam-webster.com/dictionary/mizzen).
- **Abaia** — Possibly Abaia, a great magical eel in Melanesian tradition. First: `return-15/p-097`. [Source](https://www.globalgreyebooks.com/online-ebooks/roland-b-dixon_oceanic-mythology_complete-text.html).
- **Samru** — Possibly the Simurgh, a mythical bird of Iranian tradition. First: `return-17/p-191`. [Source](https://www.iranicaonline.org/articles/simorg/).
- **narthex** — The entrance vestibule of a church. First: `return-16/p-084`. [Source](https://www.merriam-webster.com/dictionary/narthex).
- **balneum** — Latin: a bath or bathing room. First: `return-18/p-005`. [Source](https://en.wiktionary.org/wiki/balneum#Latin).
- **dimber** — Old cant for pretty or fine. First: `return-18/p-046`. [Source](https://www.gutenberg.org/cache/epub/5402/pg5402-images.html).
- **Mamelta** — Possibly Saint Mamelta, a Persian martyr. First: `blue-01/p-260`. [Source](https://www.oca.org/saints/lives/2012/10/05/102881-martyr-memelchtha-of-persia).
- **Siyuf** — Possibly Arabic siyūf, swords. First: `blue-02/p-102`. [Source](https://fada.birzeit.edu/jspui/bitstream/20.500.11889/4947/1/spokenarabicofeg00willuoft.pdf).
- **Saba** — Possibly Arabic ṣabā, the east wind. First: `blue-01/p-182`. [Source](https://www.rekhtadictionary.com/meaning-of-sabaa).
- **Abanja** — Possibly Arabic banj, an anesthetic. First: `green-25/p-048`. [Source](https://kutub.nur.nu/Arabic-Language/Hans-Wehr.pdf).
- **Lemur** — A Madagascan primate; its name derives from Latin spirits of the dead. First: `return-09/p-060`. [Source](https://www.merriam-webster.com/dictionary/lemur).
- **Ermine** — A stoat, especially in its white winter coat. First: `blue-03/p-057`. [Source](https://www.merriam-webster.com/dictionary/ermine).
- **Mattak** — Whale skin and attached blubber eaten in Greenland. First: `green-17/p-217`. [Source](https://visitgreenland.com/activities/greenlandic-gastronomy-a-taste-of-greenland/).
- **Moly** — Possibly the magical herb in the Odyssey. First: `blue-01/p-254`. [Source](https://www.merriam-webster.com/dictionary/moly).
- **Aster** — A flowering plant whose name is Greek for star. First: `return-01/p-023`. [Source](https://www.merriam-webster.com/dictionary/aster).
- **Orchid** — A flowering plant of the family Orchidaceae. First: `blue-05/p-025`. [Source](https://www.merriam-webster.com/dictionary/orchid).
- **Vulpes** — Latin for a fox. First: `blue-01/p-082`. [Source](https://atlas.perseus.tufts.edu/dictionaries/entry/urn%3Acite2%3Ascaife-viewer%3Adictionary-entries.atlas_v1%3Alat.ls.perseus-eng2-n51431/).
- **Shrike** — A predatory songbird that often impales its prey. First: `blue-01/p-236`. [Source](https://www.merriam-webster.com/dictionary/shrike).
- **Bison** — Large wild cattle with a shoulder hump. First: `return-10/p-005`. [Source](https://www.merriam-webster.com/dictionary/bison).
- **Moorgrass** — Possibly moor-grass, a tufted grass with purple flower clusters. First: `blue-10/p-121`. [Source](https://www.rhs.org.uk/plants/11169/molinia-caerulea/details).

Revised existing entries: eata, gurloes, drotte, inclito, eschar, olivine, cijfer, vadsig, nat, aanvagen, affito, chrasmologic.

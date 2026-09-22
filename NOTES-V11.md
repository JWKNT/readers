# External-reference sweep — version 11

The margins explain external words, name meanings, possible namesakes, language roots, history, mythology, and natural history. They do not identify fictional people or explain plot events. Tentative derivations and namesakes begin with “Possibly” in both the brief gloss and full note. A documented dictionary meaning is distinguished from a proposed namesake.

The supplied scholarly guides served as leads. Accepted entries were checked against independently linked dictionaries, historical texts, church records, museum and university resources, and botanical or zoological references. All definitions use concise original wording. Neither guide nor the extracted research material is included in the site.

## Scope and counts

| Series | Before | Added | Existing entries revised | After |
|---|---:|---:|---:|---:|
| New Sun | 608 | 152 | 0 | 760 |
| Long Sun | 260 | 58 | 6 | 318 |
| Short Sun | 307 | 58 | 13 | 365 |

There are 1,443 series-specific notes: 268 added and 19 existing entries revised in this pass. A reference used in multiple series is counted separately in each. All 324 chapters keep their reading text, paragraph IDs, routes, and design.

## Editorial review

- Expanded New Sun saints, classical deities, astronomical names, Greek and Latin meanings, historic clothing, military vocabulary, and rare words. Found all three sundial mottoes in external sources and identified the traditional Fair Rosamund epitaph behind “Rose the Graced.”
- Restored Vodalus only after independently establishing the historical Saint Vodalus/Vodoaldus/Voel. The note begins “Possibly” and describes the saint alone. Pinian is linked tentatively to Pinianus, not the previously unsupported Piran connection. Shiprock remains excluded.
- Extended Long Sun botanical and zoological names, Arabic expressions, and historical slang. Ganymedia has a possible connection to Ganymeda/Hebe attested in Pausanias. The nest sense of Arabic ʿishsh replaces a misleading verb lead; speculative resemblance alone did not qualify for a note.
- Extended Short Sun Hindi, German, Gaelic, Scots, Italian, Japanese, and Cocopa references, along with animals, plants, maritime vocabulary, and material names. Sweetbay now includes Magnolia virginiana alongside bay laurel; Mucor has corrected fungal morphology; Heleno includes the attested Esperanto meaning Hellene.
- Corrected guide leads concerning Minias’s location, Egino’s allegiance, Anian’s abbey association, and Goslin’s Turin connection. Kept uncertain traditional biographies qualified. These are external traditions, not claims of authorial intent.
- Checked senses in actual passages: quadrille includes the card game; cornet includes the cavalry officer; fibula includes the brooch; maniple includes the military unit; gravid includes its figurative sense; dulcimer covers both hammered and plucked instruments; cant includes insincere talk.
- Reviewed cross-series matches individually. Rejected the plant sense for Scots Canna, the house sense for Scots ken, the slang sense for literal twigs, and the Biblical place-name sense for dialect Nod. Ordinary water-lily references do not receive the Lilium definition. Capital-only names such as Ash, Lily, Ray, and Warren avoid ordinary-word collisions.
- Added eight context-verified Short Sun spelling aliases without changing the prose: Galada, Advocast, Gioiosio, Proloctor, Sifido, Saldo, Adatto, and Inclitor. Duka was withheld because the existing masculine definition would lose the distinction.

## Validation

`python3 tools/validate.py --baseline 4dac1a4` passes for all 324 chapters. It checks preservation of reading text and paragraph IDs, annotation counts, first and local-first flags, manifest/library totals, ordinary HTML/JSON consistency, static source links/tooltips, local routes, and uncertainty wording. `git diff --check` passes.

Every addition’s first prose context was reviewed. Independent integration checks covered all 77 new proper-name proposals for New Sun and all 58 Short Sun additions, including spelling aliases. A separate review checked the New Sun lexical proposals. Long Sun’s slang and other potentially ambiguous matches were reviewed in their passages.

Browser checks exercised the new Latin notes at 1440px in light mode and 390px in dark mode. Long labels wrap, popups remain inside the viewport, Escape closes them, and keyboard Tab reaches the source link. At 200% reading/popup text size the note scrolls internally and its source remains keyboard-reachable, without page-wide horizontal overflow. Temporary testing styles were removed by navigation. Ganymedia’s new popup with its Pausanias source and Rajya Mantri’s Hindi note with its external sources were also checked. No browser console errors were observed. The existing reader script’s edition query is preserved; the three entry pages and manifests now request edition 11.

## Added references

The first location and first external source for each new series-specific note follow. The glossary can include additional sources.

### New Sun

- **Emilian** — Possibly Aemilian, a name borne by several saints. First: `citadel-08/p-049`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n27/mode/2up?q=Emilian).
- **Trason** — Possibly Saint Trason, a Roman martyr. First: `citadel-37/p-028`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n282/mode/2up?q=Trason).
- **Kyrin** — Possibly Saint Kyrin, also called Boniface. First: `urth-30/p-058`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n183/mode/2up?q=Kyrin).
- **Timon** — Possibly Timon, one of the seven chosen in Acts. First: `shadow-05/p-007`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n281/mode/2up?q=Timon).
- **Canog** — Possibly Saint Cynog, son of Brychan of Brycheiniog. First: `urth-37/p-048`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n79/mode/2up?q=Canog).
- **Caesidius** — Possibly Saint Caesidius, a martyr near Lake Fucino. First: `urth-46/p-062`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n76/mode/2up?q=Caesidius).
- **Sulpicius** — Possibly Sulpicius, the name of saints of Bourges. First: `shadow-06/p-043`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n271/mode/2up?q=Sulpicius).
- **Pelagia** — Possibly Saint Pelagia, a martyr of Antioch. First: `urth-44/p-022`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n235/mode/2up?q=Pelagia).
- **Olaguer** — Possibly Saint Olegarius, bishop of Barcelona and Tarragona. First: `citadel-35/p-065`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n227/mode/2up?q=Olaguer).
- **Nympha** — Possibly Saint Nympha, remembered with Tryphon and Respicius. First: `claw-15/p-010`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n283/mode/2up?q=Nympha).
- **Mineas** — Possibly Saint Minias, the martyr honored at San Miniato. First: `claw-13/p-042`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n218/mode/2up?q=Mineas).
- **Midan** — Possibly Saint Nidan, an early Welsh saint. First: `citadel-01/p-009`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n217/mode/2up?q=Midan).
- **Mesmin** — Possibly Saint Memorius, a deacon of Troyes. First: `claw-02/p-009`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n222/mode/2up?q=Mesmin).
- **Mennas** — Possibly Saint Menas, the Egyptian soldier-martyr. First: `shadow-03/p-008`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n216/mode/2up?q=Mennas).
- **Lelia** — Possibly Saint Lelia, an Irish saint of Munster. First: `claw-16/p-066`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n185/mode/2up?q=Lelia).
- **Kyneburga** — Possibly Saint Cyneburh, a Mercian princess and abbess. First: `claw-24/p-078`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n183/mode/2up?q=Kyneburga).
- **Ivo** — Possibly Saint Ivo, namesake of St Ives in Cambridgeshire. First: `claw-24/p-121`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n166/mode/2up?q=Ivo).
- **Gwinoc** — Possibly Saint Gwinoc, a Welsh monk associated with poetry. First: `shadow-06/p-081`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n44/mode/2up?q=Gwinoc).
- **Blaithmaic** — Possibly Saint Blathmac, an abbot killed at Iona. First: `shadow-06/p-081`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n70/mode/2up?q=Blaithmaic).
- **Bega** — Possibly Saint Bega, namesake of St Bees. First: `citadel-07/p-005`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n64/mode/2up?q=Bega).
- **Aphrodisius** — Possibly Saint Aphrodisius, a martyr of North Africa. First: `citadel-02/p-017`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n237/mode/2up?q=Aphrodisius).
- **Zambdas** — Possibly Saint Zambdas, an early bishop of Jerusalem. First: `sword-28/p-025`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n295/mode/2up?q=Zambdas).
- **Herais** — Possibly Saint Irais, an Egyptian martyr. First: `sword-14/p-038`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n164/mode/2up?q=Herais).
- **Vodalus** — Possibly Saint Vodalus, an early medieval hermit. First: `shadow-01/p-043`. [Source](https://www.katolsk.no/biografier/historisk/vodalus).
- **Sancha** — Possibly Blessed Sancha, a Portuguese princess and nun. First: `claw-15/p-010`. [Source](https://www.liturgia.pt/lh/pdf/0906Jun.pdf).
- **Mafalda** — Possibly Blessed Mafalda, a Portuguese princess and Cistercian. First: `urth-32/p-048`. [Source](https://www.liturgia.pt/lh/pdf/0906Jun.pdf).
- **Gerbold** — Possibly Saint Gerbold, bishop of Bayeux. First: `shadow-06/p-043`. [Source](https://nominis.cef.fr/contenus/saint/9487/Saint-Gerbold.html).
- **Quartillosa** — Possibly Quartillosa, a Christian martyr of Carthage. First: `shadow-05/p-041`. [Source](https://nominis.cef.fr/contenus/saint/11308/Saint-Libosus.html).
- **Josepha** — Possibly Blessed Josepha Maria of Benigànim. First: `shadow-10/p-033`. [Source](https://nominis.cef.fr/contenus/saint/5268/Bienheureuse-Agn%C3%A8s-Albinana.html).
- **Einhildis** — Possibly Saint Einhildis of Niedermünster. First: `sword-12/p-002`. [Source](https://www.katolsk.no/biografier/historisk/gunnieder).
- **Petronax** — Possibly Saint Petronax, restorer of Monte Cassino. First: `shadow-14/p-060`. [Source](https://nominis.cef.fr/contenus/saint/1107/Saint-P%C3%A9tronax.html).
- **Guibert** — Possibly Saint Guibert, founder of Gembloux Abbey. First: `claw-16/p-026`. [Source](https://nominis.cef.fr/contenus/saint/1205/Saint-Guibert-de-Gembloux.html).
- **Eigil** — Possibly Eigil, abbot of Fulda and biographer of Saint Sturm. First: `shadow-03/p-008`. [Source](https://www.deutsche-biographie.de/gnd118688359.html).
- **Grimkeld** — Possibly Saint Grimkeld, one of the Crowland martyrs. First: `urth-24/p-015`. [Source](https://www.katolsk.no/biografier/historisk/tcroylan).
- **Gracia** — Possibly Saint Gracia, one of the martyrs of Alzira. First: `shadow-09/p-017`. [Source](https://www.alzira.es/wp-content/uploads/2011/06/2-ANEXO-7-1-1-FICHAS-RECURSOS-CULTURALES.pdf).
- **Lybe** — Possibly Saint Lybe, a martyr of Palmyra. First: `claw-24/p-079`. [Source](https://www.catholic.org/saints/saint.php?saint_id=4372).
- **Lollian** — Possibly Saint Lollian, one of the Seven Martyrs of Samosata. First: `claw-16/p-026`. [Source](https://syriaca.org/work/320).
- **Anian** — Possibly Saint Anian, the saint commemorated at Saint-Chinian. First: `urth-33/p-040`. [Source](https://www.patrimoinereligieux34.catholique.fr/ancienne-abbaye-benedictine/114-fiche-ancienne-abbaye-benedictine-saint-chinian).
- **Branwallader** — Possibly Saint Branwalader, also called Brélade. First: `shadow-05/p-043`. [Source](https://www.katolsk.no/biografier/historisk/branwala).
- **Egino** — Possibly Egino of Chur, a twelfth-century bishop. First: `shadow-07/p-027`. [Source](https://hls-dhs-dss.ch/de/articles/012579/2000-10-30/).
- **Ia** — Possibly Saint Ia, a martyr of Persia. First: `claw-07/p-004`. [Source](https://www.oca.org/saints/lives/2018/09/11/102579-martyr-ia-and-9000-martyrs-with-her-of-persia).
- **Tanco** — Possibly Saint Tanco, traditionally a bishop of Verden. First: `urth-35/p-043`. [Source](https://www.katolsk.no/biografier/historisk/tanco).
- **Alcmund** — Possibly Saint Alchmund, a Northumbrian prince and martyr. First: `claw-11/p-017`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n34/mode/2up?q=Alcmund).
- **Gaudentius** — Possibly Saint Gaudentius, bishop of Brescia. First: `urth-39/p-047`. [Source](https://nominis.cef.fr/contenus/saint/2079/Saint-Gaudence.html).
- **Pinian** — Possibly Pinianus, a late Roman Christian ascetic. First: `urth-31/p-040`. [Source](https://www.newadvent.org/fathers/1102126.htm).
- **Ash** — Possibly Askr, the first man in Norse mythology. First: `citadel-16/p-006`. [Source](https://sacred-texts.com/neu/pre/pre04.htm).
- **Phoenix** — Possibly the phoenix, the bird of renewal. First: `claw-05/p-033`. [Source](https://www.theoi.com/Thaumasios/Phoinix.html).
- **Hesperus** — Possibly Hesperos, the evening star personified. First: `claw-17/p-043`. [Source](https://www.theoi.com/Titan/AsterEosphoros.html).
- **Gea** — Possibly Gaia, the Greek personification of Earth. First: `claw-24/p-085`. [Source](https://www.theoi.com/Protogenos/Gaia.html).
- **Erinys** — Possibly an Erinys, one of the Greek Furies. First: `claw-24/p-106`. [Source](https://www.theoi.com/Khthonios/Erinyes.html).
- **Moira** — Possibly Greek moira, an allotted share or fate. First: `shadow-14/p-014`. [Source](https://www.theoi.com/Daimon/Moirai.html).
- **Paeon** — Possibly Paeon, the physician of the Greek gods. First: `citadel-25/p-049`. [Source](https://atlas.perseus.tufts.edu/dictionaries/entry/urn%3Acite2%3Ascaife-viewer%3Adictionaries.v1%3Alsj-n76532/).
- **Phlegethon** — Possibly Phlegethon, a fiery river of the Greek underworld. First: `shadow-23/p-005`. [Source](https://www.theoi.com/Khthonios/PotamosPyriphlegethon.html).
- **Danaides** — Possibly the fifty daughters of Danaus. First: `urth-02/p-026`. [Source](https://www.theoi.com/Text/AeschylusSuppliants.html).
- **Abraxas** — Possibly Abraxas, a mystical name linked with Gnosticism. First: `claw-31/p-042`. [Source](https://www.newadvent.org/fathers/0319.htm).
- **Adonai** — Possibly Adonai, a Hebrew divine title meaning “my Lord.” First: `sword-38/p-010`. [Source](https://www.chabad.org/library/article_cdo/aid/904982/jewish/Yesodei-haTorah-Chapter-6.htm).
- **Apeiron** — Possibly the apeiron, Anaximander’s boundless first principle. First: `citadel-19/p-004`. [Source](https://plato.stanford.edu/archives/spr2014/entries/presocratics/).
- **Arioch** — Possibly Arioch, a royal officer in the Book of Daniel. First: `citadel-01/p-002`. [Source](https://bible.usccb.org/bible/daniel/2).
- **Nod** — Possibly the land of Nod, Cain’s place of exile. First: `claw-24/p-315`. [Source](https://bible.usccb.org/bible/genesis/4).
- **Paraclete** — Possibly the Paraclete, the advocate or helper. First: `claw-24/p-086`. [Source](https://www.vatican.va/content/john-paul-ii/en/audiences/1989/documents/hf_jp-ii_aud_19890524.html).
- **Camoena** — Possibly Camena, a Roman name for a Muse. First: `sword-33/p-038`. [Source](https://alatius.com/ls/index.php?l=Camena).
- **Jurupari** — Possibly Yuruparí, an ancestral being in Amazonian traditions. First: `shadow-29/p-048`. [Source](https://ich.unesco.org/en/Decisions/6.COM/13.9).
- **Gandharvas** — Possibly gandharvas, celestial musicians of Indian tradition. First: `urth-15/p-016`. [Source](https://www.metmuseum.org/art/collection/search/38142).
- **Sefiroth** — Possibly the sefirot, ten divine attributes in Kabbalah. First: `urth-39/p-061`. [Source](https://www.chabad.org/library/article_cdo/aid/361885/jewish/The-Sefirot.htm).
- **Savitar** — Possibly Savitar, a solar deity of the Rigveda. First: `citadel-35/p-057`. [Source](https://sacred-texts.com/hin/rigveda/rv01035.htm).
- **Surya** — Possibly Surya, the Hindu sun god. First: `citadel-35/p-057`. [Source](https://www.metmuseum.org/art/collection/search/75359).
- **Caitanya** — Possibly Sanskrit caitanya, consciousness or spirit. First: `citadel-02/p-017`. [Source](https://kosha.sanskrit.today/word/sa/caitanya).
- **Fauna** — Possibly Fauna, the Roman goddess associated with Bona Dea. First: `urth-33/p-006`. [Source](https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP%2A/Bona_Dea_Subsaxana.html).
- **Venant** — Possibly Venant, a traditional name associated with Regulus. First: `urth-22/p-068`. [Source](https://www.rasc.ca/sites/default/files/World%20Asterisms%20Project%20Handbook%20V%202024.4.pdf).
- **Barbara** — Possibly Saint Barbara, the patron saint of artillery. First: `shadow-11/p-003`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n60/mode/2up?q=Barbara).
- **Oringa** — Possibly Blessed Oringa, a medieval Tuscan religious woman. First: `urth-41/p-011`. [Source](https://archive.org/details/bookofsaintsdict00stau/page/n228/mode/2up?q=Oringa).
- **Maxentius** — Possibly Maxentius, the Roman emperor in Catherine’s legend. First: `shadow-11/p-012`. [Source](https://resources.metmuseum.org/resources/metpublications/pdf/Late_Medieval_Sculpture_The_Metropolitan_Museum_of_Art_Bulletin_v_64_no_4_Spring_2007.pdf).
- **Makar** — Possibly Saint Macarius the Great, an Egyptian monastic founder. First: `citadel-01/p-026`. [Source](https://archives.iccrom.org/oggetti/40786-wadi-el-natrun-mra-egy-nat-005).
- **Helios** — Possibly Helios, the Greek sun god. First: `citadel-35/p-057`. [Source](https://www.theoi.com/Titan/Helios.html).
- **Hyperion** — Possibly Hyperion, the Titan associated with heavenly light. First: `citadel-35/p-057`. [Source](https://www.theoi.com/Titan/Helios.html).
- **Sirius** — The Dog Star, the brightest star in Earth’s night sky. First: `claw-17/p-043`. [Source](https://science.nasa.gov/image-article/apod-1996-september-02-sirius-the-brightest-star-in-the-night/).
- **Goslin** — Possibly Saint Goscelinus, abbot of San Solutore. First: `citadel-12/p-066`. [Source](https://www.katolsk.no/biografier/historisk/gtorino).
- **pelagic** — Of the open ocean. First: `shadow-10/p-014`. [Source](https://www.gutenberg.org/ebooks/29765).
- **Reechy** — Foul-smelling or blackened by smoke. First: `urth-36/p-020`. [Source](https://www.merriam-webster.com/dictionary/reechy).
- **thalassic** — Of the sea, especially an inland sea. First: `urth-42/p-062`. [Source](https://www.merriam-webster.com/dictionary/thalassic).
- **taffrail** — The rail around a ship’s stern. First: `urth-27/p-056`. [Source](https://www.merriam-webster.com/dictionary/taffrail).
- **pyx** — A small container for consecrated bread. First: `sword-38/p-019`. [Source](https://www.merriam-webster.com/dictionary/pyx).
- **isochronon** — A clock designed for precise timekeeping. First: `sword-34/p-009`. [Source](https://www.gutenberg.org/ebooks/29765).
- **casern** — A barracks or soldiers’ lodging. First: `shadow-16/p-041`. [Source](https://www.gutenberg.org/ebooks/29765).
- **cariole** — A light carriage. First: `claw-01/p-002`. [Source](https://www.gutenberg.org/ebooks/29765).
- **camarilla** — A ruler’s private circle of advisers. First: `shadow-25/p-048`. [Source](https://www.gutenberg.org/ebooks/29765).
- **amadou** — Tinder prepared from tree-growing fungi. First: `citadel-36/p-029`. [Source](https://www.gutenberg.org/ebooks/29765).
- **agnation** — Kinship traced through the male line. First: `urth-42/p-051`. [Source](https://www.gutenberg.org/ebooks/29765).
- **Velleity** — A wish too weak to become action. First: `shadow-23/p-033`. [Source](https://www.merriam-webster.com/dictionary/velleity).
- **Pyrexia** — Fever. First: `claw-02/p-011`. [Source](https://www.gutenberg.org/ebooks/29765).
- **hypostasis** — An underlying reality or distinct divine person. First: `shadow-06/p-108`. [Source](https://www.gutenberg.org/ebooks/29765).
- **capote** — A long cloak, often hooded. First: `shadow-16/p-051`. [Source](https://www.gutenberg.org/ebooks/29765).
- **loggia** — A roofed gallery open on one or more sides. First: `urth-41/p-022`. [Source](https://www.gutenberg.org/ebooks/29765).
- **cornet** — A cavalry standard-bearer; also a brass instrument. First: `claw-13/p-042`. [Source](https://www.gutenberg.org/ebooks/29765).
- **heliotrope** — A fragrant flower; also a purple color or bloodstone. First: `claw-22/p-009`. [Source](https://www.gutenberg.org/ebooks/29765).
- **cerise** — A vivid cherry-red color. First: `shadow-27/p-015`. [Source](https://www.gutenberg.org/ebooks/29765).
- **peregrine** — A swift falcon; also wandering or foreign. First: `sword-28/p-053`. [Source](https://www.gutenberg.org/ebooks/29765).
- **vicuña** — A small Andean relative of the llama. First: `shadow-17/p-003`. [Source](https://www.gutenberg.org/ebooks/29765).
- **skewbald** — White and another color besides black. First: `sword-02/p-013`. [Source](https://www.gutenberg.org/ebooks/29765).
- **sateen** — A smooth, glossy fabric. First: `shadow-12/p-005`. [Source](https://www.gutenberg.org/ebooks/29765).
- **quadrille** — A four-player card game; also a square dance. First: `shadow-07/p-078`. [Source](https://www.gutenberg.org/ebooks/29765).
- **pentadactyl** — Having five fingers or toes. First: `citadel-21/p-016`. [Source](https://www.gutenberg.org/ebooks/29765).
- **palatinate** — A territory governed by a palatine. First: `shadow-18/p-017`. [Source](https://www.gutenberg.org/ebooks/29765).
- **parterre** — An ornamental arrangement of garden beds. First: `shadow-16/p-040`. [Source](https://www.gutenberg.org/ebooks/29765).
- **nocturne** — A musical night-piece. First: `citadel-10/p-012`. [Source](https://www.gutenberg.org/ebooks/29765).
- **maniple** — A Roman military unit; also a priest’s vestment. First: `citadel-16/p-003`. [Source](https://www.gutenberg.org/ebooks/29765).
- **hellebore** — A flowering plant, often poisonous. First: `sword-33/p-003`. [Source](https://www.gutenberg.org/ebooks/29765).
- **gravid** — Pregnant; figuratively full or heavy with meaning. First: `urth-23/p-016`. [Source](https://www.merriam-webster.com/dictionary/gravid).
- **fibula** — A fastening brooch; also the outer lower-leg bone. First: `shadow-19/p-008`. [Source](https://www.gutenberg.org/ebooks/29765).
- **espalier** — A tree trained flat against a support. First: `claw-21/p-051`. [Source](https://www.gutenberg.org/ebooks/29765).
- **eschatology** — Religious teaching about last things. First: `urth-49/p-007`. [Source](https://www.gutenberg.org/ebooks/29765).
- **equerry** — An officer responsible for a noble household’s horses. First: `urth-25/p-007`. [Source](https://www.gutenberg.org/ebooks/29765).
- **dulcimer** — A stringed instrument with a resonating soundboard. First: `shadow-19/p-008`. [Source](https://www.merriam-webster.com/dictionary/dulcimer).
- **dryad** — A tree or woodland nymph. First: `claw-10/p-060`. [Source](https://www.gutenberg.org/ebooks/29765).
- **condottiere** — An Italian mercenary commander. First: `citadel-19/p-028`. [Source](https://www.gutenberg.org/ebooks/29765).
- **comfit** — A sweet made by coating fruit or seeds in sugar. First: `shadow-18/p-026`. [Source](https://www.gutenberg.org/ebooks/29765).
- **cohort** — A subdivision of a Roman legion. First: `citadel-35/p-063`. [Source](https://www.gutenberg.org/ebooks/29765).
- **citron** — A thick-rinded citrus fruit. First: `shadow-16/p-040`. [Source](https://www.gutenberg.org/ebooks/29765).
- **chandler** — A candle-maker or dealer in supplies. First: `shadow-35/p-010`. [Source](https://www.gutenberg.org/ebooks/29765).
- **celeriac** — Celery grown for its swollen edible base. First: `urth-05/p-001`. [Source](https://www.gutenberg.org/ebooks/29765).
- **cantle** — The raised rear part of a saddle. First: `shadow-35/p-049`. [Source](https://www.gutenberg.org/ebooks/29765).
- **burgess** — A citizen or representative of a borough. First: `shadow-02/p-018`. [Source](https://www.gutenberg.org/ebooks/29765).
- **belvedere** — A building or gallery designed for a view. First: `claw-11/p-064`. [Source](https://www.gutenberg.org/ebooks/29765).
- **atelier** — An artist’s studio or workshop. First: `citadel-26/p-011`. [Source](https://www.gutenberg.org/ebooks/29765).
- **Theologoumenon** — A theological opinion outside established doctrine. First: `claw-10/p-035`. [Source](https://www.collinsdictionary.com/us/dictionary/english/theologoumenon).
- **Numen** — A divine presence or power. First: `shadow-21/p-011`. [Source](https://www.merriam-webster.com/dictionary/numen).
- **Ylem** — The primordial matter of cosmological theories. First: `sword-27/p-016`. [Source](https://www.merriam-webster.com/dictionary/ylem).
- **Urbis** — Possibly Latin: of a city. First: `urth-33/p-019`. [Source](https://atlas.perseus.tufts.edu/dictionaries/entry/urn%3Acite2%3Ascaife-viewer%3Adictionary-entries.atlas_v1%3Alat.ls.perseus-eng2-n49895/).
- **Serenus** — Latin: clear, tranquil, or serene. First: `urth-01/p-030`. [Source](https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.04.0060%3Aentry%3Dserenus).
- **Pascua** — Possibly Latin: pastures. First: `citadel-13/p-003`. [Source](https://www.mobot.org/mobot/latindict/keyDetail.aspx?keyWord=pascuum).
- **Fors** — Latin: chance or luck. First: `claw-15/p-012`. [Source](https://atlas.perseus.tufts.edu/dictionaries/entry/urn%3Acite2%3Ascaife-viewer%3Adictionary-entries.atlas_v1%3Alat.ls.perseus-eng2-n18623/).
- **xenagie** — An ancient Greek military formation. First: `shadow-27/p-001`. [Source](https://www.littre.org/definition/x%C3%A9nagie).
- **braquemar** — Possibly braquemart, a broad short sword. First: `shadow-28/p-018`. [Source](https://www.cnrtl.fr/definition/braquemart).
- **Lux dei vitae viam monstrat** — Latin: God’s light shows the way of life. First: `shadow-04/p-038`. [Source](https://digital.library.upenn.edu/women/gatty/sundials/321.html).
- **Felicibus brevis, miseris hora longa** — Latin: the hour is short for the happy, long for the unhappy. First: `shadow-04/p-038`. [Source](https://www.dizionario-italiano.it/dizionario-italiano-brocardi.php?browse=2474).
- **Aspice ut aspiciar** — Latin: look upon me so that I may be seen. First: `shadow-04/p-038`. [Source](https://upload.wikimedia.org/wikipedia/commons/d/da/Historic_devices%2C_badges%2C_and_war-cries_%28IA_cu31924029796939%29.pdf).
- **Hieros** — Greek: sacred or holy. First: `urth-21/p-012`. [Source](https://www.billmounce.com/greek-dictionary/hieros).
- **Incusus** — Latin: hammered or forged. First: `claw-24/p-154`. [Source](https://www.latinlexicon.org/definition.php?p1=2027995&p2=i).
- **Hypogeon** — Possibly hypogeum, an underground chamber. First: `shadow-18/p-004`. [Source](https://www.merriam-webster.com/dictionary/hypogeum).
- **Quasar** — An exceptionally luminous galactic nucleus. First: `shadow-30/p-007`. [Source](https://science.nasa.gov/mission/hubble/science/science-behind-the-discoveries/hubble-quasars/).
- **Catodon** — A scientific name associated with the sperm whale. First: `urth-43/p-043`. [Source](https://animaldiversity.org/accounts/Physeter_catodon/).
- **Murene** — Possibly French murène, a moray eel. First: `sword-32/p-032`. [Source](https://www.cnrtl.fr/definition/mur%C3%A8ne).
- **Zelezo** — Possibly Czech železo: iron. First: `urth-04/p-051`. [Source](https://m.dict.cc/czech-english/%C5%BEelezo.html).
- **Hierro** — Spanish: iron. First: `urth-08/p-033`. [Source](https://dle.rae.es/hierro).
- **Hadid** — Arabic: iron. First: `urth-08/p-033`. [Source](https://www.lisaanmasry.org/online/word.php?cn=3&id=5378).
- **Conexa** — Possibly Latin: joined or connected. First: `citadel-10/p-032`. [Source](https://atlas.perseus.tufts.edu/dictionaries/entry/urn%3Acite2%3Ascaife-viewer%3Adictionary-entries.atlas_v1%3Alat.ls.perseus-eng2-n10062/).
- **Theoanthropos** — Possibly Greek theanthropos: god-man. First: `shadow-21/p-012`. [Source](https://ahdictionary.com/word/search.html?q=Theanthropic).
- **Rose the Graced** — Possibly Fair Rosamund and her punning epitaph. First: `shadow-10/p-035`. [Source](https://words.fromoldbooks.org/Brewer-DictionaryOfPhraseAndFable/r/rosamond.html).
- **whorl** — A spiral, coil, or ring. First: `shadow-15/p-055`. [Source](https://www.merriam-webster.com/dictionary/whorl).
- **hanger** — A short sword, formerly carried by sailors. First: `claw-07/p-036`. [Source](https://www.merriam-webster.com/dictionary/hanger).
- **jakes** — An old word for a privy or toilet. First: `citadel-12/p-076`. [Source](https://www.gutenberg.org/cache/epub/5402/pg5402-images.html).
- **virescent** — Greenish or becoming green. First: `urth-45/p-040`. [Source](https://www.merriam-webster.com/dictionary/virescent).

### Long Sun

- **Sigada** — Possibly Arabic sajjāda, a prayer rug. First: `exodus-02/p-178`. [Source](https://www.rekhta.org/urdudictionary?keyword=sajjaada).
- **Silah** — Possibly Arabic silāḥ, a weapon or arms. First: `exodus-04/p-061`. [Source](https://rekhtadictionary.com/meaning-of-silaah).
- **Ganymedia** — Possibly Ganymeda, an ancient name for Hebe. First: `nightside-06/p-031`. [Source](https://www.theoi.com/Text/Pausanias2A.html).
- **Hymenocallis** — The spider-lily genus; Greek for beautiful membrane. First: `lake-07/p-231`. [Source](https://plants.ces.ncsu.edu/plants/hymenocallis/common-name/peruvian-daffodil/).
- **Magnesia** — Magnesium oxide, a white heat-resistant compound. First: `exodus-16/p-195`. [Source](https://www.merriam-webster.com/dictionary/magnesia).
- **Ur** — Possibly Ur, the ancient Sumerian city. First: `lake-06/p-308`. [Source](https://www.penn.museum/sites/expedition/ur-and-its-treasures/).
- **Gayfeather** — Liatris, also called blazing-star. First: `calde-03/p-193`. [Source](https://plants.ces.ncsu.edu/plants/liatris-scariosa/).
- **Macaque** — A monkey of the genus Macaca. First: `calde-03/p-193`. [Source](https://www.merriam-webster.com/dictionary/macaque).
- **Marten** — A slender woodland mammal of the weasel family. First: `nightside-09/p-004`. [Source](https://www.merriam-webster.com/dictionary/marten).
- **Femur** — The thighbone; Latin femur means thigh. First: `calde-06/p-025`. [Source](https://www.merriam-webster.com/dictionary/femur).
- **Gecko** — A small lizard, usually active at night. First: `calde-05/p-421`. [Source](https://www.merriam-webster.com/dictionary/gecko).
- **Bream** — A name for several kinds of freshwater and marine fish. First: `calde-02/p-070`. [Source](https://www.merriam-webster.com/dictionary/bream).
- **Rook** — Corvus frugilegus, a crow that nests in colonies. First: `calde-09/p-265`. [Source](https://www.merriam-webster.com/dictionary/rook).
- **Holly** — An Ilex shrub or tree, often with red berries. First: `calde-03/p-193`. [Source](https://www.merriam-webster.com/dictionary/holly).
- **Aloe** — A succulent plant with thick, fleshy leaves. First: `calde-03/p-193`. [Source](https://www.merriam-webster.com/dictionary/aloe).
- **Flax** — Linum, the plant that supplies linen fibre and linseed. First: `lake-12/p-006`. [Source](https://www.merriam-webster.com/dictionary/flax).
- **’ishsh** — Possibly Arabic ʿishsh, a nest. First: `exodus-14/p-126`. [Source](https://upload.wikimedia.org/wikipedia/commons/9/9f/English-Arabic_vocabulary_for_the_use_of_officials_in_the_Anglo-Egyptian_Sudan_%281905%29.pdf).
- **Betifham ’arabi** — Arabic: Do you understand Arabic? First: `exodus-05/p-037`. [Source](https://yojik.eu/languages/DLI/Arabic-Saudi/Headstart-Texts/DLI%20Saudi%20Arabic%20Headstart.pdf).
- **jefe** — Spanish for chief or boss. First: `nightside-01/p-085`. [Source](https://dle.rae.es/jefe).
- **abram** — Old cant for mad or insane. First: `nightside-11/p-090`. [Source](https://www.horntip.com/html/books_%26_MSS/1890s/1890-1909_slang_and_its_analogues_%28HCs%29/1909_vol_1_%28revised%29/1909_slang_and_its_analogues_vol_1_revised.pdf).
- **bing** — Old cant: to go or depart. First: `exodus-12/p-402`. [Source](https://www.gutenberg.org/cache/epub/5402/pg5402-images.html).
- **cant** — A group’s private vocabulary; also insincere talk. First: `nightside-02/p-056`. [Source](https://www.merriam-webster.com/dictionary/cant).
- **cully** — A fool or easily deceived person. First: `nightside-02/p-038`. [Source](https://www.gutenberg.org/cache/epub/5402/pg5402-images.html).
- **dell** — Old cant for a young woman. First: `nightside-11/p-088`. [Source](https://www.gutenberg.org/cache/epub/5402/pg5402-images.html).
- **doss** — A rough bed; to sleep or bed down. First: `exodus-02/p-084`. [Source](https://www.merriam-webster.com/dictionary/doss).
- **gammon** — Old slang for chatter, humbug, or deceptive talk. First: `lake-05/p-164`. [Source](https://www.merriam-webster.com/dictionary/gammon).
- **hanger** — A short sword, formerly carried by sailors. First: `nightside-03/p-055`. [Source](https://www.merriam-webster.com/dictionary/hanger).
- **hog grubber** — Old slang for a miserly person. First: `exodus-06/p-283`. [Source](https://www.gutenberg.org/cache/epub/5402/pg5402-images.html).
- **jakes** — An old word for a privy or toilet. First: `exodus-08/p-024`. [Source](https://www.gutenberg.org/cache/epub/5402/pg5402-images.html).
- **kate** — A lock-pick or false key in thieves’ cant. First: `exodus-12/p-396`. [Source](https://www.gutenberg.org/cache/epub/5402/pg5402-images.html).
- **ken** — A house or lodging in old thieves’ cant. First: `lake-05/p-220`. [Source](https://www.gutenberg.org/cache/epub/5402/pg5402-images.html).
- **lushes** — Drinks alcohol, in old slang. First: `exodus-06/p-283`. [Source](https://www.gutenberg.org/cache/epub/5402/pg5402-images.html).
- **go the nose** — To act as an informer. First: `nightside-03/p-189`. [Source](https://www.gutenberg.org/cache/epub/5402/pg5402-images.html).
- **padken** — Possibly padding-ken, a lodging-house used by thieves. First: `exodus-06/p-360`. [Source](https://readingroo.ms/3/8/6/9/38699/38699-h/38699-h.htm).
- **plonk** — Cheap or poor-quality wine. First: `exodus-06/p-321`. [Source](https://www.merriam-webster.com/dictionary/plonk).
- **putt** — Possibly putz, a Yiddish-derived insult for a fool. First: `nightside-01/p-102`. [Source](https://www.merriam-webster.com/dictionary/putz).
- **pure quill** — The genuine article; something of the best quality. First: `exodus-11/p-147`. [Source](https://upload.wikimedia.org/wikipedia/commons/3/31/Farmer_-_Slang_and_its_analogues_past_and_present_-_Volume_5.pdf).
- **scavy** — Possibly scavey: knowledge, sense, or understanding. First: `nightside-04/p-072`. [Source](https://www.gutenberg.org/cache/epub/5402/pg5402-images.html).
- **scut** — A short upright tail, as on a rabbit or hare. First: `lake-04/p-212`. [Source](https://www.merriam-webster.com/dictionary/scut).
- **snaffle** — To obtain by stealth or irregular means. First: `lake-03/p-187`. [Source](https://www.merriam-webster.com/dictionary/snaffle).
- **snoodge** — Old cant: to snooze or sleep. First: `nightside-04/p-070`. [Source](https://www.gutenberg.org/cache/epub/5402/pg5402-images.html).
- **sojer** — A dialect spelling of soldier. First: `calde-02/p-201`. [Source](https://www.dsl.ac.uk/entry/snd00082630).
- **twig** — To notice, recognize, or understand. First: `lake-05/p-131`. [Source](https://www.gutenberg.org/cache/epub/5402/pg5402-images.html).
- **chit** — A dismissive word for a child or young woman. First: `nightside-11/p-027`. [Source](https://www.merriam-webster.com/dictionary/chit).
- **gelt** — Money; from German, Dutch, and Yiddish forms. First: `nightside-02/p-049`. [Source](https://www.merriam-webster.com/dictionary/gelt).
- **peery** — Watchful, suspicious, or inquisitive. First: `exodus-06/p-279`. [Source](https://www.gutenberg.org/cache/epub/5402/pg5402-images.html).
- **lily** — A flowering bulb; also pure or unsullied. First: `nightside-01/p-107`. [Source](https://www.dictionary.com/browse/lily).
- **cits** — An old term for citizens or townspeople. First: `lake-05/p-220`. [Source](https://www.gutenberg.org/cache/epub/5402/pg5402-images.html).
- **cornet** — A cavalry standard-bearer; also a brass instrument. First: `calde-06/p-358`. [Source](https://www.gutenberg.org/ebooks/29765).
- **peregrine** — A swift falcon; also wandering or foreign. First: `nightside-07/p-246`. [Source](https://www.gutenberg.org/ebooks/29765).
- **gravid** — Pregnant; figuratively full or heavy with meaning. First: `nightside-11/p-114`. [Source](https://www.merriam-webster.com/dictionary/gravid).
- **citron** — A thick-rinded citrus fruit. First: `nightside-02/p-002`. [Source](https://www.gutenberg.org/ebooks/29765).
- **bombazine** — A twilled fabric traditionally made of silk and worsted wool. First: `lake-05/p-048`. [Source](https://www.merriam-webster.com/dictionary/bombazine).
- **coracle** — A small skin- or fabric-covered boat. First: `exodus-afterward/p-007`. [Source](https://www.merriam-webster.com/dictionary/coracle).
- **cresset** — A metal vessel holding a lighted fire. First: `nightside-02/p-010`. [Source](https://www.merriam-webster.com/dictionary/cresset).
- **crenels** — The gaps between a battlement’s raised sections. First: `nightside-05/p-010`. [Source](https://www.merriam-webster.com/dictionary/crenel).
- **virescent** — Greenish or becoming green. First: `calde-01/p-214`. [Source](https://www.merriam-webster.com/dictionary/virescent).
- **Loganstone** — A delicately balanced rock that can be made to sway. First: `lake-10/p-137`. [Source](https://www.collinsdictionary.com/us/dictionary/english/rocking-stone).

### Short Sun

- **Darjan** — Hindi: a dozen. First: `blue-12/p-110`. [Source](https://www.collinsdictionary.com/dictionary/hindi-english/दर्जन).
- **Rajya Mantri** — Hindi: minister of state. First: `blue-01/p-010`. [Source](https://cabsec.nic.in/writereaddata/changeinportfolio/english/1_Upload_2797.pdf).
- **Kilhari** — Possibly a traditional name for a cattle herder. First: `blue-10/p-003`. [Source](https://www.gazetteers.maharashtra.gov.in/cultural.maharashtra.gov.in/english/gazetteer/Nashik%20District/pro_animals.html).
- **Roti** — Hindi: bread, especially an unleavened flatbread. First: `blue-11/p-102`. [Source](https://www.collinsdictionary.com/dictionary/english/roti).
- **Ram** — Possibly Rama, hero of the Ramayana and an incarnation of Vishnu. First: `blue-10/p-009`. [Source](https://www.metmuseum.org/exhibitions/listings/2019/sita-and-rama-ramayana-indian-painting).
- **Mura** — Japanese: a village. First: `blue-04/p-213`. [Source](https://www.dictionary.com/browse/mura).
- **Schreiner** — German: a joiner or cabinetmaker. First: `green-13/p-008`. [Source](https://www.duden.de/rechtschreibung/Schreiner).
- **Flosser** — Possibly German Flößer: a raftman. First: `green-13/p-054`. [Source](https://www.duden.de/rechtschreibung/Floeszer).
- **Dusra Agast** — Hindi: the second of August. First: `blue-10/p-224`. [Source](https://www.collinsdictionary.com/us/dictionary/hindi-english/दूसरा).
- **Merfrow** — Possibly Dutch mevrouw: madam or Mrs. First: `blue-06/p-181`. [Source](https://assets.cambridge.org/97805216/42538/sample/9780521642538ws.pdf).
- **Rimo** — Possibly Italian rimo: I rhyme. First: `green-20/p-032`. [Source](https://www.treccani.it/vocabolario/rimare/).
- **Cantoro** — Possibly Italian cantore: a singer or chorister. First: `green-14/p-174`. [Source](https://www.treccani.it/vocabolario/cantore/).
- **Badour** — Possibly Badoura, a princess of the Arabian Nights. First: `green-23/p-035`. [Source](https://www.gutenberg.org/cache/epub/51219/pg51219-images.html).
- **Choora** — A straight dagger from the Khyber region. First: `blue-12/p-017`. [Source](https://www.metmuseum.org/art/collection/search/31612).
- **tentie** — Scots: watchful or careful. First: `return-16/p-151`. [Source](https://www.dsl.ac.uk/entry/snd/tent_n3_v1_adj2).
- **Skany** — Possibly Cocopa skany: to break a long object into pieces. First: `blue-06/p-001`. [Source](https://books.google.com/books?id=km67EAAAQBAJ&pg=PA246).
- **Seanettle** — A stinging jellyfish of the genus Chrysaora. First: `return-13/p-196`. [Source](https://www.aquariumofpacific.org/onlinelearningcenter/species/pacific_sea_nettle).
- **Firebrat** — A heat-loving, wingless insect related to silverfish. First: `return-02/p-006`. [Source](https://extension.umd.edu/resource/silverfish-and-firebrats).
- **Smew** — A small Eurasian diving duck. First: `blue-15/p-008`. [Source](https://www.rspb.org.uk/birds-and-wildlife/smew).
- **Hawkowl** — A northern owl that often hunts by day. First: `return-02/p-283`. [Source](https://www.allaboutbirds.org/guide/Northern_Hawk_Owl/overview).
- **Spirea** — A flowering shrub of the genus Spiraea. First: `return-04/p-301`. [Source](https://plants.ces.ncsu.edu/plants/spiraea/common-name/spirea/).
- **Verbena** — A flowering plant also called vervain. First: `return-04/p-301`. [Source](https://www.rhs.org.uk/plants/18816/verbena-officinalis/details).
- **Myrtle** — An aromatic evergreen shrub with white flowers. First: `return-04/p-303`. [Source](https://plants.ces.ncsu.edu/plants/myrtus-communis/).
- **Honeysuckle** — A flowering shrub or vine of the genus Lonicera. First: `return-03/p-023`. [Source](https://www.rhs.org.uk/plants/68665/lonicera-fragrantissima/details).
- **Tomcod** — A small codlike coastal fish. First: `return-17/p-321`. [Source](https://www.maine.gov/dmr/fisheries/sea-run-fisheries/sea-run-species/tomcod).
- **brathair** — Scottish Gaelic: brother. First: `return-04/p-209`. [Source](https://www.learngaelic.scot/sol/episodes/ep.jsp?clip=1&prog=14).
- **Seadh** — Scottish Gaelic: yes or indeed. First: `return-08/p-297`. [Source](https://www.faclair.com/?txtSearch=seagh).
- **Wight** — An old word for a person; also brave or stalwart. First: `green-13/p-199`. [Source](https://www.merriam-webster.com/dictionary/wight).
- **Hephaestus** — The Greek god of fire and metalworking. First: `blue-05/p-113`. [Source](https://www.theoi.com/Olympios/Hephaistos.html).
- **carabao** — A water buffalo. First: `blue-15/p-032`. [Source](https://www.merriam-webster.com/dictionary/carabao).
- **bombazine** — A twilled fabric traditionally made of silk and worsted wool. First: `return-02/p-171`. [Source](https://www.merriam-webster.com/dictionary/bombazine).
- **fashed** — Scots: troubled, bothered, or worried. First: `return-06/p-221`. [Source](https://dsl.ac.uk/entry/snd/fash).
- **ghaists** — Scots: ghosts. First: `return-08/p-073`. [Source](https://dsl.ac.uk/entry/snd/ghaist).
- **muckle** — Scots: much, large, or great. First: `return-02/p-293`. [Source](https://dsl.ac.uk/entry/snd/muckle).
- **Fient** — Scots: the Devil; also an emphatic exclamation or denial. First: `return-14/p-340`. [Source](https://dsl.ac.uk/entry/snd/fient).
- **braw** — Scots: fine, splendid, or handsome. First: `return-14/p-076`. [Source](https://dsl.ac.uk/entry/snd/braw).
- **rais-man** — Possibly Arabic raʾīs: a chief, leader, or captain. First: `green-24/p-050`. [Source](https://www.merriam-webster.com/dictionary/rais).
- **coracle** — A small skin- or fabric-covered boat. First: `blue-01/p-027`. [Source](https://www.merriam-webster.com/dictionary/coracle).
- **cresset** — A metal vessel holding a lighted fire. First: `green-23/p-002`. [Source](https://www.merriam-webster.com/dictionary/cresset).
- **pannikin** — A small pan or drinking cup. First: `return-04/p-072`. [Source](https://www.merriam-webster.com/dictionary/pannikin).
- **ratlines** — Rope steps used to climb a ship’s rigging. First: `return-17/p-246`. [Source](https://www.merriam-webster.com/dictionary/ratline).
- **crenels** — The gaps between a battlement’s raised sections. First: `return-06/p-223`. [Source](https://www.merriam-webster.com/dictionary/crenel).
- **gaff-topsail** — A usually triangular sail set above a gaff. First: `blue-05/p-062`. [Source](https://www.merriam-webster.com/dictionary/gaff-topsail).
- **virescent** — Greenish or becoming green. First: `green-23/p-002`. [Source](https://www.merriam-webster.com/dictionary/virescent).
- **tenebrious** — Dark, murky, or gloomy. First: `return-01/p-057`. [Source](https://www.merriam-webster.com/dictionary/tenebrious).
- **auspicatory** — Relating to auspices or omens. First: `return-10/p-062`. [Source](https://www.wordnik.com/words/auspicatory).
- **Tallow** — Rendered animal fat used for candles and soap. First: `return-02/p-174`. [Source](https://www.merriam-webster.com/dictionary/tallow).
- **Ray** — A flattened fish related to skates and stingrays. First: `return-10/p-219`. [Source](https://www.merriam-webster.com/dictionary/ray).
- **Warren** — A rabbit breeding ground or small-game preserve. First: `green-13/p-199`. [Source](https://www.merriam-webster.com/dictionary/warren).
- **Loganstone** — A delicately balanced rock that can be made to sway. First: `green-14/p-155`. [Source](https://www.collinsdictionary.com/us/dictionary/english/rocking-stone).
- **Lann** — Possibly Gaelic: a blade; also an enclosure or church. First: `return-06/p-219`. [Source](https://www.faclair.com/?txtSearch=lann).
- **Legume** — A plant of the pea family, or its pod. First: `return-20/p-037`. [Source](https://www.merriam-webster.com/dictionary/legume).
- **Lily** — A bulbous flowering plant of the genus Lilium. First: `return-13/p-196`. [Source](https://www.rhs.org.uk/plants/lilies).
- **familiare** — Possibly a familiar spirit, a supernatural attendant. First: `green-01/p-112`. [Source](https://www.cultus.hk/Latin_vocab/adject3/familiaris.html).
- **dulcimer** — A stringed instrument with a resonating soundboard. First: `blue-05/p-088`. [Source](https://www.merriam-webster.com/dictionary/dulcimer).
- **Magnesia** — Magnesium oxide, a white heat-resistant compound. First: `blue-01/p-217`. [Source](https://www.merriam-webster.com/dictionary/magnesia).
- **cant** — A group’s private vocabulary; also insincere talk. First: `return-14/p-249`. [Source](https://www.merriam-webster.com/dictionary/cant).
- **gelt** — Money; from German, Dutch, and Yiddish forms. First: `blue-01/p-047`. [Source](https://www.merriam-webster.com/dictionary/gelt).

## Revised existing entries

- **Long Sun:** prolocutor, gelada, mucor, asphodella, hyacinth, mint.
- **Short Sun:** prolocutor, gelada, inclito, soldo, mucor, gioioso, adatta, hyacinth, mint, sfido, advocaat, sweetbay, heleno.

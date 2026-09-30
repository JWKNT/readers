"""Small original pen-drawn ornaments and lossless source-divider decoration.

Run ``python3 tools/reader_ornaments.py`` to regenerate the authored SVGs.
The drawings are original project artwork, require no fonts or external assets,
and share the existing Sun ornaments' monochrome 60 × 52 coordinate system.
"""
from pathlib import Path
import html
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SEPARATORS = re.compile(r'[\s*•●◦·‧∙⋅⁂⁎❦]+\Z')

def _local(tag):
    return tag.rsplit('}', 1)[-1] if isinstance(tag, str) else ''

def _class(node, value):
    classes = node.get('class', '').split()
    if value not in classes:
        classes.append(value)
    node.set('class', ' '.join(classes))

def _tag(node, local):
    return node.tag.rsplit('}', 1)[0] + '}' + local if '}' in node.tag else local

def _image(node, slug):
    return ET.Element(_tag(node, 'img'), {
        'src': f'../../assets/ornaments/{slug}.svg', 'alt': '',
        'aria-hidden': 'true', 'width': '60', 'height': '52',
        'class': 'scene-ornament', 'decoding': 'async'})

def decorate(tree, slug, tailpiece=False):
    """Decorate source breaks without changing their text, attributes, or IDs.

    Accept an Element or ElementTree. Return the number of breaks decorated.
    Only a whole separator paragraph/div or an explicit scene-divider span is
    eligible. Other text (including bullets within prose) is left untouched.
    """
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        raise ValueError(f'Invalid ornament slug: {slug!r}')
    root = tree.getroot() if isinstance(tree, ET.ElementTree) else tree
    parents = {child: parent for parent in root.iter() for child in parent}
    candidates = []
    for node in root.iter():
        if _local(node.tag) not in {'p', 'div', 'span'}:
            continue
        if any({'scene-break', 'story-tailpiece', 'source-divider-text'} & set(item.get('class', '').split())
               for item in [node, *_ancestors(node, parents)]):
            continue
        value = ''.join(node.itertext())
        explicit = 'scene-divider' in node.get('class', '').split()
        if explicit:
            parent = parents.get(node)
            if parent is not None and _local(parent.tag) in {'p', 'div'} and ''.join(parent.itertext()).strip() == value.strip() and len(parent) == 1:
                candidates.append(parent)
            else:
                candidates.append(node)
        elif _local(node.tag) in {'p', 'div'} and value.strip() and SEPARATORS.fullmatch(value):
            # Prefer leaf containers; never replace an outer wrapper around breaks.
            if not any(_local(child.tag) in {'p', 'div'} for child in node):
                candidates.append(node)
    done = set()
    count = 0
    for node in candidates:
        if id(node) in done or 'scene-break' in node.get('class', '').split():
            continue
        # A promoted paragraph owns its span; do not decorate the removed span.
        if any(id(ancestor) in done for ancestor in _ancestors(node, parents)):
            continue
        original_text, original_children = node.text, list(node)
        descendants = set(node.iter())
        attrs, tail = dict(node.attrib), node.tail
        node.clear()
        node.attrib.update(attrs)
        if 'scene-divider' in node.get('class', '').split():
            node.set('class', ' '.join(c for c in node.get('class', '').split() if c != 'scene-divider'))
        node.tail = tail
        _class(node, 'scene-break')
        hidden = ET.SubElement(node, _tag(node, 'span'), {'class': 'source-divider-text', 'hidden': 'hidden'})
        hidden.text = original_text
        hidden.extend(original_children)
        for child in hidden.iter():
            if 'scene-divider' in child.get('class', '').split():
                child.set('class', ' '.join(c for c in child.get('class', '').split() if c != 'scene-divider'))
        node.append(_image(node, slug))
        done.update(map(id, descendants))
        count += 1
    if tailpiece and not any('story-tailpiece' in node.get('class', '').split() for node in root.iter()):
        end = ET.SubElement(root, _tag(root, 'div'), {'class': 'story-tailpiece', 'aria-hidden': 'true'})
        end.append(_image(root, slug))
    return count

def _ancestors(node, parents):
    while node in parents:
        node = parents[node]
        yield node

# Drawing primitives. Fine secondary strokes and small solid accents reproduce
# clearly at reading size; no lettering or plot-dependent symbols are used.
def path(d, fill='none', width=1.45):
    return f'<path d="{d}" fill="{fill}" stroke="black" stroke-width="{width}"/>'

def dot(x,y,r=1.5):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="black" stroke="none"/>'

def circle(x,y,r,width=1.3):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="black" stroke-width="{width}"/>'

def group(body,transform):
    return f'<g transform="{transform}">{body}</g>'

def star(x,y,r=5):
    return path(f'M{x} {y-r}Q{x+1} {y-1} {x+r} {y}Q{x+1} {y+1} {x} {y+r}Q{x-1} {y+1} {x-r} {y}Q{x-1} {y-1} {x} {y-r}Z','black',.5)

def leaf(x,y,angle=0,scale=1):
    return group(path('M0 0C-9 -4 -10 -13 0 -20C10 -13 9 -4 0 0Z','black',.4)+path('M0 -2V-16',width=.65).replace('stroke="black"','stroke="white"'),f'translate({x} {y}) rotate({angle}) scale({scale})')

def waves(y=34):
    return path(f'M7 {y}Q13 {y-5} 19 {y}T31 {y}T43 {y}T55 {y}M12 {y+6}Q18 {y+1} 24 {y+6}T36 {y+6}T48 {y+6}',width=1.15)

def crescent(x=30,y=22,r=12):
    return path(f'M{x+.4*r} {y-r}A{r} {r} 0 1 0 {x+.4*r} {y+r}C{x-.25*r} {y+.6*r} {x-.25*r} {y-.6*r} {x+.4*r} {y-r}Z','black',.5)

def book():
    return path('M30 17Q20 11 9 15V37Q20 33 30 39Q40 33 51 37V15Q40 11 30 17ZM30 17V39M13 19Q20 17 26 20M13 24Q20 22 26 25M34 20Q40 17 47 19M34 25Q40 22 47 24',width=1.25)

def pine(x,y,scale=1):
    return group(path('M0 -30L-7 -19H-4L-11 -10H-6L-14 0H14L6 -10H11L4 -19H7Z','black',.5)+path('M0 0V8',width=1.8),f'translate({x} {y}) scale({scale})')

def eye():
    return path('M6 26Q30 5 54 26Q30 47 6 26Z')+circle(30,26,7)+dot(30,26,2.5)

def hourglass():
    return path('M18 8H42M18 44H42M21 9C21 20 24 21 30 26C36 31 39 32 39 43M39 9C39 20 36 21 30 26C24 31 21 32 21 43')+path('M23 12H37L30 22ZM24 40L30 32L36 40Z','black',.5)

def house():
    return path('M9 25L30 8L51 25M15 21V43H45V21M25 43V31H35V43M20 26H24M36 26H40',width=1.5)

def bird():
    return path('M12 34Q22 35 27 28C22 23 20 17 21 13C26 16 29 17 33 19C35 11 40 9 43 13L50 15L44 18C43 30 34 36 23 35L14 41L18 34Z','black',.6)+dot(40,14,.65).replace('fill="black"','fill="white"')

def key():
    return circle(19,19,8)+path('M25 25L44 44M34 34L39 29M39 39L44 34',width=2)+circle(19,19,3,width=.8)

def rose():
    return path('M30 9C22 4 16 13 19 19C10 23 17 33 24 32C26 41 37 39 39 32C48 30 49 20 41 18C43 9 35 4 30 9ZM30 15C23 14 22 24 28 26C35 31 41 21 35 18C29 14 24 24 31 25M30 34V47M30 42Q20 33 15 38Q20 45 30 45M30 39Q41 31 45 34Q41 42 30 43',width=1.2)

def gear():
    return path('M25 8H35L36 14L42 16L47 13L52 22L47 27L48 33L53 37L47 45L40 42L35 44L33 49H23L22 43L17 40L10 42L5 33L11 29L11 23L6 19L12 11L19 14L24 13Z',width=1.25)+circle(29,28,10)+circle(29,28,3)

# All forms are independently composed; titles identify an ornament, not a
# claim about a work's hidden meaning. Existing Sun assets are never rewritten.
MOTIFS = {}
MOTIFS.update({
 'the-fifth-head-of-cerberus': (
    path('M13 35V42Q30 48 47 42V35M23 33L13 34L6 28L8 22L15 23L17 13L23 21M37 33L47 34L54 28L52 22L45 23L43 13L37 21M24 33L23 20L24 12L30 17L36 12L37 20L36 33L30 37Z',width=1.4)
    +dot(17,27,1)+dot(27,24,1)+dot(33,24,1)+dot(43,27,1)+path('M27 29H33L30 32Z','black',.5)),
 'the-island-of-doctor-death-and-other-stories':
    path('M6 32Q18 26 30 35Q42 26 54 32V42Q42 36 30 44Q18 36 6 42ZM30 35V44M16 26Q23 22 27 18L32 22L37 17L44 26Z','none',1.2)+star(30,9,3),
 'the-toy-theater':
    path('M13 9L47 17M43 8L17 18M19 11V31M42 16V32M30 16V27M30 27L24 35L30 43L36 35Z')+path('M12 45Q30 49 48 45',width=.8)+dot(19,33,1)+dot(42,34,1),
 'beech-hill':
    leaf(29,37,-30,1.35)+path('M8 42Q22 31 37 39T54 42M19 46H41',width=1.1),
 'the-recording':
    circle(28,26,18)+circle(28,26,14,.8)+circle(28,26,10,.8)+circle(28,26,4)+dot(28,26,1)+path('M51 9L46 11L39 30L35 32',width=2),
 'hour-of-trust':
    circle(30,12,7)+path('M30 8V12L34 14M12 29L42 24L51 36L20 42ZM20 42V47M12 29V37M51 36V44',width=1.2)+path('M20 25L17 21M37 21V18M9 36H5M53 29H57',width=1.8),
 'the-death-of-dr-island':
    circle(30,23,17)+path('M28 37Q30 23 34 16M34 16Q20 9 15 23M34 16Q30 8 23 10M34 16Q46 12 47 23M34 16Q40 6 43 12M34 16Q30 16 25 25',width=1.45)+path('M12 43H48M22 47H38',width=1),
 'la-befana':
    path('M15 41L40 12M19 33L11 32L5 42L18 47L26 36ZM8 42L17 34M12 44L21 35',width=1.3)+star(43,18,7)+star(29,7,2.5),
 'forlesen':
    path('M18 6H42V21H18ZM30 9V14L36 17M14 27H46V47H14Z',width=1.2)+path('M20 32H25M30 32H35M20 37H25M30 37H35M20 42H25M38 42H41',width=2),
 'westwind':
    path('M16 7H45V43H16ZM30 7V43M16 24H45M4 20C11 9 26 25 37 17M8 31C17 20 35 37 52 25',width=1.3)+path('M10 44C21 38 40 48 52 40',width=.8),
 'the-hero-as-werwolf':
    group(crescent(27,17,10),'translate(5 -2)')+path('M30 28C25 24 20 30 20 35C14 44 22 48 30 44C38 48 46 44 40 35C40 30 35 24 30 28Z','black',.5)+dot(16,28,3)+dot(23,23,3)+dot(37,23,3)+dot(44,28,3),
 'the-marvelous-brass-chessplaying-automaton':
    path('M8 43H32L30 38H12ZM13 37C16 31 21 30 19 25L11 28L8 23L19 11L20 6L26 11C34 20 28 29 28 37M12 23L19 17',width=1.3)+dot(22,16,1)+group(gear(),'translate(31 21) scale(.42)'),
 'straw':
    path('M30 30C10 13 20 5 30 5C40 5 50 13 30 30ZM28 31H32M30 32Q25 36 30 40M15 46L42 35M18 35L42 46M19 42L18 38M24 40L23 36M36 41L37 37',width=1.2),
 'the-eyeflash-miracles':
    path('M9 27Q30 45 51 27M15 31L10 36M23 35L21 41M30 36V43M37 35L39 41M45 31L50 36M30 17V6M20 19L15 11M40 19L45 11',width=1.5)+star(30,25,3),
 'seven-american-nights':
    group(book(),'translate(0 9) scale(1 .8)')+''.join(star(x,y,2.2) for x,y in [(8,16),(15,10),(23,7),(31,5),(39,7),(47,10),(54,16)]),
 'the-detective-of-dreams':
    circle(25,22,15)+path('M36 34L48 46M39 34L50 44',width=2)+group(crescent(25,22,9),'translate(0 0)')+dot(33,17,1),
 'kevin-malone':
    path('M10 44V24C10 1 50 1 50 24V44M14 44V24C14 7 46 7 46 24V44M23 27V39M37 27V39M21 33H39M22 38H38M24 39L22 46M36 39L38 46M23 27H37M27 27V33M33 27V33',width=1.2),
 'the-god-and-his-man':
    path('M30 5L27 24L30 29L33 24ZM23 26H37M30 29V35M6 43Q18 26 32 40Q43 29 54 43M12 47Q24 34 40 47',width=1.2)+path('M18 15L13 12M42 15L47 12M20 6L18 2M40 6L42 2',width=.8),
 'on-the-train':
    circle(30,22,17)+path('M13 47Q19 31 30 21M47 47Q41 31 30 21M20 38H40M23 32H37M26 27H34M15 44H45',width=1.4)+path('M17 19H22M39 17H44',width=.8),
 'from-the-desk-of-gilmer-c-merton':
    path('M7 25L30 16L53 25V45H7ZM7 25L30 39L53 25M7 45L22 34M53 45L38 34M18 23V10H42V23M23 15H37M23 19H34',width=1.2)+dot(13,8,2)+dot(48,12,1),
 'death-of-the-island-doctor':
    path('M9 27Q19 19 29 27ZM18 23V12M18 12Q10 8 8 16M18 12Q28 7 29 16M34 29H52L48 34H39ZM43 29V18L50 25H43',width=1.3)+waves(39)+star(44,9,3),
 'redbeard':
    path('M9 23L30 6L51 23M15 20V45H45V20',width=1.25)+group(key(),'translate(15 11) scale(.52)'),
 'the-boy-who-hooked-the-sun':
    circle(35,18,9)+''.join(group(path('M35 5V2',width=1),f'rotate({a} 35 18)') for a in range(0,360,45))+path('M8 46C20 46 13 24 25 18M25 18C27 16 30 17 29 21C29 25 24 24 25 21',width=1.35),
 'parkroadsa-review':
    circle(25,20,15)+dot(25,20,2)+circle(25,11,4,1)+circle(17,23,4,1)+circle(33,23,4,1)+path('M40 20C53 27 16 31 17 39C18 46 44 43 51 49M41 23C48 27 12 32 14 40C16 49 42 46 48 51',width=1.25),
 'game-in-the-popes-head':
    path('M10 9H33V42H10ZM16 16L20 11L24 16L20 21ZM20 28L16 33L20 38L24 33Z','none',1.25)+path('M38 25L53 28V43L38 40ZM38 25L44 20L57 23L53 28M57 23V38L53 43',width=1.1)+dot(42,30,1)+dot(48,37,1)+dot(46,33.5,1),
 'and-when-they-appear':
    pine(30,37,.8)+star(30,7,5)+path('M13 46Q30 40 47 46',width=1)+dot(11,24,1)+dot(50,20,1),
 'bed-and-breakfast':
    group(key(),'translate(0 -1) scale(.7)')+path('M30 28H49V38Q40 48 31 38ZM49 30C60 27 58 39 49 37M27 45H53M36 23Q32 19 36 15M43 23Q39 19 43 15',width=1.2),
 'petting-zoo':
    path('M11 38C5 23 11 12 24 14C38 14 38 36 28 41C22 43 14 42 11 38ZM10 24Q15 19 16 26M17 17Q22 14 23 23M24 17Q30 17 30 25',width=1.25)+path('M43 46Q50 30 46 9M47 17L40 12M47 24L55 17M46 29L39 23M45 36L53 28M43 42L37 34',width=1.2),
 'the-tree-is-my-hat':
    path('M12 31C7 13 27 4 49 8C48 24 35 39 12 31ZM12 31L45 11M22 23L20 12M29 18L29 9M25 21L39 22M33 15L43 16',width=1.3)+waves(41),
 'has-anybody-seen-junie-moon':
    crescent(30,18,12)+path('M30 33V37M14 38H46M22 45L30 37L38 45ZM22 45H38',width=1.25)+dot(47,13,1.5),
 'a-cabin-on-the-coast':
    group(house(),'translate(10 0) scale(.66)')+waves(34)+path('M17 46H43',width=.8),
})
MOTIFS.update({
 'the-map':
    path('M7 12L22 8L38 13L53 8V40L38 45L22 40L7 45ZM22 8V40M38 13V45M12 20C22 13 22 29 32 25C43 20 42 36 49 32',width=1.2)+star(46,17,3),
 'the-dark-of-the-june':
    path('M12 5H48V47H12ZM16 9H44V43H16M23 38Q22 32 29 29L28 24C19 22 24 11 31 14C39 15 37 20 40 23L36 25L35 30Q40 31 41 38Z','none',1.15)+path('M23 38Q22 32 29 29L28 24C19 22 24 11 31 14C39 15 37 20 40 23L36 25L35 30Q40 31 41 38Z','black',.5),
 'the-death-of-hyle':
    path('M22 16Q20 4 30 4Q40 4 38 16M18 16H42L39 20V41L43 45H17L21 41V20ZM21 20H39M21 41H39M30 22V38',width=1.2)+path('M30 37C21 33 29 26 30 24C30 30 39 32 30 37Z','black',.5)+path('M11 23L6 21M11 32H5M49 23L54 21M49 32H55',width=.8),
 'from-the-notebook-of-dr-stein':
    path('M13 22Q13 17 20 17H41Q48 17 48 22V34Q48 39 41 39H20Q13 39 13 34ZM20 17Q27 28 20 39M41 17Q34 28 41 39M26 19V37M30 19V37M34 19V37M8 43H53M11 43V39M50 43V39M18 13L47 7L50 14L31 25',width=1.1),
 'thag':
    circle(39,30,14)+circle(39,30,10,.7)+circle(39,30,3)+path('M9 7L15 10L23 36L18 38L10 15ZM18 38L23 36L27 47L22 49ZM16 38L26 35',width=1.3),
 'the-nebraskan-and-the-nereid':
    path('M16 40V8M16 13L11 8M16 19L22 13M16 25L9 18M16 31L23 24M16 36L10 30M30 38C42 36 35 24 43 20C48 17 50 23 46 26M43 20Q34 15 42 9Q49 10 46 18',width=1.35)+waves(43),
 'in-the-house-of-gingerbread':
    house()+path('M10 25Q14 30 18 24Q22 29 26 23Q30 29 34 23Q38 29 42 24Q46 30 50 25M19 36H22M39 36H42',width=1.1)+dot(30,15,2)+dot(17,45,1)+dot(43,45,1),
 'the-headless-man':
    path('M21 16L27 13H33L39 16L45 31L39 34L35 27V46H25V27L21 34L15 31ZM27 13L30 18L33 13M30 18V34M25 39H35',width=1.35)+path('M23 8H37M26 5H34',width=.8),
 'the-last-thrilling-wonder-story':
    path('M12 11H42L48 17V44H12ZM42 11V17H48M17 17H34M17 21H28',width=1.2)+star(33,32,10)+dot(19,32,1)+dot(44,25,1)+path('M22 41H39',width=.8),
 'house-of-ancestors':
    path('M8 22L30 6L52 22M13 22H47M14 44H46M16 24V40M25 24V40M35 24V40M44 24V40M10 44V48H50V44M20 19L30 12L40 19',width=1.5)+dot(30,20,1),
 'our-neighbour-by-david-copperfield':
    path('M9 43V21L21 10L33 21V43ZM30 43V17L42 7L54 17V43ZM15 43V32H23V43M37 43V29H45V43M16 24H21M38 20H43',width=1.2)+path('M5 47H55',width=.8),
 'when-i-was-ming-the-merciless':
    path('M10 13L18 23L22 10L30 21L38 10L42 23L50 13L45 34H15ZM15 38H45M19 42H41',width=1.5)+circle(30,28,3)+dot(10,11,1.5)+dot(22,8,1.5)+dot(38,8,1.5)+dot(50,11,1.5),
 'the-cat':
    path('M19 24L17 9L29 18L42 9L41 26Q47 42 32 44Q22 46 18 38C5 45 4 27 12 29C17 31 8 37 17 36M22 27L26 28M34 28L38 27M28 33L31 36L34 33M31 36V39M22 33L10 31M22 37L10 39M39 33L51 31M39 37L51 39',width=1.35),
 'war-beneath-the-tree':
    pine(30,34,.85)+path('M12 46L21 38M17 38L21 38V42M39 46L48 38M43 38L48 38V43M26 47H34',width=1.6)+dot(10,46,1)+dot(50,46,1),
 'eyebem':
    circle(38,18,11)+circle(38,18,3)+path('M38 29C50 34 26 40 39 45M12 40L16 37M21 30L25 27M10 25L14 22M19 15L23 12',width=2)+dot(15,35,1.8)+dot(24,25,1.8)+dot(13,20,1.8)+dot(22,10,1.8),
 'the-horars-of-war':
    path('M13 24Q12 9 30 9Q48 9 47 24ZM10 25H50M19 28V37L30 44L41 37V28M24 30H27M33 30H36M25 36H35M30 9V23',width=1.4)+path('M11 41L17 46M49 41L43 46',width=1),
 'peritonitis':
    path('M30 7C15 7 7 15 11 28C15 41 20 45 30 45C40 45 45 41 49 28C53 15 45 7 30 7ZM22 13C10 16 22 24 17 29C12 34 21 39 28 38M34 14C45 10 46 22 37 22C29 22 37 33 28 32C20 31 24 21 29 18M35 39C45 37 39 31 43 28',width=1.15),
 'the-woman-who-loved-the-centaur-pholus':
    path('M20 9H37M23 10V18C12 28 18 38 26 42V46H33V42C42 38 47 28 35 18V10M22 21C6 13 10 36 19 32M37 21C53 13 49 36 40 32M19 28H39M20 32H38M22 47H37',width=1.3)+path('M7 43Q2 27 7 12M7 12V43M4 28H14M11 25L14 28L11 31',width=.8),
 'the-woman-the-unicorn-loved':
    path('M13 43H42M16 41Q24 32 20 26L11 28L9 23L20 13L25 16Q41 19 39 39M20 13L26 3L26 16M25 16L31 11L31 19M25 26Q32 30 28 39',width=1.3)+dot(21,21,1)+leaf(45,45,30,.55),
 'the-peace-spy':
    path('M10 36C18 36 23 26 30 26M30 26C28 17 35 10 43 12L50 15L44 18C44 26 40 30 31 32L23 41L24 32M30 26C21 27 18 18 12 17C11 26 18 33 24 32',width=1.3)+path('M42 19L51 27M48 24L53 21M45 21L47 17',width=1)+dot(41,15,.8),
 'all-the-hues-of-hell':
    path('M8 42Q5 29 15 21C13 32 23 31 23 18C23 13 28 8 32 5C30 22 42 20 42 31C49 29 48 22 47 20C62 38 45 47 30 47C20 47 10 47 8 42ZM25 41C19 33 28 31 29 24C31 33 38 34 34 41',width=1.3)+path('M18 9H23M38 10H43',width=.8),
 'procreation':
    group(path('M10 26C10 5 50 5 50 26C50 47 10 47 10 26Z',width=1.2),'rotate(35 30 26)')+group(path('M10 26C10 5 50 5 50 26C50 47 10 47 10 26Z',width=1.2),'rotate(-35 30 26)')+dot(22,25,2)+dot(38,27,2)+star(30,26,3),
 'lukora':
    group(crescent(39,15,8),'translate(0 0)')+path('M13 46L14 16M14 24L8 18M14 30L21 22M14 37L7 29M14 43L22 34M28 47V25M28 32L22 26M28 40L35 31M42 47L44 30M43 37L50 30M42 43L37 37',width=1.2),
 'suzanne-delage':
    '<ellipse cx="32" cy="27" rx="14" ry="18" fill="none" stroke="black" stroke-width="1.15"/>'+path('M8 44V8H36M12 43V12H35M8 20Q19 10 8 8M8 32Q20 23 8 20M8 44Q20 35 8 32M20 8Q29 20 32 8',width=.85)+dot(13,16,.8)+dot(13,28,.8)+dot(13,40,.8)+dot(25,13,.8),
 'sweet-forest-maid':
    path('M30 45V24M16 44Q30 36 44 44',width=1.2)+leaf(30,29,0,.8)+leaf(29,36,-55,.72)+leaf(31,37,55,.72)+star(30,6,3),
 'my-book':
    book()+path('M38 6L48 7L43 30L40 27L36 29Z','black',.5)+path('M12 43Q23 40 30 44Q38 40 49 43',width=.8),
 'the-other-dead-man':
    path('M9 12H29V42H9ZM31 8H51V38H31M36 14C41 9 47 15 44 20Q40 23 39 26L39 29M35 33H46M15 18Q24 14 24 22Q24 26 20 27M20 27V31M15 36H24',width=1.2)+path('M29 17H34M29 32H34',width=.8),
 'the-most-beautiful-woman-on-the-world':
    '<ellipse cx="30" cy="23" rx="13" ry="17" fill="none" stroke="black" stroke-width="1.3"/>'+path('M30 40V48M24 48H36M21 24L33 12M27 30L38 19',width=1.1)+star(11,15,3)+star(49,31,3),
 'the-tale-of-the-rose-and-the-nightingale-and-what-came-of-it':
    group(rose(),'translate(-2 2) scale(.78)')+group(bird(),'translate(29 5) scale(.53)')+path('M29 42Q43 46 51 39',width=1.2),
 'silhouette':
    circle(30,25,20)+path('M18 41Q16 34 24 30L24 25C18 23 19 14 25 12C33 11 34 17 36 20L32 23V29Q38 32 38 40Z','black',.5)+path('M32 10C39 10 40 17 44 20L40 24L40 29L45 35',width=1),
 'three-body-problem':
    group('<ellipse cx="30" cy="26" rx="24" ry="11" fill="none" stroke="black" stroke-width="1.1"/>','rotate(-30 30 26)')+group('<ellipse cx="30" cy="26" rx="24" ry="11" fill="none" stroke="black" stroke-width="1.1"/>','rotate(45 30 26)')+dot(14,18,4)+dot(43,16,3.2)+dot(34,40,4.5)+circle(30,26,2,.7),
 'dark-forest':
    pine(16,36,.55)+pine(32,40,1)+pine(47,36,.5)+star(15,11,2.8)+dot(47,10,1.2)+path('M10 48H48',width=.8),
 'deaths-end':
    group(hourglass(),'translate(9 4) scale(.72)')+path('M5 26C14 12 45 12 55 26C45 40 14 40 5 26Z',width=.85)+star(48,10,3)+dot(12,41,1.3),
})
MOTIFS['parkroads-a-review'] = MOTIFS.pop('parkroadsa-review')
MOTIFS.update({
 'hyperion':
    group(hourglass(),'translate(6 1) scale(.8)')+
    path('M12 46C4 30 8 12 16 6M11 36L5 33M10 27L16 22M11 18L6 13M48 46C56 30 52 12 44 6M49 36L55 33M50 27L44 22M49 18L54 13',width=1.2)+
    path('M20 45Q30 49 40 45',width=.8)+star(30,5,2.5),
 'the-fall-of-hyperion':
    path('M14 12C7 19 14 27 19 31V40Q30 46 41 40V31C46 27 53 19 46 12M14 12Q20 8 24 15M46 12Q40 8 36 15M19 19H41M22 19V38M27 19V40M33 19V40M38 19V38M19 35H41M24 46H36',width=1.2)+
    star(31,8,4)+path('M34 5L42 2M35 9L46 6M15 45L10 48M46 44L51 47',width=.7),
})

# Strange Travelers: distinct drawings for roads, folklore, music, language,
# domestic miniatures and architecture, rather than anthology-wide decoration.
MOTIFS.update({
 'bluesberry-jam':
    path('M12 47L22 5M48 47L38 5M29 42V34M30 26V19M30 12V8',width=1.2)+
    circle(30,30,10)+path('M25 23L39 9L43 13L29 27M22 34L27 39M38 10L43 15',width=1.4)+dot(30,30,2),
 'one-two-three-for-me':
    path('M10 43V10M19 43V10M28 43V10M7 35L32 19',width=1.7)+
    path('M40 45V19L45 10L50 19V45M40 24H50M38 46H52',width=1.2)+dot(45,15,1),
 'counting-cats-in-zanzibar':
    path('M19 32L16 18L26 24L36 18L34 33Q40 43 27 44Q16 44 19 32M24 31H26M30 31H32M8 43Q1 31 10 30Q17 30 12 38',width=1.3)+
    path('M43 45V14M38 15L43 7L48 15ZM39 19H47M39 26H47M39 33H47',width=1.1)+star(15,10,3),
 'the-death-of-koshchei-the-deathless':
    path('M30 8C15 24 17 40 30 43C43 40 45 24 30 8ZM30 14V39M25 45H35',width=1.2)+
    path('M4 28Q11 18 20 23M40 23Q49 18 56 28M5 28L13 26M55 28L47 26',width=1.1)+
    path('M26 23L34 30M26 30L34 23',width=.8),
 'no-planets-strike':
    star(30,10,5)+path('M15 20Q8 28 13 38Q17 44 25 43M45 20Q52 28 47 38Q43 44 35 43M12 36Q7 43 7 47M48 36Q53 43 53 47',width=1.2)+
    path('M24 24L30 20L36 24V43H24ZM21 46H39M28 27H32M28 32H32',width=1.25),
 'to-the-seventh':
    path('M19 43H42M21 39H40L36 30V22L42 17L36 10L27 7L27 14L18 22L21 27L28 23V31ZM21 47H40',width=1.3)+
    path('M8 12V44M5 20H11M5 28H11M5 36H11M48 10V40M45 17H51M45 25H51M45 33H51',width=.8)+dot(31,17,1),
 'queen-of-the-night':
    crescent(30,27,16)+path('M19 13L17 5L25 9L30 3L35 9L43 5L41 13M23 16H38',width=1.2)+
    star(45,34,4)+dot(47,21,1)+dot(14,42,1),
 'flash-company':
    path('M9 22H51V43H9ZM9 28H51M15 29V42M21 29V42M27 29V42M33 29V42M39 29V42M45 29V42M9 47H51',width=1.2)+
    path('M12 29V36H18V29M24 29V36H30V29M36 29V36H42V29','black',.5)+
    path('M30 20C15 14 15 5 22 7C27 9 28 16 30 20C32 16 33 9 38 7C45 5 45 14 30 20M30 19L25 25M30 19L35 25',width=1.2),
 'the-haunted-boardinghouse':
    path('M11 45V20L30 7L49 20V45ZM8 45H52M20 25H25V31H20ZM35 25H40V31H35ZM26 45V36H34V45M29 15H31',width=1.2)+
    path('M40 17C34 13 38 4 43 5C48 7 42 10 46 13L43 12L40 17Z',width=1)+dot(29,39,1),
 'useful-phrases':
    book()+path('M19 7Q14 5 16 2M41 7Q46 5 44 2M30 12V4M27 5L30 2L33 5',width=1)+
    path('M14 29H24M36 29H46M19 46H41',width=.8)+dot(30,47,1.4),
 'the-man-in-the-pepper-mill':
    path('M23 11Q30 5 37 11L36 17H24ZM24 20H36Q32 29 36 38L40 43H20L24 38Q28 29 24 20ZM20 47H40M30 8V4M26 4H34M24 35H36',width=1.25)+
    path('M7 30L13 24L19 30M10 29V39H16V29M43 32L49 26L55 32M46 31V41H52V31',width=.85),
 'the-ziggurat':
    path('M6 46V39H14V30H22V21H26V12H34V21H38V30H46V39H54V46ZM6 42H54M14 34H46M22 25H38M30 15V20',width=1.2)+
    star(13,13,4)+star(47,18,3)+dot(38,6,1),
 'aint-you-most-done':
    path('M11 38H49L43 45H17ZM30 37V7M30 9L44 29H32M26 14L15 30H27M8 48H52',width=1.2)+
    path('M9 7L18 7M13 5V10M48 12V24M48 13L54 11V22',width=1)+dot(45,25,2)+dot(51,23,2)+waves(35),
})

def generate(root=ROOT):
    catalog = json.loads((root / 'data/wolfe-fiction/catalog.json').read_text())
    titles = {entry['id']: entry['title'] for entry in catalog}
    titles.update({'three-body-problem': 'The Three-Body Problem',
                   'dark-forest': 'The Dark Forest', 'deaths-end': 'Death’s End',
                   'hyperion': 'Hyperion', 'the-fall-of-hyperion': 'The Fall of Hyperion'})
    missing = set(titles) - MOTIFS.keys()
    if missing:
        raise ValueError(f'Missing ornament drawings: {sorted(missing)}')
    directory = root / 'assets/ornaments'
    directory.mkdir(parents=True, exist_ok=True)
    for slug, title in titles.items():
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 52" '
               'fill="none" stroke-linecap="round" stroke-linejoin="round">\n'
               f'<title>{html.escape(title)} — ornament</title>\n'
               '<!-- Original project drawing; generated by tools/reader_ornaments.py. -->\n'
               + MOTIFS[slug] + '\n</svg>\n')
        ET.fromstring(svg)
        (directory / f'{slug}.svg').write_text(svg)
    return len(titles)

if __name__ == '__main__':
    print(f'Wrote {generate()} original SVG ornaments.')

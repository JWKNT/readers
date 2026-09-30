#!/usr/bin/env python3
"""Export the seven Long/Short Sun initial alphabets as standalone SVG artwork.

Build dependencies: fonttools, cairosvg, Pillow. No font program is shipped.
Download https://mirrors.ctan.org/fonts/initials.zip and supply its extracted
initials directory with --source-dir. New Sun artwork and metrics are preserved.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import string

import cairosvg
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.t1Lib import T1Font
from PIL import Image

FAMILIES = {
    'nightside': ('Eileen', 'Eileen Caps Regular'),
    'lake': ('Elzevier', 'Elzevier Caps'),
    'calde': ('Carrickc', 'Carrick Caps'),
    'exodus': ('Rothdn', 'Rothenburg Decorative'),
    'blue': ('Nouveaud', 'Nouveau Drop Caps'),
    'green': ('Acorn', 'Acorn Initials'),
    'return': ('MorrisIn', 'Morris Initialen'),
}
SOURCE_URL = 'https://mirrors.ctan.org/fonts/initials.zip'


def glyph_art(glyphs, letter):
    glyph = glyphs[letter]
    bounds = BoundsPen(glyphs)
    glyph.draw(bounds)
    x0, y0, x1, y1 = bounds.bounds
    # Keep all flourishes, with a tiny antialiasing allowance around the ink.
    pad = max(x1 - x0, y1 - y0) * .003
    width, height = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    path = SVGPathPen(glyphs)
    glyph.draw(path)
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width:.3f} {height:.3f}" role="img">'
        f'<g transform="translate({-x0+pad:.3f} {y1+pad:.3f}) scale(1 -1)">'
        f'<path d="{path.getCommands()}"/></g></svg>\n'
    )
    return svg, width / height


def contour(svg):
    # A stepped right-edge envelope lets prose follow the actual ornament,
    # while including every visible pixel rather than cutting into the artwork.
    png = cairosvg.svg2png(bytestring=svg.encode(), output_height=512)
    alpha = Image.open(io.BytesIO(png)).convert('RGBA').getchannel('A')
    width, height = alpha.size
    points = ['0% 0%']
    for band in range(32):
        y0, y1 = band * height // 32, (band + 1) * height // 32
        ink = alpha.crop((0, y0, width, y1)).point(lambda a: 255 if a > 8 else 0).getbbox()
        right = min(100, (ink[2] / width * 100 + .4) if ink else 0)
        points.extend([f'{right:.2f}% {band*100/32:.3f}%', f'{right:.2f}% {(band+1)*100/32:.3f}%'])
    points.append('0% 100%')
    return 'polygon(' + ','.join(points) + ')'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'assets' / 'initials')
    args = parser.parse_args()
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    metadata = {}
    css = []
    provenance = {'source': SOURCE_URL, 'license': 'LPPL (permission in the CTAN initials README)', 'families': {}}
    for name, (stem, title) in FAMILIES.items():
        source = args.source_dir / (stem + '.pfb')
        font = T1Font(str(source), encoding='latin1')
        glyphs = font.getGlyphSet()
        target = output / name
        target.mkdir(exist_ok=True)
        metadata[name] = {'name': title, 'letters': {}}
        for letter in string.ascii_uppercase:
            svg, ratio = glyph_art(glyphs, letter)
            (target / (letter + '.svg')).write_text(svg)
            shape = contour(svg)
            metadata[name]['letters'][letter] = {'ratio': round(ratio, 5), 'contour': shape}
            css.append(f'.initial[data-set="{name}"][data-letter="{letter}"]{{--initial-ratio:{ratio:.5f};--initial-shape:{shape};}}')
        info = font['FontInfo']
        provenance['families'][name] = {
            'name': title, 'sourceFile': source.name,
            'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'notice': info.get('Notice', '').replace('\\050', '(').replace('\\051', ')'),
            'version': info.get('version'),
        }
    css_path = output / 'initials.css'
    original_css = css_path.read_text() if css_path.exists() else ''
    # Retain the New Sun rules literally, including whitespace and precision.
    retained = [line for line in original_css.splitlines(keepends=True)
                if not any(f'data-set="{name}"' in line for name in FAMILIES)]
    css_path.write_text(''.join(retained).rstrip('\n') + '\n' + '\n'.join(css) + '\n')
    metrics_path = output / 'metrics.json'
    original_metrics = json.loads(metrics_path.read_text()) if metrics_path.exists() else {}
    original_metrics.update(metadata)
    metrics_path.write_text(json.dumps(original_metrics, ensure_ascii=False, separators=(',', ':')) + '\n')
    (output / 'decorated-initials.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
    print(f'Exported {len(FAMILIES)*26} initials; New Sun families preserved.')


if __name__ == '__main__':
    main()

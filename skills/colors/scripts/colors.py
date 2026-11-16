#!/usr/bin/env python3
"""Offline Sanzo Wada palette lookup; Python standard library only."""
import argparse
import itertools
import json
import math
from pathlib import Path
import re

DATA = Path(__file__).resolve().parents[1] / 'data' / 'colors.json'
SOURCE = 'https://sanzo-wada.dmbk.io/'
MOODS = {'calm': '#8ea99b', 'warm': '#c2975a', 'earthy': '#718600',
         'playful': '#ff7399', 'bold': '#f20000', 'cool': '#417777',
         'editorial': '#503d00', 'soft': '#e6adcf'}

def rgb(value):
    if not re.fullmatch(r'#[0-9a-fA-F]{6}', value):
        raise ValueError('Expected a six-digit hex color, e.g. #417777')
    return [int(value[i:i+2], 16) / 255 for i in (1, 3, 5)]

def linear(value):
    return [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in rgb(value)]

def luminance(value):
    return sum(a*b for a,b in zip(linear(value), (.2126, .7152, .0722)))

def contrast(a, b):
    x, y = sorted((luminance(a), luminance(b)))
    return (y + .05) / (x + .05)

def oklab(value):
    r,g,b = linear(value)
    l = (.4122214708*r + .5363325363*g + .0514459929*b)**(1/3)
    m = (.2119034982*r + .6806995451*g + .1073969566*b)**(1/3)
    s = (.0883024619*r + .2817188376*g + .6299787005*b)**(1/3)
    return (.2104542553*l + .793617785*m - .0040720468*s,
            1.9779984951*l - 2.428592205*m + .4505937099*s,
            .0259040371*l + .7827717662*m - .808675766*s)

def load():
    colors = json.loads(DATA.read_text())['colors']
    combos = {}
    for c in colors:
        for n in c['combinations']:
            combos.setdefault(n, []).append(c)
    return colors, combos

def palette(n, colors):
    pairs = [{'colors': [a['name'], b['name']], 'ratio': round(contrast(a['hex'], b['hex']), 3),
              'normal_text_aa': contrast(a['hex'], b['hex']) >= 4.5,
              'large_text_aa': contrast(a['hex'], b['hex']) >= 3}
             for a,b in itertools.combinations(colors, 2)]
    return {'id': n, 'source': SOURCE, 'colors': [
        {k:c[k] for k in ('name','hex','slug')} for c in colors], 'contrast': pairs}

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    q = sub.add_parser('show'); q.add_argument('id', type=int); q.add_argument('--format', choices=['json','css'], default='json')
    q = sub.add_parser('search'); q.add_argument('name')
    q = sub.add_parser('recommend'); q.add_argument('--hex'); q.add_argument('--mood', choices=MOODS)
    q.add_argument('--size', type=int, choices=[2,3,4]); q.add_argument('--limit', type=int, default=3)
    q = sub.add_parser('contrast'); q.add_argument('foreground'); q.add_argument('background')
    a = p.parse_args(argv)
    colors, combos = load()
    try:
        if a.command == 'contrast':
            ratio = contrast(a.foreground, a.background)
            out = {'ratio': round(ratio, 3), 'normal_text_aa': ratio >= 4.5, 'large_text_aa': ratio >= 3,
                   'note': 'Opaque sRGB pair only; not a whole-interface accessibility audit.'}
        elif a.command == 'show':
            if a.id not in combos:
                raise ValueError('Combination absent from bundled DMBK data (available: 1–348). Check the Wada Sanzo Colors reference for additional combinations.')
            out = palette(a.id, combos[a.id])
            if a.format == 'css':
                print('/* DMBK / Sanzo Wada combination %s; original swatches, not semantic roles */' % a.id)
                print(':root {')
                for c in out['colors']:
                    print('  --wada-%s: %s;' % (c['slug'], c['hex']))
                print('}')
                return
        elif a.command == 'search':
            out = [c for c in colors if a.name.casefold() in c['name'].casefold() or a.name.casefold() in c['slug']]
        else:
            if not 1 <= a.limit <= 348:
                raise ValueError('--limit must be between 1 and 348')
            target = a.hex or MOODS.get(a.mood, '#417777')
            lab = oklab(target)
            distance = lambda c: math.dist(oklab(c['hex']), lab)
            candidates = [(n, cs) for n,cs in combos.items() if not a.size or len(cs) == a.size]
            ranked = sorted(candidates, key=lambda item: (min(map(distance,item[1])), item[0]))
            out = {'method': 'Nearest swatch in OKLab; moods are modern seed-color heuristics, not historical labels. Ties use combination ID.',
                   'target': target, 'mood': a.mood, 'palettes': [palette(n,cs) for n,cs in ranked[:a.limit]]}
        print(json.dumps(out, indent=2))
    except ValueError as e:
        p.error(str(e))

if __name__ == '__main__':
    main()

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
MOODS = {
    'calm': '#8ea99b', 'warm': '#c2975a', 'earthy': '#718600',
    'playful': '#ff7399', 'bold': '#f20000', 'cool': '#417777',
    'editorial': '#503d00', 'soft': '#e6adcf',
}


def rgb(value):
    if not re.fullmatch(r'#[0-9a-fA-F]{6}', value):
        raise ValueError('Expected a six-digit hex color, e.g. #417777')
    return [int(value[i:i + 2], 16) / 255 for i in (1, 3, 5)]


def linear(value):
    return [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in rgb(value)]


def luminance(value):
    return sum(a * b for a, b in zip(linear(value), (.2126, .7152, .0722)))


def contrast(a, b):
    darker, lighter = sorted((luminance(a), luminance(b)))
    return (lighter + .05) / (darker + .05)


def contrast_report(a, b):
    ratio = contrast(a, b)
    return {
        'ratio': round(ratio, 3),
        'normal_text_aa': ratio >= 4.5,
        'large_text_aa': ratio >= 3,
    }


def oklab(value):
    r, g, b = linear(value)
    l = (.4122214708 * r + .5363325363 * g + .0514459929 * b) ** (1 / 3)
    m = (.2119034982 * r + .6806995451 * g + .1073969566 * b) ** (1 / 3)
    s = (.0883024619 * r + .2817188376 * g + .6299787005 * b) ** (1 / 3)
    return (
        .2104542553 * l + .793617785 * m - .0040720468 * s,
        1.9779984951 * l - 2.428592205 * m + .4505937099 * s,
        .0259040371 * l + .7827717662 * m - .808675766 * s,
    )


def load():
    colors = json.loads(DATA.read_text())['colors']
    combinations = {}
    for color in colors:
        for number in color['combinations']:
            combinations.setdefault(number, []).append(color)
    return colors, combinations


def palette(number, colors):
    return {
        'id': number,
        'source': SOURCE,
        'colors': [{key: color[key] for key in ('name', 'hex', 'slug')} for color in colors],
        'contrast': [
            {'colors': [a['name'], b['name']], **contrast_report(a['hex'], b['hex'])}
            for a, b in itertools.combinations(colors, 2)
        ],
    }


def recommend(combinations, target, size=None, limit=3, mood=None):
    if not 1 <= limit <= 348:
        raise ValueError('--limit must be between 1 and 348')
    target_lab = oklab(target)

    def rank(item):
        number, colors = item
        nearest = min(math.dist(oklab(color['hex']), target_lab) for color in colors)
        return nearest, number

    candidates = [(n, colors) for n, colors in combinations.items() if not size or len(colors) == size]
    ranked = sorted(candidates, key=rank)
    return {
        'method': 'Nearest swatch in OKLab; moods are modern seed-color heuristics, not historical labels. Ties use combination ID.',
        'target': target,
        'mood': mood,
        'palettes': [palette(n, colors) for n, colors in ranked[:limit]],
    }


def css(selected):
    lines = [f'/* DMBK / Sanzo Wada combination {selected["id"]}; original swatches, not semantic roles */', ':root {']
    lines.extend(f'  --wada-{color["slug"]}: {color["hex"]};' for color in selected['colors'])
    return '\n'.join([*lines, '}'])


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    commands = cli.add_subparsers(dest='command', required=True)
    show = commands.add_parser('show')
    show.add_argument('id', type=int)
    show.add_argument('--format', choices=['json', 'css'], default='json')
    search = commands.add_parser('search')
    search.add_argument('name')
    suggest = commands.add_parser('recommend')
    suggest.add_argument('--hex')
    suggest.add_argument('--mood', choices=MOODS)
    suggest.add_argument('--size', type=int, choices=[2, 3, 4])
    suggest.add_argument('--limit', type=int, default=3)
    check = commands.add_parser('contrast')
    check.add_argument('foreground')
    check.add_argument('background')
    return cli


def run(args):
    if args.command == 'contrast':
        return {
            **contrast_report(args.foreground, args.background),
            'note': 'Opaque sRGB pair only; not a whole-interface accessibility audit.',
        }
    colors, combinations = load()
    if args.command == 'show':
        if args.id not in combinations:
            raise ValueError('Combination absent from bundled DMBK data (available: 1–348). Use a DMBK combination ID from 1 to 348.')
        selected = palette(args.id, combinations[args.id])
        return css(selected) if args.format == 'css' else selected
    if args.command == 'search':
        query = args.name.casefold()
        return [color for color in colors if query in color['name'].casefold() or query in color['slug']]
    target = args.hex or MOODS.get(args.mood, '#417777')
    return recommend(combinations, target, args.size, args.limit, args.mood)


def main(argv=None):
    cli = parser()
    args = cli.parse_args(argv)
    try:
        result = run(args)
    except ValueError as error:
        cli.error(str(error))
    print(result if isinstance(result, str) else json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

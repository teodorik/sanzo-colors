# Sources and provenance

- Numerical source: https://sanzo-wada.dmbk.io/assets/colors.json (retrieved 2026-11-16), linked from https://sanzo-wada.dmbk.io/.
- Upstream project: https://github.com/dblodorn/sanzo-wada, credited by its About page. MIT license by Dain Blodorn; preserved at `../data/LICENSE`.
- Bundled snapshot: 159 colors, 348 combinations: 120 pairs, 120 triples, 108 quadruples. Reconstructed by grouping each color's combination memberships. This does not establish the historical swatch display order or proportions.
- Complementary reference: https://www.wada-sanzo-colors.com/ and https://www.wada-sanzo-colors.com/combinations/classic/all. It lists 360 classic combinations plus a separate seasons collection. The extra combinations and seasons dataset are not bundled. Use its public pages for live research; do not claim they are in the offline dataset or bypass access controls.
- Additional live reference: https://wscolors.com/palettes (checked 2026-11-16) lists 348 palettes. Its IDs are source-specific: palette #1 is listed with three colors, whereas bundled DMBK combination #1 has two. Do not assume equal IDs identify equal palettes. Match verified color membership before claiming equivalence, retain source-specific HEX values, and cite the actual inspected page. W.S. Colors data is not bundled and no API or redistribution license has been verified. The offline CLI continues to use DMBK IDs only.
- Digital HEX values may differ across sources and print reproductions. Attribute values to their source and do not silently mix source values in a single historical palette.
- Mood labels, ranking, role assignments, and accessibility adaptations in this plugin are contemporary design decisions, not Wada's classifications.

For a particular bundled combination, link the DMBK site and, when available, verify the exact combination permalink by following that site's navigation. Never guess a permalink.

Contrast method: WCAG relative luminance for opaque sRGB and `(Llighter + .05)/(Ldarker + .05)`. Reference: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html . Text thresholds alone do not establish that an entire interface is accessible.

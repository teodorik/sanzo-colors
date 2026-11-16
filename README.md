# Sanzo Colors

Use Sanzo Wada color combinations in your website, app, or visual work. The `colors` skill recommends palettes from DMBK, checks text contrast, and can apply your choice to an existing theme.

```sh
npx skills add teodorik/sanzo-colors
```

Choose your assistant if prompted. Supports Codex, Claude Code, Cursor, and other [agents](https://github.com/vercel-labs/skills#supported-agents). Requires Node.js 22.20+.

To update:

```sh
npx skills update
```

## Use it

Start a new assistant session, then ask:

> Use the colors skill to show me three Sanzo Wada combinations for a calm editorial website.

> Find a Wada palette that works with our existing green, and explain the tradeoffs.

> Apply combination 238 to this page. Keep the original colors and check readability.

Or invoke `/colors` in Claude Code or Cursor, and `$colors` in Codex.

Each recommendation includes the DMBK combination number, original color names and HEX values, suggested background/text/accent roles, and measured contrast when a calculation tool is available. The skill labels any added neutrals or adjusted colors.

## Data and tools

[DMBK](https://sanzo-wada.dmbk.io/) is the only palette source. The skill includes 348 combinations for offline use, including [#96](https://sanzo-wada.dmbk.io/combination/96). Names such as “calm editorial” and suggested website roles are design choices, not historical labels.

The assistant can read the data directly. The optional Python 3.9+ helper looks up palettes, exports CSS, and calculates contrast without extra dependencies. If it cannot calculate contrast, it says so.

[Installation and migration](docs/install.md) · [Source details](skills/colors/references/sources.md) · [Contributing](CONTRIBUTING.md)

## License

MIT. The dataset includes [Dain Blodorn's MIT notice](skills/colors/data/LICENSE). This project is not affiliated with DMBK.

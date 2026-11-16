# Sanzo Colors

An agent skill for choosing and applying Sanzo Wada color combinations to websites, interfaces, and visual work. It turns a brief into three considered palettes, shows how to use them, and checks text contrast.

```sh
npx skills add teodorik/sanzo-colors
```

Choose your coding assistant in the installer. Works with Codex, Claude Code, Cursor, and other [supported agents](https://github.com/vercel-labs/skills#supported-agents). Requires Node.js 22.20+; no account or API key is needed.

To update installed skills:

```sh
npx skills update
```

## Usage

Ask your assistant naturally:

> Use the colors skill to show me three Sanzo Wada combinations for a calm editorial website.

> Find a Wada palette that works with our existing green, and explain the tradeoffs.

> Apply combination 238 to this page. Keep the original colors and check readability.

You can also use `/colors` in Claude Code or Cursor, and `$colors` in Codex. Start a new session after installing.

## What it does

| Capability | Result |
|---|---|
| Recommend | Three distinct palettes suited to your brief |
| Show | Original color names, HEX values, and source-specific combination IDs |
| Apply | Background, text, and accent roles mapped to your existing theme |
| Check | Measured text contrast, with any adaptations clearly labelled |
| Explore | 348 bundled combinations from DMBK |

The original combinations stay intact. Mood names, usage proportions, and website roles are design interpretations. Extra neutrals or adjusted colors are labelled as adaptations.

## Source

[DMBK's Sanzo Wada collection](https://sanzo-wada.dmbk.io/) is the sole palette source, including the bundled offline dataset. Browse a combination such as [#96](https://sanzo-wada.dmbk.io/combination/96), or ask the skill to find one for your brief.

All palette IDs and digital color values follow DMBK. [Source details](skills/colors/references/sources.md).

## More

- [Install for all projects, update, remove, or migrate an old installation](docs/install.md).
- [Optional terminal CLI and curl installer](docs/terminal.md). `npx skills add` installs the agent skill; it does not add a shell command named `colors`.
- [Contributing and verification](CONTRIBUTING.md).

The skill can read its bundled data without Python. Its optional lookup, CSS export, and contrast helper uses Python 3.9+ with no dependencies. Without a calculation tool, contrast is reported as unverified.

## License

MIT. The bundled dataset retains [Dain Blodorn's MIT notice](skills/colors/data/LICENSE). Not affiliated with the source website.

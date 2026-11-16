# Contributing

Keep installation to one command: `npx skills add teodorik/sanzo-colors`.

## Layout

- `skills/colors/`: the skill, its data, references, and Python helper. Keep everything the assistant needs in this directory.
- `docs/install.md`: installation, update, removal, and migration guidance.
- `scripts/package.py`: export the saved account plugin.
- `plugin.json`, `assets/`: private account plugin compatibility; not required for Skills CLI installation.
- `tests/`: dataset, contrast, CLI behavior, and packaging checks.

Use DMBK IDs and values. Keep its attribution and license notice. The helper ranks palettes by color distance; the assistant chooses which ones fit the brief.

## Verify

```sh
python3 -m unittest discover -s tests -v
npx skills add . --list
```

In a disposable project, install from this checkout using `npx skills add /absolute/path/to/sanzo-colors --skill colors -a codex claude-code cursor -y`. Check that the installed directory contains the helper, data, licenses, and references. Run the helper there.

Try a calm editorial brief, an existing brand color, and a specific combination number. Check that the assistant keeps the original swatches, reports low contrast, and says when it could not calculate or browse.

## Plugin export

```sh
python3 scripts/package.py /absolute/path/sanzo-colors.zip
```

Publish the ZIP separately when updating the account plugin. Pushing to GitHub does not update it.

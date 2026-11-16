# Contributing

Keep the main experience simple: install with `npx skills add teodorik/sanzo-colors`, then ask the assistant to use `colors`.

## Layout

- `skills/colors/`: the self-contained Agent Skill. All references and executable helpers needed by the skill belong here.
- `docs/`: optional installation, migration, and terminal details.
- `scripts/`, `bin/`, `install.sh`: optional terminal installation and plugin packaging.
- `plugin.json`, `assets/`: private account plugin compatibility; not required for Skills CLI installation.
- `tests/`: dataset, contrast, packaging, and legacy installer regression checks.

Do not invent palette IDs, quietly change original values, or merge source numbering. Keep attribution and upstream notices. The CLI's mood ranking is a heuristic; the assistant must curate for the brief.

## Verify

```sh
python3 -m unittest discover -s tests -v
npx skills add . --list
```

In a disposable project, install from this checkout using `npx skills add /absolute/path/to/sanzo-colors --skill colors -a codex claude-code cursor -y`. Check that the helper, data, licenses, and references were installed with SKILL.md. Run the helper from its installed location.

Useful behavior checks: recommend three calm editorial palettes; anchor to an existing HEX color; apply a specific combination; handle a low-contrast pair; distinguish W.S. Colors IDs from DMBK IDs; disclose unavailable calculations or browsing.

## Plugin export

```sh
python3 scripts/package.py /absolute/path/sanzo-colors.zip
```

The ZIP is a separate plugin distribution. GitHub and Skills CLI updates do not publish a new account-plugin release.

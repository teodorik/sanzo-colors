# Install and manage the colors skill

## Install

Run this from your project and choose your assistant:

```sh
npx skills add teodorik/sanzo-colors
```

For all your projects, add `-g`:

```sh
npx skills add teodorik/sanzo-colors -g
```

For a project installation with Codex, Claude Code, and Cursor selected explicitly:

```sh
npx skills add teodorik/sanzo-colors --skill colors -a codex claude-code cursor -y
```

Requires Node.js 22.20+ and network access to download the skill. The installed palette data works offline. Start a new assistant session afterward.

## Update

```sh
npx skills update
```

This manages skills installed through the Skills CLI. To update only this skill in the current project:

```sh
npx skills update colors -p -y
```

For a global installation, use `npx skills update colors -g -y`.

## Remove

```sh
npx skills remove colors
```

For a global installation, add `-g`. Removal does not uninstall the optional terminal wrapper from the old curl installer.

## Coming from the old curl installer?

The custom installer has been retired. Existing installed copies still run, but future installs and updates use the Skills CLI.

1. Back up any custom edits in your existing `colors` skill folders. Global installs use `~/.agents/skills/colors` and `~/.claude/skills/colors`; project installs use the same paths inside the project without `~/`.
2. Run `npx skills add teodorik/sanzo-colors` in your project, or add `-g` for global use. Select your assistants and review the replacement summary.
3. Use `npx skills update` from then on. The old automatic backup directories are no longer managed; keep any you need.

If you no longer need the old `~/.local/bin/colors` launcher, remove that file. It is not installed or removed by the Skills CLI. No shell configuration changes are required for the skill.

## Run the helper directly

The skill still includes offline lookup, CSS export, and contrast calculations. From a source checkout:

```sh
python3 skills/colors/scripts/colors.py show 96
python3 skills/colors/scripts/colors.py recommend --mood calm --size 3
python3 skills/colors/scripts/colors.py contrast '#340059' '#9cb29e'
```

Python 3.9+ is required for the helper. Assistants resolve this script relative to their installed skill directory, so no extra terminal launcher is needed.

# Install and manage the colors skill

## Install

Run this from your project. Choose your assistant if prompted:

```sh
npx skills add teodorik/sanzo-colors
```

For all your projects, add `-g`:

```sh
npx skills add teodorik/sanzo-colors -g
```

To select Codex, Claude Code, and Cursor without prompts:

```sh
npx skills add teodorik/sanzo-colors --skill colors -a codex claude-code cursor -y
```

Use Node.js 22.20+ and an internet connection for installation. The downloaded palette data works offline. Start a new assistant session after installing.

## Update

```sh
npx skills update
```

To update only `colors` in this project:

```sh
npx skills update colors -p -y
```

For a global installation, use `npx skills update colors -g -y`.

## Remove

```sh
npx skills remove colors
```

Add `-g` to remove a global installation. If you installed the old terminal launcher, remove `~/.local/bin/colors` separately.

## Migrate a curl installation

Your installed copy still works. To manage its updates with the Skills CLI:

1. Back up any custom edits in your existing `colors` skill folders. Global installs use `~/.agents/skills/colors` and `~/.claude/skills/colors`; project installs use the same paths inside the project without `~/`.
2. Run `npx skills add teodorik/sanzo-colors` in your project, or add `-g` for global use. Select your assistants and review the replacement summary.
3. Use `npx skills update` from then on. Keep any old backup directories you need.

The skill does not need a shell launcher or PATH changes.

## Run the helper directly

From a source checkout:

```sh
python3 skills/colors/scripts/colors.py show 96
python3 skills/colors/scripts/colors.py recommend --mood calm --size 3
python3 skills/colors/scripts/colors.py contrast '#340059' '#9cb29e'
```

The helper requires Python 3.9+. Assistants run it from their installed skill directory.

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

## Coming from the curl installer?

Existing installations still work. You do not have to migrate. The [curl installer](terminal.md#updates) continues to install and update the optional terminal command and skills, with backups.

To let the Skills CLI manage an old installation:

1. Back up the existing `colors` skill folders before replacing them, especially if you edited them. Global installs use `~/.agents/skills/colors` and `~/.claude/skills/colors`; project installs use the same paths inside the project without `~/`.
2. Run `npx skills add teodorik/sanzo-colors` in the project, or add `-g` for the global scope. Select the same assistants and inspect the replacement summary before confirming.
3. Use `npx skills update` for that installation from then on. Do not alternate installers on the same destination: their ownership, links, and update tracking differ.

Skills CLI updates are separate from the old installer's automatic backups. Preserve custom edits before using either installation manager. Global `npx` installation keeps the canonical `.agents/skills/colors` location, so an existing `~/.local/bin/colors` wrapper can still use its helper. If removing the skill, remove that wrapper too or it will point to missing files.

## Need just the terminal command?

See [optional terminal tools](terminal.md). They remain available without Node.js. The standard `npx` flow installs skills for assistants; it does not install `colors` on your shell PATH.

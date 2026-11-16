# Sanzo Colors

A portable `/colors` skill and offline terminal tool for recommending and applying Sanzo Wada color combinations. Built with Plugin Creator. No API keys, server, Python dependencies, or paid services required. Python 3.9+.

## One-line installation from GitHub

Requires **Python 3.9+**, Git, curl, and bash on macOS or Linux. No GitHub account or authentication is required.

```sh
(set -o pipefail; curl -fsSL https://raw.githubusercontent.com/teodorik/sanzo-colors/main/install.sh | bash)
```

This downloads the installer from GitHub, clones the source into a temporary directory, installs the terminal command and assistant skills, and removes the temporary checkout. It installs or updates an existing Sanzo Colors installation and preserves previous files in backups. It does not change shell configuration. See [update behavior](#updates). `pipefail` makes a download failure fail the overall command too.

For a project-only skill installation:

```sh
(set -o pipefail; curl -fsSL https://raw.githubusercontent.com/teodorik/sanzo-colors/main/install.sh | bash -s -- --project /path/to/project)
```

You can [read the installer](install.sh) before running it, or use the manual installation below. The one-line command installs the latest `main` branch.

After installing, if needed:

```sh
export PATH="$HOME/.local/bin:$PATH"
colors show 238
```

## Terminal installation (macOS / Linux)

Requires **Python 3.9+** and Git. Check your prerequisites:

```sh
python3 --version
git --version
```

If a command is missing, install [Python](https://www.python.org/downloads/), [Git](https://git-scm.com/downloads) first. Windows users can run these instructions inside WSL; native Windows installation is not covered.

### 1. Download and install

Run in the directory where you want to keep the source checkout:

```sh
git clone https://github.com/teodorik/sanzo-colors.git
cd sanzo-colors
python3 scripts/install.py --global
```

If you already cloned the repository, enter that checkout instead of cloning again.

The installer needs no `sudo`, `pip`, or API key. It installs:

| Location | Purpose |
|---|---|
| `~/.local/bin/colors` | Terminal command |
| `~/.agents/skills/colors/` | Self-contained skill and data for Codex, Cursor, and compatible agents |
| `~/.claude/skills/colors/` | Self-contained skill and data for Claude Code |

These are copies, so moving the source checkout will not break the installed command. The installer updates recognized Sanzo Colors installations, including older versions, with backups; unrelated files and symlinks are not replaced.

### 2. Make the command available

For the current terminal session:

```sh
export PATH="$HOME/.local/bin:$PATH"
```

To keep this setting in future terminals, add that same line once to `~/.zshrc` for zsh (the macOS default), or `~/.bashrc` for interactive bash. macOS bash login shells typically read `~/.bash_profile` instead. Open a new terminal after saving.

### 3. Verify

```sh
command -v colors
colors --help
colors show 238
colors contrast '#000000' '#ffffff'
```

`command -v` should point to your home directory's `.local/bin/colors`. The last command should return a ratio of `21.0`, with both text checks set to `true`.

### 4. Use it

```sh
# Get three candidate palettes
colors recommend --mood calm --size 3 --limit 3

# Find combinations near an existing brand color
colors recommend --hex '#417777' --size 3 --limit 5

# Search named swatches and their combination memberships
colors search 'green'

# Inspect one original combination, including pairwise contrast
colors show 238

# Export the original swatches as CSS variables
colors show 238 --format css > palette.css

# Check your chosen text and background colors
colors contrast '#340059' '#9cb29e'
```

Quote HEX values so the shell does not treat `#` as a comment. CSS redirection creates or replaces `palette.css` in your current directory.

Available moods: `calm`, `warm`, `earthy`, `playful`, `bold`, `cool`, `editorial`, `soft`. Sizes: `2`, `3`, or `4`. Combination IDs: `1`–`348`. The CLI prints JSON by default; `show --format css` prints CSS. All palette operations work offline after installation.

### Use from an AI terminal assistant

Open Codex or Claude Code in your project, then enter the prompt **inside the assistant**, not at the shell prompt:

```text
Codex:       $colors recommend three palettes for a calm editorial website
Claude Code: /colors recommend three palettes for a calm editorial website
Cursor:      /colors recommend three palettes for a calm editorial website
```

Start a new assistant session after installation so it can discover the skill. In a normal shell, use `colors`, with no `/` or `$` prefix. The assistant curates recommendations and can apply them to project files when asked; the terminal command itself only looks up and exports data.

### Updates

**Run the same one-line command again:**

```sh
(set -o pipefail; curl -fsSL https://raw.githubusercontent.com/teodorik/sanzo-colors/main/install.sh | bash)
```

It downloads the latest `main` and updates the terminal command and installed skills. No manual deletion, permanent checkout, or extra update flag is needed. Project installations use the same command with `bash -s -- --project /path/to/project`.

For a manual checkout:

```sh
cd /path/to/sanzo-colors
git pull --ff-only
python3 scripts/install.py --global
```

Update behavior:

- Recognized Sanzo Colors installations are replaced with the downloaded version. Older v0.1.x installations are recognized from their supporting files; new installs include an ownership marker.
- Previous files, including your custom edits and additions, are preserved in a hidden sibling directory named `.sanzo-colors-<unique-id>/previous`. The installer prints each exact backup path. Backups persist until you remove them.
- Custom edits are **backed up, not merged** into the new version. Reapply any wanted customizations after updating.
- New files are staged before replacement. A handled installation failure rolls back replaced targets. An interruption such as a power failure may require manual recovery from the printed paths or hidden sibling backup directories.
- Unrecognized installations and symlinks at the destination are refused. Move them aside explicitly if you want Sanzo Colors to use those paths.
- A lock prevents simultaneous installers for the same home or project. If an interrupted process leaves `.sanzo-colors-install.lock` there, remove that empty lock directory only after confirming no installer is running.

To restore a backup, move the current target aside, then move the printed `previous` file or directory back to its original target. Backups live alongside `colors` under `.agents/skills`, `.claude/skills`, and (for the terminal wrapper) `.local/bin`.

Restart your assistant after updating. This updates local files only; the separately saved account plugin has its own release process. Repeating the command creates another backup even when the downloaded version has not changed.

### Uninstall

Remove only these Sanzo Colors files and directories:

```sh
rm -r "$HOME/.agents/skills/colors" "$HOME/.claude/skills/colors"
rm "$HOME/.local/bin/colors"
```

Keep `~/.local/bin` on PATH if you use it for other commands. The source checkout and account plugin are separate from this local installation.

### Troubleshooting

| Symptom | Fix |
|---|---|
| `colors: command not found` | Set PATH as above, or run `~/.local/bin/colors --help` directly. |
| `Repository not found` when cloning | Check the repository URL and network connection. This public repository does not require authentication. |
| `Refusing to replace unrecognized installation or symlink …` | The destination cannot be identified as Sanzo Colors. Preserve it by moving it aside, then retry. |
| `python3: command not found` | Install Python 3.9+ and open a new terminal. |
| Another `colors` command runs | Check `command -v colors`; put `~/.local/bin` first on PATH or use the full path. |
| Skill missing in an assistant | Start a new session and check the installed skill directory. Codex can use `$colors` or `/skills`; slash menus depend on the host. |

## Project-only installation and other hosts

```sh
python3 scripts/install.py --project /path/to/project
```

This creates `.agents/skills/colors` and `.claude/skills/colors` in that project. It does **not** install a terminal command. For other Agent Skills hosts, copy `skills/colors` into their supported skills directory, preserving supporting files. Hosts without skills can read `skills/colors/SKILL.md` directly.

To try the CLI from a checkout without installing anything:

```sh
python3 bin/colors show 238
```

## Invoke

- **Cursor and Claude Code:** `/colors calm editorial palette for this site`.
- **Codex:** select `colors` from `/skills` or invoke `$colors calm editorial palette for this site`. Some clients expose skills via slash menus; a literal `/colors` alias is host-dependent.
- **Account plugin:** attach Sanzo Colors and ask `/colors …`. A namespaced command may be exposed by the host; the package cannot register universal slash syntax.
- **Plain terminal:** `colors …` (no leading slash; `/colors` means an absolute filesystem path to a shell).

Examples:

```sh
colors recommend --mood calm --size 3
colors recommend --hex '#417777' --limit 5
colors search 'pink'
colors show 176
colors show 176 --format css > palette.css
colors contrast '#ffffff' '#417777'
```

Run without installing: `python3 bin/colors show 176`.

The CLI returns data; the assistant skill interprets the brief, curates candidates, assigns semantic roles, and edits theme files when requested. The CLI does not autonomously rewrite a project. Mood ranking uses modern seed colors and nearest swatches in OKLab, not historical mood labels. Exact ties use combination IDs.

## Sources and coverage

[W.S. Colors](https://wscolors.com/palettes) is also used by the assistant skill for live palette exploration and comparison. It lists 348 palettes, but its numbering differs from DMBK: always cite the source and verify the actual swatches before matching palettes. Its data is not included in the offline CLI; `colors show 238` still means **DMBK combination 238**. No W.S. Colors API or redistribution license has been verified.

[Wada Sanzo Colors](https://www.wada-sanzo-colors.com/) is a complementary live reference including additional classic and seasonal combinations. [DMBK's collection](https://sanzo-wada.dmbk.io/) supplies the bundled MIT-licensed snapshot: 159 colors and 348 combinations. Its [upstream](https://github.com/dblodorn/sanzo-wada) is credited to Dain Blodorn; the original license is retained under the skill's data directory. See [provenance and limitations](skills/colors/references/sources.md).

Digital values are source-specific. Added neutrals or adjusted colors must be labelled as adaptations. Contrast checks cover opaque sRGB pairs, not full-interface accessibility. Original CSS exports contain named swatches rather than assumed semantic roles.

## Development and packaging

```sh
python3 -m unittest discover -s tests -v
python3 scripts/package.py /absolute/path/sanzo-colors.zip
```

The ZIP contains the portable plugin manifest, icon, and self-contained skill only. The GitHub repository also includes the CLI, installers, and tests. To update installations, rerun the installer; previous files are backed up and unrelated destinations are refused. To uninstall, remove the installed `colors` skill directories and `~/.local/bin/colors`.

Host formats: [Cursor Skills](https://cursor.com/docs/skills), [Claude Code Skills](https://code.claude.com/docs/en/skills), [Codex Skills](https://developers.openai.com/codex/skills/).

License: MIT for original code and instructions; bundled data retains its upstream MIT notice. Not affiliated with any of the reference websites.

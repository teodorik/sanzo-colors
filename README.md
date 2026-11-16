# Sanzo Colors

A portable `/colors` skill and offline terminal tool for recommending and applying Sanzo Wada color combinations. Built with Plugin Creator. No API keys, server, Python dependencies, or paid services required. Python 3.9+.

## Install

```sh
git clone https://github.com/teodorik/sanzo-colors.git
cd sanzo-colors
python3 scripts/install.py --global
```

The repository is private; authenticate with GitHub first (or use `gh repo clone teodorik/sanzo-colors`). The installer copies the self-contained skill to `~/.agents/skills/colors` (Codex, Cursor and compatible agents) and `~/.claude/skills/colors` (Claude Code), and installs `~/.local/bin/colors`. It refuses existing destinations. If needed, add `export PATH="$HOME/.local/bin:$PATH"` to your shell configuration. Restart your assistant or start a new chat to refresh skill discovery.

For a single project instead:

```sh
python3 scripts/install.py --project /path/to/project
```

This creates `.agents/skills/colors` and `.claude/skills/colors` in that project. It does not install a terminal command. For other Agent Skills hosts, copy `skills/colors` into their supported skills directory, preserving its supporting files. Hosts without skills can read `skills/colors/SKILL.md` directly.

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

[Wada Sanzo Colors](https://www.wada-sanzo-colors.com/) is a complementary live reference including additional classic and seasonal combinations. [DMBK's collection](https://sanzo-wada.dmbk.io/) supplies the bundled MIT-licensed snapshot: 159 colors and 348 combinations. Its [upstream](https://github.com/dblodorn/sanzo-wada) is credited to Dain Blodorn; the original license is retained under the skill's data directory. See [provenance and limitations](skills/colors/references/sources.md).

Digital values are source-specific. Added neutrals or adjusted colors must be labelled as adaptations. Contrast checks cover opaque sRGB pairs, not full-interface accessibility. Original CSS exports contain named swatches rather than assumed semantic roles.

## Development and packaging

```sh
python3 -m unittest discover -s tests -v
python3 scripts/package.py /absolute/path/sanzo-colors.zip
```

The ZIP contains the portable plugin manifest, icon, and self-contained skill only. The GitHub repository also includes the CLI, installers, and tests. To update installations, explicitly remove only this skill's previous installation and rerun the installer; it never overwrites another skill. To uninstall, remove the installed `colors` skill directories and `~/.local/bin/colors`.

Host formats: [Cursor Skills](https://cursor.com/docs/skills), [Claude Code Skills](https://code.claude.com/docs/en/skills), [Codex Skills](https://developers.openai.com/codex/skills/).

License: MIT for original code and instructions; bundled data retains its upstream MIT notice. Not affiliated with either reference website.

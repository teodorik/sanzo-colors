# Lookup and contrast helper

Resolve paths relative to the installed `SKILL.md`, not the user's project or a fixed home directory. The helper uses Python 3.9+, no dependencies, and no network.

```sh
python3 <skill-directory>/scripts/colors.py recommend --mood calm --size 3 --limit 8
python3 <skill-directory>/scripts/colors.py recommend --hex '#417777' --size 3 --limit 8
python3 <skill-directory>/scripts/colors.py search 'blue'
python3 <skill-directory>/scripts/colors.py show 238
python3 <skill-directory>/scripts/colors.py show 238 --format css
python3 <skill-directory>/scripts/colors.py contrast '#340059' '#9cb29e'
```

Moods: calm, warm, earthy, playful, bold, cool, editorial, soft. Sizes: 2, 3, 4. IDs: DMBK 1–348. Quote HEX values in shell commands.

`recommend` ranks combinations by nearest swatch in OKLab to a seed color; mood seeds are modern heuristics, and ties use combination ID. Curate the results for the brief and request more candidates if needed. `show` returns every pair's contrast and the original names and values. CSS export contains original named swatches, not semantic roles.

If Python or execution is unavailable, read `../data/colors.json`. For combination N, select every color whose `combinations` array contains N. This preserves membership but does not establish historical display order or proportions. Reading the JSON is enough to recommend colors; numerical contrast still needs an available calculation tool. Do not install dependencies just to read data.

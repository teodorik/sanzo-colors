#!/usr/bin/env bash
# Install or update Sanzo Colors with backups. Requires Python 3.9+ and Git.
# Public repository: no GitHub account or authentication required.
set -euo pipefail

sanzo_install() (
  set -euo pipefail
  command -v git >/dev/null 2>&1 || { echo 'Install Git first: https://git-scm.com/downloads' >&2; exit 1; }
  command -v python3 >/dev/null 2>&1 || { echo 'Install Python 3.9+ first: https://www.python.org/downloads/' >&2; exit 1; }
  python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else "Python 3.9+ is required")'

  if [ "$#" -eq 0 ]; then set -- --global; fi
  case "$1" in
    --global) [ "$#" -eq 1 ] || { echo 'Usage: install.sh [--global | --project PATH]' >&2; exit 2; } ;;
    --project) [ "$#" -eq 2 ] || { echo 'Usage: install.sh [--global | --project PATH]' >&2; exit 2; } ;;
    *) echo 'Usage: install.sh [--global | --project PATH]' >&2; exit 2 ;;
  esac

  sanzo_tmp=$(mktemp -d "${TMPDIR:-/tmp}/sanzo-colors-install.XXXXXX")
  trap 'rm -rf -- "$sanzo_tmp"' EXIT
  echo 'Downloading teodorik/sanzo-colors…'
  GIT_TERMINAL_PROMPT=0 git -c credential.helper= clone --depth 1 --branch main --quiet https://github.com/teodorik/sanzo-colors.git "$sanzo_tmp/repo" || {
    echo 'Download failed. Check your network and https://github.com/teodorik/sanzo-colors, then retry.' >&2
    exit 1
  }
  python3 "$sanzo_tmp/repo/scripts/install.py" "$@"
  echo 'Done. Start a new assistant session to discover the colors skill.'
  if [ "$1" = '--global' ]; then
    echo 'If colors is not found, add ~/.local/bin to PATH:'
    echo '  export PATH="$HOME/.local/bin:$PATH"'
    echo 'Try: colors show 238'
  fi
)

sanzo_install "$@"

#!/usr/bin/env bash
# Create .venv, install requirements.txt into it, and check that the system tools
# manim needs (ffmpeg, LaTeX) are on PATH.
#
#   bash setup.sh
#
# macOS / Linux: any terminal. Windows: run it from Git Bash.
set -e
cd "$(dirname "$0")"

if [[ ! -d .venv ]]; then
  # a Python >= 3.11 to create the venv with. "py -3" is the Windows launcher; the
  # Microsoft Store "python3" placeholder fails this check and is skipped.
  BASE=()
  for cand in python3 python "py -3"; do
    if $cand -c 'import sys; sys.exit(sys.version_info < (3, 11))' 2> /dev/null; then
      BASE=($cand)
      break
    fi
  done
  if (( ${#BASE[@]} == 0 )); then
    echo "Python 3.11 or newer not found on PATH. Install it (see README.md) and open a new terminal." >&2
    exit 1
  fi
  echo "Creating .venv with $("${BASE[@]}" --version)"
  "${BASE[@]}" -m venv .venv
fi

if [[ -x .venv/bin/python ]]; then PY=.venv/bin/python; else PY=.venv/Scripts/python.exe; fi
if ! "$PY" -c '' 2> /dev/null; then
  echo ".venv exists but its Python doesn't run (was it made on another machine?). Delete .venv and run this again." >&2
  exit 1
fi

"$PY" -m pip install --upgrade pip
"$PY" -m pip install -r requirements.txt

echo
echo "System tools:"
missing=0
for tool in ffmpeg ffprobe latex dvisvgm; do
  if command -v "$tool" > /dev/null; then
    echo "  ok       $tool"
  else
    echo "  MISSING  $tool"
    missing=1
  fi
done
echo
if (( missing )); then
  echo "Python packages are installed, but install the missing tools above before rendering (see README.md)."
  exit 1
fi
echo "All set: $("$PY" -m manim --version)"
echo "Render everything with:  bash render_all.sh"

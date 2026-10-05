# Sourced by the render scripts: sets PY to the Python that runs manim.
# Uses the project venv if there is one (.venv/bin on macOS/Linux, .venv/Scripts
# in Git Bash on Windows), otherwise the first python3/python on PATH.
LAPLACE_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
if [[ -x $LAPLACE_ROOT/.venv/bin/python ]]; then
  PY=$LAPLACE_ROOT/.venv/bin/python
elif [[ -x $LAPLACE_ROOT/.venv/Scripts/python.exe ]]; then
  PY=$LAPLACE_ROOT/.venv/Scripts/python.exe
else
  for PY in python3 python; do "$PY" -c '' 2> /dev/null && break; done
fi
export PY

# Windows: read and write files as UTF-8 rather than the ANSI code page
export PYTHONUTF8=1

if ! "$PY" -c 'import manim' 2> /dev/null; then
  echo "manim is not installed for $PY. Run 'bash setup.sh' in $LAPLACE_ROOT first." >&2
  exit 1
fi

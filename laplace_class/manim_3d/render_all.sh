#!/usr/bin/env bash
# Render every scene into ./videos, then build the combined video (with chapter
# markers) and the presenter player.
#
#   bash render_all.sh              # 1080p60 (default)
#   bash render_all.sh -ql          # quick 480p15 preview
#   JOBS=8 bash render_all.sh       # scenes rendered in parallel (default 4)
#   bash render_all.sh -qh s07_landscape.py:SPlaneLandscape   # just one scene
set -e
cd "$(dirname "$0")"
source ../_python.sh

QUALITY=${1:--qh}
JOBS=${JOBS:-4}

# heaviest first, so the parallel jobs finish together
ALL=(
  "s10_examples_landscapes.py LandscapeExamples"
  "s09_examples_sided.py RightVsLeftSided"
  "s07_landscape.py SPlaneLandscape"
  "s01_complex_euler.py ComplexToEuler"
  "s12_roc_examples.py ROCStrips"
  "s11_roc_properties.py ROCProperties"
  "s13_inverse.py InverseLaplace"
  "s02_exponentials.py ComplexExponentials"
  "s04_fourier.py FourierRecap"
  "s00_big_picture.py BigPicture"
  "s14_partial_fractions.py PartialFractions"
  "s06_definition.py LaplaceDefinition"
  "s08_uses.py HowItsUsed"
  "s03_integrals.py IntegralsConverge"
  "s05_lti.py HowItComesUp"
)
if (( $# >= 2 )); then
  SCENES=("${2/:/ }")
else
  SCENES=("${ALL[@]}")
fi

case $QUALITY in
  -ql) RES=480p15 ;; -qm) RES=720p30 ;; -qh) RES=1080p60 ;; -qp) RES=1440p60 ;; -qk) RES=2160p60 ;;
  *) echo "unknown quality $QUALITY"; exit 1 ;;
esac

# Each scene gets its own media dir: parallel manim processes would otherwise share
# one LaTeX cache, and one process's cleanup deletes another's half-built files.
mkdir -p build videos
printf '%s\n' "${SCENES[@]}" | xargs -P "$JOBS" -L1 bash -c \
  '"$PY" -m manim '"$QUALITY"' --disable_caching --progress_bar none --media_dir build/$1 $0 $1 > build/$1.log 2>&1 \
     && echo "done   $1" || echo "FAILED $1 (see build/$1.log)"'

for entry in "${SCENES[@]}"; do
  file=${entry%% *}; scene=${entry##* }
  src="build/$scene/videos/${file%.py}/$RES/$scene.mp4"
  [[ -f $src ]] && cp "$src" "videos/${file:1:2}_$scene.mp4"
done

"$PY" make_presenter.py
echo "Done -> $(pwd)/videos"

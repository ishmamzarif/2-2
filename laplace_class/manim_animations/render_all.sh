#!/usr/bin/env bash
# Render every scene and collect the videos in ./videos (plus one combined video per lecture).
#
#   bash render_all.sh            # 1080p60 (default)
#   bash render_all.sh -ql        # quick 480p15 preview
#   JOBS=4 bash render_all.sh     # render 4 scenes in parallel
set -e
cd "$(dirname "$0")"
source ../_python.sh

QUALITY=${1:--qh}
JOBS=${JOBS:-1}

case $QUALITY in
  -ql) RES=480p15 ;; -qm) RES=720p30 ;; -qh) RES=1080p60 ;; -qp) RES=1440p60 ;; -qk) RES=2160p60 ;;
  *) echo "unknown quality $QUALITY"; exit 1 ;;
esac

SCENES=(
  "l6_01_exponentials.py ExponentialsOnSPlane"
  "l6_02_definition.py LaplaceAsWeightedFourier"
  "l6_02_definition.py IntegralAsSpiral"
  "l6_03_roc.py SameFormulaDifferentROC"
  "l6_03_roc.py ROCProperties"
  "l6_04_poles_zeros.py PoleZeroLandscape"
  "l6_05_inverse.py InverseLaplaceBuildUp"
  "l6_05_inverse.py PartialFractionsAndROC"
  "l7_01_properties.py PropertiesOnSPlane"
  "l7_01_properties.py DerivativeMeansMultiplyByS"
  "l7_01_properties.py RepeatedPoles"
  "l7_02_convolution.py ConvolutionBecomesMultiplication"
  "l7_03_systems.py CausalityAndStability"
  "l7_03_systems.py PoleDragStability"
  "l7_04_diff_eq.py ODEBecomesAlgebra"
  "l7_04_diff_eq.py SpringMassPoles"
)

# LaTeX snippets are cached under media/Tex; warm the cache with one scene first so
# parallel jobs don't race on compiling the same snippet.
printf '%s\n' "${SCENES[@]}" | head -1 | xargs -L1 "$PY" -m manim $QUALITY --progress_bar none
printf '%s\n' "${SCENES[@]}" | tail -n +2 | xargs -L1 -P "$JOBS" "$PY" -m manim $QUALITY --progress_bar none || true

mkdir -p videos
: > videos/.lec6.txt
: > videos/.lec7.txt
i=1
for entry in "${SCENES[@]}"; do
  file=${entry%% *}; scene=${entry##* }
  out="videos/$(printf '%02d' $i)_${scene}.mp4"
  src="media/videos/${file%.py}/$RES/$scene.mp4"
  # a parallel job can occasionally lose a race on the LaTeX cache; just redo it alone
  [[ -f $src ]] || "$PY" -m manim $QUALITY --progress_bar none $file $scene
  cp "$src" "$out"
  if [[ $file == l6_* ]]; then echo "file '${out#videos/}'" >> videos/.lec6.txt; else echo "file '${out#videos/}'" >> videos/.lec7.txt; fi
  i=$((i + 1))
done

# one combined video per lecture
for lec in 6 7; do
  ffmpeg -loglevel error -y -f concat -safe 0 -i videos/.lec$lec.txt -c copy "videos/Lecture${lec}_all.mp4"
  rm videos/.lec$lec.txt
done
echo "Done -> $(pwd)/videos"

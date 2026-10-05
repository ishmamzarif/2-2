#!/usr/bin/env bash
# Render both sets of animations, one after the other.
#
#   bash render_all.sh            # 1080p60 (default)
#   bash render_all.sh -ql        # quick 480p15 preview
#   JOBS=4 bash render_all.sh     # render 4 scenes at a time
#
# Each set can also be rendered on its own:
#   bash manim_animations/render_all.sh    -> manim_animations/videos/
#   bash manim_3d/render_all.sh            -> manim_3d/videos/, player.html, PRESENTER_GUIDE.md
set -e
cd "$(dirname "$0")"

QUALITY=${1:--qh}

bash manim_animations/render_all.sh "$QUALITY"
bash manim_3d/render_all.sh "$QUALITY"

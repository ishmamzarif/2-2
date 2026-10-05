# Laplace transform animations

[Manim](https://www.manim.community/) animations for the Laplace transform lectures
(`6 - Laplace.pdf`, `7 - More Laplace.pdf`), plus an interactive 3D explorer that runs in the browser.

| Folder | What's in it | What you get after rendering |
|---|---|---|
| [`manim_animations/`](manim_animations/) | 16 short scenes that follow the Lecture 6 and 7 slides ([scene list](manim_animations/README.md)) | `videos/01_….mp4` to `16_….mp4`, plus `Lecture6_all.mp4` and `Lecture7_all.mp4` |
| [`manim_3d/`](manim_3d/) | *The Laplace transform in 3D*: 15 scenes (about 14½ minutes) made for presenting, with a pause point at every talking point ([presenter guide](manim_3d/PRESENTER_GUIDE.md)) | `videos/00_….mp4` to `14_….mp4`, `videos/Laplace3D_all.mp4`, and `player.html` |
| [`interactive_3d/`](interactive_3d/) | 3D views of the s-plane that you can rotate and drag | nothing to render: open `laplace_3d_explorer.html` in a browser |

**The videos are not in the repository** (they add up to a few hundred MB), so you need to render them yourself with the scripts below.

## Quick start

Run every command from inside `laplace_class/`, in a bash terminal. On Windows, use **Git Bash** ([details below](#windows)).

```bash
bash setup.sh          # once: creates .venv and installs the Python packages
bash render_all.sh     # renders every video at 1080p60
```

Before you run `setup.sh`, install the [system tools](#1-install-the-system-tools).

| Script | What it does |
|---|---|
| [`setup.sh`](setup.sh) | creates `.venv/`, installs [`requirements.txt`](requirements.txt) into it, and checks that ffmpeg and LaTeX are on PATH |
| [`render_all.sh`](render_all.sh) | renders both sets, one after the other |
| [`manim_animations/render_all.sh`](manim_animations/render_all.sh) | renders the 2D set only |
| [`manim_3d/render_all.sh`](manim_3d/render_all.sh) | renders the 3D set only (or a single scene), then builds `player.html` and `PRESENTER_GUIDE.md` |

## 1. Install the system tools

pip installs the Python packages, but manim also needs these programs on your PATH:

| Tool | Why it's needed |
|---|---|
| Python 3.11 or newer | manim 0.21 requires 3.11+ |
| LaTeX (`latex`, `dvisvgm`) | every equation in the videos is typeset with LaTeX |
| ffmpeg (`ffmpeg`, `ffprobe`) | the scripts use it to join the scenes into the combined videos |
| bash | runs the `.sh` scripts. macOS and Linux already have it; on Windows it comes with Git Bash |

### Windows

1. **Install the tools.** You can use winget in PowerShell or Windows Terminal:

   ```powershell
   winget install -e --id Git.Git
   winget install -e --id Python.Python.3.13
   winget install -e --id Gyan.FFmpeg
   winget install -e --id MiKTeX.MiKTeX
   ```

   Or use the installers: [Git for Windows](https://git-scm.com/download/win) (includes Git Bash),
   [Python](https://www.python.org/downloads/) (tick **Add python.exe to PATH**),
   [ffmpeg](https://www.gyan.dev/ffmpeg/builds/) (then add its `bin` folder to PATH),
   [MiKTeX](https://miktex.org/download).

2. **Let MiKTeX install packages without asking.** Open **MiKTeX Console → Settings** and set
   *Install missing packages on-the-fly* to **Always**. The first render needs several LaTeX packages that
   MiKTeX doesn't have yet. With the default setting, MiKTeX opens a dialog for each one, and a render running
   in the background can hang while it waits.

3. **Close and reopen Git Bash** so it picks up the new PATH.

4. **Use Git Bash for every command in this README.** PowerShell and Command Prompt can't run `.sh` scripts.
   To open Git Bash in the right folder, right-click inside `laplace_class` in File Explorer and choose
   **Open Git Bash here** (on Windows 11 it's under **Show more options**). You can also start Git Bash and `cd` there:

   ```bash
   cd /c/Users/<you>/path/to/Labs/laplace_class    # C:\Users\... is written /c/Users/... in Git Bash
   ```

Check that the tools work: `python --version`, `ffmpeg -version` and `latex --version` should each print a version in Git Bash.

### macOS

```bash
brew install python ffmpeg cairo pango pkg-config
brew install --cask mactex-no-gui        # or the full MacTeX from https://tug.org/mactex/
```

Open a new terminal afterwards so that `/Library/TeX/texbin` is on your PATH.

### Linux (Debian / Ubuntu)

```bash
sudo apt install python3 python3-venv python3-dev build-essential pkg-config \
                 libcairo2-dev libpango1.0-dev ffmpeg texlive texlive-latex-extra dvisvgm
```

## 2. Install the Python packages

```bash
bash setup.sh
```

This creates a virtual environment in `.venv/`, installs `requirements.txt` into it (manim 0.21, numpy, pycairo),
and checks that the tools from step 1 are on PATH. It's safe to run again, because it reuses an existing `.venv`.

To do the same by hand:

```bash
python3 -m venv .venv              # Windows: python -m venv .venv
source .venv/bin/activate          # Windows (Git Bash): source .venv/Scripts/activate
pip install -r requirements.txt
```

## 3. Render the videos

```bash
bash render_all.sh                 # everything, 1080p60
bash render_all.sh -ql             # quick 480p15 preview: much faster, good for checking that everything works
JOBS=4 bash render_all.sh          # render 4 scenes at a time
```

The quality flags are `-ql` (480p15), `-qm` (720p30), `-qh` (1080p60, the default), `-qp` (1440p60) and `-qk` (2160p60).
A full-quality render takes a while, so try `-ql` first. Setting `JOBS` higher renders faster but uses more memory.
By default the 3D set renders 4 scenes at a time and the 2D set renders 1.

To render one set, or one 3D scene:

```bash
bash manim_animations/render_all.sh                                  # 2D set only
bash manim_3d/render_all.sh                                          # 3D set only
bash manim_3d/render_all.sh -qh s07_landscape.py:SPlaneLandscape     # one 3D scene, then rebuild player.html
```

The scripts find `.venv` on their own, so you don't need to activate it first.

To preview a single scene while you edit it, activate the venv and call manim directly:

```bash
source .venv/bin/activate          # Windows (Git Bash): source .venv/Scripts/activate
cd manim_animations
manim -pql l6_02_definition.py IntegralAsSpiral    # -p opens the video when it's done
```

### Where the output goes

| Set | Output |
|---|---|
| 2D | `manim_animations/videos/`: one file per scene, plus `Lecture6_all.mp4` and `Lecture7_all.mp4` |
| 3D | `manim_3d/videos/`: one file per scene, plus `Laplace3D_all.mp4`, which has a chapter marker at every pause point (VLC and IINA show them) |
| 3D | `manim_3d/player.html`: open it in Chrome, Edge or Safari. It plays the scenes and stops at every pause point (press Space to continue). [PRESENTER_GUIDE.md](manim_3d/PRESENTER_GUIDE.md) lists the keys and what to say at each pause |

Manim's intermediate files go to `manim_animations/media/` and `manim_3d/build/`. Both folders are git-ignored and safe to delete.
A 3D render also rewrites `manim_3d/beats/*.json`, `player.html` and `PRESENTER_GUIDE.md`, so if the timings changed, git will show those files as modified.

## Interactive explorer

`interactive_3d/laplace_3d_explorer.html` is a single self-contained page, so you can double-click it and it works offline.
You only need to rebuild it if you edit `explorer.src.html`. To rebuild, run `python interactive_3d/build.py`
(with the venv active, or with any Python 3).

## Troubleshooting

| Problem | Fix |
|---|---|
| `$'\r': command not found` or `syntax error near unexpected token` | The scripts have Windows line endings. A git clone avoids this (the repo's `.gitattributes` keeps them LF). If you got the files another way, run `sed -i 's/\r$//' *.sh manim_*/*.sh` |
| `manim is not installed for …` | Run `bash setup.sh` |
| Windows: `Python was not found; run without arguments to install from the Microsoft Store` | Python isn't on PATH. Reinstall it with **Add python.exe to PATH** ticked. Then go to *Settings → Apps → Advanced app settings → App execution aliases* and turn off the `python.exe` / `python3.exe` aliases |
| `.venv exists but its Python doesn't run` | The `.venv` was made on another machine or moved. Delete it and run `bash setup.sh` again |
| `latex: command not found`, or a LaTeX error | LaTeX isn't installed or isn't on PATH. On Windows, reopen Git Bash after installing MiKTeX and check the on-the-fly setting from step 2 |
| `ffmpeg: command not found` | The scene videos are rendered, but the combined videos aren't built. Install ffmpeg and run the script again |
| `FAILED SomeScene (see build/SomeScene.log)` (3D set) | Read that log. The other scenes still render. Then re-render just that scene with the one-scene command above |
| The computer freezes or the render gets killed | Lower the parallelism: `JOBS=1 bash render_all.sh` |

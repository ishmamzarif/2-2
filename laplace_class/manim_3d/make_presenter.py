"""Build the presenter material from the rendered videos and beats/*.json.

* videos/Laplace3D_all.mp4 - all scenes back to back, a chapter marker at every pause point
* PRESENTER_GUIDE.md       - per scene: each pause point, what is on screen, what to say
* player.html              - plays the scenes and stops at every pause point (Space / arrows / clicker)

render_all.sh runs this at the end; run it by hand after re-rendering single scenes.
"""
import json
import subprocess
from pathlib import Path

from presenter_notes import NOTES, SCENES

ROOT = Path(__file__).resolve().parent
VIDEOS = ROOT / "videos"
BEATS = ROOT / "beats"
HOLD = 0.35          # how far into a beat's held frame the player stops


def video_name(file, cls):
    return f"{file[1:3]}_{cls}.mp4"


def probe_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def load():
    scenes = []
    for i, (file, cls, title, part) in enumerate(SCENES):
        data = json.loads((BEATS / f"{cls}.json").read_text())
        notes = NOTES.get(cls, [])
        if len(notes) != len(data["beats"]):
            print(f"warning: {cls} has {len(data['beats'])} beats but {len(notes)} notes")
        path = VIDEOS / video_name(file, cls)
        scenes.append({
            "n": i, "cls": cls, "title": title, "part": part, "file": path.name, "exists": path.exists(),
            "duration": probe_duration(path) if path.exists() else data["duration"],
            "beats": [{"t": b["t"], "label": b["label"], "note": notes[k] if k < len(notes) else ""}
                      for k, b in enumerate(data["beats"])],
        })
    return scenes


def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


# ---------------------------------------------------------------- combined video
def _meta_escape(s):
    for ch in "\\=;#\n":
        s = s.replace(ch, "\\" + ch)
    return s


def combined_video(scenes):
    missing = [s["file"] for s in scenes if not s["exists"]]
    if missing:
        print("combined video skipped, missing:", ", ".join(missing))
        return
    marks, offset = [], 0.0
    for s in scenes:
        marks.append((offset, f"{s['n']:02d} {s['title']}"))
        for b in s["beats"]:
            marks.append((offset + b["t"], f"{s['n']:02d} · {b['label']}"))
        offset += s["duration"]
    meta = [";FFMETADATA1", "title=The Laplace transform in 3D"]
    for k, (start, title) in enumerate(marks):
        end = marks[k + 1][0] if k + 1 < len(marks) else offset
        if end - start > 0.05:
            meta += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(start * 1000)}", f"END={int(end * 1000)}",
                     f"title={_meta_escape(title)}"]
    lst, chap = VIDEOS / ".concat.txt", VIDEOS / ".chapters.txt"
    lst.write_text("".join(f"file '{s['file']}'\n" for s in scenes))
    chap.write_text("\n".join(meta) + "\n")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(chap),
                    "-map", "0", "-map_metadata", "1", "-map_chapters", "1", "-c", "copy", str(VIDEOS / "Laplace3D_all.mp4")],
                   check=True)
    lst.unlink()
    chap.unlink()
    print(f"videos/Laplace3D_all.mp4: {mmss(offset)}, {len(marks)} chapters")


# ---------------------------------------------------------------- guide
def guide(scenes):
    total = sum(s["duration"] for s in scenes)
    pauses = sum(len(s["beats"]) for s in scenes)
    out = [
        "# Presenter guide: the Laplace transform in 3D",
        "",
        f"{len(scenes)} scenes, {mmss(total)} of animation, {pauses} pause points. Syllabus: Lecture 6 (`6 - Laplace.pdf`).",
        "On screen there is deliberately little text; what to say at each pause point is below.",
        "",
        "## How to present",
        "",
        "- **`player.html`** (open it in Chrome, Edge or Safari): plays scene by scene and **stops at every pause point**.",
        "  - `Space` / `→` / `PageDown` / clicker: play on to the next pause point (pressed while playing: jump straight there)",
        "  - `←` / `PageUp`: back one pause point · `]` / `[`: next / previous scene · `Home`: restart the scene",
        "  - `N`: talking points (hidden by default, in case your screen is mirrored) · `L`: scene list · `F`: fullscreen · `B`: black screen",
        "- **`videos/Laplace3D_all.mp4`**: everything in one file, with a chapter marker at every pause point (VLC or IINA show them).",
        "- **`videos/NN_Scene.mp4`**: one file per scene, if you want to drop them into slides.",
        "- **Interactive 3D explorer** for live \"what if\" questions: `../interactive_3d/laplace_3d_explorer.html` (works offline)",
        "  or the published page https://claude.ai/artifact/DaYCmbwM76a5kbFnoYBDGy. Nine views in the same order as the talk;",
        "  `←` / `→` switch views, drag to rotate, `P` hides the side panel, `R` resets the camera.",
        "",
        "## Running order",
        "",
        "| # | Scene | Part | Length | Pauses |",
        "|---|---|---|---|---|",
    ]
    for s in scenes:
        out.append(f"| {s['n']:02d} | {s['title']} | {s['part']} | {mmss(s['duration'])} | {len(s['beats'])} |")
    for s in scenes:
        out += ["", f"## {s['n']:02d} · {s['title']}", "",
                f"`videos/{s['file']}` · {mmss(s['duration'])} · part: {s['part']}", "",
                "| At | On screen | Say |", "|---|---|---|"]
        for b in s["beats"]:
            label = b["label"].replace("|", "/")
            note = b["note"].replace("|", "/")
            out.append(f"| {mmss(b['t'])} | {label} | {note} |")
    out += ["", "## Re-rendering", "",
            "```sh", "cd manim_3d", "JOBS=8 ./render_all.sh                               # everything, 1080p60",
            "./render_all.sh -qh s07_landscape.py:SPlaneLandscape    # one scene, then rebuilds this guide and the player",
            "```", ""]
    (ROOT / "PRESENTER_GUIDE.md").write_text("\n".join(out))
    print("PRESENTER_GUIDE.md written")


# ---------------------------------------------------------------- player
PLAYER = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Laplace 3D Player</title>
<style>
  :root { --bg: #0c0c0f; --fg: #ececf0; --muted: #a0a0aa; --accent: #f7d96f; --panel: rgba(18, 18, 24, 0.94); --line: #2a2a33; }
  html, body { margin: 0; height: 100%; background: var(--bg); color: var(--fg);
               font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; overflow: hidden; }
  video { position: fixed; inset: 0; width: 100%; height: 100%; object-fit: contain; background: #000; }
  #bar { position: fixed; top: 0; left: 0; right: 0; display: flex; align-items: center; gap: 14px; padding: 12px 18px;
         background: linear-gradient(rgba(0,0,0,.75), rgba(0,0,0,0)); transition: opacity .4s; z-index: 3; }
  #bar.hide { opacity: 0; }
  #where { flex: 1; min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  #where b { color: var(--accent); font-weight: 600; }
  #where span { color: var(--muted); }
  button { background: rgba(255,255,255,.08); color: var(--fg); border: 1px solid var(--line); border-radius: 8px;
           padding: 6px 12px; font: inherit; cursor: pointer; }
  button:hover { background: rgba(255,255,255,.16); }
  #notes { position: fixed; left: 50%; bottom: 18px; transform: translateX(-50%); width: min(920px, calc(100% - 32px));
           box-sizing: border-box; background: var(--panel); border: 1px solid var(--line); border-radius: 12px;
           padding: 14px 18px; display: none; z-index: 3; }
  #notes.show { display: block; }
  #notes .label { color: var(--accent); font-weight: 600; margin-bottom: 4px; }
  #notes .next { color: var(--muted); margin-top: 8px; font-size: 13px; }
  #list { position: fixed; top: 0; bottom: 0; left: 0; width: min(380px, 90vw); background: var(--panel);
          border-right: 1px solid var(--line); overflow-y: auto; transform: translateX(-102%); transition: transform .25s; z-index: 4; }
  #list.open { transform: none; }
  #list h2 { font-size: 13px; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin: 18px 18px 6px; }
  .scene { padding: 8px 18px; cursor: pointer; border-top: 1px solid var(--line); }
  .scene:hover { background: rgba(255,255,255,.05); }
  .scene.cur > .st { color: var(--accent); }
  .scene .st { font-weight: 600; }
  .scene .meta { color: var(--muted); font-size: 12px; }
  .beat { padding: 3px 0 3px 14px; color: var(--muted); font-size: 13px; cursor: pointer; }
  .beat:hover, .beat.cur { color: var(--fg); }
  #hint { position: fixed; left: 50%; top: 50%; transform: translate(-50%, -50%); background: var(--panel); border: 1px solid var(--line);
          border-radius: 14px; padding: 22px 26px; max-width: 520px; z-index: 5; display: none; }
  #hint.show { display: block; }
  #hint kbd { display: inline-block; min-width: 22px; text-align: center; padding: 1px 6px; border: 1px solid var(--line);
              border-radius: 5px; background: rgba(255,255,255,.06); font: 13px ui-monospace, monospace; }
  #hint td { padding: 3px 10px 3px 0; vertical-align: top; }
  #black { position: fixed; inset: 0; background: #000; z-index: 6; display: none; }
  #black.on { display: block; }
  #missing { position: fixed; left: 50%; top: 50%; transform: translate(-50%, -50%); color: var(--muted); z-index: 2; display: none;
             text-align: center; }
  @media (max-width: 640px) { #bar { padding: 10px 16px; } #bar button.wide { display: none; } }
</style>
</head>
<body>
<video id="v" playsinline preload="auto"></video>
<div id="missing"></div>
<div id="bar">
  <button id="bList" title="Scene list (L)">&#9776;</button>
  <div id="where"></div>
  <button id="bPrev" title="Back one pause (&larr;)">&#9664;</button>
  <button id="bNext" title="Play to next pause (Space)">&#9654;</button>
  <button id="bNotes" class="wide" title="Talking points (N)">Notes</button>
  <button id="bFull" class="wide" title="Fullscreen (F)">&#x26F6;</button>
  <button id="bHelp" title="Keys (?)">?</button>
</div>
<div id="notes"><div class="label"></div><div class="text"></div><div class="next"></div></div>
<nav id="list"></nav>
<div id="hint">
  <table>
    <tr><td><kbd>Space</kbd> <kbd>&rarr;</kbd> <kbd>PgDn</kbd></td><td>play to the next pause point (while playing: jump there)</td></tr>
    <tr><td><kbd>&larr;</kbd> <kbd>PgUp</kbd></td><td>back one pause point</td></tr>
    <tr><td><kbd>]</kbd> <kbd>[</kbd></td><td>next / previous scene</td></tr>
    <tr><td><kbd>Home</kbd></td><td>restart this scene</td></tr>
    <tr><td><kbd>N</kbd></td><td>talking points (keep hidden if the screen is mirrored)</td></tr>
    <tr><td><kbd>L</kbd></td><td>scene list</td></tr>
    <tr><td><kbd>F</kbd></td><td>fullscreen</td></tr>
    <tr><td><kbd>B</kbd> <kbd>.</kbd></td><td>black screen</td></tr>
  </table>
  <p style="color:var(--muted);margin:12px 0 0">Press any key to close.</p>
</div>
<div id="black"></div>
<script>
const DATA = __DATA__;
const HOLD = __HOLD__;
const v = document.getElementById('v');
const $ = (id) => document.getElementById(id);
let si = 0, bi = -1, target = null, idle = null;

function scene() { return DATA[si]; }

function load(i, then) {
  si = Math.max(0, Math.min(DATA.length - 1, i));
  bi = -1; target = null;
  const s = scene();
  $('missing').style.display = s.exists ? 'none' : 'block';
  $('missing').textContent = s.exists ? '' : 'videos/' + s.file + ' is missing - run ./render_all.sh';
  v.src = 'videos/' + s.file;
  v.pause();
  v.addEventListener('loadeddata', () => { if (then) then(); render(); }, { once: true });
  try { history.replaceState(null, '', '#' + si); } catch (e) {}
  render();
}

function seekBeat(k) {             // show the held frame of beat k (k = -1: the start)
  v.pause(); target = null; bi = k;
  v.currentTime = k < 0 ? 0 : scene().beats[k].t + HOLD;
  render();
}

function next() {
  const beats = scene().beats;
  if (!v.paused && target !== null) {          // already playing towards a pause: jump there
    seekBeat(bi + 1); return;
  }
  if (bi + 1 < beats.length) {
    target = beats[bi + 1].t + HOLD;
    v.play();
  } else if (!v.ended && v.currentTime < v.duration - 0.05) {
    target = null; v.play();                   // play out the end of the scene
  } else if (si + 1 < DATA.length) {
    load(si + 1, () => next());
  }
  render();
}

function prev() {
  if (bi >= 0) { seekBeat(bi - 1); return; }
  if (si > 0) load(si - 1, () => seekBeat(DATA[si].beats.length - 1));
}

function tick() {
  if (!v.paused && target !== null && v.currentTime >= target) {
    v.pause(); v.currentTime = target; target = null; bi += 1; render();
  }
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
v.addEventListener('ended', render);
v.addEventListener('play', render);
v.addEventListener('pause', render);

function fmt(t) { return Math.floor(t / 60) + ':' + String(Math.floor(t % 60)).padStart(2, '0'); }

function render() {
  const s = scene();
  const n = s.beats.length;
  let state;
  if (!v.paused) state = '&#9654; playing';
  else if (v.ended || (bi === n - 1 && v.currentTime >= v.duration - 0.05)) state = 'end of scene &middot; Space for the next';
  else if (bi < 0) state = 'ready &middot; Space to play';
  else state = 'pause ' + (bi + 1) + '/' + n + ': ' + escapeHtml(s.beats[bi].label);
  $('where').innerHTML = '<b>' + String(s.n).padStart(2, '0') + ' &middot; ' + escapeHtml(s.title) + '</b> <span>&mdash; ' + state + '</span>';
  const cur = bi >= 0 ? s.beats[bi] : null;
  const up = s.beats[bi + 1];
  $('notes').querySelector('.label').textContent = cur ? cur.label : s.title;
  $('notes').querySelector('.text').textContent = cur ? cur.note : 'Scene ' + s.n + ' of ' + (DATA.length - 1) + ' (' + s.part + ').';
  $('notes').querySelector('.next').textContent = up ? 'Next pause: ' + up.label : (si + 1 < DATA.length ? 'Next scene: ' + DATA[si + 1].title : 'Last scene');
  document.querySelectorAll('.scene').forEach((el, i) => el.classList.toggle('cur', i === si));
  document.querySelectorAll('.beat').forEach((el) => el.classList.toggle('cur', +el.dataset.s === si && +el.dataset.b === bi));
}

function escapeHtml(t) { return t.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }

function buildList() {
  const nav = $('list');
  let part = null, h = '';
  DATA.forEach((s, i) => {
    if (s.part !== part) { part = s.part; h += '<h2>' + escapeHtml(part) + '</h2>'; }
    h += '<div class="scene" data-s="' + i + '"><div class="st">' + String(s.n).padStart(2, '0') + ' &middot; ' + escapeHtml(s.title) +
         '</div><div class="meta">' + fmt(s.duration) + ' &middot; ' + s.beats.length + ' pauses</div>';
    s.beats.forEach((b, k) => { h += '<div class="beat" data-s="' + i + '" data-b="' + k + '">' + fmt(b.t) + ' &nbsp;' + escapeHtml(b.label) + '</div>'; });
    h += '</div>';
  });
  nav.innerHTML = h;
  nav.addEventListener('click', (e) => {
    const b = e.target.closest('.beat'), sc = e.target.closest('.scene');
    if (b) { const i = +b.dataset.s, k = +b.dataset.b; if (i === si) seekBeat(k); else load(i, () => seekBeat(k)); }
    else if (sc) load(+sc.dataset.s);
    nav.classList.remove('open');
  });
}

function toggleFull() {
  if (document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen().catch(() => {});
}

function wake() {
  $('bar').classList.remove('hide');
  clearTimeout(idle);
  idle = setTimeout(() => $('bar').classList.add('hide'), 2500);
}

document.addEventListener('mousemove', wake);
document.addEventListener('keydown', (e) => {
  if ($('hint').classList.contains('show')) { $('hint').classList.remove('show'); e.preventDefault(); return; }
  const k = e.key;
  if (k === ' ' || k === 'ArrowRight' || k === 'PageDown' || k === 'ArrowDown') next();
  else if (k === 'ArrowLeft' || k === 'PageUp' || k === 'ArrowUp') prev();
  else if (k === ']') load(si + 1);
  else if (k === '[') load(si - 1);
  else if (k === 'Home') seekBeat(-1);
  else if (k === 'n' || k === 'N') $('notes').classList.toggle('show');
  else if (k === 'l' || k === 'L') $('list').classList.toggle('open');
  else if (k === 'f' || k === 'F') toggleFull();
  else if (k === 'b' || k === 'B' || k === '.') $('black').classList.toggle('on');
  else if (k === '?' || k === 'h' || k === 'H') $('hint').classList.add('show');
  else if (k === 'Escape') { $('list').classList.remove('open'); $('black').classList.remove('on'); }
  else return;
  e.preventDefault();
});
v.addEventListener('click', next);
$('bNext').onclick = next;
$('bPrev').onclick = prev;
$('bList').onclick = () => $('list').classList.toggle('open');
$('bNotes').onclick = () => $('notes').classList.toggle('show');
$('bFull').onclick = toggleFull;
$('bHelp').onclick = () => $('hint').classList.add('show');

buildList();
const start = parseInt(location.hash.slice(1), 10);
load(Number.isFinite(start) ? start : 0);
wake();
</script>
</body>
</html>
"""


def player(scenes):
    data = json.dumps(scenes, ensure_ascii=False)
    (ROOT / "player.html").write_text(PLAYER.replace("__DATA__", data).replace("__HOLD__", str(HOLD)))
    print("player.html written")


if __name__ == "__main__":
    sc = load()
    combined_video(sc)
    guide(sc)
    player(sc)

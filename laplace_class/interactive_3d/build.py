"""Build the interactive explorer from explorer.src.html.

  laplace_3d_explorer.html          open this one: a complete page with every script inlined, works offline
  explorer.publish.html             the source published as the Artifact (no doctype, the host adds it;
                                    three.js and KaTeX load from cdnjs)

KaTeX's stylesheet is always inlined, with its fonts as data URIs, because the
Artifact sandbox only lets scripts (not stylesheets or fonts) load from a CDN.
"""
import base64
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENDOR = HERE / "vendor"
CDN = {
    "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js": VENDOR / "three.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js": VENDOR / "katex.min.js",
}


def katex_css():
    css = (VENDOR / "katex.min.css").read_text()

    def face(m):
        block = m.group(0)
        woff2 = re.search(r"url\(fonts/(KaTeX_[A-Za-z0-9-]+)\.woff2\)", block)
        path = VENDOR / "fonts" / f"{woff2.group(1)}.woff2" if woff2 else None
        if not path or not path.exists():
            return ""  # a face we don't ship (Fraktur, Script, ...): drop it
        data = base64.b64encode(path.read_bytes()).decode()
        return re.sub(r"src:[^}]*", f'src:url(data:font/woff2;base64,{data}) format("woff2")', block)

    return re.sub(r"@font-face\{[^}]*\}", face, css)


def main():
    src = (HERE / "explorer.src.html").read_text()
    page = src.replace("/*__KATEX_CSS__*/", katex_css())
    (HERE / "explorer.publish.html").write_text(page)

    offline = page
    for url, path in CDN.items():
        tag = f'<script src="{url}"></script>'
        assert tag in offline, url
        offline = offline.replace(tag, "<script>" + path.read_text().replace("</script", "<\\/script") + "</script>")
    title = re.search(r"<title>.*?</title>", offline).group(0)
    offline = offline.replace(title, "", 1)
    offline = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
               "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
               f"{title}\n</head>\n<body>\n{offline}\n</body>\n</html>\n")
    (HERE / "laplace_3d_explorer.html").write_text(offline)
    for name in ("laplace_3d_explorer.html", "explorer.publish.html"):
        print(f"{name}: {(HERE / name).stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()

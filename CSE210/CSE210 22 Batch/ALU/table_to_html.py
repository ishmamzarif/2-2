import sys
import html

def tsv_to_html(tsv_path, html_path):
    with open(tsv_path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f if line.strip()]

    rows = [line.split("\t") for line in lines]

    with open(html_path, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n<html>\n<head>\n<meta charset='utf-8'>\n")
        f.write("<title>TSV Table</title>\n")
        f.write("""
<style>
table { border-collapse: collapse; }
th, td { border: 1px solid #333; padding: 6px 10px; }
th { background: #eee; }
tr.odd { background: #fff; }
tr.even { background: #f0f0f0; }
</style>
</head>
<body>
<table>
""")

        for i, row in enumerate(rows):
            row_class = "even" if i % 2 == 0 else "odd"
            f.write(f"<tr class='{row_class}'>")
            tag = "th" if i == 0 else "td"
            for cell in row:
                f.write(f"<{tag}>{html.escape(cell)}</{tag}>")
            f.write("</tr>\n")

        f.write("</table>\n</body>\n</html>")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python tsv_to_html.py input.tsv output.html")
        sys.exit(1)

    tsv_to_html(sys.argv[1], sys.argv[2])

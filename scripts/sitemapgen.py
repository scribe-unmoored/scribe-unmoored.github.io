
# This code generates the sitemap.

from pathlib import Path

base = Path(".")


# Basic Files to include: 

include_files = [
    "index.html",
    "timeline.html",
    "scribe/index.html",
    "writings/index.html",
    "adventures/index.html",
  # "adventures/characters.html",
  # "adventures/map.html",
]

adventure_series = [
  # "glasscrown",
    "brasstower",
    "falsedreamer",
  # "marblejaws",
  # "riventhrone",
  # "worldeater",
  # "starlesssky",
  # "deadmoon",
]

links = []

# top-level fixed pages
for f in include_files:
    path = base / f
    if path.exists():
        links.append((f.replace(".html", "").title(), f))

# episode index pages
for ep in adventure_series:
    path = Path("adventures") / ep / "index.html"
    if path.exists():
        links.append((ep.title(), str(path).replace("\\", "/")))

# build sitemap
out = ["<h1>Sitemap</h1>", "<ul>"]

for title, href in sorted(links):
    out.append(f'<li><a href="{href}">{title}</a></li>')

out.append("</ul>")

Path("sitemap.html").write_text("\n".join(out), encoding="utf-8")

print("Sitemap generated.")

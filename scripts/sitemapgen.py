#!/usr/bin/env python3
# Generate a standards-compliant XML sitemap (sitemap.xml).

from pathlib import Path
from datetime import datetime, timezone
from xml.sax.saxutils import escape

# If set, URLs will be absolute using this base (no trailing slash). Leave empty for relative URLs.
BASE_URL = ""

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
        links.append((f.replace(".html", ""), f))

# episode index pages
for ep in adventure_series:
    path = Path("adventures") / ep / "index.html"
    if path.exists():
        links.append((ep, str(path).replace("\\", "/")))

def lastmod_for(path_str: str):
    try:
        ts = Path(path_str).stat().st_mtime
        return datetime.fromtimestamp(ts, tz=timezone.utc).date().isoformat()
    except Exception:
        return None

# build XML sitemap
xml_lines = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

for title, href in sorted(links):
    if BASE_URL:
        loc = BASE_URL.rstrip('/') + '/' + href.lstrip('/')
    else:
        loc = href
    loc = escape(loc)
    lm = lastmod_for(href)
    xml_lines.append("  <url>")
    xml_lines.append(f"    <loc>{loc}</loc>")
    if lm:
        xml_lines.append(f"    <lastmod>{lm}</lastmod>")
    xml_lines.append("  </url>")

xml_lines.append("</urlset>")

Path("sitemap.xml").write_text("\n".join(xml_lines), encoding="utf-8")
print("Sitemap XML generated.")

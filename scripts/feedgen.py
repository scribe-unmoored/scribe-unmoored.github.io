#!/usr/bin/env python3
# Generate or update rss.xml by merging existing entries and adding new files in order.

from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
import xml.dom.minidom as md

SITE_URL = "https://scribe-unmoored.github.io"

# --- episode references ---
# Full list of available episode series. Change EPISODE_FILTER to limit which series are included.
episodes = [
    "glasscrown", "brasstower", "falsedreamer", "marblejaws",
    "riventhrone", "worldeater", "bleedingsun", "starlesssky",
]

# Toggle: set to a single series name (e.g. 'brasstower') to only include that series,
# or set to None to include all series in `episodes`.
EPISODE_FILTER = 'brasstower'  # change this when new episodes are ready

# Helper: convert filesystem mtime to timezone-aware datetime
def mtime_to_dt(path: Path):
    try:
        ts = path.stat().st_mtime
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    except Exception:
        return datetime.now(timezone.utc)

# Collect new candidates from disk (use file mtime for ordering)
candidates = {}
# Decide which episode series to scan
if EPISODE_FILTER:
    episodes_to_scan = [EPISODE_FILTER]
else:
    episodes_to_scan = episodes

for ep in episodes_to_scan:
    for chap in Path(f"adventures/{ep}").glob("*.html"):
        url = f"{SITE_URL}/adventures/{ep}/{chap.name}"
        candidates[url] = {
            "title": f"{ep.title()} — {chap.stem.replace('-', ' ').title()}",
            "url": url,
            "date": mtime_to_dt(chap),
        }

for story in Path("writings/writings").glob("*.html"):
    url = f"{SITE_URL}/writings/writings/{story.name}"
    candidates[url] = {
        "title": story.stem.replace("-", " ").title(),
        "url": url,
        "date": mtime_to_dt(story),
    }

# Load existing rss.xml entries (if any) and keep them
existing = {}
rss_path = Path('rss.xml')
if rss_path.exists():
    try:
        tree = ET.parse(rss_path)
        root = tree.getroot()
        # Find channel -> item elements
        for item in root.findall('.//item'):
            guid_el = item.find('guid') or item.find('link')
            if guid_el is None:
                continue
            guid = guid_el.text.strip()
            title_el = item.find('title')
            pub_el = item.find('pubDate')
            title = title_el.text.strip() if title_el is not None and title_el.text else guid
            pub = None
            if pub_el is not None and pub_el.text:
                try:
                    pub = parsedate_to_datetime(pub_el.text.strip())
                    if pub.tzinfo is None:
                        pub = pub.replace(tzinfo=timezone.utc)
                except Exception:
                    pub = None
            existing[guid] = {
                'title': title,
                'url': guid,
                'date': pub or datetime.now(timezone.utc),
            }
    except Exception:
        # If parsing fails, ignore existing file
        existing = {}

# Merge: prefer existing entry if present, otherwise use candidate
merged = {}
for url, item in {**candidates, **existing}.items():
    # If both exist, keep the one with the earlier stored date? keep existing to preserve history
    if url in existing:
        merged[url] = existing[url]
    else:
        merged[url] = candidates[url]

# Sort newest first
items = sorted(merged.values(), key=lambda x: x['date'], reverse=True)

# Build RSS
rss = ET.Element('rss', version='2.0')
channel = ET.SubElement(rss, 'channel')
ET.SubElement(channel, 'title').text = 'The Scribe Unmoored'
ET.SubElement(channel, 'link').text = SITE_URL
ET.SubElement(channel, 'description').text = 'Home of The Adventures. A repository of fiction, essays, and miscellanies.'

for it in items:
    node = ET.SubElement(channel, 'item')
    ET.SubElement(node, 'title').text = it['title']
    ET.SubElement(node, 'link').text = it['url']
    ET.SubElement(node, 'guid').text = it['url']
    ET.SubElement(node, 'pubDate').text = it['date'].strftime('%a, %d %b %Y %H:%M:%S GMT')

# Pretty-print and write
raw = ET.tostring(rss, encoding='utf-8')
pretty = md.parseString(raw).toprettyxml(indent='  ', encoding='utf-8')
Path('rss.xml').write_bytes(pretty)
print('rss.xml updated (merged).')

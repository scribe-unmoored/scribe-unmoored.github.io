
# This is a program for generating an rss feed. It probably needs an update once the site gets bigger.

#------------------------------------------------------------------- IMPORT BLOCK
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET




SITE_URL = "https://scribe-unmoored.github.io"#-------------------- SITE URL


# --- episode references ---

episodes = [
    "glasscrown", "brasstower", "falsedreamer", "marblejaws",
    "riventhrone", "worldeater", "bleedingsun", "starlesssky",
]


# This is where new items are placed in the rss feed.

items = [] 


# --- Episode chapters ---

for ep in episodes:
    chapter_paths = Path(f"adventures/{ep}").glob("*.html")

    for chap in chapter_paths:
        items.append({
            "title": f"{ep.title()} — {chap.stem.replace('-', ' ').title()}",
            "url": f"{SITE_URL}/adventures/{ep}/{chap.name}",
            "date": datetime.utcnow(),
        })


# --- Standalone stories ---

story_paths = Path("writings/writings").glob("*.html")

for story in story_paths:
    items.append({
        "title": story.stem.replace("-", " ").title(),
        "url": f"{SITE_URL}/writings/writings/{story.name}",
        "date": datetime.utcnow(),
    })


# --- Sorting by date ---

items.sort(key=lambda x: x["date"])

# --- RSS build ---
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")

ET.SubElement(channel, "title").text = "The Adventures"
ET.SubElement(channel, "link").text = SITE_URL
ET.SubElement(channel, "description").text = "Serialized fiction and short stories."

for item in items:
    node = ET.SubElement(channel, "item")

    ET.SubElement(node, "title").text = item["title"]
    ET.SubElement(node, "link").text = item["url"]
    ET.SubElement(node, "guid").text = item["url"]
    ET.SubElement(node, "pubDate").text = item["date"].strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )

tree = ET.ElementTree(rss)
tree.write("rss.xml", encoding="utf-8", xml_declaration=True)

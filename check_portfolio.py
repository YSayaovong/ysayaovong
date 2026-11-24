"""Check local portfolio assets, anchor targets, and role alignment.

This is a local structure check, not a remote-link or accessibility audit.
"""
from html.parser import HTMLParser
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parent

class PortfolioLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.anchors = []
        self.assets = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            assert attributes["id"] not in self.ids, "Duplicate HTML ID"
            self.ids.add(attributes["id"])
        if tag == "a" and "href" in attributes:
            self.anchors.append(attributes["href"])
        if tag == "script" and "src" in attributes:
            self.assets.append(attributes["src"])
        if tag == "link" and attributes.get("rel") == "stylesheet":
            self.assets.append(attributes["href"])

html = (ROOT / "index.html").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")
parser = PortfolioLinks()
parser.feed(html)
assert all(anchor[1:] in parser.ids for anchor in parser.anchors if anchor.startswith("#")), "Missing navigation target"
assert all((ROOT / asset).is_file() for asset in parser.assets), "Missing static asset"
portfolio_title = "CAD Application Support & Engineering Systems Portfolio"
assert portfolio_title in readme, "Missing README portfolio title"
assert f"<h1>{escape(portfolio_title)}</h1>" in html, "Missing website portfolio title"
assert {"cad-support", "change-control", "bom-reconciliation", "manufacturing"} <= parser.ids
assert "synthetic" in readme.lower()
assert not re.search(r'<a[^>]+href="#[^"]+"[^>]*>\s*</a>', html), "Empty navigation link"
featured = (
    "Creo-CAD-Application-Support-Toolkit",
    "Engineering-Change-Revision-Tracker",
    "Engineering-BOM-Validation-System",
    "Transformer-BOM-Quality-Analytics",
    "Manufacturing-Station-Capacity-Simulation",
    "Manufacturing-Scrap-Rate-Analytics",
    "manufacturing-operations-analytics-portfolio",
)
for repo in featured:
    url = f"https://github.com/YSayaovong/{repo}"
    assert url in parser.anchors and url in readme, f"Missing featured project: {repo}"
print("Local assets, anchors, and featured project links verified.")

"""Check local portfolio assets, anchor targets, and role alignment.

This is a local structure check, not a remote-link or accessibility audit.
"""
from html.parser import HTMLParser
from pathlib import Path
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
assert "ENGINEERING SYSTEMS" in readme.upper()
assert "CAD APPLICATION SUPPORT" in readme.upper()
assert "Engineering Systems" in html
assert "CAD Application Support" in html
assert "planned" in readme.lower()
assert "synthetic" in readme.lower()
assert not re.search(r'<a[^>]+href="#[^"]+"[^>]*>\s*</a>', html), "Empty navigation link"
print("Local assets, anchors, and engineering systems positioning verified.")

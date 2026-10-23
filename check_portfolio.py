"""Check local portfolio assets, anchor targets and allowed public project links."""
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent
class Links(HTMLParser):
    def __init__(self):super().__init__();self.ids=set();self.links=[];self.assets=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if tag=='script' and 'src' in a:self.assets.append(a['src'])
        if tag=='link' and a.get('rel')=='stylesheet':self.assets.append(a['href'])
p=Links();p.feed((ROOT/'index.html').read_text())
assert all(link[1:] in p.ids for link in p.links if link.startswith('#'))
assert all((ROOT/asset).is_file() for asset in p.assets)
assert len(p.ids)==len(re.findall(r'id="([^"]+)"',(ROOT/'index.html').read_text())), 'Duplicate HTML IDs'
for link in p.links:
    assert 'Hmong-Education' not in link and 'Regulatory-Document' not in link, 'Outdated/private project link'
assert 'DATA ANALYST' in (ROOT/'README.md').read_text().upper()
assert 'Data Analyst' in (ROOT/'index.html').read_text()
print('Portfolio anchors, local assets and analyst direction validated; remote URLs are not network-tested.')

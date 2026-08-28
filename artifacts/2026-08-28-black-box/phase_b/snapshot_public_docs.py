"""Fetch only the explicitly selected public user-documentation pages below.

No crawl, repository code, developer documentation, or implementation is read.
"""
import datetime as dt
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import urllib.request

BASE = "https://cu-esiil.github.io/cubedynamics/"
PAGES = {
    "nouns": "library/",
    "sources": "library/sources/",
    "verbs": "reference/verbs/",
    "callables": "reference/verbs/a-z/",
    "pipe": "api/pipe/",
    "data": "api/data/",
    "custom_nouns": "extending/custom_nouns/",
    "custom_verbs": "extending/custom_verbs/",
    "learn": "learn/",
}

class Article(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.parts, self.links, self.tables = [], [], []
        self.table = self.row = self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "article":
            self.active = True
        if not self.active:
            return
        attrs = dict(attrs)
        if tag in {"p", "h1", "h2", "h3", "li", "pre", "tr", "br"}:
            self.parts.append("\n")
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "table": self.table = []
        if tag == "tr": self.row = []
        if tag in {"td", "th"}: self.cell = []

    def handle_endtag(self, tag):
        if tag == "article": self.active = False
        if tag in {"td", "th"} and self.row is not None and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        if tag == "tr" and self.table is not None:
            self.table.append(self.row)
        if tag == "table" and self.table is not None:
            self.tables.append(self.table)
            self.table = None

    def handle_data(self, text):
        if self.active: self.parts.append(text)
        if self.cell is not None: self.cell.append(text)

output = Path(__file__).parent / "public_docs"
output.mkdir(exist_ok=True)
records = []
for name, path in PAGES.items():
    record = {"name": name, "url": BASE + path, "timestamp": dt.datetime.now(dt.timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(BASE + path, headers={"User-Agent": "CubeDynamics-public-acceptance/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
            record.update(status=response.status, resolved_url=response.url, headers=dict(response.headers))
        (output / f"{name}.html").write_bytes(raw)
        parser = Article()
        parser.feed(raw.decode("utf-8"))
        (output / f"{name}.txt").write_text("".join(parser.parts))
        record.update(sha256=hashlib.sha256(raw).hexdigest(), tables=parser.tables, links=parser.links)
    except Exception as exc:
        record.update(status="failed", error=f"{type(exc).__name__}: {exc}")
    records.append(record)
    print(json.dumps({key: record[key] for key in ("name", "url", "status")}))
(output / "manifest.json").write_text(json.dumps(records, indent=2) + "\n")

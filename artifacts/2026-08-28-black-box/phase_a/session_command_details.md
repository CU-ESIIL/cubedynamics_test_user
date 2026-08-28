# Exact direct-fetch and extraction commands (A-010)

The three fetches ran independently with approved network access. Results and URLs are recorded in `public_docs/direct_fetch_results.json`.

```sh
curl -L --fail --max-time 30 https://cu-esiil.github.io/cubedynamics/getting_started/install/ -D artifacts/2026-08-28-black-box/phase_a/public_docs/install.headers -o artifacts/2026-08-28-black-box/phase_a/public_docs/install.html
curl -L --fail --max-time 30 https://cu-esiil.github.io/cubedynamics/quickstart/ -D artifacts/2026-08-28-black-box/phase_a/public_docs/quickstart.headers -o artifacts/2026-08-28-black-box/phase_a/public_docs/quickstart.html
curl -L --fail --max-time 30 https://raw.githubusercontent.com/CU-ESIIL/cubedynamics/main/README.md -D artifacts/2026-08-28-black-box/phase_a/public_docs/readme.headers -o artifacts/2026-08-28-black-box/phase_a/public_docs/readme.md
```

The following standard-library extraction only reads the downloaded public website HTML, not package implementation:

```python
from html.parser import HTMLParser
from pathlib import Path
class MainText(HTMLParser):
    def __init__(self): super().__init__(); self.inarticle=False; self.out=[]
    def handle_starttag(self,t,a):
        if t=='article':self.inarticle=True
        if self.inarticle and t in ['p','h1','h2','h3','li','pre','tr','br']:self.out.append('\n')
    def handle_endtag(self,t):
        if t=='article':self.inarticle=False
    def handle_data(self,d):
        if self.inarticle:self.out.append(d)
for name in ['install','quickstart']:
    p=Path('artifacts/2026-08-28-black-box/phase_a/public_docs')/(name+'.html'); h=MainText(); h.feed(p.read_text()); text=''.join(h.out); p.with_suffix('.txt').write_text(text); print(name+':\n'+text)
```

Pre-freeze check: parsed all Phase A JSON files, confirmed A-001 through A-011 occur sequentially, and ran `git diff --check -- reports/naive_session.md artifacts/2026-08-28-black-box/phase_a`; all passed. File hashing is in `public_doc_snapshot_manifest.json`. The coordinator performs the actual evidence freeze.

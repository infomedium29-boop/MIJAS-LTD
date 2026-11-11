"""Creates minimal public Cloudflare Pages artifact dist/ without sources or private docs.
Cloudflare Pages build command: python3 tools/build.py && python3 tools/publish.py
Cloudflare Pages output directory: dist
Serverless functions are loaded from repo-root functions/ by Cloudflare Pages.
"""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir(parents=True)
PAGES=['o-nama','usluge','projekti','kontakt','politika-privatnosti','uvjeti-koristenja','404']
for d in PAGES:
 shutil.copytree(ROOT/d,OUT/d)
for d in ['assets']:
 shutil.copytree(ROOT/d,OUT/d)
for file in ['index.html','404.html','_headers','_redirects','robots.txt','sitemap.xml']:
 src=ROOT/file
 if src.exists():shutil.copy2(src,OUT/file)
restricted=['tools','README.md','ZAVRSNA-PROVJERA.md','.git']
assert not any((OUT/x).exists() for x in restricted)
print(f'Public artifact: {OUT} ({len(list(OUT.rglob("*.html")))} HTML files, no source or docs)')

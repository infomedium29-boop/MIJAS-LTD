"""Finalize SEO for confirmed domain after client's written approval.
Run `python tools/prepare_production.py https://example.hr` and commit changes.
"""
from pathlib import Path
from urllib.parse import urlparse
import sys,re,html
root=Path(__file__).resolve().parents[1]
if len(sys.argv)!=2:
 raise SystemExit('Usage: python tools/prepare_production.py https://your-confirmed-domain.hr')
origin=sys.argv[1].strip().rstrip('/')
u=urlparse(origin)
if u.scheme!='https' or not u.hostname or '.' not in u.hostname or u.hostname.endswith(('.example','.invalid','.test')):
 raise SystemExit('Provide confirmed HTTPS production domain, e.g. https://actual-domain.hr')
paths=[]
for p in root.rglob('index.html'):
 if p.parts and 'tools' in p.parts: continue
 path='/' if p.parent==root else '/'+p.parent.relative_to(root).as_posix()+'/'
 if path=='/404/': continue
 paths.append(path)
 for target in (p,):
  content=target.read_text(encoding='utf-8')
  content=re.sub(r'(<link rel="canonical" href=")[^"]+("\s*>)',lambda m:m[1]+html.escape(origin+path,quote=True)+m[2],content)
  content=content.replace('<meta property="og:image" content="/assets/images/hero.avif">',f'<meta property="og:image" content="{html.escape(origin,quote=True)}/assets/images/og-cover.jpg">')
  content=content.replace('<meta name="twitter:card" content="summary_large_image">',f'<meta property="og:url" content="{html.escape(origin+path,quote=True)}"><meta name="twitter:card" content="summary_large_image">')
  target.write_text(content,encoding='utf-8')
root.joinpath('404.html').write_text(root.joinpath('404/index.html').read_text(encoding='utf-8'),encoding='utf-8')
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{html.escape(origin+p)}</loc></url>\n' for p in sorted(paths))+'</urlset>\n'
(root/'sitemap.xml').write_text(xml,encoding='utf-8')
(root/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+origin+'/sitemap.xml\n',encoding='utf-8')
headers=(root/'_headers').read_text(encoding='utf-8').replace('  X-Robots-Tag: noindex, nofollow\n','')
(root/'_headers').write_text(headers,encoding='utf-8')
print(f'Production SEO prepared for {origin} ({len(paths)} URLs). Verify before launch.')

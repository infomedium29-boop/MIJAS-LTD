from pathlib import Path
from bs4 import BeautifulSoup
from collections import Counter
import re
ROOT=Path(__file__).resolve().parents[1]
html_files=sorted(ROOT.rglob('index.html'))
errors=[]; external=set(); title_set=[];desc_set=[]
for html in html_files:
 soup=BeautifulSoup(html.read_text(encoding='utf-8'),'html.parser')
 path='/'+html.parent.relative_to(ROOT).as_posix()+'/' if html.parent!=ROOT else '/'
 if len(soup.select('h1'))!=1:errors.append((path,'H1 count '+str(len(soup.select('h1')))))
 if not soup.title: errors.append((path,'no title'))
 else:title_set.append(soup.title.text)
 if not soup.select_one('meta[name="description"]'): errors.append((path,'no meta desc'))
 else:desc_set.append(soup.select_one('meta[name="description"]').get('content'))
 for tag in soup.find_all(['a','link','script','img']):
  att='href' if tag.name in ('a','link') else 'src'
  uri=tag.get(att,'')
  if not uri or uri.startswith(('#','mailto:','tel:','data:','javascript:')):continue
  if uri.startswith(('https://','http://')):
   external.add(uri);continue
  if uri.startswith('/'):
   clean_uri=uri.split('#',1)[0].split('?',1)[0]
   dest=ROOT/clean_uri.strip('/')
   if clean_uri.endswith('/'):
    dest=dest/'index.html'
   if clean_uri.startswith('/api/') or clean_uri=='/sitemap.xml':continue
   if not dest.exists():errors.append((path,tag.name,uri,'MISSING'))
   elif '#' in uri and tag.name=='a':
    fragment=uri.split('#',1)[1]
    if fragment and not BeautifulSoup(dest.read_text(encoding='utf-8'),'html.parser').find(id=fragment):errors.append((path,uri,'TARGET ID MISSING'))
 for img in soup.find_all('img'):
  if img.get('alt') is None: errors.append((path,'alt missing',img.get('src')))
 if soup.select_one('link[rel="canonical"]') is None: errors.append((path,'no canonical'))
 if soup.select_one('meta[property="og:title"]') is None: errors.append((path,'no og:title'))
 if soup.select_one('meta[property="og:image"]') is None: errors.append((path,'no og:image'))
 if soup.select_one('main') is None: errors.append((path,'no main'))
if len(title_set)!=len(set(title_set)):errors.append('DUPLICATE TITLES '+str(Counter(title_set)))
if len(desc_set)!=len(set(desc_set)):errors.append('DUPLICATE DESCRIPTIONS '+str(Counter(desc_set)))
print(f'HTML routes: {len(html_files)}; unique titles: {len(set(title_set))}; unique descriptions: {len(set(desc_set))}; external links: {len(external)}')
for e in external:print('External:',e)
print('ERRORS:',len(errors))
for e in errors:print('ERROR:',e)
if errors:raise SystemExit(1)

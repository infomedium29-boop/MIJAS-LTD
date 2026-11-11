"""Cloudflare Pages build entry point: python3 tools/deploy.py
Set PUBLIC_SITE_URL in Cloudflare Pages *production* environment after approval.
Set PRODUCTION_BRANCH if main is not the release branch.
"""
import os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(*args):subprocess.run([sys.executable,*args],cwd=ROOT,check=True)
run('tools/build.py')
url=os.environ.get('PUBLIC_SITE_URL','').strip()
branch=os.environ.get('CF_PAGES_BRANCH','').strip()
prod=os.environ.get('PRODUCTION_BRANCH','main').strip()
if url and branch==prod:
 run('tools/prepare_production.py',url)
else:
 print('DEMO / preview: search-engine indexing stays blocked. No confirmed production domain.')
run('tools/publish.py')

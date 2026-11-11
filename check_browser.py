from pathlib import Path
import http.server, socketserver, threading, time, json
from playwright.sync_api import sync_playwright
root=Path('/mnt/data/mijas_float_contact/dist')
class Server(socketserver.ThreadingMixIn,http.server.HTTPServer):
 allow_reuse_address=True
 daemon_threads=True
handler=lambda *a,**kw: http.server.SimpleHTTPRequestHandler(*a,directory=str(root),**kw)
server=Server(('127.0.0.1',0),handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'
errs=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 for w,h in [(390,844),(320,720),(1440,900)]:
  context=browser.new_context(viewport={'width':w,'height':h},is_mobile=(w<720),device_scale_factor=1)
  page=context.new_page()
  page.on('pageerror',lambda exc: errs.append(str(exc)))
  page.goto(base+'/',wait_until='networkidle',timeout=30000)
  page.evaluate("sessionStorage.setItem('mijas-intro-played','1');localStorage.setItem('mijas-cookie-consent-v1',JSON.stringify({analytics:false,updatedAt:Date.now()}))")
  page.reload(wait_until='networkidle')
  page.locator('#brand-intro').wait_for(state='detached',timeout=5000)
  a=page.locator('.floating-contact__button')
  assert a.count()==2,(w,a.count())
  assert a.nth(0).get_attribute('href')=='tel:+385915090790'
  assert a.nth(1).get_attribute('href')=='https://wa.me/385915090790'
  r=a.nth(0).bounding_box()
  r2=a.nth(1).bounding_box()
  print('VIEWPORT',w,h,'floating_boxes',r,r2,'scrollWidth',page.evaluate('document.documentElement.scrollWidth'))
  assert r['x']>w/2 and r['y']>h/2
  assert r2['y']>r['y']
  assert page.evaluate('document.documentElement.scrollWidth')<=w+2
  if w==390:
   page.screenshot(path='/mnt/data/mijas_float_contact/mobile_floating_buttons.png',full_page=False)
   page.evaluate('window.scrollTo(0,1200)')
   page.wait_for_timeout(300)
   rscroll=a.nth(0).bounding_box()
   print('SCROLL fixed x,y:',rscroll['x'],rscroll['y'])
   assert abs(rscroll['y']-r['y'])<2
   page.goto(base+'/kontakt/',wait_until='networkidle')
   assert page.locator('.floating-contact__button').count()==2
   page.screenshot(path='/mnt/data/mijas_float_contact/contact_floating_buttons.png',full_page=False)
  if w==1440:page.screenshot(path='/mnt/data/mijas_float_contact/desktop_floating_buttons.png',full_page=False)
  context.close()
 browser.close()
server.shutdown()
print('PAGEERRORS',errs)
assert not errs

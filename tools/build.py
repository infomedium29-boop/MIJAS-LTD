from pathlib import Path
from html import escape
import json, textwrap, re, hashlib
ROOT=Path(__file__).resolve().parents[1]
STYLE_REV=hashlib.sha256((ROOT/'assets/css/style.css').read_bytes()).hexdigest()[:12]
JS_REV=hashlib.sha256((ROOT/'assets/js/main.js').read_bytes()).hexdigest()[:12]
S=[
('vodoinstalacije','Vodoinstalacije','Planiranje, izvedba i prilagodba vodovodnih instalacija za različite vrste prostora.','Vodovodne instalacije','Instalacije koje prate potrebe svakog prostora.','Ugradnja novih vodovodnih vodova, zamjena dotrajalih instalacija i priprema priključaka za sanitarne uređaje. Sadržaj se u završnoj verziji prilagođava stvarnom opsegu usluga.',['Razvod tople i hladne vode','Zamjena postojećih cjevovoda','Priprema priključaka za sanitarije','Instalacije tijekom novogradnje i adaptacije'],'equipment.avif'),
('grijanje','Sustavi grijanja','Instalaterska rješenja za ugodnu temperaturu i funkcionalnost prostora.','Grijanje i toplinski sustavi','Pouzdana toplina, promišljena izvedba.','Od pripreme instalacija do prilagodbe postojećih sustava, pristup se definira prema tehničkim zahtjevima objekta.',['Razvod instalacija grijanja','Radijatorski sustavi','Priprema za podno grijanje','Modernizacija postojećih instalacija'],'floor-heating.avif'),
('klimatizacija','Klimatizacija','Tehnička rješenja za ugodan boravak i rad tijekom cijele godine.','Klimatizacijski sustavi','Ugodna klima, svaki dan.','Odabir pristupa i rasporeda instalacija treba odgovarati namjeni i karakteristikama prostora. Izvedba se dogovara nakon procjene projekta.',['Priprema instalacijskih vodova','Ugradnja klimatizacijskih sustava','Prilagodba postojećih instalacija','Rješenja za stambene i poslovne objekte'],'pipework.avif'),
('odvodnja','Odvodnja i kanalizacija','Izvedba i prilagodba sustava odvodnje i sanitarnih instalacija.','Odvodnja i kanalizacija','Sustavi koje ne primjećujete. I tako treba biti.','Dobro projektiran i izveden sustav odvodnje važan je dio svakog funkcionalnog objekta.',['Odvodni vodovi u objektima','Prilagodba postojećih priključaka','Priprema sanitarnih odvodnih instalacija','Instalacije tijekom adaptacija'],'details.avif'),
('sanitarne-instalacije','Sanitarne instalacije','Priprema, povezivanje i zamjena instalacija u kupaonicama i kuhinjama.','Sanitarne instalacije','Detalji od kojih nastaje funkcionalan prostor.','Sanitarne instalacije povezuju svakodnevnu udobnost s tehnički kvalitetnom izvedbom.',['Priprema priključaka za kupaonice','Priključci za kuhinje','Prilagodba sanitarnih vodova','Zamjena tijekom renovacije'],'equipment.avif'),
('adaptacije-i-odrzavanje','Adaptacije i održavanje','Prilagodba postojećih instalacija tijekom obnove i uređenja prostora.','Adaptacije instalacija','Postojećem prostoru dajte novu funkciju.','Tijekom renovacija često su potrebne prilagodbe vodovodnih, odvodnih i toplinskih instalacija.',['Zamjena dotrajalih instalacija','Preinake vodovoda i odvodnje','Prilagodba rasporeda priključaka','Priprema sustava za nove uređaje'],'pipework.avif')]

# Radni katalog usluga; klijent potvrđuje opseg prije objave.
S = [(*s[:5], {
 'vodoinstalacije':'Vodovodni razvod uključuje cijevi tople i hladne vode, zaporne ventile te priključke za kuhinju i kupaonicu.',
 'grijanje':'U instalacijama grijanja razlikuju se podni, radijatorski i kombinirani sustavi. Važni su izvor topline i raspored prostorija.',
 'klimatizacija':'Za klimatizaciju su važni položaji unutarnje i vanjske jedinice, trasa vodova i odvod kondenzata.',
 'odvodnja':'Odvodni vodovi povezuju sanitarne uređaje s kanalizacijskim sustavom. Položaj priključaka i potreban pad cijevi važni su za izvedbu.',
 'sanitarne-instalacije':'Kupaonica i kuhinja zahtijevaju precizno postavljene priključke vode i odvodnje prema rasporedu sanitarija i uređaja.',
 'adaptacije-i-odrzavanje':'Kod obnove kupaonice ili kuhinje provjeravaju se postojeći vodovi, zaporni ventili i mjesta budućih priključaka.'
 }[s[0]], {
 'vodoinstalacije':['Razvod tople i hladne vode','PPR i bakrene cijevi','Zamjena postojećih vodova','Priključci za kuhinju i kupaonicu','Priprema vodovoda u novogradnji'],
 'grijanje':['Razvod radijatorskog grijanja','Cijevi podnog grijanja','Priključci uz postojeći kotao','Kombinirani sustavi grijanja'],
 'klimatizacija':['Položaj unutarnje i vanjske jedinice','Instalacijski vodovi i odvod kondenzata','Priprema u fazi gradnje'],
 'odvodnja':['Odvodni vodovi kupaonice i kuhinje','Prilagodba položaja priključaka','Pad i trasa odvodnih cijevi'],
 'sanitarne-instalacije':['Priključci za umivaonik i WC','Priključci za tuš i kadu','Priključci sudopera i perilica','Zamjena vodova pri adaptaciji'],
 'adaptacije-i-odrzavanje':['Provjera postojećih vodova','Zamjena dotrajalih cijevi','Premještanje priključaka','Priprema za novu sanitarnu opremu','Prilagodba kupaonice ili kuhinje']
 }[s[0]], s[7]) for s in S]

# Navedene vrijednosti objavljuju se samo kad ih klijent izričito potvrdi.
DETAILS_FILE = ROOT/'tools/business_details.json'
DETAILS = json.loads(DETAILS_FILE.read_text(encoding='utf-8')) if DETAILS_FILE.exists() else {}
PHONE = str(DETAILS.get('public_phone') or '').strip()
EMAIL = str(DETAILS.get('public_email') or '').strip()
WHATSAPP = str(DETAILS.get('public_whatsapp') or '').strip()
BUSINESS_HOURS = str(DETAILS.get('public_working_hours') or '').strip()
SERVICE_AREA = [str(x).strip() for x in DETAILS.get('confirmed_service_towns',[]) if str(x).strip()]
PHONE_TEL = ''.join(ch for ch in PHONE if ch in '+0123456789')
WA_NUM = ''.join(ch for ch in WHATSAPP if ch.isdigit())
# Odobren broj za stalno vidljive plutajuće gumbe; odvojen od poslovnih kontakata.
FLOAT_PHONE = str(DETAILS.get('floating_phone') or '').strip()
FLOAT_WA = str(DETAILS.get('floating_whatsapp') or '').strip()
FLOAT_TEL = ''.join(ch for ch in FLOAT_PHONE if ch in '+0123456789')
FLOAT_WA_NUM = ''.join(ch for ch in FLOAT_WA if ch.isdigit())
FLOAT_WA_CALL_URL = str(DETAILS.get('floating_whatsapp_call_url') or '').strip()

def floating_contacts():
 if not FLOAT_TEL and not FLOAT_WA_NUM:return ''
 items=[]
 if FLOAT_TEL:
  items.append(f'''<a class="floating-contact__button floating-contact__button--phone" href="tel:{FLOAT_TEL}" aria-label="Nazovite MIJAS LTD na {escape(FLOAT_PHONE)}" title="Običan poziv: {escape(FLOAT_PHONE)}">{icon('phone').replace('<svg ', '<svg width="25" height="25" ',1)}</a>''')
 if FLOAT_WA_NUM:
  # Službeni WhatsApp wa.me otvara razgovor. Za direktan poziv potreban je provjereni poslovni call link.
  wa_url = FLOAT_WA_CALL_URL if FLOAT_WA_CALL_URL.startswith('https://') else f'https://wa.me/{FLOAT_WA_NUM}'
  items.append(f'''<a class="floating-contact__button floating-contact__button--whatsapp" href="{escape(wa_url,quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Otvorite WhatsApp za razgovor ili poziv na {escape(FLOAT_WA)}" title="WhatsApp: {escape(FLOAT_WA)}"><svg class="floating-contact__whatsapp-icon" width="29" height="29" viewBox="0 0 32 32" aria-hidden="true" fill="currentColor"><path d="M16.02 3.2C9.1 3.2 3.45 8.83 3.44 15.75c0 2.2.58 4.35 1.68 6.25L3.3 28.7l6.87-1.8c1.84 1 3.92 1.53 6.05 1.53h.01c6.92 0 12.57-5.64 12.58-12.56.01-3.36-1.3-6.52-3.67-8.9a12.45 12.45 0 0 0-9.12-3.77zm.2 23.1c-1.88 0-3.72-.5-5.33-1.46l-.38-.22-3.97 1.04 1.06-3.87-.24-.4a10.47 10.47 0 0 1-1.61-5.57c.01-5.77 4.71-10.47 10.49-10.47a10.4 10.4 0 0 1 7.42 3.08 10.4 10.4 0 0 1 3.07 7.43c0 5.78-4.71 10.48-10.5 10.48zm5.76-7.86c-.31-.16-1.87-.92-2.16-1.02-.29-.11-.5-.16-.71.16-.21.32-.82 1.02-1 1.23-.18.21-.36.24-.67.08-.31-.15-1.32-.48-2.51-1.55-.92-.82-1.54-1.83-1.72-2.14-.18-.32-.02-.49.14-.65.14-.14.31-.37.47-.55.16-.18.21-.31.32-.52.1-.21.05-.39-.03-.55-.08-.16-.71-1.71-.97-2.35-.26-.62-.52-.54-.71-.55l-.61-.01a1.16 1.16 0 0 0-.84.39c-.29.32-1.1 1.08-1.1 2.63 0 1.55 1.13 3.05 1.29 3.26.16.21 2.22 3.39 5.38 4.75.75.32 1.34.52 1.8.66.76.24 1.45.21 2 .13.61-.09 1.87-.76 2.13-1.5.26-.73.26-1.36.18-1.49-.08-.13-.29-.21-.61-.37z"/></svg></a>''')
 return '<aside class="floating-contact" aria-label="Brzi kontakt">'+''.join(items)+'</aside>'

def contact_button(css='btn btn--copper'):
 if PHONE_TEL:
  return f'<a href="tel:{PHONE_TEL}" class="{css}">{icon("phone")} Nazovite {escape(PHONE)}</a>'
 return f'<a href="/kontakt/#upit" class="{css}">Pošaljite upit {icon("arrow")}</a>'

def public_contacts():
 parts=[]
 if PHONE_TEL:parts.append(f'<div class="contact-info-item">{icon("phone")}<div><strong>Telefon</strong><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></div></div>')
 if EMAIL and '@' in EMAIL:parts.append(f'<div class="contact-info-item">{icon("file")}<div><strong>E-mail</strong><a href="mailto:{escape(EMAIL,quote=True)}">{escape(EMAIL)}</a></div></div>')
 if WA_NUM:parts.append(f'<p><a class="text-link" href="https://wa.me/{WA_NUM}" target="_blank" rel="noopener noreferrer">WhatsApp {icon("arrow-up-right")}</a></p>')
 if BUSINESS_HOURS:parts.append(f'<p><strong>Radno vrijeme:</strong> {escape(BUSINESS_HOURS)}</p>')
 return ''.join(parts)

SERVICE_URL=lambda s:'/usluge/'+s[0]+'/'
I={
'arrow':'<path d="M5 12h14m-6-6 6 6-6 6"/>',
'arrow-up-right':'<path d="M7 17 17 7M8 7h9v9"/>',
'chevron-down':'<path d="m6 9 6 6 6-6"/>',
'plus':'<path d="M12 5v14m-7-7h14"/>',
'menu':'<path d="M4 7h16M4 12h16M4 17h16"/>',
'close':'<path d="M18 6 6 18M6 6l12 12"/>',
'location':'<path d="M20 10c0 5-8 11-8 11S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
'check':'<path d="m5 12 4 4L19 6"/>',
'phone':'<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.2 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72l.41 2.81a2 2 0 0 1-.57 1.71L7.1 10.1a16 16 0 0 0 6 6l1.86-1.85a2 2 0 0 1 1.71-.57l2.81.41A2 2 0 0 1 22 16.92Z"/>',
'droplet':'<path d="M12 22a8 8 0 0 0 8-8c0-4.5-8-12-8-12S4 9.5 4 14a8 8 0 0 0 8 8Z"/>',
'heat':'<path d="M8 3v3m8-3v3M6 10v8m4-8v8m4-8v8m4-8v8M3 9h18M3 19h18"/>',
'snow':'<path d="M12 2v20M4.93 4.93l14.14 14.14M2 12h20M4.93 19.07 19.07 4.93"/>',
'pipe':'<path d="M5 3v8a5 5 0 0 0 5 5h9M5 7h4m10 9v5M2 3h6M16 13h6"/>',
'bath':'<path d="M3 12h18v2a6 6 0 0 1-6 6H9a6 6 0 0 1-6-6v-2ZM7 12V5a2 2 0 0 1 4 0M6 22v-2m12 2v-2"/>',
'wrench':'<path d="M14 7a6 6 0 0 1-7 7l-5 5a2 2 0 0 0 3 3l5-5a6 6 0 0 0 7-7l-4 4-3-3 4-4Z"/>',
'shield':'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/>',
'layers':'<path d="m12 2 9 5-9 5-9-5 9-5Zm-9 10 9 5 9-5M3 17l9 5 9-5"/>',
'clipboard':'<rect x="5" y="4" width="14" height="18" rx="2"/><path d="M9 4v-2h6v2M9 12h6M9 16h6"/>',
'chat':'<path d="M21 11.5a8.5 8.5 0 0 1-8.5 8.5 9 9 0 0 1-4-.9L3 21l1.9-5.5A9 9 0 1 1 21 11.5Z"/>',
'arrow-left':'<path d="M19 12H5m6 6-6-6 6-6"/>',
'file':'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Zm0 0v6h6M8 13h8m-8 4h8"/>',
}
def icon(name, cls='icon'):
 return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round">{I[name]}</svg>'
def logo(light=False):
 return f'''<a class="brand {'brand--light' if light else ''}" href="/" aria-label="MIJAS LTD – početna"><svg class="brand-mark" width="51" height="44" viewBox="0 0 51 44" role="img" aria-label="Monogram M"><path d="M2 40 11.9 5 25.5 26.4 38.2 5 49 40" fill="none" stroke="currentColor" stroke-width="6.3" stroke-linecap="square" stroke-linejoin="miter"/><path d="m25.5 26.4 12.7-21.4 6.5 21.6" fill="none" stroke="#C78C55" stroke-width="6.3" stroke-linecap="square"/></svg><span class="brand-label">MIJAS <span>LTD</span><small>VODOVOD · GRIJANJE · KLIMA</small></span></a>''' 
def nav(active=''):
 links=[('Početna','/','home'),('O nama','/o-nama/','about'),('Usluge','/usluge/','services'),('Radovi','/projekti/','projects'),('Kontakt','/kontakt/','contact')]
 items=[]
 for name,url,key in links:
  if key=='services':
   drop=''.join(f'<a href="{SERVICE_URL(s)}">{escape(s[1])}</a>' for s in S)
   items.append(f'<div class="nav-service"><a class="nav-link {'is-active' if active==key else ''}" href="{url}">{name}</a><button class="nav-drop-toggle" aria-label="Otvori izbornik usluga" aria-expanded="false">{icon("chevron-down")}</button><div class="nav-drop">{drop}</div></div>')
  else:items.append(f'<a class="nav-link {'is-active' if active==key else ''}" href="{url}">{name}</a>')
 return f'''<header class="site-header {'site-header--home' if active=='home' else ''}" id="header"><div class="header-inner container-wide">{logo(True)}<nav class="main-nav" aria-label="Glavna navigacija">{''.join(items)}</nav>{contact_button('btn btn--copper header-cta')}{f'<a class="mobile-call-header" href="tel:{PHONE_TEL}" aria-label="Nazovite MIJAS LTD">{icon("phone")}</a>' if PHONE_TEL else ''}<button id="menu-toggle" class="menu-toggle" aria-expanded="false" aria-controls="mobile-nav" aria-label="Otvori navigaciju">{icon('menu')}<span></span></button></div></header><div class="mobile-nav" id="mobile-nav" aria-hidden="true"><nav aria-label="Mobilna navigacija">{''.join(f'<a href="{url}" class="{'is-active' if active==key else ''}">{name}{icon("arrow-up-right")}</a>' for name,url,key in links)}<div class="mobile-subnav">{''.join(f'<a href="{SERVICE_URL(s)}">{escape(s[1])}</a>' for s in S)}</div>{contact_button('btn btn--copper mobile-cta')}</nav></div>''' 
def footer():
 public=[]
 if PHONE_TEL:public.append(f'<a href="tel:{PHONE_TEL}">{escape(PHONE)}</a>')
 if EMAIL and '@' in EMAIL:public.append(f'<a href="mailto:{escape(EMAIL,quote=True)}">{escape(EMAIL)}</a>')
 return f'''<footer class="footer"><div class="container"><div class="footer-top"><div class="footer-brand">{logo(True)}<p>MIJAS LTD j.d.o.o., Širinec. Vodovod, odvodnja, grijanje i klimatizacija.</p></div><div class="footer-col"><span>STRANICE</span><a href="/">Početna</a><a href="/o-nama/">O nama</a><a href="/usluge/">Usluge</a><a href="/projekti/">Radovi</a></div><div class="footer-col"><span>USLUGE</span><a href="/usluge/vodoinstalacije/">Vodoinstalacije</a><a href="/usluge/grijanje/">Grijanje</a><a href="/usluge/klimatizacija/">Klimatizacija</a><a href="/usluge/odvodnja/">Odvodnja</a></div><div class="footer-col"><span>KONTAKT I PRAVILA</span>{''.join(public)}<a href="/kontakt/">Kontakt</a><a href="/politika-privatnosti/">Politika privatnosti</a><a href="/uvjeti-koristenja/">Uvjeti korištenja</a><button class="footer-link" id="cookie-settings">Postavke kolačića</button></div></div><div class="footer-bottom"><div><strong>MIJAS LTD j.d.o.o.</strong> <span>·</span> Širinec 36, 10314 Širinec, Hrvatska <span>·</span> OIB: 40827941362</div><div>© <span id="year">2026</span> MIJAS LTD. Sva prava pridržana.</div></div></div></footer>''' 
def cookie():
 return '''<div id="cookie-banner" class="cookie-banner" role="dialog" aria-label="Postavke kolačića" aria-modal="false" hidden><div class="cookie-inner"><div><p class="cookie-title" style="font-size:20px;letter-spacing:-.04em;margin:7px 0 6px;font-weight:700">Kolačići</p><p>Koristimo nužnu lokalnu pohranu za rad stranice. Neobaveznu analitiku uključujemo samo uz vašu privolu. <a href="/politika-privatnosti/">Saznajte više.</a></p><label class="cookie-options" hidden><input type="checkbox" id="analytics-choice"> Dopusti analitičke kolačiće</label></div><div class="cookie-actions"><button class="btn btn--copper" data-consent="accept">Prihvati sve</button><button class="btn btn--dark-outline" data-consent="reject">Odbij neobavezne</button><button class="btn btn--text" data-consent="settings">Postavke kolačića</button></div></div></div>''' 
def intro():
 letters=''.join(f'<span style="--letter:{idx}">{escape(ch) if ch!=' ' else '&nbsp;'}</span>' for idx,ch in enumerate('MIJAS LTD'))
 return f'''<div class="intro" id="brand-intro" aria-label="MIJAS LTD – uvodna animacija"><div class="intro-bg"></div><div class="intro-shade"></div><div class="intro-middle"><svg class="intro-mark" viewBox="0 0 120 90" aria-hidden="true" fill="none" stroke-linecap="square" stroke-linejoin="miter"><path class="intro-stroke" d="M10 80 28 14 59 57 86 14 108 80" stroke="#F4F5F3" stroke-width="9"/><path class="intro-gold" d="m59 57 27-43 14 40" stroke="#C78C55" stroke-width="9"/></svg><div class="intro-letters" aria-hidden="true">{letters}</div><span class="intro-tagline">INSTALACIJE <b>·</b> GRIJANJE <b>·</b> KLIMATIZACIJA</span><span class="intro-line"></span></div><button class="intro-skip" id="intro-skip">Preskoči uvod {icon('arrow')}</button></div>'''

def cta(title='Trebate ponudu?',subtitle='Napišite mjesto i vrstu radova u upitu.',variant='general'):
 return f'''<section class="contact-cta"><div class="contact-cta__glow"></div><div class="container contact-cta__inner"><div><h2>{escape(title)}</h2><p>{escape(subtitle)}</p></div>{contact_button()}</div></section>''' 
def page(title,desc,path,body,active='',hero=False,extra_class=''):
 # Zadržati kurziv samo u tri potvrđena glavna naslova.
 def normalize_heading(match):
  level, attrs, content = match.group(1),match.group(2),match.group(3)
  keep = level=='1' and path in ('/','/o-nama/','/kontakt/')
  if not keep:content=content.replace('<em>','').replace('</em>','')
  return f'<h{level}{attrs}>{content}</h{level}>'
 body=re.sub(r'<h([1-6])([^>]*)>(.*?)</h\1>',normalize_heading,body, flags=re.S)
 # relative canonical supported for demo; deploy script replaces with absolute
 safe_title=escape(title+' | MIJAS LTD')
 desc=escape(desc)
 og='/assets/images/og-cover.jpg'
 full='''<!doctype html><html lang="hr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#112634"><meta name="description" content="'''+desc+'''"><title>'''+safe_title+'''</title><link rel="canonical" href="'''+path+'''"><meta property="og:type" content="website"><meta property="og:locale" content="hr_HR"><meta property="og:site_name" content="MIJAS LTD"><meta property="og:title" content="'''+safe_title+'''"><meta property="og:description" content="'''+desc+'''"><meta property="og:image" content="'''+og+'''"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/svg+xml" href="/assets/images/favicon.svg"><link rel="preload" as="image" type="image/avif" href="/assets/images/hero.avif" fetchpriority="high"><link rel="stylesheet" href="/assets/css/style.css?v=20261112fix1"><script src="/assets/js/config.js" defer></script><script src="/assets/js/main.js?v=20261112fix1" defer></script><script type="application/ld+json">'''+json.dumps({'@context':'https://schema.org','@type':['Plumber','HVACBusiness'],'name':'MIJAS LTD j.d.o.o.','legalName':'Mijas LTD j.d.o.o.','taxID':'40827941362','address':{'@type':'PostalAddress','streetAddress':'Širinec 36','postalCode':'10314','addressLocality':'Širinec','addressCountry':'HR'}, **({'telephone':PHONE_TEL} if PHONE_TEL else {}),**({'email':EMAIL} if EMAIL else {}),**({'areaServed':SERVICE_AREA} if SERVICE_AREA else {}),**({'openingHours':BUSINESS_HOURS} if BUSINESS_HOURS else {})},ensure_ascii=False)+'''</script></head><body class="'''+('home ' if hero else 'inner ')+extra_class+'''">'''+(intro() if hero else '')+'''<a class="skip-link" href="#main">Preskoči na sadržaj</a>'''+nav(active)+'''<main id="main">'''+body+'''</main>'''+footer()+floating_contacts()+cookie()+'''</body></html>'''
 if not hero: full=full.replace('<link rel="preload" as="image" type="image/avif" href="/assets/images/hero.avif" fetchpriority="high">','')
 p=ROOT/path.strip('/')/'index.html' if path!='/' else ROOT/'index.html'
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(full,encoding='utf-8')
 print('Created',p.relative_to(ROOT))

def title_intro(top,h1,desc):
 return f'''<section class="page-hero"><div class="page-hero__geometry"></div><div class="container"><h1>{h1}</h1><p>{desc}</p></div></section>'''

def service_card(s,n):
 sl,name,desc,*_=s
 ic=['droplet','heat','snow','pipe','bath','wrench'][n]
 return f'''<a href="{SERVICE_URL(s)}" class="service-card reveal"><div class="service-card__top"><span class="service-card__number">0{n+1}</span><span class="service-card__icon">{icon(ic)}</span></div><h3>{escape(name)}</h3><p>{escape(desc)}</p><span class="service-card__more">Više o usluzi {icon('arrow-up-right')}</span></a>'''

def faq_html(items):
 return '<div class="faq-list">'+''.join(f'<details class="faq-item"><summary>{escape(q)}{icon("plus")}</summary><p>{escape(a)}</p></details>' for q,a in items)+'</div>'

# Sadržaj stranica – urednički prilagođen konkretnim pitanjima kupaca, bez nepotvrđenih obećanja.
HOME_FAQ = [
 ('Gdje se nalazi sjedište MIJAS LTD-a?', 'Sjedište tvrtke je na adresi Širinec 36, 10314 Širinec, u općini Križ. Mjesto izvođenja radova navedite u upitu.'),
 ('Koje podatke treba poslati za ponudu?', 'Navedite mjesto radova, vrstu objekta i što treba napraviti. Za zamjenu cijevi napišite i radi li se o kupaonici, kuhinji ili cijelom objektu.'),
 ('Mogu li poslati upit za adaptaciju stana?', 'U obrascu odaberite „Adaptacije i održavanje”, navedite grad te opišite postojeće instalacije i željene izmjene.'),
 ('Kako mogu poslati upit za grijanje?', 'Odaberite „Sustavi grijanja” i napišite radi li se o podnom grijanju, radijatorima ili zamjeni dijela sustava.'),
 ('Kako ću znati je li poruka poslana?', 'Nakon uspješnog slanja obrazac prikazuje potvrdu. Ako sustav slanja nije aktiviran, prikazat će se poruka da upit nije poslan.')
]
SERVICE_FAQS={
 'vodoinstalacije':[
  ('Što trebam navesti za zamjenu postojećih cijevi?', 'Napišite radi li se o stanu ili kući, koje su prostorije zahvaćene te jesu li postojeće cijevi vidljive ili skrivene u zidu.'),
  ('Koja je razlika između PPR i bakrenih cijevi?', 'PPR je plastični sustav koji se spaja zavarivanjem, a bakrene cijevi izrađuju se od metala. Odabir ovisi o namjeni i uvjetima ugradnje.'),
  ('Može li se pripremiti priključak za novu kuhinju?', 'U upitu navedite položaj sudopera i perilice te priložite skicu ili fotografiju postojeće kuhinje ako je imate.')],
 'grijanje':[
  ('Koja je razlika između podnog i radijatorskog grijanja?', 'Podno grijanje predaje toplinu preko velike površine poda, dok radijatori griju prostor putem zasebnih grijaćih tijela.'),
  ('Što trebam navesti ako već imam kotao?', 'Navedite model postojećeg kotla, približnu površinu objekta i želite li radijatore, podno grijanje ili kombinaciju.'),
  ('Zašto je važna visina poda kod podnog grijanja?', 'Cijevi, izolacija i estrih zauzimaju dio visine poda; taj podatak bitan je pri planiranju nove instalacije.')],
 'klimatizacija':[
  ('Koje informacije trebam poslati za klimu?', 'Pošaljite veličinu prostorije, kat objekta, položaj unutarnje i vanjske jedinice te mjesto izvođenja radova.'),
  ('Kada se priprema instalacija za klimu u novogradnji?', 'Položaj instalacijskih vodova uobičajeno se planira prije završnih zidarskih i fasaderskih radova.'),
  ('Imam vlastiti klima uređaj. Što navesti u upitu?', 'Napišite proizvođača i model uređaja te da je uređaj već kupljen. Mogućnost montaže treba prethodno potvrditi.')],
 'odvodnja':[
  ('Zašto je pad odvodne cijevi važan?', 'Pravilan pad omogućuje otjecanje otpadne vode. Premali ili nepravilno izveden pad povećava mogućnost zastoja.'),
  ('Koje podatke trebam poslati za premještanje odvoda?', 'Napišite što se premješta, na koju udaljenost i u kojoj prostoriji. Fotografija postojećeg odvoda može pomoći.'),
  ('Je li za priključak na javnu kanalizaciju potrebna dokumentacija?', 'Uvjeti priključenja ovise o nadležnom isporučitelju vodnih usluga i lokalnim pravilima. Za ponudu navedite lokaciju i status priključka.')],
 'sanitarne-instalacije':[
  ('Što je potrebno za izmjenu rasporeda kupaonice?', 'Pošaljite skicu prostora i raspored WC-a, tuša, umivaonika te postojećih priključaka vode i odvoda.'),
  ('Kako pripremiti upit za novu kuhinju?', 'Navedite gdje će se nalaziti sudoper, perilica posuđa i ostali uređaji koji trebaju vodu ili odvod.'),
  ('Trebam li dostaviti model sanitarne opreme?', 'Ako je oprema odabrana, korisno je priložiti dimenzije i upute za ugradnju radi planiranja položaja priključaka.')],
 'adaptacije-i-odrzavanje':[
  ('Što pripremiti prije pregleda instalacija?', 'Pripremite podatke o starosti objekta, položaju glavnog ventila i opis problema. Korisne su fotografije pristupa cijevima.'),
  ('Može li se preurediti samo jedna prostorija?', 'U upitu navedite radi li se o kupaonici ili kuhinji i koji dio postojećih instalacija želite promijeniti.'),
  ('Treba li prije adaptacije zatvoriti dovod vode?', 'Kod zahvata na vodovodnim cijevima dovod vode mora se sigurno zatvoriti. Točan postupak ovisi o instalaciji i opsegu radova.')]
}
SERVICE_H1={
 'vodoinstalacije':'Vodoinstalacije i zamjena cijevi',
 'grijanje':'Instalacije grijanja i podno grijanje',
 'klimatizacija':'Ugradnja klima uređaja',
 'odvodnja':'Odvodnja i kanalizacija',
 'sanitarne-instalacije':'Sanitarne instalacije za kupaonice i kuhinje',
 'adaptacije-i-odrzavanje':'Preinake instalacija kod adaptacija',
}
SERVICE_H2={
 'vodoinstalacije':'Vodoinstalaterski radovi',
 'grijanje':'Radovi na sustavima grijanja',
 'klimatizacija':'Priprema i montaža klimatizacije',
 'odvodnja':'Odvodni vodovi i priključci',
 'sanitarne-instalacije':'Priključci u kupaonici i kuhinji',
 'adaptacije-i-odrzavanje':'Zahvati kod obnove objekta',
}
SERVICE_CTA={
 'vodoinstalacije':'Trebate vodoinstalacije?',
 'grijanje':'Trebate sustav grijanja?',
 'klimatizacija':'Trebate klimatizaciju?',
 'odvodnja':'Trebate odvodnju ili kanalizaciju?',
 'sanitarne-instalacije':'Trebate sanitarne instalacije?',
 'adaptacije-i-odrzavanje':'Trebate preinaku postojećih instalacija?',
}
SERVICE_META={
 'vodoinstalacije':'Vodoinstalacije i zamjena vodovodnih cijevi. MIJAS LTD j.d.o.o. sa sjedištem u Širincu. Pošaljite upit s lokacijom radova.',
 'grijanje':'Podno i radijatorsko grijanje: vrste sustava i potrebni podaci za upit. MIJAS LTD, Širinec. Opišite planirane radove.',
 'klimatizacija':'Klimatizacija za kuće i stanove: priprema vodova i ugradnja uređaja. MIJAS LTD, Širinec. Pošaljite informacije o prostoru.',
 'odvodnja':'Odvodnja i kanalizacija: odvodni vodovi, priključci i adaptacije. MIJAS LTD, Širinec. Pošaljite upit s lokacijom.',
 'sanitarne-instalacije':'Sanitarni priključci u kupaonicama i kuhinjama te izmjene rasporeda. MIJAS LTD, Širinec. Opišite što planirate.',
 'adaptacije-i-odrzavanje':'Preinake vodovodnih i odvodnih instalacija kod adaptacija. MIJAS LTD, Širinec. Pošaljite opis postojećeg stanja.',
}
IMAGE_ALTS={
 'equipment.avif':'Bakrene cijevi, ventili i razdjelnik u kotlovnici',
 'floor-heating.avif':'Cijevi podnog grijanja položene na pod prije estriha',
 'pipework.avif':'Bakreni razvod s ventilima i manometrom u strojarnici',
 'details.avif':'Bakrene cijevi, spojni elementi i mjerni instrument u kotlovnici',
 'hero.avif':'Sustav bakrenih cijevi i toplinske opreme u strojarnici',
 'intro.avif':'Tamna kotlovnica s bakrenim cijevima i razdjelnicima',
}

def service_heading(s):
 return SERVICE_H1[s[0]]

home='''<section class="hero"><div class="hero-image"></div><div class="hero-overlay"></div><div class="container hero-content"><div class="hero-inner"><h1 class="reveal">Vodovod, grijanje i <em>klimatizacija.</em></h1><p class="hero-description reveal">MIJAS LTD j.d.o.o. iz Širinca. Vodovodne i odvodne instalacije, sustavi grijanja i klimatizacija za stambene i poslovne objekte.</p><div class="hero-actions reveal">'''+contact_button('btn btn--copper')+('''<a href="/kontakt/#upit" class="btn btn--outline-light">Pošaljite upit'''+icon('arrow-up-right')+'''</a>''' if PHONE_TEL else '''<a href="/usluge/" class="btn btn--outline-light">Pogledajte usluge'''+icon('arrow-up-right')+'''</a>''')+'''</div></div></div></section>
<section class="intro-strip"><div class="container intro-strip__grid"><div><strong>Vodovodne instalacije</strong></div><div><strong>Sustavi grijanja</strong></div><div><strong>Klimatizacija</strong></div><a href="/usluge/">Sve usluge'''+icon('arrow-up-right')+'''</a></div></section>
<section class="section about-home"><div class="container about-grid"><div class="about-visual reveal"><img src="/assets/images/equipment.avif" alt="Bakrene cijevi, ventili i razdjelnik u kotlovnici" loading="lazy" width="1100" height="966"><div class="about-visual__accent"><span>MIJAS</span></div></div><div class="about-copy reveal"><h2>Što radimo i gdje nam je sjedište</h2><p class="lead">Vodovod, grijanje, klimatizacija i odvodnja za kuće, stanove i poslovne prostore.</p><p>MIJAS LTD j.d.o.o. registriran je u Širincu, u općini Križ. Za ponudu navedite vrstu zahvata, mjesto i postojeće stanje instalacija.</p><a class="text-link" href="/o-nama/">O nama'''+icon('arrow')+'''</a></div></div></section>
<section class="section services-section" id="usluge"><div class="container"><div class="section-heading reveal"><div><h2>Naše usluge</h2></div><p>Od vodovodnih priključaka do podnog grijanja: otvorite pojedinu uslugu za opis zahvata i podatke potrebne za upit.</p></div><div class="services-grid">'''+''.join(service_card(s,n) for n,s in enumerate(S))+'''</div></div></section>
<section class="section featured-section"><div class="container"><div class="section-heading reveal"><div><h2>Na kakvim objektima se primjenjuju ove instalacije</h2></div><div><p>Stanovi, kuće i poslovni prostori. Novogradnja i adaptacije.</p><a class="text-link" href="/projekti/">Pogledajte radove'''+icon('arrow')+'''</a></div></div><div class="featured-grid"><a class="feature-large" href="/projekti/"><img src="/assets/images/floor-heating.avif" alt="Cijevi podnog grijanja položene na pod prije estriha" loading="lazy" width="1024" height="540"><div class="feature-shade"></div><div class="feature-copy"><h3>Podno grijanje za kuću ili stan</h3><span class="feature-arrow">'''+icon('arrow-up-right')+'''</span></div></a><a class="feature-small" href="/projekti/"><img src="/assets/images/pipework.avif" alt="Bakreni razvod s ventilima i manometrom u strojarnici" loading="lazy" width="950" height="964"><div class="feature-shade"></div><div class="feature-copy"><h3>Cjevovodi i razdjelnici</h3><span class="feature-arrow">'''+icon('arrow-up-right')+'''</span></div></a></div></div></section>
<section class="section process-section"><div class="container"><div class="process-head reveal"><h2>Kako do ponude</h2></div><div class="process-grid">'''+''.join(f'<div class="process-card reveal"><h3>{t}</h3><p>{d}</p></div>' for t,d in [('Opišite radove','Navedite mjesto, vrstu objekta i postojeće stanje.'),('Dodajte detalje','Za vodovod navedite prostorije; za grijanje površinu i postojeći sustav.'),('Pošaljite upit','Obrazac javlja je li poruka uspješno dostavljena.')])+'''</div></div></section>
<section class="section faq-section"><div class="container faq-layout"><div class="faq-left reveal"><h2>Česta pitanja</h2><p>Za detalje o pojedinoj vrsti cijevi, grijanju i klimatizaciji pogledajte odgovarajuću stranicu usluge.</p><a class="text-link" href="/kontakt/">Pošaljite upit'''+icon('arrow')+'''</a></div>'''+faq_html(HOME_FAQ)+'''</div></section>'''+cta('Trebate ponudu?','Navedite lokaciju i vrstu radova u obrascu.','home')
page('Vodovod, grijanje i klimatizacija','MIJAS LTD j.d.o.o., Širinec kraj Križa. Vodovod, grijanje, odvodnja i klimatizacija. Pošaljite upit za instalaterske radove.','/',home,active='home',hero=True)

about=title_intro('O nama','Instalaterski radovi za <em>vaš objekt.</em>','MIJAS LTD j.d.o.o. sa sjedištem u Širincu, općina Križ.')+'''<section class="section"><div class="container about-grid"><div class="about-visual reveal"><img src="/assets/images/pipework.avif" alt="Bakreni razvod s ventilima i manometrom u strojarnici" width="950" height="964"><div class="about-visual__accent"><span>MIJAS</span></div></div><div class="about-copy reveal"><h2>Tko smo</h2><p class="lead">MIJAS LTD j.d.o.o. registrirana je hrvatska tvrtka sa sjedištem u Širincu.</p><p>Pretežita djelatnost društva obuhvaća instalacije vodovoda, odvodnje, grijanja i klimatizacije. Na stranicama usluga opisani su tipični radovi iz tih područja.</p><p>Za razgovor o konkretnom zahvatu pošaljite mjesto, vrstu objekta i kratak opis postojećeg stanja.</p><a href="/kontakt/#upit" class="text-link">Pošaljite upit'''+icon('arrow')+'''</a></div></div></section>'''+cta('Pitanje o vodovodu ili grijanju?','Pošaljite opis objekta i potrebnih instalacija.','about')
page('O nama','MIJAS LTD j.d.o.o. iz Širinca. Vodovodne i odvodne instalacije, grijanje i klimatizacija. Informacije o tvrtki i kontakt.','/o-nama/',about,'about')

services_intro=title_intro('Usluge','Instalaterske usluge','Vodovod, odvodnja, grijanje, klimatizacija i zahvati tijekom adaptacije objekata.')+'''<section class="section services-section"><div class="container"><div class="section-heading"><div><h2>Što sve obuhvaća registrirana djelatnost</h2></div><p>Ako niste sigurni koju kategoriju odabrati, u upitu napišite što mijenjate ili ugrađujete.</p></div><div class="services-grid">'''+''.join(service_card(s,n) for n,s in enumerate(S))+'''</div></div></section><section class="section"><div class="container split-feature"><div class="split-feature__copy"><h2>Pošaljite opis zahvata</h2><p>Navedite lokaciju, tip objekta i postojeće stanje. Ako imate nacrt ili dimenzije, opišite ih u poruci.</p><a class="btn btn--dark" href="/kontakt/#upit">Pošaljite upit'''+icon('arrow')+'''</a></div><img src="/assets/images/details.avif" alt="Bakrene cijevi, spojni elementi i mjerni instrument u kotlovnici" width="760" height="900" loading="lazy"></div></section>'''+cta('Pitanje o instalaterskim uslugama?','U obrascu navedite mjesto i vrstu planiranih radova.','services')
page('Usluge','Vodovod, odvodnja, podno grijanje, klimatizacija i sanitarne instalacije – pregled područja MIJAS LTD, Širinec.','/usluge/',services_intro,'services')

for j,s in enumerate(S):
 slug,name,short,eyebrow,statement,description,bullets,img=s
 # Usluge imaju različite strukture i broj elemenata; ne pretpostavljamo ugovorene rokove.
 details = {
 'vodoinstalacije':'Za upit navedite je li riječ o cijelom razvodu, jednoj prostoriji ili zamjeni pojedinog priključka.',
 'grijanje':'U upitu napišite grijete li kuću, stan ili poslovni prostor, površinu i imate li postojeći kotao.',
 'klimatizacija':'Za pripremu instalacije prije žbukanja navedite fazu gradnje. Ako je klima već kupljena, napišite model; mogućnost montaže treba potvrditi.',
 'odvodnja':'Navedite položaj odvoda, broj sanitarnih uređaja i radi li se o novom ili postojećem objektu.',
 'sanitarne-instalacije':'Ako premještate WC, umivaonik ili sudoper, pošaljite dimenzije i opis novog rasporeda.',
 'adaptacije-i-odrzavanje':'Kod obnove stana korisno je znati gdje je glavni ventil, koliko su stare cijevi i koje prostorije se mijenjaju.'
 }[slug]
 title=service_heading(s)
 body=title_intro('Usluge / '+name,escape(title),short)+f'''<section class="section"><div class="container service-detail-grid"><div class="service-detail-copy"><h2>{escape(SERVICE_H2[slug])}</h2><p class="lead">{escape(description)}</p><p>{escape(details)}</p><div class="detail-points">'''+''.join(f'<div>{icon("check")}{escape(b)}</div>' for b in bullets)+f'''</div><a href="/kontakt/#upit" class="btn btn--dark">Pošaljite upit {icon('arrow')}</a></div><div class="service-detail-image"><img src="/assets/images/{img}" alt="{IMAGE_ALTS[img]}" loading="lazy" width="950" height="964"></div></div></section>'''
 if slug=='grijanje':
  body+='''<section class="section"><div class="container split-feature"><div class="split-feature__copy"><h2>Podno, radijatorsko ili kombinirano</h2><p><strong>Podno:</strong> cijevi u podu, važno je uračunati izolaciju i estrih. <strong>Radijatorsko:</strong> zasebna grijaća tijela, često u postojećim objektima. <strong>Kombinirano:</strong> oba načina grijanja uz odgovarajuće upravljanje sustavom.</p></div><img src="/assets/images/floor-heating.avif" loading="lazy" width="1024" height="540" alt="Cijevi podnog grijanja položene na pod prije estriha"></div></section>'''
 if slug=='adaptacije-i-odrzavanje':
  body+='''<section class="section"><div class="container split-feature"><div class="split-feature__copy"><h2>Što pripremiti prije dolaska majstora</h2><div class="detail-points"><div>'''+icon('check')+'''Fotografirajte postojeće priključke i raspored prostorije.</div><div>'''+icon('check')+'''Provjerite gdje se zatvara dovod vode.</div><div>'''+icon('check')+'''Zapišite koje uređaje premještate ili zamjenjujete.</div></div></div><img src="/assets/images/details.avif" loading="lazy" width="760" height="900" alt="Bakrene cijevi i ventili u kotlovnici"></div></section>'''
 body+='''<section class="section services-section"><div class="container"><div class="section-heading"><div><h2>Ostale usluge</h2></div></div><div class="services-grid">'''+''.join(service_card(S[k],k) for k in [(j+1)%6,(j+2)%6,(j+3)%6])+'''</div></div></section>'''+f'''<section class="section faq-section"><div class="container faq-layout"><div class="faq-left"><h2>Česta pitanja</h2><p>Odgovori o {escape(name.lower())} i podacima koje je korisno navesti u upitu.</p></div>{faq_html(SERVICE_FAQS[slug])}</div></section>'''+cta(SERVICE_CTA[slug],'Za konkretan zahvat napišite mjesto, vrstu objekta i potrebnu izmjenu.','service')
 page(name,SERVICE_META[slug],SERVICE_URL(s),body,'services')

projects=title_intro('Radovi','Objekti na kojima se koriste ove instalacije','Vrste instalaterskih zahvata u kućama, stanovima i poslovnim prostorima.')+'''<section class="section"><div class="container"><div class="section-heading"><div><h2>Vrste radova</h2></div><p>Fotografije prikazuju moguće vrste instalaterskih zahvata i nisu potvrđene reference MIJAS LTD-a.</p></div><div class="projects-grid">'''+''.join(f'''<article class="project-card"><div class="project-card__image"><img src="/assets/images/{img}" alt="{IMAGE_ALTS[img]}" loading="lazy" width="950" height="964"></div><div class="project-card__body"><h3>{title}</h3><p>{desc}</p></div></article>''' for img,kicker,title,desc in [('equipment.avif','VODOVOD','Cjevovodi u stambenom objektu','Razvod tople i hladne vode te priključci za kuhinju i kupaonicu.'),('floor-heating.avif','GRIJANJE','Cijevi podnog grijanja','Polaganje grijaćih cijevi prije izrade završnih podnih slojeva.'),('hero.avif','STROJARNICA','Tehnička prostorija sustava grijanja','Kotao, razdjelnik i prateća oprema kao dio suvremenog sustava grijanja.'),('details.avif','ADAPTACIJE','Prilagodba i obnova instalacija','Spojni elementi, ventili i prilagodbe vodova tijekom adaptacije prostora.')])+'''</div></div></section>'''+cta('Planirate zamjenu cijevi ili grijanja?','Napišite vrstu objekta i lokaciju, pa pošaljite upit.','projects')
page('Radovi','Primjeri vrsta vodovodnih, odvodnih i toplinskih instalacija za stanove, kuće i poslovne objekte. MIJAS LTD.','/projekti/',projects,'projects')

contact=title_intro('Kontakt','Pošaljite nam <em>upit.</em>','Navedite mjesto, tip objekta i što se treba napraviti.')+'''<section class="section"><div class="container contact-grid"><div class="contact-information"><h2>Kontakt podaci</h2><p>Sjedište: Širinec 36, 10314 Širinec. U obrascu napišite grad ili mjesto gdje su planirani radovi.</p>'''+public_contacts()+'''<div class="contact-info-item">'''+icon('location')+'''<div><strong>Sjedište tvrtke</strong><span>Širinec 36, 10314 Širinec, Hrvatska</span></div></div><div class="contact-info-item">'''+icon('file')+'''<div><strong>Poslovni podaci</strong><span>MIJAS LTD j.d.o.o.<br>OIB: 40827941362</span></div></div><a class="text-link" href="https://www.google.com/maps/search/?api=1&amp;query=%C5%A0irinec%2036%2C%2010314%20%C5%A0irinec" target="_blank" rel="noopener noreferrer">Sjedište na karti'''+icon('arrow-up-right')+'''</a><div class="contact-photo"><img src="/assets/images/pipework.avif" alt="Bakreni razvod s ventilima i manometrom u strojarnici" loading="lazy" width="950" height="964"></div></div><div class="contact-form-panel" id="upit"><h2>Opišite radove</h2><p>Upišite vrstu instalacije, lokaciju, približnu površinu objekta i, ako je riječ o adaptaciji, postojeće stanje.</p><form id="contact-form" class="contact-form" novalidate><div class="form-row"><label>Ime i prezime <sup>*</sup><input name="name" type="text" required autocomplete="name" maxlength="110" placeholder="Vaše ime i prezime"></label><label>Telefon<input name="phone" type="tel" autocomplete="tel" maxlength="40" placeholder="Broj telefona"></label></div><label>E-mail adresa <sup>*</sup><input name="email" type="email" required autocomplete="email" maxlength="160" placeholder="ime@primjer.hr"></label><div class="form-row"><label>Vrsta usluge <sup>*</sup><select name="service" required><option value="" selected disabled>Odaberite uslugu</option>'''+''.join(f'<option value="{escape(s[1])}">{escape(s[1])}</option>' for s in S)+'''<option value="Ostalo">Ostalo</option></select></label><label>Lokacija radova <sup>*</sup><input name="location" type="text" required maxlength="120" placeholder="Grad ili mjesto"></label></div><label>Željeni termin<select name="preferred_time"><option value="">Nije određeno</option><option value="Što prije">Što prije</option><option value="U iduća 2 tjedna">U iduća 2 tjedna</option><option value="Tijekom mjeseca">Tijekom mjeseca</option><option value="Dogovor">Prema dogovoru</option></select></label><label>Opis projekta <sup>*</sup><textarea name="message" rows="5" required minlength="15" maxlength="3500" placeholder="Npr. zamjena vodovodnih cijevi u stanu 60 m², Ivanić-Grad"></textarea></label><label class="form-check"><input name="privacy" type="checkbox" required><span>Suglasan/na sam s obradom podataka radi odgovora na upit, prema <a href="/politika-privatnosti/" target="_blank">Politici privatnosti</a>. <sup>*</sup></span></label><div class="honeypot" aria-hidden="true"><label>Website <input name="website" tabindex="-1" autocomplete="off"></label></div><button class="btn btn--copper form-submit" type="submit">Pošaljite upit'''+icon('arrow')+'''</button><p id="form-status" class="form-status" role="status" aria-live="polite"></p></form></div></div></section>'''
page('Kontakt','Pošaljite upit tvrtki MIJAS LTD j.d.o.o., Širinec. Navedite mjesto, vrstu objekta i planirane instalaterske radove.','/kontakt/',contact,'contact')

privacy=title_intro('Privatnost','Politika <em>privatnosti.</em>','Informacije o obradi osobnih podataka tijekom korištenja web stranice MIJAS LTD.')+'''<section class="section legal-section"><article class="container legal-copy"><p class="legal-date">Posljednje ažuriranje: 11. studenoga 2026.</p><h2>1. Voditelj obrade</h2><p>Voditelj obrade osobnih podataka je MIJAS LTD j.d.o.o., Širinec 36, 10314 Širinec, Hrvatska, OIB: 40827941362. Pitanja povezana s privatnošću možete dostaviti putem kontakt obrasca na ovoj web stranici.</p><h2>2. Koji se podaci prikupljaju?</h2><p>Putem kontakt obrasca korisnik može dostaviti ime i prezime, e-mail adresu, telefon (nije obavezan), vrstu tražene usluge, lokaciju radova i opis projekta. Tehnički sustavi hostinga mogu obraditi osnovne tehničke podatke nužne za rad i sigurnost stranice.</p><h2>3. Svrha i pravni temelj</h2><p>Podaci poslani kroz kontakt obrazac obrađuju se radi zaprimanja i odgovora na upit te poduzimanja radnji na zahtjev korisnika prije mogućeg sklapanja ugovora (čl. 6. st. 1. t. b GDPR-a), odnosno na temelju legitimnog interesa kada je primjenjivo. Neobavezna analitika, ako bude aktivirana, provodi se isključivo na temelju prethodne privole.</p><h2>4. Primatelji i vanjske usluge</h2><p>Za isporuku web stranice koristi se Cloudflare Pages. Za prijenos upita preko obrasca predviđen je Web3Forms. Analitički alati ne učitavaju se bez prethodne privole korisnika.</p><h2>5. Trajanje pohrane</h2><p>Osobni podaci čuvaju se samo onoliko dugo koliko je potrebno za obradu upita, eventualnu poslovnu suradnju i ispunjenje primjenjivih zakonskih obveza. </p><h2>6. Vaša prava</h2><p>Sukladno GDPR-u imate pravo zatražiti pristup, ispravak, brisanje, ograničenje obrade, prenosivost kada je primjenjivo te uložiti prigovor. Kada se obrada temelji na privoli, možete je povući u svakom trenutku. Pritužbu možete podnijeti Agenciji za zaštitu osobnih podataka (AZOP).</p><h2>7. Kolačići i lokalna pohrana</h2><p>Ova web stranica koristi lokalnu pohranu preglednika za pamćenje izbora postavki kolačića i uvodne animacije. Neobavezne analitičke tehnologije ne uključuju se bez odgovarajuće privole. Svoj izbor možete promijeniti putem poveznice „Postavke kolačića” u podnožju stranice.</p><h2>8. Sigurnost i izmjene</h2><p>Primjenjuju se primjerene tehničke mjere zaštite. Ova politika može se ažurirati pri izmjenama funkcionalnosti web stranice. </p></article></section>'''
page('Politika privatnosti','Politika privatnosti tvrtke MIJAS LTD – obrada podataka, kontakt obrazac, kolačići i prava korisnika.','/politika-privatnosti/',privacy)
terms=title_intro('Uvjeti korištenja','Uvjeti <em>korištenja.</em>','Pravila i informacije povezane s korištenjem web stranice MIJAS LTD.')+'''<section class="section legal-section"><article class="container legal-copy"><p class="legal-date">Posljednje ažuriranje: 11. studenoga 2026.</p><h2>1. Podaci o pružatelju</h2><p>MIJAS LTD j.d.o.o., Širinec 36, 10314 Širinec, Hrvatska. OIB: 40827941362. Web stranica služi informativnom predstavljanju tvrtke i mogućnosti slanja poslovnog upita.</p><h2>2. Sadržaj i informacije</h2><p>Informacije na stranicama služe općem upoznavanju s vrstama instalaterskih radova. Objavljeni opisi ne predstavljaju obvezujuću ponudu, jamstvo dostupnosti usluga ili tehničku specifikaciju izvedbe. Pojedine usluge i radovi definiraju se u neposrednom dogovoru.</p><h2>3. Slanje upita</h2><p>Slanje obrasca ne stvara obvezu sklapanja ugovora. Sadržaj upita treba biti točan i primjeren. Odgovor ili ponuda ovisi o dostatnosti informacija, dostupnosti i dogovoru. </p><h2>4. Fotografije i prikazi</h2><p>Fotografije na web stranici služe vizualnom predstavljanju vrsta instalacija i primjene tehničkih sustava. One nisu dokaz izvedenih projekata MIJAS LTD, osim kada je to izričito navedeno uz provjerenu referencu.</p><h2>5. Intelektualno vlasništvo</h2><p>Tekst, dizajn i grafički elementi zaštićeni su sukladno mjerodavnim propisima, osim gdje je navedeno drukčije. Fotografije mogu imati prava svojih autora ili nositelja licenci.</p><h2>6. Vanjske poveznice</h2><p>Web stranica može sadržavati poveznice na vanjske servise. Za njihov sadržaj i pravila privatnosti odgovaraju njihovi pružatelji.</p><h2>7. Dostupnost i odgovornost</h2><p>Nastojimo osigurati točnost i dostupnost sadržaja, no moguća su privremena ograničenja ili tehničke poteškoće. Ništa ovdje ne isključuje prava koja korisnicima pripadaju prema prisilnim propisima.</p><h2>8. Primjenjivo pravo</h2><p>Na korištenje web stranice primjenjuje se pravo Republike Hrvatske, uz poštivanje primjenjivih pravila o zaštiti potrošača i osobnih podataka.</p></article></section>'''
page('Uvjeti korištenja','Uvjeti korištenja web stranice tvrtke MIJAS LTD.','/uvjeti-koristenja/',terms)
# build special 404 independently (Cloudflare Pages handles root 404.html)
notfound='''<section class="notfound"><div class="container"><div class="notfound-number">404</div><h1>Ovdje nema <em>tražene stranice.</em></h1><p>Možda je poveznica promijenjena ili stranica više nije dostupna. Vratite se na početnu ili otvorite popis usluga.</p><a href="/" class="btn btn--dark">'''+icon('arrow-left')+''' Povratak na početnu</a></div></section>'''
page('Stranica nije pronađena','Tražena stranica ne postoji. Povratak na početnu stranicu MIJAS LTD.','/404/',notfound)
# copy 404/ page to root 404.html
(ROOT/'404.html').write_text((ROOT/'404'/'index.html').read_text(encoding='utf-8'),encoding='utf-8')

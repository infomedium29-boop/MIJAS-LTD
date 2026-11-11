from pathlib import Path
import json
root=Path('/mnt/data/mijas_float_contact')
p=root/'tools/business_details.json'
d=json.loads(p.read_text(encoding='utf-8'))
d['floating_phone']='+385 91 509 0790'
d['floating_whatsapp']='+385 91 509 0790'
d['floating_whatsapp_call_url']=''  # Optionally supply a verified WhatsApp call link, otherwise reliably open chat.
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')

b=root/'tools/build.py'
s=b.read_text(encoding='utf-8')
anchor="WA_NUM = ''.join(ch for ch in WHATSAPP if ch.isdigit())\n"
new=anchor+"""# Odobren broj za stalno vidljive plutajuće gumbe; odvojen od poslovnih kontakata.
FLOAT_PHONE = str(DETAILS.get('floating_phone') or '').strip()
FLOAT_WA = str(DETAILS.get('floating_whatsapp') or '').strip()
FLOAT_TEL = ''.join(ch for ch in FLOAT_PHONE if ch in '+0123456789')
FLOAT_WA_NUM = ''.join(ch for ch in FLOAT_WA if ch.isdigit())
FLOAT_WA_CALL_URL = str(DETAILS.get('floating_whatsapp_call_url') or '').strip()

def floating_contacts():
 if not FLOAT_TEL and not FLOAT_WA_NUM:return ''
 items=[]
 if FLOAT_TEL:
  items.append(f'''<a class="floating-contact__button floating-contact__button--phone" href="tel:{FLOAT_TEL}" aria-label="Nazovite MIJAS LTD na {escape(FLOAT_PHONE)}" title="Običan poziv: {escape(FLOAT_PHONE)}">{icon('phone')}</a>''')
 if FLOAT_WA_NUM:
  # Službeni WhatsApp wa.me otvara razgovor. Za direktan poziv potreban je provjereni poslovni call link.
  wa_url = FLOAT_WA_CALL_URL if FLOAT_WA_CALL_URL.startswith('https://') else f'https://wa.me/{FLOAT_WA_NUM}'
  items.append(f'''<a class="floating-contact__button floating-contact__button--whatsapp" href="{escape(wa_url,quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Otvorite WhatsApp za razgovor ili poziv na {escape(FLOAT_WA)}" title="WhatsApp: {escape(FLOAT_WA)}"><svg class="floating-contact__whatsapp-icon" viewBox="0 0 32 32" aria-hidden="true" fill="currentColor"><path d="M16.02 3.2C9.1 3.2 3.45 8.83 3.44 15.75c0 2.2.58 4.35 1.68 6.25L3.3 28.7l6.87-1.8c1.84 1 3.92 1.53 6.05 1.53h.01c6.92 0 12.57-5.64 12.58-12.56.01-3.36-1.3-6.52-3.67-8.9a12.45 12.45 0 0 0-9.12-3.77zm.2 23.1c-1.88 0-3.72-.5-5.33-1.46l-.38-.22-3.97 1.04 1.06-3.87-.24-.4a10.47 10.47 0 0 1-1.61-5.57c.01-5.77 4.71-10.47 10.49-10.47a10.4 10.4 0 0 1 7.42 3.08 10.4 10.4 0 0 1 3.07 7.43c0 5.78-4.71 10.48-10.5 10.48zm5.76-7.86c-.31-.16-1.87-.92-2.16-1.02-.29-.11-.5-.16-.71.16-.21.32-.82 1.02-1 1.23-.18.21-.36.24-.67.08-.31-.15-1.32-.48-2.51-1.55-.92-.82-1.54-1.83-1.72-2.14-.18-.32-.02-.49.14-.65.14-.14.31-.37.47-.55.16-.18.21-.31.32-.52.1-.21.05-.39-.03-.55-.08-.16-.71-1.71-.97-2.35-.26-.62-.52-.54-.71-.55l-.61-.01a1.16 1.16 0 0 0-.84.39c-.29.32-1.1 1.08-1.1 2.63 0 1.55 1.13 3.05 1.29 3.26.16.21 2.22 3.39 5.38 4.75.75.32 1.34.52 1.8.66.76.24 1.45.21 2 .13.61-.09 1.87-.76 2.13-1.5.26-.73.26-1.36.18-1.49-.08-.13-.29-.21-.61-.37z"/></svg></a>''')
 return '<aside class="floating-contact" aria-label="Brzi kontakt">'+''.join(items)+'</aside>'

"""
assert s.count(anchor)==1
s=s.replace(anchor,new)
end="+footer()+cookie()+'''</body></html>'''"
assert s.count(end)==1, s.count(end)
s=s.replace(end,"+footer()+floating_contacts()+cookie()+'''</body></html>'''")
b.write_text(s,encoding='utf-8')

css=root/'assets/css/style.css'
css.write_text(css.read_text(encoding='utf-8')+'''

/* Stalni kontakt: dva elegantna gumba na donjoj desnoj strani svih stranica. */
.floating-contact{position:fixed;right:max(24px,env(safe-area-inset-right));bottom:calc(28px + env(safe-area-inset-bottom));z-index:95;display:flex;flex-direction:column;gap:13px;align-items:center;transition:bottom .22s ease,opacity .2s ease}
.floating-contact__button{display:flex;align-items:center;justify-content:center;width:56px;height:56px;border-radius:50%;border:1px solid rgba(255,255,255,.28);text-decoration:none;color:white;box-shadow:0 8px 25px rgba(4,20,28,.32);transition:transform .18s ease,box-shadow .18s ease,background-color .18s ease;isolation:isolate}
.floating-contact__button--phone{background:#bb8657}
.floating-contact__button--phone:hover{background:#a77043}
.floating-contact__button--whatsapp{background:#25d366}
.floating-contact__button--whatsapp:hover{background:#1eb858}
.floating-contact__button:hover{transform:translateY(-3px);box-shadow:0 13px 28px rgba(4,20,28,.36)}
.floating-contact__button:focus-visible{outline:3px solid #fff;outline-offset:3px;box-shadow:0 0 0 6px #17303f,0 8px 25px rgba(4,20,28,.3)}
.floating-contact__button .icon{width:25px;height:25px;stroke-width:1.9}
.floating-contact__whatsapp-icon{width:31px;height:31px}
body.menu-open .floating-contact{opacity:0;pointer-events:none}
@media(max-width:720px){.floating-contact{right:calc(18px + env(safe-area-inset-right));bottom:calc(23px + env(safe-area-inset-bottom));gap:12px}.floating-contact__button{width:52px;height:52px}.floating-contact__button .icon{width:24px;height:24px}.floating-contact__whatsapp-icon{width:29px;height:29px}}
@media(max-width:340px){.floating-contact{right:12px}.floating-contact__button{width:48px;height:48px}}
@media(prefers-reduced-motion:reduce){.floating-contact,.floating-contact__button{transition:none}}
''',encoding='utf-8')

r=root/'README.md'
r.write_text(r.read_text(encoding='utf-8')+'''

## Plutajući gumbi za brzi kontakt

Na svim stranicama pri dnu desno prikazuju se dva stalna kontaktna gumba: telefonski poziv na `+385 91 509 0790` (`tel:+385915090790`) i WhatsApp razgovor za isti broj (`https://wa.me/385915090790`). WhatsApp razgovor omogućuje da korisnik zatim pritisne ikonu telefona za glasovni poziv; obična `wa.me` poveznica **ne pokreće automatski WhatsApp glasovni poziv**. Ako tvrtka dobije i potvrdi podržani WhatsApp poslovni *call link*, može ga unijeti u `floating_whatsapp_call_url` u `tools/business_details.json`.

Brojevi plutajućih gumbića su namjenski u `floating_phone` i `floating_whatsapp`, odvojeni od općih podataka `public_phone` / `public_whatsapp`. Za promjenu broja uredite konfiguraciju i ponovno pokrenite build. Gumbi su dostupni na svim HTML rutama, a mobilni izbornik ih prekriva dok je otvoren.
''',encoding='utf-8')
print('patched')

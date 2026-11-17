# MIJAS LTD — sinkronizirana intro animacija (17.11.2026.)

Izmijenjena je isključivo uvodna animacija, a izvorni logotip i ostali vizualni identitet nisu redizajnirani.

- Postojeći brzi ravni wipe zamijenjen je povezanim reveal slijedom: kapljica i plamen → naziv MIJAS LTD → završni kolor potezi → dva reda usluga.
- Koristi se ista izvorna transparentna WebP datoteka u svim fazama te završni puni sloj kako bi logotip ostao identičan originalu.
- Pokretanje animacije i brojača izlaska slijedi nakon dekodiranja slike (uz sigurnosni fallback) umjesto dva neovisna vremena, što uklanja nesinkroniziranost pri sporijem učitavanju.
- Uklonjen je vizualni artefakt zbog prerano otkrivenih donjih natpisa.
- Ukupno trajanje nakon početka animacije približno je 3 sekunde, s glatkim izlaskom; poštuje se `prefers-reduced-motion` i gumb „Preskoči uvod”.
- Verzije CSS i JS resursa promijenjene su radi osvježavanja predmemorije.

## Testiranje
- `python3 tools/build.py` — uspješno.
- `python3 tools/deploy.py` — uspješno, `dist/` za Cloudflare Pages.
- `python3 tools/qa_static.py` — 17 HTML ruta, bez prijavljenih grešaka.
- `node --check assets/js/main.js` — prolazi.
- Lokalni izolirani Chromium vizualni pregled faza i konačnog kadra na 390px i 1440px — prolazi, bez JS grešaka. Izolirani pregled korišten je zato što pregledavanje lokalne URL adrese nije dopušteno u ovom okruženju.

Napomena: intro se na webu obično prikazuje jedanput po sesiji. Za ponovno testiranje otvorite novu anonimnu karticu/prozor ili novu sesiju preglednika.

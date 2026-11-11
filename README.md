# MIJAS LTD – web stranica (revizija prema PDF nalogu, 11.11.2026.)

Statički HTML/CSS/JavaScript projekt s optimiziranim ilustrativnim fotografijama, originalnom uvodnom animacijom, 14 HTML ruta i poslužiteljskom Cloudflare Pages Function za upite. Izvor sadržaja nalazi se u **`tools/build.py`**. Nemojte uređivati generirane HTML datoteke, jer ih generator prepisuje.

## Postavljanje na GitHub i Cloudflare Pages

1. Raspakirajte ZIP i prenesite **sve datoteke i mape** u korijen novog GitHub repozitorija (bez dodatne vanjske mape).
2. Cloudflare → Workers & Pages → Create → Pages → povežite GitHub repozitorij.
3. `Framework preset`: **None**.
4. `Build command`: **`python3 tools/deploy.py`**.
5. `Build output directory`: **`dist`**.
6. Deployment objavljuje samo HTML, javne skripte, fotografije i ostale statičke datoteke iz mape **`dist`**. Mapa `tools/` i datoteke `README.md`, `ZAVRSNA-PROVJERA.md` **nisu javne**, premda ostaju u GitHub repozitoriju. Serverless funkcije u `functions/` ostaju u korijenu repozitorija radi Cloudflare Pages Functions.
7. Ako build okruženje ne nudi `python3`, unaprijed generirana mapa `dist/` već je uključena: ostavite Build command prazan i kao izlaz odaberite `dist`. Nakon budućih promjena tada morate lokalno pokrenuti `python3 tools/deploy.py` i prenijeti ažurirani `dist/`.

**Za demo:** ne postavljajte `PUBLIC_SITE_URL`. `robots.txt` i `_headers` sprječavaju indeksaciju. ZIP je pripremljen kao demo, ne kao javna službena stranica.

## Obavezno potvrditi kontakt informacije

U `tools/business_details.json` popunjavajte isključivo podatke koje je tvrtka MIJAS LTD **izričito odobrila za javnu objavu**:

- `public_phone`: službeni broj telefona. Nakon unosa prikazuje se `tel:` poveznica u zaglavlju, kontaktu, podnožju i mobilna ikona za poziv.
- `public_email`: službena e-mail adresa; pojavljuje se na Kontakt stranici i u podnožju.
- `public_whatsapp`: ako ga tvrtka koristi i odobri.
- `public_working_hours`: točno radno vrijeme.
- `confirmed_service_towns`: samo potvrđena mjesta rada, za strukturirane podatke i budući tekst.

Broj i e-mail iz Meta lead obrasca **nisu automatski službeni kontakti**. Dok ih vlasnik ne odobri, stranica ima ispravan CTA „Pošaljite upit” koji vodi na obrazac, bez lažnih kontakata.

Treba potvrditi i rok odgovora, rok dolaska, naplatu izlaska, jamstva, izdavanje računa, nabavu materijala, sve stvarne usluge te fotografije izvedenih radova. Ništa od toga nije izmišljeno.

## Aktiviranje kontaktnog obrasca

`functions/api/contact.js` koristi Web3Forms na poslužitelju, bez javno izloženog pristupnog ključa.

1. Potvrdite službenu adresu za dolazne poruke.
2. Otvorite Web3Forms račun i verificirajte primatelja upita.
3. U Cloudflare Pages → Settings → Variables and Secrets dodajte secret `WEB3FORMS_ACCESS_KEY` u odgovarajuće okruženje.
4. Ponovno pokrenite deployment.
5. Pošaljite probni upit na pravoj Cloudflare adresi i potvrdite primitak poruke na odredišnu adresu.

Bez ključa endpoint vraća HTTP 503 i **ne potvrđuje lažno slanje**. Lokalni Python HTTP server također ne izvršava Cloudflare Functions.

## Produkcijski SEO – tek po odobrenju klijenta

Nakon pisane potvrde domene, teksta, usluga, javnih kontakata i pravnih podataka:

1. U Cloudflare Pages **production environment** postavite `PUBLIC_SITE_URL=https://stvarna-domena.hr` (bez završne `/`).
2. Ako produkcijska grana nije `main`, postavite `PRODUCTION_BRANCH=ime-grane`.
3. Build `python3 tools/deploy.py` tada na produkcijskoj grani automatski izvršava redom: `build.py` → `prepare_production.py` → `publish.py`. Preview grane ostaju blokirane za indeksiranje.
4. Provjerite apsolutni canonical, `og:image`, `og:url`, `/sitemap.xml`, `/robots.txt` i HTTP zaglavlja.
5. Tek tada dodajte stranicu u Google Search Console / Google Business Profile.

**Ako ručno pripremate produkciju:**

```bash
python3 tools/build.py
python3 tools/prepare_production.py https://stvarna-domena.hr
python3 tools/publish.py
```

Nemojte nakon pripreme produkcije još jednom pokrenuti `build.py` bez ponavljanja `prepare_production.py` jer će se vratiti demo oznake.

## Provjera

```bash
python3 tools/qa_static.py
python3 tools/qa_static.py dist
```

Korisni sadržaji:
- `tools/build.py` – generator svih stranica i SEO metapodataka.
- `tools/business_details.json` – centralno mjesto za *potvrđene* kontakte.
- `tools/deploy.py` – automatizirani Cloudflare build.
- `tools/prepare_production.py` – aktiviranje produkcijskih SEO postavki.
- `tools/publish.py` – javni artefakt bez izvornog generatora i internih dokumenata.
- `ZAVRSNA-PROVJERA.md` – detaljne realizirane promjene i otvorene stavke.

## Dizajn i mediji

Postojeće fotografije i SVG logotip ostali su nepromijenjeni. Intro u `intro()` i svi `.intro-*` CSS stilovi ostali su isti. Font Inter nije bio učitan, pa je iz neispravne font liste uklonjen; stranica sada eksplicitno koristi postojeći sistemski font `Segoe UI` / Arial bez uključivanja vanjskog CDN-a. U CSS-u su dodatno prilagođeni isključivo selektori za promijenjenu HTML hijerarhiju i mreža skraćenog procesa. Pri objavi stvarnih referenci postojeće ilustrativne prikaze treba zamijeniti dopuštenim fotografijama klijenta.


## Plutajući gumbi za brzi kontakt

Na svim stranicama pri dnu desno prikazuju se dva stalna kontaktna gumba: telefonski poziv na `+385 91 509 0790` (`tel:+385915090790`) i WhatsApp razgovor za isti broj (`https://wa.me/385915090790`). WhatsApp razgovor omogućuje da korisnik zatim pritisne ikonu telefona za glasovni poziv; obična `wa.me` poveznica **ne pokreće automatski WhatsApp glasovni poziv**. Ako tvrtka dobije i potvrdi podržani WhatsApp poslovni *call link*, može ga unijeti u `floating_whatsapp_call_url` u `tools/business_details.json`.

Brojevi plutajućih gumbića su namjenski u `floating_phone` i `floating_whatsapp`, odvojeni od općih podataka `public_phone` / `public_whatsapp`. Za promjenu broja uredite konfiguraciju i ponovno pokrenite build. Gumbi su dostupni na svim HTML rutama, a mobilni izbornik ih prekriva dok je otvoren.

## Ažuriranje galerije i fotografija usluga

Na stranici `Radovi` četiri vizualno različite kartice prikazuju adaptaciju vodovodnih instalacija, podno grijanje, kotlovnicu i razdjelnike grijanja. Nove fotografije spremljene su lokalno u AVIF formatu. Relevantne fotografije povezane su i sa stranicama vodoinstalacija, grijanja, sanitarnih instalacija te adaptacija. One su ilustrativne i ne predstavljaju stvarne reference tvrtke bez klijentove potvrde.

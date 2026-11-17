# MIJAS LTD – web stranica (vlasnikov originalni logotip i nove usluge, 17.11.2026.)

Statički HTML/CSS/JavaScript projekt s optimiziranim ilustrativnim fotografijama, originalnom uvodnom animacijom, 17 glavnih HTML ruta (uz 404) i poslužiteljskom Cloudflare Pages Function za upite. Izvor sadržaja nalazi se u **`tools/build.py`**. Nemojte uređivati generirane HTML datoteke, jer ih generator prepisuje.

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

Broj **+385 91 509 0790** javno je istaknut na vlasnikovom dostavljenom vizualu te se koristi u zaglavlju, kontaktu i plutajućim gumbima. Poslovni e-mail i radno vrijeme još nisu potvrđeni, pa se ne izmišljaju.

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

Fotografije postojećih radova ostale su na istim mjestima. **Prethodni SVG monogram zamijenjen je točno vlasnikovim logotipom** izdvojenim iz dostavljene slike bez redizajna. Original je u `tools/vlasnikov-logo-originalna-slika.png`, a neizmijenjeni izrez u `assets/images/mijas-logo-izvorni.png`. Za prikaz se koristi prozirna verzija `mijas-logo-dark.png` s kontrastnim svijetlim natpisom na tamnoj pozadini; svi oblici, plamen, kapljica i boje simbola ostali su isti. Uvodna animacija zadržava svoju tehničku pozadinu i trajanje približno 2,5–3 s; originalni logo otkriva se postupno. Font Inter nije bio učitan, pa je iz neispravne font liste uklonjen; stranica sada eksplicitno koristi postojeći sistemski font `Segoe UI` / Arial bez uključivanja vanjskog CDN-a. U CSS-u su dodatno prilagođeni isključivo selektori za promijenjenu HTML hijerarhiju i mreža skraćenog procesa. Pri objavi stvarnih referenci postojeće ilustrativne prikaze treba zamijeniti dopuštenim fotografijama klijenta.


## Plutajući gumbi za brzi kontakt

Na svim stranicama pri dnu desno prikazuju se dva stalna kontaktna gumba: telefonski poziv na `+385 91 509 0790` (`tel:+385915090790`) i WhatsApp razgovor za isti broj (`https://wa.me/385915090790`). WhatsApp razgovor omogućuje da korisnik zatim pritisne ikonu telefona za glasovni poziv; obična `wa.me` poveznica **ne pokreće automatski WhatsApp glasovni poziv**. Ako tvrtka dobije i potvrdi podržani WhatsApp poslovni *call link*, može ga unijeti u `floating_whatsapp_call_url` u `tools/business_details.json`.

Brojevi plutajućih gumbića su namjenski u `floating_phone` i `floating_whatsapp`, odvojeni od općih podataka `public_phone` / `public_whatsapp`. Za promjenu broja uredite konfiguraciju i ponovno pokrenite build. Gumbi su dostupni na svim HTML rutama, a mobilni izbornik ih prekriva dok je otvoren.

## Ažuriranje galerije i fotografija usluga

Na stranici `Radovi` četiri vizualno različite kartice prikazuju adaptaciju vodovodnih instalacija, podno grijanje, kotlovnicu i razdjelnike grijanja. Nove fotografije spremljene su lokalno u AVIF formatu. Relevantne fotografije povezane su i sa stranicama vodoinstalacija, grijanja, sanitarnih instalacija te adaptacija. One su ilustrativne i ne predstavljaju stvarne reference tvrtke bez klijentove potvrde.

## Izmjene 17.11.2026.

- Vlasnikov logo prikazuje se u navigaciji, footeru i introu, **bez precrtavanja** i bez bijelog pravokutnika. Na tamnim pozadinama tamnoplava slova dobila su svijetlu kontrastnu varijantu; simbol i oblici ostaju nepromijenjeni.
- Iz vlasnikove slike preuzete su glavne usluge: **Vodoinstalacije, Grijanje, Dizalice topline, Servisi, Montaža**.
- Dodane su tri zasebne podstranice `/usluge/dizalice-topline/`, `/usluge/servisi/`, `/usluge/montaza/` s vlastitim sadržajem, FAQ-om i SEO opisom.
- Zadržane su prethodne stranice za klimatizaciju, odvodnju, sanitarne instalacije i adaptacije.
- Glavni hero, početna, kontaktni telefon, footer i katalog usluga usklađeni su s dostavljenim vizualom.
- Iz originalne slike izrezana je favicon ikona; OG slika koristi isti originalni logotip.
- Vlasnikov kontakt s vizuala +385 91 509 0790 postavljen je na telefonske poveznice i WhatsApp razgovor.
- Stranica **ostaje demo** bez Google indeksiranja i bez lažnih referenci. Kontakt forma zahtijeva stvarni `WEB3FORMS_ACCESS_KEY` i probno slanje.

**Napomena:** Na vlasnikovom vizualu nisu navedeni brandovi dizalica topline, servisna ovlaštenja, jamstva ni radno vrijeme. Na webu se te informacije ne tvrde bez potvrde.

## Uklonjena bijela pozadina (17.11.2026.)

Logotip u navigaciji, footeru i introu koristi `assets/images/mijas-logo-dark.png`, PNG s transparentnom pozadinom. Izvorni vlasnikov dizajn i izvorni rez sačuvani su u datoteci `mijas-logo-izvorni.png`, a inačica s prozirnom podlogom i izvornom tamnom tipografijom u `mijas-logo-transparent.png`. Zbog čitljivosti na tamnoplavoj podlozi tekst je u varijanti `mijas-logo-dark.png` svijetao. Favicon ima transparentnu podlogu, a OG slika tamnu pozadinu bez bijelog panela.

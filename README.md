# MIJAS LTD – premium web stranica (demo)

Kompletna statička web stranica izrađena kao prezentacijski demo za MIJAS LTD j.d.o.o.
Tehnologija: HTML, CSS, JavaScript, AVIF, Cloudflare Pages Functions. Bez frameworka i npm builda.

## Sadržaj

- Početna s uvodnom animacijom logotipa (približno 2,9 s, uključujući izlazni prijelaz), prikazuje se jednom po sesiji i može se preskočiti.
- O nama, pregled usluga i šest zasebnih SEO podstranica.
- Područja primjene s filtriranjem (ne tvrdi da su ilustracije stvarne reference).
- Kontakt s obrascem i poslužiteljskom Cloudflare Function funkcijom.
- Politika privatnosti, uvjeti korištenja, cookie banner, posebna 404 stranica.
- Mobilna navigacija, animacije, favicon, SEO metapodaci i dinamički `/sitemap.xml` za Cloudflare.
- `robots.txt` i `_headers` namjerno blokiraju indeksiranje dok je projekt demo.

## GitHub + Cloudflare Pages

1. Napravite novi GitHub repozitorij, npr. `mijas-ltd`.
2. **Raspakirajte ZIP** i prenesite sve datoteke i mape iznutra u korijen repozitorija. `index.html`, `assets/` i `functions/` trebaju biti u korijenu.
3. Cloudflare Dashboard → Workers & Pages → Create application → Pages → Connect to Git.
4. Odaberite GitHub repozitorij. Framework preset: **None**, Build command: **ostaviti prazno**, Build output directory: `.` (korijen repozitorija).
5. Deploy. Cloudflare Pages automatski servira HTML, CSS, AVIF, te `functions/api/contact.js` i `functions/sitemap.xml.js`.
6. Testirajte početnu, navigaciju, podstranice i `/sitemap.xml` na novoj Cloudflare adresi.

### Aktivacija kontakt obrasca

Prije stvarnog slanja kontakt upita:
1. Vlasnik treba potvrditi službenu e-mail adresu na koju će stizati upiti.
2. U servisu Web3Forms kreirajte i verificirajte pristupni ključ za tu adresu.
3. Cloudflare Pages projekt → Settings → Variables and Secrets → dodajte **secret** naziva `WEB3FORMS_ACCESS_KEY`, vrijednost preuzetu iz Web3Forms računa. Dodajte za okruženje u kojem obrazac treba raditi.
4. Pokrenite novi deployment i testirajte slanje sa stvarnom probnom porukom te provjerite da je primljena na poslovnu e-mail adresu.

Bez ključa obrazac **namjerno vraća poruku da još nije aktiviran**. Nikada se ne prikazuje lažna potvrda slanja.

### Analytics

Postavke su u `assets/js/config.js`:

```js
window.MIJAS_CONFIG = Object.freeze({
  ga4Id: '',
  analyticsEnabled: false,
  contactEndpoint: '/api/contact'
});
```

Nakon što klijent potvrdi GA4 mjerni ID i politiku privatnosti, postavite `ga4Id` i `analyticsEnabled: true`. GA4 se učitava isključivo kada je korisnik odabrao analitičku privolu.

### Produkcijska domena i indeksiranje

**Važno: stranica je namjerno u DEMO modu.** Ona nije automatski spremna za indeksiranje.

Nakon odobrenja klijenta, potvrde domene, podataka i pravnih tekstova pokrenite u korijenu projekta:

```bash
python tools/prepare_production.py https://stvarna-domena.hr
```

Skripta:
- pretvara relativne canonical adrese u apsolutne produkcijske URL-ove;
- postavlja apsolutnu OG sliku i `og:url`;
- generira statički `sitemap.xml` sa stvarnom domenom;
- mijenja `robots.txt` na indeksabilnu verziju;
- uklanja `X-Robots-Tag: noindex, nofollow` iz `_headers`.

**Nemojte pokretati prije odobrenja klijenta.** Ako kasnije ponovno pokrenete `tools/build.py`, ponovno pokrenite i produkcijsku skriptu prije deploya.

### Podaci koje treba potvrditi s klijentom

- Da je pronađeni Mijas LTD j.d.o.o. doista klijent koji je poslao upit.
- Registrirane i **stvarno aktivne** vrste usluga; opseg i eventualna potrebna ovlaštenja.
- Područja poslovanja i izlazak na teren.
- Službeni logo, telefon, poslovni e-mail, WhatsApp.
- Pravo korištenja stvarnih fotografija i eventualnih referenci.
- Status adrese sjedišta za javni prikaz i Google poslovni profil.
- Korištene vanjske usluge, rokovi čuvanja podataka i konačna pravna provjera.
- Produkcijska domena i Analytics ID.

## Fotografije

Fotografije industrijske opreme i instalacija u ovom demu **ilustrativni su vizuali** i nisu dokaz radova ili stvarnih referenci tvrtke. Prije konačne objave preporučuje se zamjena fotografijama radova koje dostavi tvrtka uz dopuštenje za javnu objavu.

Svi bitmap vizuali u `assets/images/` lokalno su optimizirani u AVIF. Datoteka `og-cover.jpg` služi za društvene mreže. Logo i favicon su lokalni SVG.

## Lokalno pokretanje

U korijenu projekta:

```bash
python -m http.server 8000
```

Otvorite `http://localhost:8000`. Običan lokalni HTTP server ne pokreće Cloudflare Pages Functions. Slanje forme testirati na Cloudflareu ili uz Wrangler Pages dev.

## Struktura

- `index.html` – početna.
- `o-nama/`, `usluge/`, `projekti/`, `kontakt/` – podstranice.
- `politika-privatnosti/`, `uvjeti-koristenja/` – pravne stranice.
- `404.html` – posebna greška stranice.
- `assets/css/style.css` – cijeli dizajn sustav.
- `assets/js/main.js` – intro, mobilna navigacija, GDPR, animacije, forme.
- `assets/js/config.js` – konfiguracija.
- `functions/api/contact.js` – Cloudflare poslužiteljska kontakt funkcija.
- `functions/sitemap.xml.js` – sitemap s ispravnom domenom deploymenta.
- `tools/build.py` – izvorni generator sadržaja.
- `tools/prepare_production.py` – aktivacija produkcijskog SEO-a.
- `ZAVRSNA-PROVJERA.md` – detaljna provjera 20 stavki.

## Napomena

Ovaj ZIP je **potpuno upotrebljiv demo**, ali bez potvrđenih poslovnih kontakata i stvarnog Web3Forms pristupnog ključa još nije završena produkcijska objava. Nužno je dovršiti integraciju i provjeru s klijentom.

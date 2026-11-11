# MIJAS LTD – završni izvještaj revizije (11. studenoga 2026.)

Temelj: korisnički PDF „MIJAS LTD – nalog za izmjene teksta i tehničke ispravke” (18 stranica). Izvorni ZIP nije zamijenjen predloškom. Sadržaj je izmijenjen u `tools/build.py`, zatim su generirane HTML stranice. Izvorni intro i fotografije nisu mijenjani.

## Realizacija po poglavljima naloga

| Poglavlje | Rezultat | Status |
|---|---|---|
| A – Gramatika i ALT | 6 ručno definiranih završnih CTA poruka, konkretni ALT opisi, uklonjeni neispravni izrazi | ✅ |
| B – Naslovi | Upravo tri `<em>` u H1 (početna, O nama, kontakt); opisni H1 za šest usluga; jednostavniji H2 | ✅ |
| C – Rečenice bez sadržaja | Uklonjeni aforizmi, generičke fraze, upadljiva ponavljanja i poruke demo-faze. Ne navode se nepoznate godine, jamstva ili rokovi | ✅ |
| D – FAQ | 5 pitanja na početnoj i po 3 različita za svaku od 6 usluga (23 različita pitanja). Nema neprovjerenih tvrdnji o dostupnosti radova, cijeni izlaska ili jamstvu | ✅ za sadašnje odgovore; ⚠️ kupčeva pitanja o cijeni, rokovima, R1 i materijalu traže potvrdu |
| E – Kontakt | Ugrađena centralna konfiguracija potvrđenog telefona/e-maila/WhatsAppa; dinamički `tel:`, `mailto:` i mobilna ikona poziva; obrazac sada pita željeni termin; SVG gumba se ispravno vraća | ✅ kod; ⚠️ javni podaci i Web3Forms secret nisu dostavljeni |
| F – Ponavljanja | Različiti FAQ po usluzi; specifični CTA; posebno objašnjenje za grijanje i popis pripreme za adaptaciju; posebni meta opisi | ✅ |
| G – Sekcije | Uklonjena generička tamna sekcija i „Naš pristup”; proces je sveden na 3 konkretna koraka; brojevi ostaju samo uz kartice usluga; uklonjen suvišni filtar četiriju kartica | ✅ |
| H – Mikrokopija | Jednostavni tekstovi tipki, „Radovi” umjesto „Primjena”, novi doslovni nadnaslovi, novi potpis uz logo | ✅ |
| I – Tehnika | Uklonjen neučitan Inter iz font-stacka; ispravljen produkcijski `og:image`, uklonjen `telephone=no`; hijerarhija H3 u karticama; SEO schema s dodatnim poljima kad podaci postanu dostupni | ✅ tehničke ispravke; ⚠️ stvarna domena, telefon, radno vrijeme |
| J – Objava | `tools/publish.py` objavljuje samo `dist/`; interni izvori i izvještaji nisu u javnom outputu; produkcijska skripta testirana na hipotetskoj domeni; demo ostaje `noindex` | ✅ |
| K – Podaci klijenta | Izdvojeni u ovom izvještaju i `tools/business_details.json`, bez izmišljanja | ⚠️ čeka potvrdu |
| L – Kontrola | Automatizirana kontrola HTML ruta, meta podataka, poveznica, sadržaja, OG, robots, sitemap i javnih datoteka; vizualni browser test i dostava e-maila nisu dovršeni | ⚠️ dio ručnih provjera preostaje |

## Rezultati provjera

- **14 HTML ruta**, 14 različitih title oznaka, 14 različitih meta opisa.
- **0 nepostojećih internih poveznica** u lokalnoj statičkoj analizi izvora i mape `dist`.
- **3** stilizirana `<em>` naslova u generiranim stranicama.
- **23** različita FAQ pitanja, **0** ponavljanja.
- Nema „Trebate klimatizacija”, „Trebate sustavi”, „Trebate odvodnja”, „Otkrijte uslugu”, „Ilustrativni prikaz”, „format-detection”, „završnoj verziji” ni „nakon njezine konfiguracije” u HTML-u.
- `intro()` uspoređen s izvornim ZIP-om: **bajtno identičan**.
- Svi izvorni slikovni, SVG i OG resursi uspoređeni s izvornim ZIP-om: **identični**.
- `node --check` za `assets/js/main.js` i `functions/api/contact.js`: bez sintaktičkih grešaka.
- Provjera testne produkcijske izgradnje: apsolutni canonical, apsolutni `og:image`, `og:url`, robots, sitemap (**13 indeksabilnih URL-ova**) te odsutnost internih datoteka u `dist`: uspješno.
- **Vizualni pregled Chromiumom nije prošao**, jer se preglednik u ovom okruženju nije uspješno pokrenuo. Stoga nisam označio mobilnu vizualnu kontrolu kao potvrđenu.
- **Stvarno slanje kontaktnog obrasca nije testirano**, jer nije dostavljen Web3Forms ključ ni službena e-mail adresa.

## Obavezna web checklista – 20 stavki

1. ✅ Politika privatnosti – stranica postoji; ⚠️ prije objave potvrditi kontakte i pravne detalje obrade.
2. ✅ Uvjeti korištenja – stranica postoji; ⚠️ konačna poslovna i pravna provjera.
3. ✅ Jasan CTA – aktivne poveznice na obrazac; ⚠️ javni poziv nakon potvrde broja.
4. ✅ FAQ – početna i šest usluga imaju zasebna pitanja.
5. ✅ `robots.txt` – demo blokiran; produkcija automatski otvara pristup nakon odobrenja.
6. ✅ `sitemap.xml` – funkcija za demo i statički produkcijski sitemap testirani.
7. ✅ Custom 404 – generiran i provjeren kao datoteka.
8. ✅ ALT opisi – sve vidljive slike imaju smislene opise.
9. ⚠️ GA4 pripremljen, Measurement ID i privola za stvarni račun još nisu konfigurirani.
10. ✅ Meta title – 14 jedinstvenih naslova.
11. ✅ Meta description – 14 jedinstvenih opisa.
12. ✅/⚠️ OG/X Card oznake postoje; produkcijska OG putanja testirana, stvarna objava i WhatsApp dijeljenje još nisu testirani.
13. ✅ Favicon – postojeći SVG ostao isti.
14. ✅ Canonical – prisutan; probno apsolutiziran u produkcijskom testu.
15. ✅ Cookie Consent – prihvaćanje, odbijanje i postavke, uz odgođeno učitavanje analitike.
16. ⚠️ Responzivni CSS ostao je uglavnom isti; nova verzija nije ponovno vizualno potvrđena u pregledniku.
17. ⚠️ Semantička struktura i pristupačnost poboljšane; potpuni WCAG 2.2 AA audit nije proveden.
18. ⚠️ Validacija i poslužiteljska funkcija postoje; stvarni prijem poruke nije moguće potvrditi bez ključa.
19. ✅ Sve lokalne interne veze provjerene; jedna vanjska poveznica na Google Maps nije mrežno testirana.
20. ⚠️ AVIF resursi ostali optimizirani i statički kod minimalan; novu Lighthouse/Core Web Vitals analizu nije moguće potvrditi bez aktivnog weba.

## Podaci koji nedostaju i ne smiju se izmišljati

1. Potvrda identiteta i opsega stvarnih usluga MIJAS LTD.
2. **Telefon za javnu objavu**, javni **e-mail**, WhatsApp/Viber i ime osobe koja se javlja.
3. Radno vrijeme, hitne intervencije, vikendi.
4. Konkretna mjesta i najveća udaljenost izlaska na teren.
5. Naplaćuje li se procjena i izlazak, rok dolaska, rok za ponudu, trajanje jamstva, R1 računi, tko nabavlja materijal.
6. Stvarna godina iskustva i eventualna ovlaštenja.
7. Stvarne reference, fotografije, mjesta i godine radova uz dopuštenje za objavu.
8. Službena domena, GA4 ID i Web3Forms pristupni ključ.

**Napomena:** Kako telefon i službeni e-mail nisu potvrđeni, javna stranica zasad ne prikazuje broj iz privatnog Meta leada. Usluga obrasca bez `WEB3FORMS_ACCESS_KEY` pošteno javlja neuspjeh, a ne lažnu potvrdu slanja. Prije prezentiranja kao potpuno funkcionalne produkcijske stranice to se mora dovršiti.

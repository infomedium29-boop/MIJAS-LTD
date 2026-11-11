# MIJAS LTD – završna kontrola kvalitete

Datum: 11.11.2026.  
Vrsta isporuke: **prezentacijski demo**, pripremljen za GitHub + Cloudflare Pages.

Oznake: ✅ Implementirano i provjereno · ⚠️ Potrebna dodatna konfiguracija/test · ❌ Nije implementirano.

| # | Stavka | Status | Rezultat |
|---|---|---|---|
| 1 | Privacy Policy | ⚠️ | Uključena politika privatnosti s poznatim poslovnim podacima; prije produkcije provjeriti stvarne pružatelje usluga, rokove čuvanja i zakonitost obrade. |
| 2 | Terms Page | ⚠️ | Stranica uvjeta korištenja postoji; finalnu verziju treba odobriti tvrtka / pravna osoba. |
| 3 | Clear CTA | ✅ | CTA na hero sekciji, stranicama usluga, footeru i zasebnoj kontakt stranici. |
| 4 | FAQ | ✅ | FAQ s funkcionalnim HTML details/summary elementima. |
| 5 | robots.txt | ✅ | Valjani demo robots.txt blokira indeksiranje. Produkcijsko aktiviranje kroz skriptu. |
| 6 | sitemap.xml | ⚠️ | Cloudflare Pages Function automatski servira `/sitemap.xml`; treba provjeriti na stvarnom deployu. Produkcijska skripta stvara statičku datoteku. |
| 7 | Custom 404 | ✅ | Postoji `404.html` s povratkom na početnu. |
| 8 | ALT Text | ✅ | Provjereno da prikazane IMG fotografije imaju ALT opise. |
| 9 | Analytics | ⚠️ | GA4 skripta i mjerenje događaja spremni; GA4 ID nije dostavljen, analytics je isključen. |
| 10 | Meta Titles | ✅ | Jedinstven naslov na svim glavnim stranicama. |
| 11 | Meta Description | ✅ | Jedinstven opis na svim glavnim stranicama. |
| 12 | Social Share | ⚠️ | OG i Twitter oznake postoje te JPG preview slika; apsolutne OG URL-ove postaviti nakon potvrde domene. |
| 13 | Favicon | ✅ | Dostavljen lokalni SVG favicon. |
| 14 | Canonical URLs | ⚠️ | Demo koristi relativne canonicals; produkcijska skripta pretvara ih u apsolutne na potvrđenoj domeni. |
| 15 | Cookie Consent | ✅ | Prihvati, odbij, postavke, lokalno spremanje; GA4 ne učitava se bez privole. |
| 16 | Mobile Version | ✅ | Provjeren prikaz početne na 320, 375, 390, 768, 1024, 1440 i 1920 px te kontakta na 320, 390, 768 i 1440 px, bez horizontalnog overflowa. |
| 17 | Accessibility | ⚠️ | Semantički HTML, ALT, labele, skip link, keyboard focus i reduced motion; nije napravljen potpuni neovisni WCAG 2.2 AA audit. |
| 18 | Test Forms | ⚠️ | Validacija obrazaca testirana; simulirani uspješan odgovor funkcionira. Stvarno slanje zahtijeva Web3Forms secret, deploy i end-to-end provjeru. |
| 19 | Check Broken Links | ✅ | Provjera internih putanja u generiranim HTML datotekama. Vanjski Maps link je opći Google Maps URL, funkcionalnost se potvrđuje nakon deploya. |
| 20 | Optimise Performance | ⚠️ | Lokalni AVIF, bez UI frameworka i velikih ovisnosti, odgođeno učitavanje fotografija; nije izvršen stvarni Lighthouse/Core Web Vitals audit na javnom URL-u. |

## Rezultat

- Izrađeno **14 HTML ruta** + Cloudflare prilagođeni `404.html`.
- Intro s ispisivanjem marke i naziva, ukupno ~2,9 sekundi do završetka izlaznog prijelaza.
- Sve stranice uključuju navigaciju, footer, cookie postavke i meta oznake.
- Stvarni osobni kontakt iz Meta leada nije objavljen kao službeni kontakt.
- Područja primjene i vizuali predstavljeni su kao ilustracije, a ne izmišljene reference.
- Demo je namjerno blokiran za indeksiranje (`robots.txt`, `X-Robots-Tag`).

## Zadaci prije javne objave

1. Od klijenta potvrditi identitet, usluge, područje rada, logo i javne kontakt podatke.
2. Nadomjestiti ilustrativne fotografije stvarnim odobrenim materijalima gdje su dostupni.
3. Aktivirati i stvarno testirati kontaktni obrazac preko Web3Forms/Cloudflare.
4. Provjeriti i finalizirati GDPR i pravne tekstove prema stvarnoj obradi podataka.
5. Po potrebi konfigurirati GA4 s ispravnom privolom.
6. Nakon potvrde domene pokrenuti `tools/prepare_production.py` i dopustiti indeksiranje.
7. Na javnom URL-u provjeriti Lighthouse, mobitele, obrazac, Cloudflare Functions i sitemap.

**Status projekta:** ✅ spreman za demonstraciju, ⚠️ nije još finaliziran za produkcijsko indeksiranje / slanje kontakt upita.

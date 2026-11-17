# MIJAS LTD — ispravak punog logotipa i introa

- Ispravljen je samo tamni završetak slova **j** u punoj verziji originalnog vlasnikova logotipa (footer i intro), bez promjene njegovih oblika ili plavo-narančastih poteza.
- Nova je datoteka `mijas-logo-full-j-jasan-v5.webp`, bez bijele pozadine i nepotrebnih praznih margina.
- Intro više nema animaciju iscrtavanja niti slojeve: prikazuje cijeli logo odmah, 0,55 sekundi, a zatim ga uklanja kroz 0,25 sekundi blagog fade-outa. Ukupno 0,8 sekundi nakon pokretanja skripte.
- Ostali dijelovi weba nisu namjerno mijenjani; demo i dalje ne dopušta indeksiranje.
- Cloudflare build: `python3 tools/deploy.py`, output directory `dist`.

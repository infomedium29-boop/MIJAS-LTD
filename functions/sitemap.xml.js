/** Generates domain-correct sitemap for Cloudflare Pages preview deployments. */
const ROUTES = [ '/', '/o-nama/', '/usluge/',
  '/usluge/vodoinstalacije/', '/usluge/grijanje/', '/usluge/klimatizacija/',
  '/usluge/odvodnja/', '/usluge/sanitarne-instalacije/', '/usluge/adaptacije-i-odrzavanje/',
  '/projekti/', '/kontakt/', '/politika-privatnosti/', '/uvjeti-koristenja/' ];
export function onRequestGet({ request }) {
  const base = new URL(request.url).origin;
  const xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ROUTES.map(path => `  <url><loc>${base}${path}</loc></url>`).join('\n') + '\n</urlset>';
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8', 'Cache-Control': 'public, max-age=3600' } });
}

/** Cloudflare Pages Function – protected contact endpoint. Configure WEB3FORMS_ACCESS_KEY. */
const reply = (status, message, success = false) => new Response(JSON.stringify({ success, message }), {
  status,
  headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' }
});
export async function onRequestPost({ request, env }) {
  const origin = request.headers.get('Origin');
  if (origin && new URL(origin).origin !== new URL(request.url).origin) return reply(403, 'Nedopušten izvor zahtjeva.');
  if (!env.WEB3FORMS_ACCESS_KEY) return reply(503, 'Kontakt obrazac još nije aktiviran. Molimo pokušajte nakon aktivacije stranice.');
  const size = Number(request.headers.get('Content-Length') || 0);
  if (size > 20_000) return reply(413, 'Upit je prevelik.');
  let data;
  try { data = await request.json(); } catch { return reply(400, 'Neispravni podaci obrasca.'); }
  const clean = key => String(data?.[key] || '').trim();
  const [name, email, phone, service, location, message] = ['name', 'email', 'phone', 'service', 'location', 'message'].map(clean);
  if (clean('website')) return reply(200, 'Upit je zaprimljen.', true); // honeypot
  if (clean('privacy') !== 'on') return reply(400, 'Potrebno je prihvatiti politiku privatnosti.');
  if (!name || name.length > 110 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 160 || phone.length > 40 || !location || location.length > 120 || !service || service.length > 80 || message.length < 15 || message.length > 3500) {
    return reply(400, 'Provjerite obavezna polja obrasca.');
  }
  const subject = 'MIJAS LTD – novi upit s web stranice';
  const payload = {
    access_key: env.WEB3FORMS_ACCESS_KEY, name, email, phone, subject,
    message: `Vrsta usluge: ${service}\nLokacija: ${location}\nTelefon: ${phone || '(nije naveden)'}\n\nOpis projekta:\n${message}`,
    from_name: 'MIJAS LTD web obrazac', replyto: email,
  };
  try {
    const response = await fetch('https://api.web3forms.com/submit', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload), signal: AbortSignal.timeout(9000)
    });
    const result = await response.json().catch(() => null);
    if (!response.ok || !result?.success) return reply(502, 'Slanje trenutačno nije uspjelo. Molimo pokušajte ponovno.');
    return reply(200, 'Poruka uspješno poslana.', true);
  } catch {
    return reply(502, 'Slanje trenutačno nije dostupno. Molimo pokušajte ponovno.');
  }
}
export function onRequestGet() { return reply(405, 'Metoda nije dopuštena.'); }

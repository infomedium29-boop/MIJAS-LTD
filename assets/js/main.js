/* MIJAS LTD: interactions, intro, consent, and forms. No JS framework required. */
(() => {
  'use strict';
  document.body.classList.add('js-ready');
  const $ = (selector, parent = document) => parent.querySelector(selector);
  const $$ = (selector, parent = document) => [...parent.querySelectorAll(selector)];
  const config = window.MIJAS_CONFIG || {};
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const intro = $('#brand-intro');
  const dismissIntro = () => {
    if (!intro || intro.classList.contains('is-exiting')) return;
    intro.classList.add('is-exiting');
    intro.setAttribute('aria-hidden', 'true');
    intro.inert = true;
    try { sessionStorage.setItem('mijas-intro-played', '1'); } catch (_) {}
    window.setTimeout(() => intro.remove(), 500);
  };
  if (intro) {
    let played = false;
    try { played = sessionStorage.getItem('mijas-intro-played') === '1'; } catch (_) {}
    if (played || reduceMotion) {
      intro.remove();
    } else {
      $('#intro-skip')?.addEventListener('click', dismissIntro);
      window.setTimeout(dismissIntro, 2450);
    }
  }
  // Navigation
  const header = $('#header');
  const menu = $('#menu-toggle');
  const mobile = $('#mobile-nav');
  const updateHeader = () => header?.classList.toggle('is-scrolled', window.scrollY > 34);
  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });
  const closeMenu = () => {
    document.body.classList.remove('menu-open');
    mobile?.classList.remove('is-open');
    menu?.setAttribute('aria-expanded', 'false');
    mobile?.setAttribute('aria-hidden', 'true');
    if (menu) menu.innerHTML = '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>';
  };
  menu?.addEventListener('click', () => {
    if (mobile?.classList.contains('is-open')) return closeMenu();
    document.body.classList.add('menu-open');
    mobile?.classList.add('is-open');
    menu.setAttribute('aria-expanded', 'true');
    mobile?.setAttribute('aria-hidden', 'false');
    menu.innerHTML = '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>';
  });
  window.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
  $$('#mobile-nav a').forEach(link => link.addEventListener('click', closeMenu));
  const dropdown = $('.nav-service');
  dropdown?.querySelector('.nav-drop-toggle')?.addEventListener('click', () => {
    const open = dropdown.classList.toggle('open');
    dropdown.querySelector('.nav-drop-toggle').setAttribute('aria-expanded', String(open));
  });
  document.addEventListener('click', e => {
    if (dropdown && !dropdown.contains(e.target)) {
      dropdown.classList.remove('open');
      dropdown.querySelector('.nav-drop-toggle').setAttribute('aria-expanded', 'false');
    }
  });
  $('#year') && ($('#year').textContent = String(new Date().getFullYear()));
  // Reveal only after content is ready; reduced motion stays readable.
  const reveal = $$('.reveal');
  if ('IntersectionObserver' in window && !reduceMotion) {
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('in-view'); obs.unobserve(entry.target); } });
    }, { threshold: .08, rootMargin: '0px 0px 20px 0px' });
    reveal.forEach(el => observer.observe(el));
  } else reveal.forEach(el => el.classList.add('in-view'));
  // Filter representative areas by type.
  const filterBar = $('.filter-bar');
  filterBar?.addEventListener('click', event => {
    const button = event.target.closest('button[data-filter]');
    if (!button) return;
    const filter = button.dataset.filter;
    $$('button[data-filter]', filterBar).forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    $$('.project-card').forEach(card => { card.hidden = filter !== 'all' && card.dataset.category !== filter; });
  });
  // Consent choices: do not add tracking cookies or third-party analytics before opt-in.
  const COOKIE_KEY = 'mijas-cookie-consent-v1';
  const banner = $('#cookie-banner');
  const analyticsChoice = $('#analytics-choice');
  const options = $('.cookie-options');
  let consent = null;
  try { consent = JSON.parse(localStorage.getItem(COOKIE_KEY) || 'null'); } catch (_) {}
  let analyticsLoaded = false;
  const canTrack = () => !!(config.analyticsEnabled && /^G-[A-Z0-9]+$/i.test(config.ga4Id || ''));
  const initGA4 = () => {
    if (!consent?.analytics || !canTrack() || analyticsLoaded) return;
    analyticsLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    const script = document.createElement('script');
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(config.ga4Id);
    script.async = true;
    document.head.appendChild(script);
    window.gtag('js', new Date());
    window.gtag('config', config.ga4Id, { 'anonymize_ip': true });
  };
  const setConsent = allowAnalytics => {
    consent = { analytics: !!allowAnalytics, updatedAt: Date.now() };
    try { localStorage.setItem(COOKIE_KEY, JSON.stringify(consent)); } catch (_) {}
    if (banner) banner.hidden = true;
    // If analytics was previously enabled and is now rejected, a full reload prevents further events.
    if (!consent.analytics && analyticsLoaded) { window.location.reload(); return; }
    initGA4();
  };
  if (banner) {
    const showCookie = () => { banner.hidden = false; if (analyticsChoice) analyticsChoice.checked = !!consent?.analytics; };
    if (!consent || !consent.updatedAt || Date.now() - consent.updatedAt > 180 * 86400000) {
      window.setTimeout(showCookie, intro && intro.isConnected ? 2800 : 250);
    } else initGA4();
    $$('[data-consent]', banner).forEach(button => button.addEventListener('click', () => {
      if (button.dataset.consent === 'accept') setConsent(canTrack());
      if (button.dataset.consent === 'reject') setConsent(false);
      if (button.dataset.consent === 'settings') {
        if (options) options.hidden = !options.hidden;
        if (!options?.hidden) { button.textContent = 'Spremi postavke'; button.dataset.consent = 'save'; }
      } else if (button.dataset.consent === 'save') {
        setConsent(canTrack() && !!analyticsChoice?.checked);
      }
    }));
  }
  $('#cookie-settings')?.addEventListener('click', () => { if (banner) { banner.hidden = false; if (analyticsChoice) analyticsChoice.checked = !!consent?.analytics; } });
  // Track click actions only with configured, consented GA4.
  document.addEventListener('click', e => {
    if (!consent?.analytics || !analyticsLoaded || !window.gtag) return;
    const link = e.target.closest('a');
    if (!link) return;
    const href = link.getAttribute('href') || '';
    const eventName = href.startsWith('tel:') ? 'phone_click' : href.startsWith('mailto:') ? 'email_click' : href.includes('wa.me') ? 'whatsapp_click' : href.includes('#upit') ? 'contact_cta_click' : '';
    if (eventName) window.gtag('event', eventName);
  });
  // Contact form: Cloudflare Pages Function + Web3Forms server-side key.
  const form = $('#contact-form');
  form?.addEventListener('submit', async e => {
    e.preventDefault();
    const status = $('#form-status');
    const button = $('.form-submit', form);
    const say = (message, type = 'error') => { status.textContent = message; status.className = 'form-status is-' + type; };
    if (!form.reportValidity()) { say('Molimo ispravno ispunite sva obavezna polja.'); return; }
    const data = Object.fromEntries(new FormData(form).entries());
    if (data.message.trim().length < 15) { say('Opis projekta treba sadržavati najmanje 15 znakova.'); return; }
    button.disabled = true;
    button.dataset.originalLabel = button.textContent;
    button.textContent = 'Šaljemo upit…';
    say('', 'success');
    try {
      const response = await fetch(config.contactEndpoint || '/api/contact', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data)
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok || !result.success) throw new Error(result.message || 'Upit nije poslan. Pokušajte ponovno kasnije.');
      form.reset();
      say('Hvala na upitu. Poruka je uspješno zaprimljena.', 'success');
      if (consent?.analytics && analyticsLoaded && window.gtag) window.gtag('event', 'generate_lead');
    } catch (error) { say(error.message || 'Slanje nije uspjelo. Pokušajte ponovno kasnije.'); }
    finally { button.disabled = false; button.textContent = 'Pošaljite upit →'; }
  });
})();

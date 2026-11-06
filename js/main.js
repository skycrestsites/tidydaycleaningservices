(function () {
  var header = document.querySelector('.site-header');
  var burger = document.querySelector('.burger');
  var mnav = document.getElementById('mnav');
  var mcta = document.querySelector('.mobile-cta');

  // header shadow + mobile CTA visibility
  function onScroll() {
    var y = window.scrollY || 0;
    if (header) header.classList.toggle('scrolled', y > 8);
    if (mcta) mcta.classList.toggle('show', y > 520 && !(mnav && !mnav.hidden));
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // mobile menu
  if (burger && mnav) {
    var openIcon = burger.innerHTML;
    var closeIcon = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>';
    function setMenu(open) {
      mnav.hidden = !open;
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      burger.innerHTML = open ? closeIcon : openIcon;
      onScroll();
    }
    burger.addEventListener('click', function () { setMenu(mnav.hidden); });
    mnav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    window.addEventListener('resize', function () { if (window.innerWidth > 1024 && !mnav.hidden) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !mnav.hidden) { setMenu(false); burger.focus(); } });
  }

  // desktop dropdown: close on Escape / outside click (hover + focus handled in CSS)
  var drop = document.querySelector('.has-drop');
  if (drop) {
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { drop.classList.remove('open'); if (drop.contains(document.activeElement)) document.activeElement.blur(); } });
  }

  // footer year
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // quote form: preselect service from ?service=slug, then open the visitor's email app pre-filled
  var form = document.getElementById('quote-form');
  if (form) {
    var params = new URLSearchParams(location.search);
    var slug = params.get('service');
    if (slug) {
      var sel = form.querySelector('select[name="service"]');
      var opt = sel.querySelector('option[data-slug="' + slug.replace(/[^a-z0-9-]/g, '') + '"]');
      if (opt) opt.selected = true;
    }
    var note = form.querySelector('.form-note');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      form.querySelectorAll('[required]').forEach(function (f) {
        var bad = !f.value.trim() || (f.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.value.trim()));
        f.classList.toggle('invalid', bad);
        if (bad && ok) { f.focus(); ok = false; }
      });
      if (!ok) { note.textContent = 'Please fill in your name, a valid email and the service you need.'; note.className = 'form-note err'; return; }
      var d = new FormData(form);
      var body = 'Name: ' + d.get('name') + '\nPhone: ' + (d.get('phone') || '') + '\nEmail: ' + d.get('email') +
        '\nCity / ZIP: ' + (d.get('city') || '') + '\nService: ' + d.get('service') + '\n\n' + (d.get('message') || '');
      var to = window.TD_EMAIL || '';
      location.href = 'mailto:' + to + '?subject=' + encodeURIComponent('Quote request: ' + d.get('service')) + '&body=' + encodeURIComponent(body);
      note.textContent = 'Thank you! Your email app should open with your request ready to send.';
      note.className = 'form-note ok';
    });
    form.addEventListener('input', function (e) { e.target.classList.remove('invalid'); });
  }

  // gentle reveal on scroll
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var els = document.querySelectorAll('.sec-head, .svc-card, .steps li, .split-copy, .split-media, .inc-col, .chips, .faq, .values > div, .checklist li, .duo figure, .cta-in, .other-svc a');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    els.forEach(function (el, i) {
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight) return; // already on screen, keep visible
      el.classList.add('rv');
      el.style.transitionDelay = ((i % 4) * 60) + 'ms';
      io.observe(el);
    });
  }
})();

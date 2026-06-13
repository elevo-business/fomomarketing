/* FOMO LIVE 26 — interactions */
(function () {
  'use strict';

  // ---- CONFIG (bitte mit echten Daten ersetzen) ----
  var CONFIG = {
    eventDate: '2026-09-24T18:30:00+02:00', // TODO: finales Event-Datum bestätigen
    whatsapp: '491700000000', // TODO: echte WhatsApp-Nummer (Format: Landesvorwahl ohne +/00)
    waText: 'Hallo FOMO Marketing, ich möchte mir einen Platz bei FOMO LIVE 26 sichern.',
    leadEndpoint: 'api/lead.php', // optional PHP-Backend; faellt sonst auf E-Mail/WhatsApp zurueck
    email: 'event@fomo-marketing.de' // TODO: echte Event-E-Mail
  };

  function $(s, c) { return (c || document).querySelector(s); }
  function $all(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function fmt(n) { return Math.round(n).toLocaleString('de-DE'); }
  function pad(n) { return (n < 10 ? '0' : '') + n; }

  document.addEventListener('DOMContentLoaded', function () {
    // year
    var y = $('#year'); if (y) y.textContent = new Date().getFullYear();

    // WhatsApp links
    var waUrl = 'https://wa.me/' + CONFIG.whatsapp + '?text=' + encodeURIComponent(CONFIG.waText);
    $all('[data-wa]').forEach(function (a) { a.href = waUrl; a.target = '_blank'; a.rel = 'noopener'; });

    // marquee: duplicate track for seamless loop
    var mq = document.getElementById('marqueeTrack');
    if (mq) mq.innerHTML += mq.innerHTML;

    // countdown
    initCountdown();

    // sticky mobile CTA: show after hero, hide while ticket section is visible
    var mcta = document.getElementById('mobileCta');
    if (mcta) {
      var ticketsVisible = false;
      var tickets = document.getElementById('tickets');
      if ('IntersectionObserver' in window && tickets) {
        new IntersectionObserver(function (es) { ticketsVisible = es[0].isIntersecting; updMcta(); }, { threshold: .12 }).observe(tickets);
      }
      var updMcta = function () {
        var pastHero = window.scrollY > window.innerHeight * 0.55;
        mcta.classList.toggle('show', pastHero && !ticketsVisible);
      };
      window.addEventListener('scroll', updMcta, { passive: true });
      window.addEventListener('resize', updMcta, { passive: true });
      updMcta();
    }

    // scroll progress + header
    var pb = $('#scrollProgress'), hd = $('#header');
    window.addEventListener('scroll', function () {
      var h = document.documentElement;
      if (pb) pb.style.width = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100 + '%';
      if (hd) hd.classList.toggle('scrolled', window.scrollY > 40);
    }, { passive: true });

    // mobile nav
    var mt = $('#menuToggle'), mn = $('#mobileNav');
    if (mt && mn) {
      mt.addEventListener('click', function () {
        var a = mn.classList.toggle('active');
        var s = mt.querySelectorAll('span');
        s[0].style.transform = a ? 'rotate(45deg) translate(6px,6px)' : '';
        s[1].style.opacity = a ? '0' : '';
        s[2].style.transform = a ? 'rotate(-45deg) translate(6px,-6px)' : '';
        document.body.style.overflow = a ? 'hidden' : '';
      });
      $all('a', mn).forEach(function (a) {
        a.addEventListener('click', function () {
          mn.classList.remove('active'); document.body.style.overflow = '';
          mt.querySelectorAll('span').forEach(function (s) { s.style.transform = ''; s.style.opacity = ''; });
        });
      });
    }

    // reveal
    var ro = $all('.reveal');
    if (ro.length && 'IntersectionObserver' in window) {
      var ob = new IntersectionObserver(function (e) {
        e.forEach(function (n) { if (n.isIntersecting) { n.target.classList.add('visible'); ob.unobserve(n.target); } });
      }, { threshold: .08, rootMargin: '0px 0px -40px 0px' });
      ro.forEach(function (e) { ob.observe(e); });
    } else { ro.forEach(function (e) { e.classList.add('visible'); }); }

    // count-up
    var ct = $all('[data-count]');
    if (ct.length && 'IntersectionObserver' in window) {
      var co = new IntersectionObserver(function (e) {
        e.forEach(function (n) {
          if (!n.isIntersecting) return;
          var el = n.target, tg = parseFloat(el.dataset.count), sf = el.dataset.suffix || '', pf = el.dataset.prefix || '',
            dr = 1500, st = performance.now();
          var an = function (now) {
            var pr = Math.min((now - st) / dr, 1), ez = 1 - Math.pow(1 - pr, 3);
            el.textContent = pf + fmt(tg * ez) + sf;
            if (pr < 1) requestAnimationFrame(an);
          };
          requestAnimationFrame(an); co.unobserve(el);
        });
      }, { threshold: .4 });
      ct.forEach(function (e) { co.observe(e); });
    } else { ct.forEach(function (e) { e.textContent = (e.dataset.prefix || '') + fmt(parseFloat(e.dataset.count)) + (e.dataset.suffix || ''); }); }

    // FAQ
    $all('.faq-q').forEach(function (q) {
      q.addEventListener('click', function () { q.parentElement.classList.toggle('open'); });
    });

    // lightbox
    var lb = $('#lightbox');
    if (lb) {
      var lbImg = lb.querySelector('img');
      $all('[data-lb]').forEach(function (m) {
        m.addEventListener('click', function () {
          lbImg.src = m.dataset.lb; lbImg.alt = m.dataset.alt || '';
          lb.classList.add('active'); document.body.style.overflow = 'hidden';
        });
      });
      lb.addEventListener('click', function (e) {
        if (e.target === lb || e.target.classList.contains('lightbox-close')) {
          lb.classList.remove('active'); document.body.style.overflow = '';
        }
      });
    }

    // escape closes overlays
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        $all('.lightbox.active,.legal-overlay.active').forEach(function (o) { o.classList.remove('active'); });
        document.body.style.overflow = '';
      }
    });

    // smooth-scroll for hash links
    $all('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var id = a.getAttribute('href');
        if (id.length < 2) return;
        var t = document.querySelector(id);
        if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth' }); }
      });
    });

    // legal overlays
    initLegal();

    // lead form
    initForm();

    if (window.lucide) lucide.createIcons();
  });

  // ---- COUNTDOWN ----
  function initCountdown() {
    var box = document.getElementById('countdown'); if (!box) return;
    var target = new Date(CONFIG.eventDate).getTime();
    if (isNaN(target)) return;
    var d = document.getElementById('cdDays'), h = document.getElementById('cdHours'),
      m = document.getElementById('cdMins'), s = document.getElementById('cdSecs');
    var timer = setInterval(tick, 1000);
    function tick() {
      var diff = target - Date.now();
      if (diff <= 0) {
        clearInterval(timer);
        box.classList.add('over');
        box.innerHTML = '<div class="cd-cell"><div class="cd-num num accent">Heute ist es so weit.</div><div class="cd-label">FOMO LIVE 26 läuft — wir sehen uns im Raum.</div></div>';
        return;
      }
      var days = Math.floor(diff / 86400000),
        hours = Math.floor(diff % 86400000 / 3600000),
        mins = Math.floor(diff % 3600000 / 60000),
        secs = Math.floor(diff % 60000 / 1000);
      d.textContent = pad(days); h.textContent = pad(hours);
      m.textContent = pad(mins); s.textContent = pad(secs);
    }
    tick();
  }

  // ---- LEAD FORM ----
  function initForm() {
    var form = document.getElementById('leadForm'); if (!form) return;
    var btn = form.querySelector('button[type="submit"]');
    var orig = btn ? btn.innerHTML : '';
    var res = document.getElementById('formResult');

    function show(ok, msg) {
      if (!res) return;
      res.className = 'form-result ' + (ok ? 'ok' : 'err');
      res.textContent = msg;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bot = form.querySelector('[name="botcheck"]');
      if (bot && bot.value) return; // honeypot
      var data = {};
      $all('input,select,textarea', form).forEach(function (f) {
        if (f.name && f.type !== 'checkbox') data[f.name] = f.value.trim();
      });
      data.consent = form.querySelector('[name="consent"]').checked;
      data.source = 'fomo-live-26';

      if (!data.vorname || !data.nachname || !data.email || !data.telefon || !data.consent) {
        show(false, 'Bitte fülle alle Pflichtfelder aus und bestätige den Datenschutz.');
        return;
      }

      if (btn) { btn.disabled = true; btn.innerHTML = 'Wird gesendet …'; }

      // Try optional backend, otherwise graceful fallback (mailto) so it always works live.
      fetch(CONFIG.leadEndpoint, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data)
      }).then(function (r) {
        if (!r.ok) throw new Error('no-backend');
        return r.json();
      }).then(function (j) {
        if (!j || !j.success) throw new Error('fail');
        success();
      }).catch(function () {
        // Fallback: open prefilled email; still confirm to the user.
        fallbackMail(data); success();
      });

      function success() {
        if (btn) { btn.disabled = false; btn.innerHTML = orig; }
        form.reset();
        show(true, 'Deine Platz-Anfrage ist raus! Du bekommst innerhalb von 24 Stunden eine Bestätigung mit allen Details. 📡');
        if (window.lucide) lucide.createIcons();
      }
    });

    function fallbackMail(d) {
      var body = 'Neue Platz-Anfrage für FOMO LIVE 26%0D%0A%0D%0A'
        + 'Name: ' + enc(d.vorname + ' ' + d.nachname) + '%0D%0A'
        + 'E-Mail: ' + enc(d.email) + '%0D%0A'
        + 'Telefon: ' + enc(d.telefon) + '%0D%0A'
        + 'Unternehmen: ' + enc(d.unternehmen || '-') + '%0D%0A'
        + 'Branche: ' + enc(d.branche || '-') + '%0D%0A'
        + 'Plätze: ' + enc(d.plaetze || '1 Person') + '%0D%0A'
        + 'Nachricht: ' + enc(d.nachricht || '-');
      var a = document.createElement('a');
      a.href = 'mailto:' + CONFIG.email + '?subject=' + enc('FOMO LIVE 26 — Platz-Anfrage: ' + d.vorname + ' ' + d.nachname) + '&body=' + body;
      a.style.display = 'none'; document.body.appendChild(a); a.click(); document.body.removeChild(a);
    }
    function enc(s) { return encodeURIComponent(s || ''); }
  }

  // ---- LEGAL OVERLAYS ----
  function initLegal() {
    var content = {
      impressum: '<h2>Impressum</h2><p><strong>Angaben gemäß § 5 TMG</strong></p><p>FOMO Marketing<br>[Inhaber / Firmierung]<br>[Straße &amp; Hausnummer]<br>[PLZ Ort]</p><p><strong>Kontakt</strong><br>E-Mail: event@fomo-marketing.de</p><p style="opacity:.6;font-size:12px;margin-top:18px">Platzhalter — bitte mit den offiziellen Angaben ersetzen.</p>',
      datenschutz: '<h2>Datenschutz</h2><p>Wir nehmen den Schutz deiner Daten ernst. Über dieses Formular übermittelte Angaben (Name, E-Mail, Telefon, Unternehmen, Nachricht) werden ausschließlich zur Bearbeitung deiner Platz-Anfrage für FOMO LIVE 26 verwendet und nicht an unbefugte Dritte weitergegeben.</p><p>Du kannst der Verarbeitung jederzeit widersprechen und die Löschung deiner Daten verlangen — eine formlose E-Mail an event@fomo-marketing.de genügt.</p><p style="opacity:.6;font-size:12px;margin-top:18px">Platzhalter — bitte vor dem Livegang durch eine vollständige Datenschutzerklärung ersetzen.</p>'
    };
    var overlay = document.createElement('div');
    overlay.className = 'legal-overlay';
    overlay.innerHTML = '<div class="legal-content"><button class="legal-close" aria-label="Schließen">&times;</button><div class="legal-body"></div></div>';
    document.body.appendChild(overlay);
    var body = overlay.querySelector('.legal-body');
    $all('[data-legal]').forEach(function (t) {
      t.addEventListener('click', function (e) {
        e.preventDefault();
        body.innerHTML = content[t.dataset.legal] || '';
        overlay.classList.add('active'); document.body.style.overflow = 'hidden';
      });
    });
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay || e.target.classList.contains('legal-close')) {
        overlay.classList.remove('active'); document.body.style.overflow = '';
      }
    });
  }
})();

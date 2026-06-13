/* FOMO LIVE 26 — interactions */
(function () {
  'use strict';

  // ---- CONFIG (bitte mit echten Daten ersetzen) ----
  var CONFIG = {
    whatsapp: '4917675892012',
    waText: 'Hallo FOMO Marketing, ich möchte mir einen Platz bei FOMO LIVE sichern.',
    leadEndpoint: 'api/lead.php' // optional PHP-Backend; faellt sonst auf WhatsApp zurueck
  };

  function $(s, c) { return (c || document).querySelector(s); }
  function $all(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function fmt(n) { return Math.round(n).toLocaleString('de-DE'); }

  document.addEventListener('DOMContentLoaded', function () {
    // year
    var y = $('#year'); if (y) y.textContent = new Date().getFullYear();

    // WhatsApp links
    var waUrl = 'https://wa.me/' + CONFIG.whatsapp + '?text=' + encodeURIComponent(CONFIG.waText);
    $all('[data-wa]').forEach(function (a) { a.href = waUrl; a.target = '_blank'; a.rel = 'noopener'; });

    // marquee: duplicate track for seamless loop
    var mq = document.getElementById('marqueeTrack');
    if (mq) mq.innerHTML += mq.innerHTML;

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
      data.source = 'fomo-live';

      if (!data.vorname || !data.nachname || !data.email || !data.telefon || !data.consent) {
        show(false, 'Bitte fülle alle Pflichtfelder aus und bestätige den Datenschutz.');
        return;
      }

      if (btn) { btn.disabled = true; btn.innerHTML = 'Wird gesendet …'; }

      // Try optional backend, otherwise graceful fallback (WhatsApp) so it always works live.
      fetch(CONFIG.leadEndpoint, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data)
      }).then(function (r) {
        if (!r.ok) throw new Error('no-backend');
        return r.json();
      }).then(function (j) {
        if (!j || !j.success) throw new Error('fail');
        success();
      }).catch(function () {
        // Fallback: open prefilled WhatsApp message; still confirm to the user.
        fallbackWhatsApp(data); success();
      });

      function success() {
        if (btn) { btn.disabled = false; btn.innerHTML = orig; }
        form.reset();
        show(true, 'Deine Platz-Anfrage ist raus! Wir melden uns innerhalb von 24 Stunden — Termin & Location erfährst du als Erstes. 📡');
        if (window.lucide) lucide.createIcons();
      }
    });

    function fallbackWhatsApp(d) {
      var text = 'Platz-Anfrage FOMO LIVE\n\n'
        + 'Name: ' + d.vorname + ' ' + d.nachname + '\n'
        + 'E-Mail: ' + d.email + '\n'
        + 'Telefon: ' + d.telefon + '\n'
        + 'Unternehmen: ' + (d.unternehmen || '-') + '\n'
        + 'Branche: ' + (d.branche || '-') + '\n'
        + 'Plätze: ' + (d.plaetze || '1 Person') + '\n'
        + 'Nachricht: ' + (d.nachricht || '-');
      window.open('https://wa.me/' + CONFIG.whatsapp + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
    }
  }

  // ---- LEGAL OVERLAYS ----
  function initLegal() {
    var content = {
      impressum: '<h2>Impressum</h2><p><strong>Angaben gemäß § 5 TMG</strong></p><p>FOMO Marketing<br>[Inhaber / Firmierung]<br>[Straße &amp; Hausnummer]<br>[PLZ Ort]</p><p><strong>Kontakt</strong><br>WhatsApp: +49 176 75892012</p><p style="opacity:.6;font-size:12px;margin-top:18px">Platzhalter — bitte mit den offiziellen Angaben ersetzen.</p>',
      datenschutz: '<h2>Datenschutz</h2><p>Wir nehmen den Schutz deiner Daten ernst. Über dieses Formular übermittelte Angaben (Name, E-Mail, Telefon, Unternehmen, Nachricht) werden ausschließlich zur Bearbeitung deiner Platz-Anfrage für FOMO LIVE verwendet und nicht an unbefugte Dritte weitergegeben.</p><p>Du kannst der Verarbeitung jederzeit widersprechen und die Löschung deiner Daten verlangen — eine formlose Nachricht per WhatsApp an +49 176 75892012 genügt.</p><p style="opacity:.6;font-size:12px;margin-top:18px">Platzhalter — bitte vor dem Livegang durch eine vollständige Datenschutzerklärung ersetzen.</p>'
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

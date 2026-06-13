/* FOMO Marketing — interactions */
(function () {
  'use strict';

  // ---- CONFIG (bitte mit echten Daten ersetzen) ----
  var CONFIG = {
    whatsapp: '4917675892012',
    waText: 'Hallo FOMO Marketing, ich interessiere mich für euer Angebot — gerne mehr Infos.',
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

    // sticky mobile CTA: show after hero, hide while contact section is visible
    var mcta = document.getElementById('mobileCta');
    if (mcta) {
      var contactVisible = false;
      var contact = document.getElementById('kontakt');
      if ('IntersectionObserver' in window && contact) {
        new IntersectionObserver(function (es) { contactVisible = es[0].isIntersecting; updMcta(); }, { threshold: .12 }).observe(contact);
      }
      var updMcta = function () {
        var pastHero = window.scrollY > window.innerHeight * 0.55;
        mcta.classList.toggle('show', pastHero && !contactVisible);
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
        $all('.lightbox.active,.legal-overlay.active,.fomo-modal.active').forEach(function (o) {
          o.classList.remove('active');
          if (o.classList.contains('fomo-modal')) o.setAttribute('aria-hidden', 'true');
        });
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

    // explainer modal ("Was macht FOMO Marketing?")
    initModal();

    // lead form
    initForm();

  });

  // ---- EXPLAINER MODAL ----
  function initModal() {
    var modal = document.getElementById('fomoModal');
    if (!modal) return;
    function open() {
      modal.classList.add('active');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }
    function close() {
      modal.classList.remove('active');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }
    $all('[data-fm-open]').forEach(function (b) {
      b.addEventListener('click', function (e) { e.preventDefault(); open(); });
    });
    $all('[data-fm-close]', modal).forEach(function (b) {
      b.addEventListener('click', function () { close(); });
    });
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
      data.source = 'fomo-website';

      if (!data.vorname || !data.nachname || !data.telefon || !data.consent) {
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
        show(true, 'Deine Anfrage ist raus! Wir melden uns innerhalb von 24 Stunden persönlich bei dir. 📡');
      }
    });

    function fallbackWhatsApp(d) {
      var text = 'Interessent über die FOMO-Marketing-Website\n\n'
        + 'Name: ' + d.vorname + ' ' + d.nachname + '\n'
        + 'Telefon: ' + d.telefon + '\n'
        + 'E-Mail: ' + (d.email || '-') + '\n'
        + 'Unternehmen: ' + (d.unternehmen || '-') + '\n'
        + 'Branche: ' + (d.branche || '-') + '\n'
        + 'Budget: ' + (d.budget || '-') + '\n'
        + 'Nachricht: ' + (d.nachricht || '-');
      window.open('https://wa.me/' + CONFIG.whatsapp + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
    }
  }

  // ---- LEGAL OVERLAYS ----
  function initLegal() {
    var content = {
      impressum: '<h2>Impressum</h2><p><strong>Angaben gemäß § 5 DDG</strong></p><p>Crusty Slices GmbH<br>Fastradaallee 1<br>52146 Würselen<br>Deutschland</p><p><strong>Vertreten durch</strong><br>die Geschäftsführung der Crusty Slices GmbH</p><p><strong>Kontakt</strong><br>Telefon / WhatsApp: +49 176 75892012</p><p><strong>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</strong><br>Crusty Slices GmbH, Fastradaallee 1, 52146 Würselen</p><p>„FOMO Marketing&quot; ist ein Angebot der Crusty Slices GmbH.</p><p><strong>Haftung für Inhalte</strong><br>Die Inhalte dieser Seite wurden mit größter Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität der Inhalte können wir jedoch keine Gewähr übernehmen. Als Diensteanbieter sind wir gemäß § 7 Abs. 1 DDG für eigene Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich.</p><p><strong>Haftung für Links</strong><br>Unser Angebot enthält ggf. Links zu externen Websites Dritter, auf deren Inhalte wir keinen Einfluss haben. Für diese fremden Inhalte ist stets der jeweilige Anbieter oder Betreiber der Seiten verantwortlich.</p><p><strong>Urheberrecht</strong><br>Die durch den Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem deutschen Urheberrecht. Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der Grenzen des Urheberrechts bedürfen der schriftlichen Zustimmung der Crusty Slices GmbH.</p>',
      datenschutz: '<h2>Datenschutzerklärung</h2><p><strong>1. Verantwortlicher</strong><br>Crusty Slices GmbH, Fastradaallee 1, 52146 Würselen, Deutschland.<br>Kontakt: Telefon / WhatsApp +49 176 75892012.</p><p><strong>2. Allgemeines</strong><br>Wir nehmen den Schutz deiner personenbezogenen Daten ernst und behandeln sie vertraulich sowie entsprechend der Datenschutz-Grundverordnung (DSGVO) und dieser Datenschutzerklärung. Diese Website kommt bewusst ohne Cookies, ohne Tracking- und ohne Analyse-Tools aus. Schriftarten und Icons werden lokal von unserem Server geladen — es werden dafür keine Verbindungen zu Drittanbietern aufgebaut.</p><p><strong>3. Hosting &amp; Server-Logfiles</strong><br>Diese Website wird bei GitHub Pages gehostet (GitHub Inc., 88 Colin P Kelly Jr St, San Francisco, CA 94107, USA). Beim Aufruf der Seite verarbeitet GitHub technisch notwendige Daten wie deine IP-Adresse, Datum und Uhrzeit des Zugriffs, aufgerufene Seite, Browsertyp und Betriebssystem (Server-Logfiles). Die Verarbeitung erfolgt auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an der sicheren und zuverlässigen Bereitstellung der Website). GitHub ist unter dem EU-U.S. Data Privacy Framework zertifiziert. Weitere Informationen: <a href=&quot;https://docs.github.com/site-policy/privacy-policies/github-privacy-statement&quot; target=&quot;_blank&quot; rel=&quot;noopener&quot;>GitHub Privacy Statement</a>.</p><p><strong>4. Interessenten-Formular &amp; WhatsApp</strong><br>Wenn du dich über das Formular einträgst oder uns per WhatsApp schreibst, verarbeiten wir die von dir angegebenen Daten (Vor- und Nachname, Telefonnummer, optional E-Mail-Adresse, Unternehmen, Branche und Nachricht) ausschließlich zur Bearbeitung deiner Anfrage und zur Kontaktaufnahme. Rechtsgrundlage ist deine Einwilligung (Art. 6 Abs. 1 lit. a DSGVO) sowie die Durchführung vorvertraglicher Maßnahmen (Art. 6 Abs. 1 lit. b DSGVO). Deine Daten werden nicht an unbefugte Dritte weitergegeben und gelöscht, sobald sie für den Zweck der Verarbeitung nicht mehr erforderlich sind und keine gesetzlichen Aufbewahrungspflichten entgegenstehen.</p><p><strong>5. Hinweis zu WhatsApp</strong><br>Die Kontaktaufnahme per WhatsApp erfolgt über den Dienst WhatsApp Ireland Ltd. (Meta). Dabei gelten ergänzend die Datenschutzhinweise von WhatsApp. Wenn du das nicht möchtest, nutze bitte das Formular oder rufe uns an.</p><p><strong>6. Deine Rechte</strong><br>Du hast jederzeit das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18) und Datenübertragbarkeit (Art. 20) sowie das Recht, eine erteilte Einwilligung jederzeit mit Wirkung für die Zukunft zu widerrufen (Art. 7 Abs. 3) und der Verarbeitung zu widersprechen (Art. 21). Eine formlose Nachricht an die oben genannten Kontaktdaten genügt.</p><p><strong>7. Beschwerderecht</strong><br>Du hast das Recht, dich bei einer Datenschutz-Aufsichtsbehörde zu beschweren. Zuständig für uns ist die Landesbeauftragte für Datenschutz und Informationsfreiheit Nordrhein-Westfalen (LDI NRW), Kavalleriestraße 2–4, 40213 Düsseldorf.</p><p><strong>Stand:</strong> Juni 2026</p>'
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

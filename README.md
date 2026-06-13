# FOMO LIVE 26 — Event-Landingpage

Conversion-fokussierte Event-Landingpage für **FOMO LIVE 26** — das Live-Event von
**FOMO Marketing × BrandsMarketingLab** für lokale Brands. Aufgebaut nach dem
Qualitätsstandard des BML-Repos, neu interpretiert in der FOMO-Radar-Identität
(dunkel, Radar-Grün, Space-Grotesk-Typo, Radar-Sweep-Animation).

## Stack
- Statisches HTML / CSS / Vanilla JS (kein Build-Step)
- Fonts: Inter + Space Grotesk · Icons: Lucide (CDN)
- Deploy: GitHub Actions → GitHub Pages (Push auf `main`)

## Struktur
```
index.html              Komplette One-Page-Event-Seite (DE) inkl. OG/Twitter-Tags + Event-JSON-LD
css/style.css           Design-System + Komponenten + Responsive + Mobile-Conversion-Bar
js/main.js              Interaktion: Countdown, Reveal, Count-up, Lightbox, FAQ, Formular, Legal
assets/img/             Radar-Logo (SVG), Favicons, OG-Image (1200×630)
assets/proof/           Echte BML-Ergebnis-Screenshots (Referenzen-Sektion)
api/lead.php            Optionales Lead-Backend (nur auf PHP-Hosting; auf Pages inaktiv)
.github/workflows/      Pages-Deployment
```

## Conversion-Elemente
- Live-Countdown bis zum Event + Scarcity (100 Plätze, Vergabe auf Anfrage)
- Echte BML-Referenzen mit Original-Screenshots + Lightbox als Social Proof
- Agenda-Timeline, „Für wen"-Qualifizierung, FAQ gegen Einwände
- Platz-Anfrage-Formular mit Honeypot + automatischem E-Mail-Fallback
- Sticky Mobile-CTA-Bar (WhatsApp + Platz sichern), Scroll-Progress
- OG/Twitter-Cards mit eigenem 1200×630-Share-Image + schema.org-Event (Rich Results)

## ⚠️ Vor dem echten Livegang ersetzen (Platzhalter)
In `js/main.js` (`CONFIG`):
- `eventDate` → finales Event-Datum (aktuell: 24.09.2026, 18:30)
- `whatsapp` → echte WhatsApp-Nummer (Format `49170…`, ohne + / 00)
- `email` → echte Event-E-Mail

Außerdem:
- **Radar-Logo:** `assets/img/logo-radar.svg` ist ein Platzhalter im Stil des
  finalen Logos. Sobald das echte Radar-Logo (mit Branding) hochgeladen ist,
  einfach unter `assets/img/` ablegen und die `logo-radar.svg`-Referenzen in
  `index.html` tauschen — OG-Image & Favicons dann ebenfalls neu erzeugen.
- Datum/Uhrzeit/Stadt in `index.html` (Hero-Meta, JSON-LD, OG-Tags) und im OG-Image
- Bei eigener Domain: `og:url`, `canonical` und absolute OG-Image-URLs anpassen
- Impressum & vollständige Datenschutzerklärung (Overlay-Texte in `js/main.js` → `initLegal`)

## Live
GitHub Pages: https://elevo-business.github.io/fomomarketing/

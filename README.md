# FOMO LIVE — Event-Landingpage

Conversion-fokussierte Event-Landingpage für **FOMO LIVE** — das Live-Event von
**FOMO Marketing × BrandsMarketingLab** für lokale Brands. Aufgebaut nach dem
Qualitätsstandard des BML-Repos, im FOMO-Branding (dunkles Espresso, Beige,
Cognac-Akzent, Cinzel-Typo, Radar-Sweep-Animation).

Bewusst **ohne Datum/Uhrzeit**: Termin & Location erfahren nur die, die auf der
Liste stehen — die Seite hat ein einziges Ziel: Platz-Anfragen (Leads) einsammeln.

## Stack
- Statisches HTML / CSS / Vanilla JS (kein Build-Step)
- Fonts: Cinzel + Inter · Icons: Lucide (CDN)
- Deploy: GitHub Actions → GitHub Pages (Push auf `main`)

## Struktur
```
index.html              Komplette One-Page-Event-Seite (DE) inkl. OG/Twitter-Tags + JSON-LD
css/style.css           Design-System + Komponenten + Responsive + Mobile-Conversion-Bar
js/main.js              Interaktion: Reveal, Count-up, Lightbox, FAQ, Formular, Legal
assets/img/             Radar-Logo (SVG, Beige), Favicons, OG-Image (1200×630)
assets/proof/           Echte BML-Ergebnis-Screenshots (Referenzen-Sektion)
api/lead.php            Optionales Lead-Backend (nur auf PHP-Hosting; auf Pages inaktiv)
.github/workflows/      Pages-Deployment
```

## Conversion-Elemente
- Scarcity ohne Datum: 100 Plätze, Vergabe nur auf Anfrage, „die Liste erfährt alles zuerst"
- Echte BML-Referenzen mit Original-Screenshots + Lightbox als Social Proof
- Programm-Ablauf (nummeriert, ohne Uhrzeiten), „Für wen"-Qualifizierung, FAQ gegen Einwände
- Platz-Anfrage-Formular mit Honeypot + automatischem E-Mail-Fallback
- WhatsApp-Direktanfrage (vorausgefüllt) + Sticky Mobile-CTA-Bar, Scroll-Progress
- OG/Twitter-Cards mit eigenem 1200×630-Share-Image im Branding

## ⚠️ Vor dem echten Livegang ersetzen (Platzhalter)
In `js/main.js` (`CONFIG`):
- `email` → echte Event-E-Mail (aktuell `event@fomo-marketing.de`)
- `whatsapp` ist bereits gesetzt (`4917675892012`)

Außerdem:
- **Radar-Logo:** `assets/img/logo-radar.svg` ist eine Vektor-Nachbildung des
  Original-Logos (Beige-Variante für den dunklen Grund). Liegt das Original als
  Datei vor, einfach unter `assets/img/` ablegen und Referenzen tauschen.
- Bei eigener Domain: `og:url`, `canonical` und absolute OG-Image-URLs anpassen
- Impressum & vollständige Datenschutzerklärung (Overlay-Texte in `js/main.js` → `initLegal`)

## Live
GitHub Pages: https://elevo-business.github.io/fomomarketing/

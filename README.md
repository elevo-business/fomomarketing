# FOMO Marketing — Website

Repräsentative, mobile-first Landingpage für **FOMO Marketing** — gedacht als
QR-Code-Ziel am Ende der Präsentation. Aufgebaut nach dem Qualitätsstandard des
BML-Repos, im FOMO-Branding (monochrom: dunkles Espresso, Beige, Cinzel-Typo,
Radar-Sweep-Animation).

Ziel der Seite: Marke repräsentieren und **Interessenten einsammeln** (Formular
oder WhatsApp). Glasklar und ohne Tricks — wer sich nach der Präsentation für
FOMO Marketing interessiert, trägt sich ein und bekommt in 24 h eine Antwort.
Design: monochrom (dunkles Espresso + Beige, Cinzel), bewusst ohne Akzentfarbe.

## Stack
- Statisches HTML / CSS / Vanilla JS (kein Build-Step)
- Fonts: Cinzel + Inter · Icons: Lucide (CDN)
- Deploy: GitHub Actions → GitHub Pages (Push auf `main`)

## Struktur
```
index.html              Komplette One-Page-Seite (DE) inkl. OG/Twitter-Tags + JSON-LD
css/style.css           Design-System + Komponenten + Responsive + Mobile-Conversion-Bar
js/main.js              Interaktion: Reveal, Count-up, Lightbox, FAQ, Formular, Legal
assets/img/             Radar-Logo (SVG, Beige), Favicons, OG-Image (1200×630)
assets/proof/           Echte BML-Ergebnis-Screenshots (Referenzen-Sektion)
api/lead.php            Optionales Lead-Backend (nur auf PHP-Hosting; auf Pages inaktiv)
.github/workflows/      Pages-Deployment
```

## Conversion-Elemente
- Schlankes Interessenten-Formular (Telefon Pflicht, E-Mail optional),
  Honeypot + automatischem WhatsApp-Fallback (keine E-Mail nötig)
- Echte Referenzen mit Original-Screenshots + Lightbox als Social Proof —
  auf Mobile als Swipe-Karussell
- „Für wen"-Qualifizierung und FAQ gegen die typischen Einwände
- WhatsApp-Direktanfrage (vorausgefüllt) + Sticky Mobile-CTA-Bar, Scroll-Progress
- Mobile-first: kompakte Sektionen, 16px-Inputs (kein iOS-Zoom), Safe-Area-Insets,
  Reduced-Motion-Support, ruhige Animationen auf kleinen Screens
- OG/Twitter-Cards mit eigenem 1200×630-Share-Image im Branding

## ⚠️ Vor dem echten Livegang ersetzen (Platzhalter)
Leads laufen komplett über WhatsApp (`4917675892012`, gesetzt in `js/main.js` →
`CONFIG`). Es gibt bewusst keine E-Mail-Adresse — falls später eine existiert,
auf PHP-Hosting die Umgebungsvariable `FOMO_LEAD_EMAIL` setzen (`api/lead.php`).

Außerdem:
- **Radar-Logo:** `assets/img/logo-radar.svg` ist eine Vektor-Nachbildung des
  Original-Logos (Beige-Variante für den dunklen Grund). Liegt das Original als
  Datei vor, einfach unter `assets/img/` ablegen und Referenzen tauschen.
- Bei eigener Domain: `og:url`, `canonical` und absolute OG-Image-URLs anpassen
- Impressum & vollständige Datenschutzerklärung (Overlay-Texte in `js/main.js` → `initLegal`)

## Live
GitHub Pages: https://elevo-business.github.io/fomomarketing/

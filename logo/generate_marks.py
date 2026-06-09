# -*- coding: utf-8 -*-
"""
FOMO MARKETING – Logo-Konzepte: BILDMARKEN / EMBLEME
Eigenstaendige Symbol-Logos im Geist von Audi (4 Ringe), VW (Monogramm im
Kreis) oder Mastercard (Kreise) – man erkennt die Marke als ZEICHEN, ohne sie
lesen zu muessen. Darunter jeweils die FOMO-Wortmarke (wie bei den Vorbildern).
"""
import io, math
import cairosvg
from pypdf import PdfWriter, PdfReader

from generate import draw_word, word_width, tagline, card, swatches, wrap, esc, FONT, W, H_PAGE


def _pol(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def arc(cx, cy, r, a0, a1, color, w, cap="round"):
    x0, y0 = _pol(cx, cy, r, a0)
    x1, y1 = _pol(cx, cy, r, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return (f'<path d="M {x0:.2f} {y0:.2f} A {r:.2f} {r:.2f} 0 {large} 1 {x1:.2f} {y1:.2f}" '
            f'fill="none" stroke="{color}" stroke-width="{w:.2f}" stroke-linecap="{cap}"/>')


def ring(cx, cy, r, color, w):
    return f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="none" stroke="{color}" stroke-width="{w:.2f}"/>'


def disc(cx, cy, r, color, op=1.0):
    return f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{color}" opacity="{op}"/>'


# ---------------------------------------------------------------------------
# Bildmarken
# ---------------------------------------------------------------------------
def mark_four_rings(cx, cy, ink, accent):
    """Audi-Hommage: 4 ineinandergreifende Ringe (= die 4 Buchstaben von FOMO),
       abwechselnd in Markenfarbe und Gold."""
    r, w, d = 56, 8.5, 74
    cols = [ink, accent, ink, accent]
    out = []
    for i in range(4):
        out.append(ring(cx + (i - 1.5) * d, cy, r, cols[i], w))
    return "".join(out)


def mark_monogram(cx, cy, ink, accent):
    """VW-Hommage: bold 'F'-Monogramm in einem Siegel-Kreis."""
    R = 108
    out = [disc(cx, cy, R, ink), ring(cx, cy, R - 12, accent, 2.2)]
    Hf, t = 116, 23
    al = Hf * 0.62
    left = cx - al / 2
    top = cy - Hf / 2
    out.append(f'<rect x="{left:.1f}" y="{top:.1f}" width="{t}" height="{Hf}" fill="{accent}"/>')          # Stamm
    out.append(f'<rect x="{left:.1f}" y="{top:.1f}" width="{al:.1f}" height="{t}" fill="{accent}"/>')        # oberer Arm
    out.append(f'<rect x="{left:.1f}" y="{cy-t/2:.1f}" width="{al*0.8:.1f}" height="{t}" fill="{accent}"/>')  # Mittelarm
    return "".join(out)


def mark_twin(cx, cy, ink, accent):
    """Mastercard-Hommage: zwei ueberlappende Kreise (die OO von fOmO) –
       die Schnittmenge ist der 'FOMO-Moment'."""
    r, off = 74, 42
    out = [disc(cx - off, cy, r, ink, 0.92), disc(cx + off, cy, r, accent, 0.92)]
    return "".join(out)


def mark_open(cx, cy, ink, accent):
    """Offener Kreis mit Punkt: in den Kreis eintreten – nichts verpassen."""
    R, w = 96, 11
    out = [arc(cx, cy, R, -52, 256, accent, w)]           # Ring mit Luecke oben rechts
    px, py = _pol(cx, cy, R, -18)
    out.append(disc(px, py, 17, ink))                      # Punkt an der Oeffnung
    return "".join(out)


def mark_bullseye(cx, cy, ink, accent):
    """Ziel/Orbit: im Zentrum der Aufmerksamkeit stehen."""
    out = [ring(cx, cy, 100, accent, 9),
           ring(cx, cy, 64, ink, 6),
           disc(cx, cy, 20, accent)]
    bx, by = _pol(cx, cy, 100, -60)
    out.append(disc(bx, by, 13, ink))                      # umlaufender Punkt
    return "".join(out)


def mark_pinwheel(cx, cy, ink, accent):
    """Vier Bogensegmente (F-O-M-O) fuegen sich zu EINEM Kreis – das Ganze,
       das man nicht verpassen will."""
    R, w, gap = 96, 15, 12
    cols = [ink, accent, ink, accent]
    out = []
    for i in range(4):
        a0 = -90 + i * 90 + gap / 2
        a1 = -90 + (i + 1) * 90 - gap / 2
        out.append(arc(cx, cy, R, a0, a1, cols[i], w, cap="round"))
    return "".join(out)


MARKS = dict(four=mark_four_rings, monogram=mark_monogram, twin=mark_twin,
             open=mark_open, bullseye=mark_bullseye, pinwheel=mark_pinwheel)


# ---------------------------------------------------------------------------
CONCEPTS = [
    dict(num="M1", name="VIER RINGE", tline="Audi-Prinzip: 4 = F·O·M·O",
         mark="four", primary="#0B1F3A", accent="#C9A24B",
         light_bg="#F7F3EA", dark_bg="#0B1F3A", dark_ink="#F1E9D6",
         desc="Vier ineinandergreifende Ringe stehen fuer die vier Buchstaben "
              "F-O-M-O und fuer Verbindung. Wie bei Audi sofort als Zeichen "
              "erkennbar – abwechselnd Marineblau und Gold machen es eigenstaendig."),
    dict(num="M2", name="F-SIEGEL", tline="VW-Prinzip: Monogramm im Kreis",
         mark="monogram", primary="#15110C", accent="#C9A24B",
         light_bg="#F4F1EA", dark_bg="#15110C", dark_ink="#EFE6D2",
         desc="Ein bold gesetztes 'F' in einem Siegel-Kreis – ein klassisches "
              "Monogramm-Emblem wie das VW-Zeichen. Schwarz-Gold wirkt wie ein "
              "Premium-Stempel und funktioniert in jeder Groesse."),
    dict(num="M3", name="DOPPEL-O", tline="Mastercard-Prinzip: zwei Kreise",
         mark="twin", primary="#0B1F3A", accent="#C9A24B",
         light_bg="#F7F3EA", dark_bg="#0B1F3A", dark_ink="#F1E9D6",
         desc="Zwei ueberlappende Kreise greifen die beiden O's von FOMO auf. "
              "Die Schnittmenge ist der Moment, den man nicht verpassen will. "
              "Reduziert, freundlich und extrem einpraegsam."),
    dict(num="M4", name="DER KREIS", tline="Eintreten – nichts verpassen",
         mark="open", primary="#0E3B2E", accent="#CDA75A",
         light_bg="#F1EEE3", dark_bg="#0A241B", dark_ink="#E9E3D2",
         desc="Ein offener Ring mit einem Punkt an der Oeffnung: der Schritt "
              "hinein in den Kreis – das Gegenteil von 'aussen vor sein'. Ein "
              "Symbol, das die Idee von FOMO direkt erzaehlt."),
    dict(num="M5", name="BULLSEYE", tline="Im Zentrum der Aufmerksamkeit",
         mark="bullseye", primary="#5E1F2E", accent="#C2A14A",
         light_bg="#F6EFE9", dark_bg="#2A0F16", dark_ink="#EBD9C7",
         desc="Konzentrische Ringe mit Mittelpunkt – das Ziel, der Fokus, das "
              "Zentrum. Steht dafuer, Marken ins Rampenlicht zu ruecken. "
              "Oxblood und Gold geben einen souveraenen, edlen Auftritt."),
    dict(num="M6", name="QUARTETT", tline="Vier Boegen werden ein Kreis",
         mark="pinwheel", primary="#0B1F3A", accent="#C9A24B",
         light_bg="#F7F3EA", dark_bg="#0B1F3A", dark_ink="#F1E9D6",
         desc="Vier Bogensegmente (F-O-M-O) fuegen sich zu einem vollstaendigen "
              "Kreis – das Ganze, das man nicht verpassen will. Dynamisch, modern "
              "und als Zeichen sofort wiedererkennbar."),
]


def lockup(c, cx, cy, scale, ink, accent, tagcol, tag=True):
    out = [f'<g transform="translate({cx:.1f} {cy:.1f}) scale({scale}) translate({-cx:.1f} {-cy:.1f})">',
           MARKS[c["mark"]](cx, cy, ink, accent), '</g>']
    if tag:
        wmH = 54 * scale
        ww = word_width("FOMO", wmH)
        wy = cy + 150 * scale
        out.append(draw_word("FOMO", cx - ww / 2, wy, wmH, wmH * 0.1, ink, accent, "butt", "plain"))
        out.append(tagline(cx, wy + wmH + wmH * 0.5, wmH * 0.34, tagcol, spacing=wmH * 0.34 * 0.62))
    return "".join(out)


def concept_page(c):
    gold = c["accent"]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H_PAGE}" '
         f'viewBox="0 0 {W} {H_PAGE}">',
         '<defs><filter id="soft" x="-20%" y="-20%" width="140%" height="140%">'
         '<feDropShadow dx="0" dy="6" stdDeviation="14" flood-color="#000" flood-opacity="0.12"/>'
         '</filter></defs>',
         f'<rect width="{W}" height="{H_PAGE}" fill="#FBFAF7"/>']
    p.append(f'<text x="80" y="86" font-family="{FONT}" font-size="20" font-weight="800" '
             f'letter-spacing="4" fill="{c["primary"]}">FOMO MARKETING</text>')
    p.append(f'<text x="80" y="112" font-family="{FONT}" font-size="13" letter-spacing="3" '
             f'fill="#999">LOGO-KONZEPT {c["num"]} &#183; BILDMARKE / EMBLEM</text>')
    p.append(f'<text x="{W-80}" y="92" font-family="{FONT}" font-size="44" font-weight="800" '
             f'text-anchor="end" fill="{c["primary"]}">{esc(c["name"])}</text>')
    p.append(f'<text x="{W-80}" y="116" font-family="{FONT}" font-size="14" font-style="italic" '
             f'text-anchor="end" fill="#888">{esc(c["tline"])}</text>')
    p.append(f'<line x1="80" y1="138" x2="{W-80}" y2="138" stroke="{gold}" stroke-width="2"/>')

    cw, ch, cy = 580, 560, 178
    lx, rx = 90, 730
    p.append(card(lx, cy, cw, ch, c["light_bg"], stroke="#0000000f"))
    p.append(card(rx, cy, cw, ch, c["dark_bg"]))
    mcy = cy + 190
    p.append(lockup(c, lx + cw / 2, mcy, 1.0, c["primary"], gold, c["primary"]))
    p.append(lockup(c, rx + cw / 2, mcy, 1.0, c["dark_ink"], gold, c["dark_ink"]))

    p.append(f'<text x="{lx+20}" y="{cy+ch-18}" font-family="{FONT}" font-size="12" '
             f'letter-spacing="2" fill="#aaa">HELLER UNTERGRUND</text>')
    p.append(f'<text x="{rx+20}" y="{cy+ch-18}" font-family="{FONT}" font-size="12" '
             f'letter-spacing="2" fill="#ffffff66">DUNKLER UNTERGRUND</text>')

    fy = cy + ch + 44
    for i, ln in enumerate(wrap(c["desc"], 96)):
        p.append(f'<text x="80" y="{fy+i*22}" font-family="{FONT}" font-size="15" '
                 f'fill="#333">{esc(ln)}</text>')
    pal = [(c["primary"], "PRIMAER"), (gold, "AKZENT"),
           (c["light_bg"], "HELL"), (c["dark_bg"], "DUNKEL")]
    p.append(swatches(812, fy - 14, pal))
    p.append('</svg>')
    return "".join(p)


def cover_page():
    c = CONCEPTS[0]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H_PAGE}" '
         f'viewBox="0 0 {W} {H_PAGE}">',
         f'<rect width="{W}" height="{H_PAGE}" fill="{c["dark_bg"]}"/>']
    p.append(lockup(c, W / 2, H_PAGE / 2 - 40, 1.5, c["dark_ink"], c["accent"], c["accent"]))
    p.append(f'<text x="{W/2}" y="{H_PAGE-160}" font-family="{FONT}" font-size="15" '
             f'letter-spacing="4" text-anchor="middle" fill="{c["dark_ink"]}">'
             f'BILDMARKEN &#183; 6 EMBLEME</text>')
    p.append(f'<text x="80" y="{H_PAGE-50}" font-family="{FONT}" font-size="13" '
             f'letter-spacing="2" fill="#ffffff55">FOMO MARKETING</text>')
    p.append(f'<text x="{W-80}" y="{H_PAGE-50}" font-family="{FONT}" font-size="13" '
             f'letter-spacing="2" text-anchor="end" fill="#ffffff55">09.06.2026</text>')
    p.append('</svg>')
    return "".join(p)


def overview_page():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H_PAGE}" '
         f'viewBox="0 0 {W} {H_PAGE}">',
         '<defs><filter id="soft" x="-20%" y="-20%" width="140%" height="140%">'
         '<feDropShadow dx="0" dy="6" stdDeviation="14" flood-color="#000" flood-opacity="0.12"/>'
         '</filter></defs>',
         f'<rect width="{W}" height="{H_PAGE}" fill="#FBFAF7"/>']
    p.append(f'<text x="80" y="86" font-family="{FONT}" font-size="20" font-weight="800" '
             f'letter-spacing="4" fill="#0B1F3A">FOMO MARKETING</text>')
    p.append(f'<text x="80" y="112" font-family="{FONT}" font-size="13" letter-spacing="3" '
             f'fill="#999">UEBERSICHT &#183; BILDMARKEN</text>')
    p.append(f'<line x1="80" y1="138" x2="{W-80}" y2="138" stroke="#0B1F3A" stroke-width="2"/>')
    cw, ch = 400, 250
    xs, ys = [90, 510, 930], [180, 490]
    for i, c in enumerate(CONCEPTS):
        gx, gy = xs[i % 3], ys[i // 3]
        p.append(card(gx, gy, cw, ch, c["light_bg"], stroke="#0000000f"))
        cx, cyc = gx + cw / 2, gy + ch / 2 - 24
        p.append(lockup(c, cx, cyc, 0.62, c["primary"], c["accent"], c["primary"], tag=False))
        p.append(f'<text x="{gx+18}" y="{gy+ch-16}" font-family="{FONT}" font-size="13" '
                 f'font-weight="800" letter-spacing="1.5" fill="{c["primary"]}">{c["num"]} {esc(c["name"])}</text>')
    p.append('</svg>')
    return "".join(p)


def main():
    pages = [("MK0_cover", cover_page())]
    for c in CONCEPTS:
        pages.append((f'{c["num"]}_{c["mark"]}', concept_page(c)))
    pages.append(("MK9_overview", overview_page()))
    writer = PdfWriter()
    for name, svg in pages:
        with open(f"logo/svg/{name}.svg", "w") as f:
            f.write(svg)
        pdf = cairosvg.svg2pdf(bytestring=svg.encode(), output_width=W * 2, output_height=H_PAGE * 2)
        writer.append(PdfReader(io.BytesIO(pdf)))
        print("ok:", name)
    with open("logo/FOMO_Marketing_Logo_Konzepte_Bildmarken.pdf", "wb") as f:
        writer.write(f)
    print("PDF: logo/FOMO_Marketing_Logo_Konzepte_Bildmarken.pdf")


if __name__ == "__main__":
    main()

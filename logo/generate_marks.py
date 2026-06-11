# -*- coding: utf-8 -*-
"""
FOMO MARKETING – Bildmarken in der BULLSEYE-RICHTUNG (Kreis / Ziel / Fokus)
Facettenreiches Entwurfsblatt: mehrere kreisfoermige Marken-FORMEN zur Auswahl,
monochrom-edel. Hauptfarbe Weinrot & Beige plus weitere edle Farbvarianten.
Hochwertige, seriöse Grotesk-Wortmarke.
"""
import io, math
import cairosvg
from pypdf import PdfWriter, PdfReader

from generate import (draw_word, word_width, tagline, card, swatches, wrap, esc,
                      FONT, W, H_PAGE)

WEIGHT = 0.135


def _pol(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def arc(cx, cy, r, a0, a1, color, w, cap="round"):
    x0, y0 = _pol(cx, cy, r, a0)
    x1, y1 = _pol(cx, cy, r, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return (f'<path d="M {x0:.2f} {y0:.2f} A {r:.2f} {r:.2f} 0 {large} 1 {x1:.2f} {y1:.2f}" '
            f'fill="none" stroke="{color}" stroke-width="{w:.2f}" stroke-linecap="{cap}"/>')


def _ring(cx, cy, r, c, w):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{c}" stroke-width="{w:.1f}"/>'


def _dot(cx, cy, r, c):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{c}"/>'


def _line(x1, y1, x2, y2, c, w):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w:.1f}" stroke-linecap="round"/>'


# ---------------------------------------------------------------------------
# Marken-Formen (monochrom – funktionieren in zwei Farben: Marke + Beige)
# ---------------------------------------------------------------------------
def m_bullseye(cx, cy, ink):
    bx, by = _pol(cx, cy, 100, -58)
    return (_ring(cx, cy, 100, ink, 9) + _ring(cx, cy, 62, ink, 5)
            + _dot(cx, cy, 15, ink) + _dot(bx, by, 10, ink))


def m_crosshair(cx, cy, ink):
    out = [_ring(cx, cy, 90, ink, 8), _dot(cx, cy, 9, ink)]
    for ang in (-90, 0, 90, 180):
        x1, y1 = _pol(cx, cy, 58, ang)
        x2, y2 = _pol(cx, cy, 118, ang)
        out.append(_line(x1, y1, x2, y2, ink, 6))
    return "".join(out)


def m_open(cx, cy, ink):
    px, py = _pol(cx, cy, 100, -18)
    return arc(cx, cy, 100, -52, 256, ink, 11) + _dot(px, py, 16, ink)


def m_twin(cx, cy, ink):
    return _ring(cx - 40, cy, 72, ink, 9) + _ring(cx + 40, cy, 72, ink, 9)


def m_pinwheel(cx, cy, ink):
    out, gap = [], 13
    for i in range(4):
        a0 = -90 + i * 90 + gap / 2
        a1 = -90 + (i + 1) * 90 - gap / 2
        out.append(arc(cx, cy, 96, a0, a1, ink, 15))
    return "".join(out)


def m_radar(cx, cy, ink):
    sx, sy = _pol(cx, cy, 100, -52)
    return (_ring(cx, cy, 100, ink, 7) + _ring(cx, cy, 68, ink, 4) + _ring(cx, cy, 36, ink, 4)
            + _dot(cx, cy, 7, ink) + _line(cx, cy, sx, sy, ink, 5) + _dot(sx, sy, 10, ink))


MARKS = dict(bullseye=m_bullseye, crosshair=m_crosshair, open=m_open,
             twin=m_twin, pinwheel=m_pinwheel, radar=m_radar)


# ---------------------------------------------------------------------------
BEIGE_DK = "#E7DBC2"
CONCEPTS = [
    dict(num="C1", name="BULLSEYE", tline="Weinrot & Beige – im Zentrum",
         mark="bullseye", primary="#6E2433", light_bg="#F0E8D8", dark_bg="#3A111B", dark_ink="#EBDFC8",
         font="Poppins SemiBold", fweight=600, fsize=92, ftrack=6, fontname="Poppins",
         desc="Der Favorit: konzentrische Ringe als Ziel – im Zentrum der "
              "Aufmerksamkeit. Schrift: Poppins (geometrische Grotesk), modern "
              "und premium. Tiefes Weinrot auf warmem Beige."),
    dict(num="C2", name="CROSSHAIR", tline="Marineblau & Beige – Praezision",
         mark="crosshair", primary="#1C2A44", light_bg="#ECE6DA", dark_bg="#111C30", dark_ink="#E7DBC2",
         font="Oswald", fweight=600, fsize=104, ftrack=7, fontname="Oswald",
         desc="Ein Fadenkreuz mit Zielring – Genauigkeit und Fokus. Schrift: "
              "Oswald (schmale, bestimmte Grotesk), technisch und selbstbewusst. "
              "Marineblau auf Beige."),
    dict(num="C3", name="ENTER", tline="Tannengruen & Beige – eintreten",
         mark="open", primary="#1F3D2F", light_bg="#EAE6D6", dark_bg="#122619", dark_ink="#E7DDC6",
         font="Playfair Display", fweight=700, fsize=92, ftrack=3, fontname="Playfair Display",
         desc="Ein offener Ring mit Punkt: der Schritt hinein in den Kreis. "
              "Schrift: Playfair Display (eleganter Didone-Serif), luxurioes und "
              "redaktionell. Tannengruen auf Beige."),
    dict(num="C4", name="TWIN", tline="Pflaume & Beige – Verbindung",
         mark="twin", primary="#3A2440", light_bg="#ECE5DA", dark_bg="#221329", dark_ink="#E9DFD2",
         font="Josefin Sans", fweight=600, fsize=98, ftrack=7, fontname="Josefin Sans",
         slogans=["Don't watch the trend. Be it.",
                  "The organic dopamine.",
                  "If you're not on the feed, you don't exist."],
         desc="Zwei ueberlappende Ringe – die beiden O's von FOMO. Schrift: "
              "Josefin Sans (geometrisch, Art-Deco-Anmutung), elegant und leicht. "
              "Pflaumen-Violett auf Beige."),
    dict(num="C5", name="QUARTETT", tline="Petrol & Beige – vier werden eins",
         mark="pinwheel", primary="#163B40", light_bg="#E8E6DC", dark_bg="#0C2528", dark_ink="#E3DDCB",
         font="Lora", fweight=600, fsize=88, ftrack=3, fontname="Lora",
         desc="Vier Bogensegmente fuegen sich zu einem Kreis. Schrift: Lora "
              "(humanistischer Serif), warm und vertrauenswuerdig. Gedecktes "
              "Petrol auf Beige."),
    dict(num="C6", name="RADAR", tline="Espresso & Beige – Aufmerksamkeit",
         mark="radar", primary="#3B2A21", light_bg="#F0E8D7", dark_bg="#221710", dark_ink="#E8DDC8",
         font="Cinzel", fweight=600, fsize=78, ftrack=5, fontname="Cinzel",
         desc="Ein Radar erfasst, was gerade passiert. Schrift: Cinzel (roemische "
              "Versal-Serife), sehr edel und zeitlos. Warmes Espresso-Braun auf "
              "Beige wie feines Leder."),
]


def lockup(cx, cy, scale, ink, tagcol, tag=True):
    fs = _FS[0]
    out = [f'<g transform="translate({cx:.1f} {cy-92*scale:.1f}) scale({scale}) translate({-cx:.1f} {-cy:.1f})">']
    out.append(_current_mark(cx, cy, ink))
    out.append('</g>')
    if tag:
        out.append(f'<text x="{cx:.1f}" y="{cy+96*scale:.1f}" font-family="{fs["font"]}" '
                   f'font-weight="{fs["fweight"]}" font-size="{fs["fsize"]*scale:.1f}" '
                   f'letter-spacing="{fs["ftrack"]*scale:.2f}" '
                   f'text-anchor="middle" fill="{ink}">FOMO</text>')
        out.append(f'<text x="{cx:.1f}" y="{cy+132*scale:.1f}" font-family="Poppins Medium" '
                   f'font-size="{18*scale:.1f}" letter-spacing="{7*scale:.2f}" '
                   f'text-anchor="middle" fill="{tagcol}">MARKETING</text>')
    return "".join(out)


_MARK_FN = [None]
_FS = [None]


def _current_mark(cx, cy, ink):
    return _MARK_FN[0](cx, cy, ink)


def concept_page(c):
    _MARK_FN[0] = MARKS[c["mark"]]
    _FS[0] = c
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H_PAGE}" '
         f'viewBox="0 0 {W} {H_PAGE}">',
         '<defs><filter id="soft" x="-20%" y="-20%" width="140%" height="140%">'
         '<feDropShadow dx="0" dy="6" stdDeviation="14" flood-color="#000" flood-opacity="0.12"/>'
         '</filter></defs>',
         f'<rect width="{W}" height="{H_PAGE}" fill="#FBFAF7"/>']
    p.append(f'<text x="80" y="86" font-family="{FONT}" font-size="20" font-weight="800" '
             f'letter-spacing="4" fill="{c["primary"]}">FOMO MARKETING</text>')
    p.append(f'<text x="80" y="112" font-family="{FONT}" font-size="13" letter-spacing="3" '
             f'fill="#999">ENTWURF {c["num"]} &#183; FORM + SCHRIFT: {esc(c["fontname"].upper())}</text>')
    p.append(f'<text x="{W-80}" y="92" font-family="{FONT}" font-size="42" font-weight="800" '
             f'text-anchor="end" fill="{c["primary"]}">{esc(c["name"])}</text>')
    p.append(f'<text x="{W-80}" y="116" font-family="{FONT}" font-size="14" font-style="italic" '
             f'text-anchor="end" fill="#888">{esc(c["tline"])}</text>')
    p.append(f'<line x1="80" y1="138" x2="{W-80}" y2="138" stroke="{c["primary"]}" stroke-width="2"/>')

    cw, ch, cy = 580, 560, 178
    lx, rx = 90, 730
    p.append(card(lx, cy, cw, ch, c["light_bg"], stroke="#0000000f"))
    p.append(card(rx, cy, cw, ch, c["dark_bg"]))
    ccy = cy + ch / 2
    p.append(lockup(lx + cw / 2, ccy, 1.0, c["primary"], c["primary"]))
    p.append(lockup(rx + cw / 2, ccy, 1.0, c["dark_ink"], c["dark_ink"]))

    p.append(f'<text x="{lx+20}" y="{cy+ch-18}" font-family="{FONT}" font-size="12" '
             f'letter-spacing="2" fill="#aaa">HELLER UNTERGRUND</text>')
    p.append(f'<text x="{rx+20}" y="{cy+ch-18}" font-family="{FONT}" font-size="12" '
             f'letter-spacing="2" fill="#ffffff66">DUNKLER UNTERGRUND</text>')

    fy = cy + ch + 44
    if c.get("slogans"):
        p.append(f'<text x="80" y="{fy-4}" font-family="{FONT}" font-size="12" '
                 f'letter-spacing="3" fill="#999">MARKEN-CLAIMS</text>')
        for i, s in enumerate(c["slogans"]):
            yy = fy + 26 + i * 34
            p.append(f'<rect x="80" y="{yy-15:.0f}" width="4" height="20" fill="{c["primary"]}"/>')
            p.append(f'<text x="100" y="{yy}" font-family="Lora" font-style="italic" '
                     f'font-size="21" fill="{c["primary"]}">{esc(s)}</text>')
    else:
        for i, ln in enumerate(wrap(c["desc"], 96)):
            p.append(f'<text x="80" y="{fy+i*22}" font-family="{FONT}" font-size="15" fill="#333">{esc(ln)}</text>')
    pal = [(c["primary"], "PRIMAER"), (c["light_bg"], "BEIGE / HELL"),
           (c["dark_bg"], "DUNKEL"), (BEIGE_DK, "BEIGE-MARKE")]
    p.append(swatches(812, fy - 14, pal))
    p.append('</svg>')
    return "".join(p)


def cover_page():
    c = CONCEPTS[0]
    _MARK_FN[0] = MARKS[c["mark"]]
    _FS[0] = c
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H_PAGE}" '
         f'viewBox="0 0 {W} {H_PAGE}">',
         f'<rect width="{W}" height="{H_PAGE}" fill="{c["dark_bg"]}"/>']
    p.append(lockup(W / 2, H_PAGE / 2 - 20, 1.7, c["dark_ink"], c["dark_ink"]))
    p.append(f'<text x="{W/2}" y="{H_PAGE-150}" font-family="{FONT}" font-size="15" '
             f'letter-spacing="4" text-anchor="middle" fill="{c["dark_ink"]}">'
             f'BULLSEYE-RICHTUNG &#183; 6 ENTWUERFE</text>')
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
             f'letter-spacing="4" fill="#6E2433">FOMO MARKETING</text>')
    p.append(f'<text x="80" y="112" font-family="{FONT}" font-size="13" letter-spacing="3" '
             f'fill="#999">UEBERSICHT &#183; BULLSEYE-RICHTUNG</text>')
    p.append(f'<line x1="80" y1="138" x2="{W-80}" y2="138" stroke="#6E2433" stroke-width="2"/>')
    cw, ch = 400, 250
    xs, ys = [90, 510, 930], [180, 490]
    for i, c in enumerate(CONCEPTS):
        _MARK_FN[0] = MARKS[c["mark"]]
        _FS[0] = c
        gx, gy = xs[i % 3], ys[i // 3]
        p.append(card(gx, gy, cw, ch, c["light_bg"], stroke="#0000000f"))
        cx, cyc = gx + cw / 2, gy + ch / 2 + 6
        p.append(lockup(cx, cyc, 0.5, c["primary"], c["primary"], tag=True))
        p.append(f'<text x="{gx+18}" y="{gy+ch-16}" font-family="{FONT}" font-size="13" '
                 f'font-weight="800" letter-spacing="1.5" fill="{c["primary"]}">{c["num"]} {esc(c["name"])}</text>')
    p.append('</svg>')
    return "".join(p)


def slogan_page():
    c = next(x for x in CONCEPTS if x["num"] == "C4")
    _MARK_FN[0] = MARKS[c["mark"]]
    _FS[0] = c
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H_PAGE}" '
         f'viewBox="0 0 {W} {H_PAGE}">',
         '<defs><filter id="soft" x="-20%" y="-20%" width="140%" height="140%">'
         '<feDropShadow dx="0" dy="6" stdDeviation="14" flood-color="#000" flood-opacity="0.12"/>'
         '</filter></defs>',
         f'<rect width="{W}" height="{H_PAGE}" fill="#FBFAF7"/>']
    p.append(f'<text x="80" y="86" font-family="{FONT}" font-size="20" font-weight="800" '
             f'letter-spacing="4" fill="{c["primary"]}">FOMO MARKETING</text>')
    p.append(f'<text x="80" y="112" font-family="{FONT}" font-size="13" letter-spacing="3" '
             f'fill="#999">ENTWURF C4 TWIN &#183; LOGO MIT CLAIM (EINZELN)</text>')
    p.append(f'<text x="{W-80}" y="92" font-family="{FONT}" font-size="42" font-weight="800" '
             f'text-anchor="end" fill="{c["primary"]}">TWIN + CLAIM</text>')
    p.append(f'<line x1="80" y1="138" x2="{W-80}" y2="138" stroke="{c["primary"]}" stroke-width="2"/>')

    xs = [70, 495, 920]
    cw, cy, ch = 410, 240, 500
    scale = 0.92
    for i, s in enumerate(c["slogans"]):
        gx = xs[i]
        cx = gx + cw / 2
        p.append(card(gx, cy, cw, ch, c["light_bg"], stroke="#0000000f"))
        cylock = cy + ch / 2 - 6
        p.append(lockup(cx, cylock, scale, c["primary"], c["primary"]))
        sy = cylock + 132 * scale + 42
        for j, ln in enumerate(wrap(s, 22)):
            p.append(f'<text x="{cx:.0f}" y="{sy+j*30:.0f}" font-family="Lora" font-style="italic" '
                     f'font-size="22" text-anchor="middle" fill="{c["primary"]}">{esc(ln)}</text>')
    p.append('</svg>')
    return "".join(p)


def radar_claim_page():
    c = next(x for x in CONCEPTS if x["num"] == "C6")
    _MARK_FN[0] = MARKS[c["mark"]]
    _FS[0] = c
    cy, scale = H_PAGE / 2 - 30, 1.5
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H_PAGE}" '
         f'viewBox="0 0 {W} {H_PAGE}">',
         f'<rect width="{W}" height="{H_PAGE}" fill="{c["light_bg"]}"/>']
    p.append(lockup(W / 2, cy, scale, c["primary"], c["primary"]))
    mk = cy + 132 * scale
    p.append(f'<line x1="{W/2-46:.0f}" y1="{mk+54:.0f}" x2="{W/2+46:.0f}" y2="{mk+54:.0f}" '
             f'stroke="{c["primary"]}" stroke-width="1.2"/>')
    claim = "DON'T WATCH THE TREND… BE IT!"
    p.append(f'<text x="{W/2:.0f}" y="{mk+98:.0f}" font-family="Cinzel" font-weight="600" '
             f'font-size="27" letter-spacing="6" text-anchor="middle" fill="{c["primary"]}">{esc(claim)}</text>')
    p.append('</svg>')
    return "".join(p)


def main():
    pages = [("MK0_cover", cover_page())]
    for c in CONCEPTS:
        pages.append((f'{c["num"]}_{c["mark"]}', concept_page(c)))
        if c["num"] == "C4":
            pages.append(("C4_claims", slogan_page()))
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

    # Eigenstaendiges Dokument: nur "Twin + Claim"
    only = PdfWriter()
    only.append(PdfReader(io.BytesIO(
        cairosvg.svg2pdf(bytestring=slogan_page().encode(), output_width=W * 2, output_height=H_PAGE * 2))))
    with open("logo/FOMO_Marketing_Twin_Claim.pdf", "wb") as f:
        only.write(f)
    print("PDF: logo/FOMO_Marketing_Twin_Claim.pdf")

    # Eigenstaendiges Dokument: Radar (C6) mit Claim
    rc = PdfWriter()
    rsvg = radar_claim_page()
    with open("logo/svg/C6_radar_claim.svg", "w") as f:
        f.write(rsvg)
    rc.append(PdfReader(io.BytesIO(
        cairosvg.svg2pdf(bytestring=rsvg.encode(), output_width=W * 2, output_height=H_PAGE * 2))))
    with open("logo/FOMO_Marketing_Radar_Claim.pdf", "wb") as f:
        rc.write(f)
    print("PDF: logo/FOMO_Marketing_Radar_Claim.pdf")


if __name__ == "__main__":
    main()

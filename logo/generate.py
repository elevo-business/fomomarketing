# -*- coding: utf-8 -*-
"""
FOMO MARKETING – Logo-Konzept-Generator
Erzeugt 6 differenzierte Logo-Entwuerfe als Vektorgrafiken (SVG) und
fuehrt sie zu einer Praesentations-PDF zusammen.

Designidee: Die symmetrische Buchstabengruppe  O · M · O  ist das visuelle
Herz von "F-OMO". Beide O's erhalten pro Konzept eine eigene, unverwechselbare
Behandlung und bilden so eine ruhige, gespiegelte Komposition.
"""
import math, io
import cairosvg
from pypdf import PdfWriter, PdfReader

W, H_PAGE = 1400, 990          # A4-Querformat-Verhaeltnis (1.414)
FONT = "Liberation Sans, Arial, DejaVu Sans, sans-serif"

# ----------------------------------------------------------------------------
# Buchstaben-Bausteine (monolineare, geometrische Eigenkonstruktion)
# ----------------------------------------------------------------------------
F_W, O_W, M_W, GAP = 0.56, 1.0, 0.56, 0.18   # Breiten / Abstand relativ zu Versalhoehe (M = F)


def _attrs(ink, w, cap):
    return (f'fill="none" stroke="{ink}" stroke-width="{w:.2f}" '
            f'stroke-linecap="{cap}" stroke-linejoin="{"round" if cap=="round" else "miter"}" '
            f'stroke-miterlimit="8"')


def letter_F(x, y, H, w, ink, cap):
    xs = x + w / 2
    arm = x + F_W * H
    s = (f'<path {_attrs(ink,w,cap)} d="'
         f'M {xs:.2f} {y:.2f} L {xs:.2f} {y+H:.2f} '
         f'M {xs:.2f} {y+w/2:.2f} L {arm:.2f} {y+w/2:.2f} '
         f'M {xs:.2f} {y+H*0.5:.2f} L {x+F_W*H*0.84:.2f} {y+H*0.5:.2f}"/>')
    return s, F_W * H


def _o_ring(cx, cy, r, w, ink, cap):
    return f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" {_attrs(ink,w,cap)}/>'


def letter_O(x, y, H, w, ink, accent, cap, treat):
    cx, cy = x + O_W * H / 2, y + H / 2
    R = H / 2 - w / 2
    out = [_o_ring(cx, cy, R, w, ink, cap)]

    if treat == "pulse":                                   # Radar / Signal
        out.append(_o_ring(cx, cy, R * 0.62, w * 0.7, accent, cap))
        out.append(_o_ring(cx, cy, R * 0.3, w * 0.7, accent, cap))
    elif treat == "eclipse":                               # zweifarbiger Ring (Eklipse)
        a0, a1 = math.radians(305), math.radians(125)
        x0, y0 = cx + R * math.cos(a0), cy + R * math.sin(a0)
        x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
        out.append(f'<path fill="none" stroke="{accent}" stroke-width="{w:.2f}" '
                   f'stroke-linecap="{cap}" d="M {x0:.2f} {y0:.2f} '
                   f'A {R:.2f} {R:.2f} 0 0 1 {x1:.2f} {y1:.2f}"/>')
    elif treat == "aperture":                              # Auge / Blende
        out.append(_o_ring(cx, cy, R * 0.5, w * 0.7, accent, cap))
        out.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{R*0.17:.2f}" fill="{accent}"/>')
    elif treat == "momentum":                              # Aufwaerts-Pfeil (Wachstum)
        aw = w * 0.85
        out.append(f'<path fill="none" stroke="{accent}" stroke-width="{aw:.2f}" '
                   f'stroke-linecap="round" stroke-linejoin="round" d="'
                   f'M {cx:.2f} {cy+R*0.52:.2f} L {cx:.2f} {cy-R*0.5:.2f} '
                   f'M {cx-R*0.42:.2f} {cy-R*0.06:.2f} L {cx:.2f} {cy-R*0.55:.2f} '
                   f'L {cx+R*0.42:.2f} {cy-R*0.06:.2f}"/>')
    elif treat == "orbit":                                 # umlaufender Punkt
        out.append(f'<circle cx="{cx:.2f}" cy="{cy-R:.2f}" r="{w*0.95:.2f}" fill="{accent}"/>')
    return "".join(out), O_W * H


def letter_M(x, y, H, w, ink, cap):
    xa, xb, mid = x + w / 2, x + M_W * H - w / 2, x + M_W * H / 2
    s = (f'<path {_attrs(ink,w,cap)} d="'
         f'M {xa:.2f} {y+H:.2f} L {xa:.2f} {y:.2f} '
         f'L {mid:.2f} {y+H*0.55:.2f} L {xb:.2f} {y:.2f} L {xb:.2f} {y+H:.2f}"/>')
    return s, M_W * H


def word_width(s, H):
    wmap = {"F": F_W, "O": O_W, "M": M_W}
    return sum(wmap[c] for c in s) * H + GAP * H * (len(s) - 1)


def draw_word(s, x, y, H, w, ink, accent, cap, treat):
    parts, cur = [], x
    for c in s:
        if c == "F":
            g, adv = letter_F(cur, y, H, w, ink, cap)
        elif c == "O":
            g, adv = letter_O(cur, y, H, w, ink, accent, cap, treat)
        else:
            g, adv = letter_M(cur, y, H, w, ink, cap)
        parts.append(g)
        cur += adv + GAP * H
    return "".join(parts)


def tagline(cx, y, size, color, text="MARKETING", spacing=None):
    sp = size * 0.42 if spacing is None else spacing
    return (f'<text x="{cx:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{size:.2f}" '
            f'font-weight="600" letter-spacing="{sp:.2f}" text-anchor="middle" '
            f'fill="{color}">{text}</text>')


def lockup(cx, cy, H, ink, accent, cap, treat, tag_color=None, word="FOMO"):
    """Zentriertes Logo-Lockup: Wortmarke + Tagline, um (cx,cy) zentriert."""
    w = H * 0.1
    ww = word_width(word, H)
    x0 = cx - ww / 2
    tg = H * 0.34
    total_h = H + tg
    y0 = cy - total_h / 2
    body = draw_word(word, x0, y0, H, w, ink, accent, cap, treat)
    tl = tagline(cx, y0 + H + tg * 0.82, H * 0.165,
                 tag_color or ink, spacing=H * 0.165 * 0.62)
    return body + tl


# ----------------------------------------------------------------------------
# Konzepte
# ----------------------------------------------------------------------------
CONCEPTS = [
    dict(num="01", name="ECLIPSE", tline="Der zweifarbige Ring",
         primary="#0B1F3A", accent="#C9A24B",
         light_bg="#F7F4EE", dark_bg="#0B1F3A", dark_ink="#F1E9D6",
         cap="butt", treat="eclipse",
         desc="Jedes O ist ein zweifarbiger Ring – wie der Moment einer Eklipse. "
              "Tiefes Marineblau trifft auf Champagner-Gold: seriös, edel, zeitlos. "
              "Steht fuer den einen Augenblick, den man nicht verpassen darf."),
    dict(num="02", name="PULSE", tline="Das Signal, das man nicht verpasst",
         primary="#141414", accent="#FF5A4D",
         light_bg="#FFFFFF", dark_bg="#141414", dark_ink="#FAFAFA",
         cap="round", treat="pulse",
         desc="Konzentrische Ringe lassen die O's pulsieren wie ein Radarsignal – "
              "die Aufmerksamkeit, die FOMO ausloest. Reduziertes Schwarz mit einem "
              "einzigen, energiegeladenen Korallton. Modern und unmittelbar."),
    dict(num="03", name="APERTURE", tline="Fokus & Aufmerksamkeit",
         primary="#0F5132", accent="#CDA75A",
         light_bg="#F3EEE4", dark_bg="#0C1F17", dark_ink="#EDE7D8",
         cap="round", treat="aperture",
         desc="Die O's werden zur Blende bzw. zum Auge – Symbol fuer den scharfen "
              "Blick und den Spotlight, den die Agentur auf Marken richtet. "
              "Smaragdgruen und warmes Gold: wertig, exklusiv, boutiquehaft."),
    dict(num="04", name="CREST", tline="Das Monogramm-Emblem",
         primary="#5E1F2E", accent="#C2A14A",
         light_bg="#F6F0EB", dark_bg="#2A0F16", dark_ink="#EBD9C7",
         cap="butt", treat="plain", emblem=True,
         desc="Die Kernmarke O·M·O sitzt in einem edlen Wappen-Emblem. "
              "Oxblood-Rot und Gold verleihen einen Heritage-Charakter wie bei "
              "exklusiven Maisons. Souveraen, premium, mit Handschrift."),
    dict(num="05", name="MOMENTUM", tline="Wachstum & Ergebnis",
         primary="#1C1C1E", accent="url(#grad5)",
         accent_solid="#14B8A6",
         light_bg="#FBFBFD", dark_bg="#121214", dark_ink="#F4F4F6",
         cap="butt", treat="momentum",
         desc="In den O's steigt ein Pfeil nach oben – Momentum, ROI, Wachstum. "
              "Anthrazit mit einem Aqua-Teal-Verlauf: technologisch, dynamisch und "
              "dennoch hochwertig. Fuer eine datengetriebene Premium-Agentur."),
    dict(num="06", name="ORBIT", tline="Im Zentrum der Aufmerksamkeit",
         primary="#3B1E54", accent="#E0B973",
         light_bg="#F4F0F8", dark_bg="#1E1029", dark_ink="#EEE3F2",
         cap="round", treat="orbit",
         desc="Ein goldener Punkt umkreist jedes O – man ist im Orbit, im Zentrum "
              "des Geschehens. Pflaumen-Violett und sanftes Gold wirken kreativ, "
              "luxurioes und unverwechselbar. Minimalistisch und elegant."),
]


def defs():
    return ('<defs>'
            '<linearGradient id="grad5" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#1FD1B6"/>'
            '<stop offset="1" stop-color="#0E7C9D"/>'
            '</linearGradient>'
            '<filter id="soft" x="-20%" y="-20%" width="140%" height="140%">'
            '<feDropShadow dx="0" dy="6" stdDeviation="14" flood-color="#000000" flood-opacity="0.12"/>'
            '</filter>'
            '</defs>')


def card(x, y, w, h, fill, stroke=None):
    st = f' stroke="{stroke}" stroke-width="1.2"' if stroke else ''
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" '
            f'fill="{fill}"{st} filter="url(#soft)"/>')


def emblem(cx, cy, ink, accent):
    """Wappen-Emblem mit O.M.O-Kernmarke fuer Konzept CREST."""
    R = 150
    s = [f'<rect x="{cx-R:.0f}" y="{cy-R:.0f}" width="{2*R}" height="{2*R}" rx="34" '
         f'fill="none" stroke="{accent}" stroke-width="3.5"/>',
         f'<rect x="{cx-R+14:.0f}" y="{cy-R+14:.0f}" width="{2*R-28}" height="{2*R-28}" rx="24" '
         f'fill="none" stroke="{accent}" stroke-width="1.4"/>']
    mh = 96
    mw = word_width("OMO", mh)
    s.append(draw_word("OMO", cx - mw / 2, cy - mh / 2 - 6, mh, mh * 0.1,
                       accent, accent, "butt", "plain"))
    s.append(f'<line x1="{cx-58:.0f}" y1="{cy+72:.0f}" x2="{cx+58:.0f}" y2="{cy+72:.0f}" '
             f'stroke="{accent}" stroke-width="1.4"/>')
    s.append(f'<text x="{cx:.0f}" y="{cy+96:.0f}" font-family="{FONT}" font-size="15" '
             f'font-weight="600" letter-spacing="6" text-anchor="middle" fill="{accent}">EST. 2026</text>')
    return "".join(s)


def swatches(x, y, colors):
    out = []
    for i, (hexv, lab) in enumerate(colors):
        cx = x + i * 128
        out.append(f'<rect x="{cx}" y="{y}" width="34" height="34" rx="7" '
                   f'fill="{hexv}" stroke="#00000022" stroke-width="1"/>')
        out.append(f'<text x="{cx+44}" y="{y+14}" font-family="{FONT}" font-size="13" '
                   f'font-weight="700" fill="#1a1a1a">{lab}</text>')
        out.append(f'<text x="{cx+44}" y="{y+30}" font-family="{FONT}" font-size="12" '
                   f'fill="#777">{hexv.upper()}</text>')
    return "".join(out)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(text, n=92):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > n:
            lines.append(cur); cur = wd
        else:
            cur = (cur + " " + wd).strip()
    if cur:
        lines.append(cur)
    return lines


def concept_page(c):
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H_PAGE}" '
         f'viewBox="0 0 {W} {H_PAGE}">', defs(),
         f'<rect width="{W}" height="{H_PAGE}" fill="#FBFAF7"/>']
    # Kopfzeile
    p.append(f'<text x="80" y="86" font-family="{FONT}" font-size="20" font-weight="800" '
             f'letter-spacing="4" fill="{c["primary"]}">FOMO MARKETING</text>')
    p.append(f'<text x="80" y="112" font-family="{FONT}" font-size="13" letter-spacing="3" '
             f'fill="#999">LOGO-KONZEPT {c["num"]}</text>')
    p.append(f'<text x="{W-80}" y="92" font-family="{FONT}" font-size="46" font-weight="800" '
             f'text-anchor="end" fill="{c["primary"]}">{c["name"]}</text>')
    p.append(f'<text x="{W-80}" y="116" font-family="{FONT}" font-size="14" font-style="italic" '
             f'text-anchor="end" fill="#888">{esc(c["tline"])}</text>')
    p.append(f'<line x1="80" y1="138" x2="{W-80}" y2="138" stroke="{c["accent_solid"] if "accent_solid" in c else c["accent"]}" stroke-width="2"/>')

    # Karten
    cw, ch, cy = 580, 560, 178
    lx, rx = 90, 730
    p.append(card(lx, cy, cw, ch, c["light_bg"], stroke="#0000000f"))
    p.append(card(rx, cy, cw, ch, c["dark_bg"]))

    ccx_l, ccx_r, ccy = lx + cw / 2, rx + cw / 2, cy + ch / 2
    if c.get("emblem"):
        p.append(emblem(ccx_l, ccy - 70, c["primary"], c["accent_solid"] if "accent_solid" in c else c["accent"]))
        ww = word_width("FOMO", 78)
        p.append(draw_word("FOMO", ccx_l - ww / 2, ccy + 118, 78, 7.8,
                            c["primary"], c["accent"], c["cap"], "plain"))
        p.append(tagline(ccx_l, ccy + 232, 14, c["primary"], spacing=9))
        p.append(emblem(ccx_r, ccy - 70, c["dark_ink"], c["accent_solid"] if "accent_solid" in c else c["accent"]))
        p.append(draw_word("FOMO", ccx_r - ww / 2, ccy + 118, 78, 7.8,
                            c["dark_ink"], c["accent"], c["cap"], "plain"))
        p.append(tagline(ccx_r, ccy + 232, 14, c["dark_ink"], spacing=9))
    else:
        p.append(lockup(ccx_l, ccy, 118, c["primary"], c["accent"], c["cap"], c["treat"]))
        p.append(lockup(ccx_r, ccy, 118, c["dark_ink"], c["accent"], c["cap"], c["treat"]))

    p.append(f'<text x="{lx+20}" y="{cy+ch-18}" font-family="{FONT}" font-size="12" '
             f'letter-spacing="2" fill="#aaa">HELLER UNTERGRUND</text>')
    p.append(f'<text x="{rx+20}" y="{cy+ch-18}" font-family="{FONT}" font-size="12" '
             f'letter-spacing="2" fill="#ffffff66">DUNKLER UNTERGRUND</text>')

    # Fusszeile: Beschreibung + Farbpalette
    fy = cy + ch + 44
    for i, ln in enumerate(wrap(c["desc"], 96)):
        p.append(f'<text x="80" y="{fy+i*22}" font-family="{FONT}" font-size="15" '
                 f'fill="#333">{esc(ln)}</text>')
    pal = [(c["primary"], "PRIMAER"),
           (c["accent_solid"] if "accent_solid" in c else c["accent"], "AKZENT"),
           (c["light_bg"], "HELL"), (c["dark_bg"], "DUNKEL")]
    p.append(swatches(812, fy - 14, pal))
    p.append('</svg>')
    return "".join(p)


def cover_page():
    c = CONCEPTS[0]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H_PAGE}" '
         f'viewBox="0 0 {W} {H_PAGE}">', defs(),
         f'<rect width="{W}" height="{H_PAGE}" fill="{c["dark_bg"]}"/>']
    # dezente Hintergrund-Ringe
    for r in (520, 410, 300):
        p.append(f'<circle cx="{W/2}" cy="{H_PAGE/2-40}" r="{r}" fill="none" '
                 f'stroke="{c["accent"]}" stroke-opacity="0.07" stroke-width="1.5"/>')
    p.append(lockup(W / 2, H_PAGE / 2 - 60, 168, c["dark_ink"], c["accent"], "butt", "eclipse"))
    p.append(f'<line x1="{W/2-150}" y1="{H_PAGE/2+150}" x2="{W/2+150}" y2="{H_PAGE/2+150}" '
             f'stroke="{c["accent"]}" stroke-width="1.5"/>')
    p.append(f'<text x="{W/2}" y="{H_PAGE/2+200}" font-family="{FONT}" font-size="22" '
             f'letter-spacing="6" text-anchor="middle" fill="{c["dark_ink"]}">LOGO-KONZEPTE</text>')
    p.append(f'<text x="{W/2}" y="{H_PAGE/2+232}" font-family="{FONT}" font-size="15" '
             f'letter-spacing="3" text-anchor="middle" fill="{c["accent"]}">'
             f'6 ENTWUERFE &#183; PRAESENTATION</text>')
    p.append(f'<text x="80" y="{H_PAGE-50}" font-family="{FONT}" font-size="13" '
             f'letter-spacing="2" fill="#ffffff55">FOMO MARKETING</text>')
    p.append(f'<text x="{W-80}" y="{H_PAGE-50}" font-family="{FONT}" font-size="13" '
             f'letter-spacing="2" text-anchor="end" fill="#ffffff55">09.06.2026</text>')
    p.append('</svg>')
    return "".join(p)


def overview_page():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H_PAGE}" '
         f'viewBox="0 0 {W} {H_PAGE}">', defs(),
         f'<rect width="{W}" height="{H_PAGE}" fill="#FBFAF7"/>']
    p.append(f'<text x="80" y="86" font-family="{FONT}" font-size="20" font-weight="800" '
             f'letter-spacing="4" fill="#0B1F3A">FOMO MARKETING</text>')
    p.append(f'<text x="80" y="112" font-family="{FONT}" font-size="13" letter-spacing="3" '
             f'fill="#999">UEBERSICHT &#183; ALLE KONZEPTE</text>')
    p.append(f'<line x1="80" y1="138" x2="{W-80}" y2="138" stroke="#0B1F3A" stroke-width="2"/>')
    cw, ch = 400, 230
    xs = [90, 510, 930]
    ys = [180, 470]
    for i, c in enumerate(CONCEPTS):
        gx, gy = xs[i % 3], ys[i // 3]
        p.append(card(gx, gy, cw, ch, c["light_bg"], stroke="#0000000f"))
        cx, cy2 = gx + cw / 2, gy + ch / 2 - 12
        if c.get("emblem"):
            ww = word_width("FOMO", 58)
            p.append(draw_word("FOMO", cx - ww / 2, cy2 - 24, 58, 5.8,
                               c["primary"], c["accent"], c["cap"], "plain"))
        else:
            p.append(lockup(cx, cy2, 74, c["primary"], c["accent"], c["cap"], c["treat"]))
        p.append(f'<text x="{gx+18}" y="{gy+ch-18}" font-family="{FONT}" font-size="14" '
                 f'font-weight="800" letter-spacing="2" fill="{c["primary"]}">{c["num"]} {c["name"]}</text>')
    p.append('</svg>')
    return "".join(p)


# ----------------------------------------------------------------------------
# Rendern
# ----------------------------------------------------------------------------
def main():
    pages = [("00_cover", cover_page())]
    for c in CONCEPTS:
        pages.append((f'{c["num"]}_{c["name"].lower()}', concept_page(c)))
    pages.append(("99_overview", overview_page()))

    writer = PdfWriter()
    for name, svg in pages:
        with open(f"logo/svg/{name}.svg", "w") as f:
            f.write(svg)
        pdf_bytes = cairosvg.svg2pdf(bytestring=svg.encode(),
                                     output_width=W * 2, output_height=H_PAGE * 2)
        writer.append(PdfReader(io.BytesIO(pdf_bytes)))
        print("ok:", name)

    with open("logo/FOMO_Marketing_Logo_Konzepte.pdf", "wb") as f:
        writer.write(f)
    print("PDF geschrieben: logo/FOMO_Marketing_Logo_Konzepte.pdf")


if __name__ == "__main__":
    main()

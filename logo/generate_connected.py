# -*- coding: utf-8 -*-
"""
FOMO MARKETING – Logo-Konzepte: VERBUNDENE / VERSCHRAENKTE Buchstaben
Immer das ganze Wort FOMO – klar lesbar, aber die Buchstaben sind auf
unterschiedliche Weise miteinander verwoben, ueberlappend oder verbunden.
Edle Farben (Navy/Gold, Schwarz/Gold, Smaragd/Gold).
"""
import io
import cairosvg
from pypdf import PdfWriter, PdfReader

from generate import (letter_F, letter_O, letter_M, word_width, tagline, card,
                      swatches, wrap, esc, FONT, W, H_PAGE, F_W, O_W, M_W)

ADV = {"F": F_W, "O": O_W, "M": M_W}


# ---------------------------------------------------------------------------
# Flexibles FOMO-Lockup mit Ueberlappung / Verbindern / Zweifarbigkeit
# ---------------------------------------------------------------------------
def fomo_horizontal(x, y, H, w, ink, ocol, cap="round", spacing=-0.10,
                    connect=False, opacity=None, o_scale=1.0, weave=False):
    """Zeichnet F O M O nebeneinander. spacing<0 => Buchstaben ueberlappen.
       connect => horizontale Verbinder auf Mittelhoehe. weave => O's ueber M."""
    seq = "FOMO"
    # x-Positionen je Buchstabe bestimmen (mit moeglicher Ueberlappung)
    xs, cur = [], x
    for i, ch in enumerate(seq):
        xs.append(cur)
        cur += ADV[ch] * H + spacing * H
    midy = y + H * 0.5

    base, tops = [], []     # tops = O/M (kommen ggf. nach oben)
    for i, ch in enumerate(seq):
        cx = xs[i]
        if ch == "F":
            g, _ = letter_F(cx, y, H, w, ink, cap)
            base.append(g)
        elif ch == "M":
            g, _ = letter_M(cx, y, H, w, ink, cap)
            (tops if weave else base).append(g)
        else:  # O
            if o_scale != 1.0:
                Ho = H * o_scale
                yo = y + (H - Ho) / 2
                g, _ = letter_O(cx - (Ho - O_W * H) / 2 + (O_W * H - O_W * Ho) / 2,
                                yo, Ho, w, ocol, ocol, cap, "plain")
            else:
                g, _ = letter_O(cx, y, H, w, ocol, ocol, cap, "plain")
            (base if weave else tops).append(g)

    parts = []
    if connect:
        for i in range(len(seq) - 1):
            x0 = xs[i] + ADV[seq[i]] * H
            x1 = xs[i + 1]
            xa, xb = min(x0, x1), max(x0, x1)
            parts.append(f'<line x1="{xa-2:.1f}" y1="{midy:.1f}" x2="{xb+2:.1f}" '
                         f'y2="{midy:.1f}" stroke="{ink}" stroke-width="{w:.1f}" '
                         f'stroke-linecap="{cap}"/>')
    body = "".join(base + parts + tops)
    if opacity is not None:
        return f'<g opacity="{opacity}">{body}</g>'
    return body


def fomo_width(H, spacing=-0.10, o_scale=1.0):
    seq = "FOMO"
    total = sum(ADV[c] for c in seq) * H + spacing * H * (len(seq) - 1)
    return total


def fomo_lockup(cx, cy, H, ink, ocol, cap, spacing, tagcol,
                connect=False, opacity=None, o_scale=1.0, weave=False, tag=True):
    w = H * 0.1
    ww = fomo_width(H, spacing, o_scale)
    x0 = cx - ww / 2
    tg = H * 0.4 if tag else 0
    y0 = cy - (H + tg) / 2
    body = fomo_horizontal(x0, y0, H, w, ink, ocol, cap, spacing,
                           connect, opacity, o_scale, weave)
    if tag:
        body += tagline(cx, y0 + H + tg * 0.78, H * 0.15, tagcol,
                        spacing=H * 0.15 * 0.62)
    return body


# ---- Konzept 5: gestapeltes Monogramm  FO / MO  ---------------------------
def fomo_stacked(cx, cy, H, ink, ocol, cap):
    """FO oben, MO unten – kompaktes Monogramm. Liest sich F-O-M-O (Z-Form)."""
    w = H * 0.1
    pair_w = (F_W + O_W) * H + (-0.06) * H
    pair_w2 = (M_W + O_W) * H + (-0.06) * H
    block_w = max(pair_w, pair_w2)
    vgap = -0.14 * H
    top_y = cy - H - vgap / 2
    bot_y = cy + vgap / 2
    out = []
    # Reihe 1: F O
    fx = cx - block_w / 2
    g, _ = letter_F(fx, top_y, H, w, ink, cap); out.append(g)
    g, _ = letter_O(fx + F_W * H - 0.06 * H, top_y, H, w, ocol, ocol, cap, "plain"); out.append(g)
    # Reihe 2: M O
    g, _ = letter_M(fx, bot_y, H, w, ink, cap); out.append(g)
    g, _ = letter_O(fx + M_W * H - 0.06 * H, bot_y, H, w, ocol, ocol, cap, "plain"); out.append(g)
    return "".join(out), block_w


# ---------------------------------------------------------------------------
CONCEPTS = [
    dict(num="V1", name="INTERLACE", tline="Verwobene Buchstaben",
         primary="#0B1F3A", accent="#C9A24B",
         light_bg="#F7F3EA", dark_bg="#0B1F3A", dark_ink="#F1E9D6",
         style=dict(cap="round", spacing=-0.13),
         desc="Die Buchstaben ueberlappen leicht und verweben sich – die O's in "
              "Gold, F und M in Marineblau. Das Wort FOMO bleibt vollstaendig und "
              "klar lesbar, wirkt aber wie aus einem Guss. Edel und modern."),
    dict(num="V2", name="CHAIN", tline="Verkettete O's",
         primary="#0B1F3A", accent="#C9A24B",
         light_bg="#F6F2E8", dark_bg="#0B1F3A", dark_ink="#F1E9D6",
         style=dict(cap="round", spacing=-0.15, o_scale=1.12, weave=True),
         desc="Groessere goldene O-Ringe greifen ueber die Schenkel des M – wie "
              "Glieder einer Kette. Das verbindet FOMO sichtbar, ohne die Lesbarkeit "
              "aufzugeben. Symbol fuer Vernetzung und Sog."),
    dict(num="V3", name="LIGATURE", tline="Durchgehende Linie",
         primary="#14110C", accent="#C9A24B",
         light_bg="#F4F1EA", dark_bg="#14110C", dark_ink="#EFE6D2",
         style=dict(cap="round", spacing=0.0, connect=True),
         desc="Eine durchlaufende Mittellinie verbindet alle vier Buchstaben zu "
              "einer Ligatur – FOMO als ein einziger, fliessender Schriftzug. "
              "Schwarz und Gold: reduziert, hochwertig, unverwechselbar."),
    dict(num="V4", name="DUOTONE", tline="Ueberlagerung & Transparenz",
         primary="#0E3B2E", accent="#CDA75A",
         light_bg="#F1EEE3", dark_bg="#0A241B", dark_ink="#E9E3D2",
         style=dict(cap="butt", spacing=-0.16, opacity=0.86),
         desc="Die Buchstaben schieben sich transparent uebereinander; an den "
              "Schnittpunkten entstehen feine Ueberlagerungen. Smaragd und Gold "
              "geben eine layered, kreative und dennoch edle Anmutung."),
    dict(num="V5", name="MONOGRAM", tline="FO / MO – kompaktes Zeichen",
         primary="#0B1F3A", accent="#C9A24B",
         light_bg="#F7F3EA", dark_bg="#0B1F3A", dark_ink="#F1E9D6",
         style=dict(cap="round"), stacked=True,
         desc="Ein quadratisches Monogramm: FO oben, MO unten, ineinander "
              "verschraenkt. Gelesen im Z – F, O, M, O – ergibt sich klar FOMO. "
              "Darunter sichert die Wortmarke die Bedeutung. Ideal als App-Icon."),
    dict(num="V6", name="BRIDGE", tline="Gemeinsame Oberlinie",
         primary="#5E1F2E", accent="#C2A14A",
         light_bg="#F6EFE9", dark_bg="#2A0F16", dark_ink="#EBD9C7",
         style=dict(cap="butt", spacing=-0.05, bridge=True),
         desc="Eine gemeinsame Oberlinie spannt sich ueber alle Buchstaben und "
              "fasst FOMO zu einer Einheit zusammen – wie ein Schriftzug unter "
              "einem Dach. Oxblood und Gold fuer einen souveraenen Auftritt."),
]


def render_logo(c, cx, cy, H, ink, ocol, tagcol, tag=True):
    st = c["style"]
    if c.get("stacked"):
        icy = cy - (H * 0.72 if tag else 0)
        block, bw = fomo_stacked(cx, icy, H, ink, ocol, st["cap"])
        out = [block]
        if tag:
            wmH = H * 0.52
            ww = fomo_width(wmH, -0.10)
            wy = cy + H * 0.86
            out.append(fomo_horizontal(cx - ww / 2, wy, wmH, wmH * 0.1, ink, ocol,
                                       "round", -0.10))
            out.append(tagline(cx, wy + wmH + wmH * 0.42, wmH * 0.4, tagcol,
                               spacing=wmH * 0.4 * 0.62))
        return "".join(out)
    if st.get("bridge"):
        w = H * 0.1
        ww = fomo_width(H, st.get("spacing", -0.05))
        x0 = cx - ww / 2
        tg = H * 0.4 if tag else 0
        y0 = cy - (H + tg) / 2
        body = [f'<line x1="{x0-2:.1f}" y1="{y0+w/2:.1f}" x2="{x0+ww+2:.1f}" y2="{y0+w/2:.1f}" '
                f'stroke="{ocol}" stroke-width="{w:.1f}" stroke-linecap="{st["cap"]}"/>']
        body.append(fomo_horizontal(x0, y0, H, w, ink, ocol, st["cap"],
                                    st.get("spacing", -0.05)))
        if tag:
            body.append(tagline(cx, y0 + H + tg * 0.78, H * 0.15, tagcol, spacing=H * 0.15 * 0.62))
        return "".join(body)
    return fomo_lockup(cx, cy, H, ink, ocol, st["cap"], st.get("spacing", -0.1),
                       tagcol, connect=st.get("connect", False),
                       opacity=st.get("opacity"), o_scale=st.get("o_scale", 1.0),
                       weave=st.get("weave", False), tag=tag)


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
             f'fill="#999">LOGO-KONZEPT {c["num"]} &#183; VERBUNDENE BUCHSTABEN</text>')
    p.append(f'<text x="{W-80}" y="92" font-family="{FONT}" font-size="44" font-weight="800" '
             f'text-anchor="end" fill="{c["primary"]}">{esc(c["name"])}</text>')
    p.append(f'<text x="{W-80}" y="116" font-family="{FONT}" font-size="14" font-style="italic" '
             f'text-anchor="end" fill="#888">{esc(c["tline"])}</text>')
    p.append(f'<line x1="80" y1="138" x2="{W-80}" y2="138" stroke="{gold}" stroke-width="2"/>')

    cw, ch, cy = 580, 560, 178
    lx, rx = 90, 730
    p.append(card(lx, cy, cw, ch, c["light_bg"], stroke="#0000000f"))
    p.append(card(rx, cy, cw, ch, c["dark_bg"]))
    ccy = cy + ch / 2
    Hh = 120 if not c.get("stacked") else 78
    p.append(render_logo(c, lx + cw / 2, ccy, Hh, c["primary"], gold, c["primary"]))
    p.append(render_logo(c, rx + cw / 2, ccy, Hh, c["dark_ink"], gold, c["dark_ink"]))

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
    p.append(render_logo(c, W / 2, H_PAGE / 2 - 30, 190, c["dark_ink"], c["accent"], c["accent"]))
    p.append(f'<text x="{W/2}" y="{H_PAGE/2+205}" font-family="{FONT}" font-size="15" '
             f'letter-spacing="4" text-anchor="middle" fill="{c["dark_ink"]}">'
             f'VERBUNDENE BUCHSTABEN &#183; 6 KONZEPTE</text>')
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
             f'fill="#999">UEBERSICHT &#183; VERBUNDENE BUCHSTABEN</text>')
    p.append(f'<line x1="80" y1="138" x2="{W-80}" y2="138" stroke="#0B1F3A" stroke-width="2"/>')
    cw, ch = 400, 250
    xs, ys = [90, 510, 930], [180, 490]
    for i, c in enumerate(CONCEPTS):
        gx, gy = xs[i % 3], ys[i // 3]
        p.append(card(gx, gy, cw, ch, c["light_bg"], stroke="#0000000f"))
        cx, cyc = gx + cw / 2, gy + ch / 2 - 14
        p.append(render_logo(c, cx, cyc, 70 if not c.get("stacked") else 54,
                             c["primary"], c["accent"], c["primary"], tag=False))
        p.append(f'<text x="{gx+18}" y="{gy+ch-16}" font-family="{FONT}" font-size="13" '
                 f'font-weight="800" letter-spacing="1.5" fill="{c["primary"]}">{c["num"]} {esc(c["name"])}</text>')
    p.append('</svg>')
    return "".join(p)


def main():
    pages = [("C0_cover", cover_page())]
    for c in CONCEPTS:
        pages.append((f'{c["num"]}_{c["name"].lower()}', concept_page(c)))
    pages.append(("C9_overview", overview_page()))
    writer = PdfWriter()
    for name, svg in pages:
        with open(f"logo/svg/{name}.svg", "w") as f:
            f.write(svg)
        pdf = cairosvg.svg2pdf(bytestring=svg.encode(), output_width=W * 2, output_height=H_PAGE * 2)
        writer.append(PdfReader(io.BytesIO(pdf)))
        print("ok:", name)
    with open("logo/FOMO_Marketing_Logo_Konzepte_Verbunden.pdf", "wb") as f:
        writer.write(f)
    print("PDF: logo/FOMO_Marketing_Logo_Konzepte_Verbunden.pdf")


if __name__ == "__main__":
    main()

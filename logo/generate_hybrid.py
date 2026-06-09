# -*- coding: utf-8 -*-
"""
FOMO MARKETING – Logo-Konzepte: Hybrid ECLIPSE x CREST
Verbindet das edle Wappen-Emblem (CREST) mit dem zweifarbigen
Eklipse-Ring (ECLIPSE). Verschiedene Rahmenformen, durchweg edle Farben
mit dezentem Gold-/Metall-Verlauf.
"""
import io
import cairosvg
from pypdf import PdfWriter, PdfReader

import generate as g          # Buchstaben-Bausteine wiederverwenden
from generate import draw_word, word_width, tagline, card, swatches, wrap, esc, FONT, W, H_PAGE


# ---- Farb-Helfer (Verlauf aus dem Akzent ableiten) ------------------------
def _hx(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def _to(t):
    return "#%02X%02X%02X" % tuple(max(0, min(255, int(v))) for v in t)


def lighten(c, f):
    r, gr, b = _hx(c)
    return _to((r + (255 - r) * f, gr + (255 - gr) * f, b + (255 - b) * f))


def darken(c, f):
    r, gr, b = _hx(c)
    return _to((r * (1 - f), gr * (1 - f), b * (1 - f)))


def page_defs(accent_solid):
    return ('<defs>'
            f'<linearGradient id="ac" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{lighten(accent_solid,0.40)}"/>'
            f'<stop offset="0.5" stop-color="{accent_solid}"/>'
            f'<stop offset="1" stop-color="{darken(accent_solid,0.28)}"/>'
            f'</linearGradient>'
            '<filter id="soft" x="-20%" y="-20%" width="140%" height="140%">'
            '<feDropShadow dx="0" dy="6" stdDeviation="14" flood-color="#000000" flood-opacity="0.12"/>'
            '</filter>'
            '</defs>')


# ---- Rahmenformen ----------------------------------------------------------
def frame_square(cx, cy, s, col):
    return (f'<rect x="{cx-s:.0f}" y="{cy-s:.0f}" width="{2*s:.0f}" height="{2*s:.0f}" rx="30" '
            f'fill="none" stroke="{col}" stroke-width="3.4"/>'
            f'<rect x="{cx-s+13:.0f}" y="{cy-s+13:.0f}" width="{2*s-26:.0f}" height="{2*s-26:.0f}" rx="22" '
            f'fill="none" stroke="{col}" stroke-width="1.3"/>')


def frame_circle(cx, cy, s, col):
    return (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{s:.0f}" fill="none" stroke="{col}" stroke-width="3.4"/>'
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{s-13:.0f}" fill="none" stroke="{col}" stroke-width="1.3"/>')


def frame_oval(cx, cy, s, col):
    rx, ry = s * 1.15, s * 0.92
    return (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="none" stroke="{col}" stroke-width="3.4"/>'
            f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx-13:.0f}" ry="{ry-13:.0f}" fill="none" stroke="{col}" stroke-width="1.3"/>')


def _shield_path(cx, cy, sw, s):
    return (f'M {cx-sw:.0f} {cy-s:.0f} L {cx+sw:.0f} {cy-s:.0f} '
            f'L {cx+sw:.0f} {cy+s*0.35:.0f} '
            f'Q {cx+sw:.0f} {cy+s*0.92:.0f} {cx:.0f} {cy+s*1.25:.0f} '
            f'Q {cx-sw:.0f} {cy+s*0.92:.0f} {cx-sw:.0f} {cy+s*0.35:.0f} Z')


def frame_shield(cx, cy, s, col):
    sw = s * 1.02
    return (f'<path d="{_shield_path(cx,cy,sw,s)}" fill="none" stroke="{col}" stroke-width="3.4" stroke-linejoin="round"/>'
            f'<path d="{_shield_path(cx,cy,sw-13,s-13)}" fill="none" stroke="{col}" stroke-width="1.3" stroke-linejoin="round"/>')


def _hex_path(cx, cy, w, h):
    return (f'M {cx-w:.0f} {cy:.0f} L {cx-w/2:.0f} {cy-h:.0f} L {cx+w/2:.0f} {cy-h:.0f} '
            f'L {cx+w:.0f} {cy:.0f} L {cx+w/2:.0f} {cy+h:.0f} L {cx-w/2:.0f} {cy+h:.0f} Z')


def frame_hex(cx, cy, s, col):
    w, h = s * 1.2, s
    return (f'<path d="{_hex_path(cx,cy,w,h)}" fill="none" stroke="{col}" stroke-width="3.4" stroke-linejoin="round"/>'
            f'<path d="{_hex_path(cx,cy,w-13,h-13)}" fill="none" stroke="{col}" stroke-width="1.3" stroke-linejoin="round"/>')


FRAMES = dict(square=frame_square, circle=frame_circle, oval=frame_oval,
              shield=frame_shield, hex=frame_hex)
FRAME_SIZE = dict(square=140, circle=150, oval=146, shield=148, hex=126)


def emblem(cx, cy, frame, ink, accent, est):
    """Wappen-Emblem (Gold-Rahmen) mit O.M.O-Kernmarke als Eklipse-Ring."""
    s = FRAME_SIZE[frame]
    out = [FRAMES[frame](cx, cy, s, accent)]
    mh = 64
    mw = word_width("OMO", mh)
    out.append(draw_word("OMO", cx - mw / 2, cy - 6 - mh / 2, mh, mh * 0.1,
                         ink, accent, "butt", "eclipse"))
    out.append(f'<line x1="{cx-46:.0f}" y1="{cy+46:.0f}" x2="{cx+46:.0f}" y2="{cy+46:.0f}" '
               f'stroke="{accent}" stroke-width="1.2"/>')
    out.append(f'<text x="{cx:.0f}" y="{cy+66:.0f}" font-family="{FONT}" font-size="13" '
               f'font-weight="600" letter-spacing="5" text-anchor="middle" fill="{accent}">{est}</text>')
    return "".join(out)


# ---- Konzepte (Hybrid, edle Farben) ---------------------------------------
CONCEPTS = [
    dict(num="H1", name="ROYAL ECLIPSE", tline="Wappen trifft Eklipse",
         frame="square", primary="#0B1F3A", accent_solid="#C9A24B", est="EST &#183; 2026",
         light_bg="#F7F3EA", dark_bg="#0B1F3A", dark_ink="#F1E9D6",
         desc="Das Eclipse-Motiv im klassischen Wappenrahmen: Marineblaue Ringe "
              "mit goldenem Eklipse-Bogen, gefasst in ein doppelt umrandetes Emblem. "
              "Tiefblau und Champagner-Gold – maximal seriös und zeitlos edel."),
    dict(num="H2", name="OXBLOOD SEAL", tline="Heritage-Siegel",
         frame="shield", primary="#5E1F2E", accent_solid="#C2A14A", est="EST &#183; 2026",
         light_bg="#F6EFE9", dark_bg="#2A0F16", dark_ink="#EBD9C7",
         desc="Ein Wappenschild fasst die Eklipse-Marke wie ein Familiensiegel. "
              "Oxblood-Rot und antikes Gold verleihen Tradition und Exklusivität – "
              "die Anmutung eines etablierten Maison."),
    dict(num="H3", name="NOIR & OR", tline="Roundel in Schwarz-Gold",
         frame="circle", primary="#15110C", accent_solid="#C9A24B", est="EST &#183; 2026",
         light_bg="#F4F1EA", dark_bg="#15110C", dark_ink="#EFE6D2",
         desc="Reduziert und luxuriös: ein kreisrundes Medaillon, tiefes Schwarz "
              "und warmes Gold. Die Eklipse-Ringe wirken wie geprägte Münzen – "
              "schlicht, hochwertig, unverwechselbar."),
    dict(num="H4", name="EMERALD CREST", tline="Oval in Smaragd & Gold",
         frame="oval", primary="#0E3B2E", accent_solid="#CDA75A", est="EST &#183; 2026",
         light_bg="#F1EEE3", dark_bg="#0A241B", dark_ink="#E9E3D2",
         desc="Ein ovales Emblem im Stil edler Petschaften. Sattes Smaragdgrün "
              "und gealtertes Gold stehen für Beständigkeit und gehobenen Anspruch – "
              "klassisch und doch eigenständig."),
    dict(num="H5", name="AUBERGINE ROYALE", tline="Hexagon in Aubergine",
         frame="hex", primary="#33203A", accent_solid="#DBBA7A", est="EST &#183; 2026",
         light_bg="#F4F0F4", dark_bg="#1F1226", dark_ink="#ECE2EE",
         desc="Ein sechseckiges Emblem verleiht eine moderne, kreative Note. "
              "Tiefes Auberginen-Violett und sanftes Sandgold wirken luxuriös und "
              "zugleich differenziert – edel mit Charakter."),
    dict(num="H6", name="MIDNIGHT PLATINUM", tline="Wappen in Platin",
         frame="square", primary="#11161F", accent_solid="#AEB4BD", est="EST &#183; 2026",
         light_bg="#F2F3F5", dark_bg="#11161F", dark_ink="#EAECEF",
         desc="Kühle Eleganz statt Gold: nahezu schwarzes Mitternachtsblau mit "
              "einem Platin-Silber-Verlauf. Modern, technologisch und sehr edel – "
              "für eine Agentur mit klarer, premiumiger Handschrift."),
]


def concept_page(c):
    accent = "url(#ac)"
    gold = c["accent_solid"]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H_PAGE}" '
         f'viewBox="0 0 {W} {H_PAGE}">', page_defs(gold),
         f'<rect width="{W}" height="{H_PAGE}" fill="#FBFAF7"/>']
    # Kopfzeile
    p.append(f'<text x="80" y="86" font-family="{FONT}" font-size="20" font-weight="800" '
             f'letter-spacing="4" fill="{c["primary"]}">FOMO MARKETING</text>')
    p.append(f'<text x="80" y="112" font-family="{FONT}" font-size="13" letter-spacing="3" '
             f'fill="#999">LOGO-KONZEPT {c["num"]} &#183; ECLIPSE x CREST</text>')
    p.append(f'<text x="{W-80}" y="92" font-family="{FONT}" font-size="42" font-weight="800" '
             f'text-anchor="end" fill="{c["primary"]}">{esc(c["name"])}</text>')
    p.append(f'<text x="{W-80}" y="116" font-family="{FONT}" font-size="14" font-style="italic" '
             f'text-anchor="end" fill="#888">{esc(c["tline"])}</text>')
    p.append(f'<line x1="80" y1="138" x2="{W-80}" y2="138" stroke="{gold}" stroke-width="2"/>')

    cw, ch, cy = 580, 560, 178
    lx, rx = 90, 730
    p.append(card(lx, cy, cw, ch, c["light_bg"], stroke="#0000000f"))
    p.append(card(rx, cy, cw, ch, c["dark_bg"]))

    ey = cy + 188
    wt = cy + 408                       # Oberkante Wortmarke
    for cardx, ink in ((lx, c["primary"]), (rx, c["dark_ink"])):
        ex = cardx + cw / 2
        p.append(emblem(ex, ey, c["frame"], ink, accent, c["est"]))
        ww = word_width("FOMO", 62)
        p.append(draw_word("FOMO", ex - ww / 2, wt, 62, 6.2, ink, accent, "butt", "eclipse"))
        p.append(tagline(ex, wt + 96, 13.5, gold, spacing=8))

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
    gold = c["accent_solid"]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H_PAGE}" '
         f'viewBox="0 0 {W} {H_PAGE}">', page_defs(gold),
         f'<rect width="{W}" height="{H_PAGE}" fill="{c["dark_bg"]}"/>']
    for r in (470, 360):
        p.append(f'<circle cx="{W/2}" cy="{H_PAGE/2-70}" r="{r}" fill="none" '
                 f'stroke="{gold}" stroke-opacity="0.08" stroke-width="1.4"/>')
    p.append(emblem(W / 2, H_PAGE / 2 - 80, "square", c["dark_ink"], "url(#ac)", "EST &#183; 2026"))
    ww = word_width("FOMO", 96)
    p.append(draw_word("FOMO", W / 2 - ww / 2, H_PAGE / 2 + 110, 96, 9.6,
                       c["dark_ink"], "url(#ac)", "butt", "eclipse"))
    p.append(tagline(W / 2, H_PAGE / 2 + 248, 20, gold, spacing=12))
    p.append(f'<text x="{W/2}" y="{H_PAGE/2+300}" font-family="{FONT}" font-size="15" '
             f'letter-spacing="4" text-anchor="middle" fill="{c["dark_ink"]}">'
             f'ECLIPSE x CREST &#183; 6 EDLE KONZEPTE</text>')
    p.append(f'<text x="80" y="{H_PAGE-50}" font-family="{FONT}" font-size="13" '
             f'letter-spacing="2" fill="#ffffff55">FOMO MARKETING</text>')
    p.append(f'<text x="{W-80}" y="{H_PAGE-50}" font-family="{FONT}" font-size="13" '
             f'letter-spacing="2" text-anchor="end" fill="#ffffff55">09.06.2026</text>')
    p.append('</svg>')
    return "".join(p)


def overview_page():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H_PAGE}" '
         f'viewBox="0 0 {W} {H_PAGE}">',
         f'<rect width="{W}" height="{H_PAGE}" fill="#FBFAF7"/>']
    p.append(f'<text x="80" y="86" font-family="{FONT}" font-size="20" font-weight="800" '
             f'letter-spacing="4" fill="#0B1F3A">FOMO MARKETING</text>')
    p.append(f'<text x="80" y="112" font-family="{FONT}" font-size="13" letter-spacing="3" '
             f'fill="#999">UEBERSICHT &#183; ECLIPSE x CREST</text>')
    p.append(f'<line x1="80" y1="138" x2="{W-80}" y2="138" stroke="#0B1F3A" stroke-width="2"/>')
    cw, ch = 400, 250
    xs, ys = [90, 510, 930], [180, 490]
    for i, c in enumerate(CONCEPTS):
        gx, gy = xs[i % 3], ys[i // 3]
        defs = page_defs(c["accent_solid"]).replace('id="ac"', f'id="ac{i}"').replace('id="soft"', f'id="soft{i}"')
        p.append(defs)
        p.append(card(gx, gy, cw, ch, c["light_bg"], stroke="#0000000f").replace('url(#soft)', f'url(#soft{i})'))
        cx, cyc = gx + cw / 2, gy + ch / 2 - 8
        p.append(f'<g transform="translate({cx:.1f} {cyc:.1f}) scale(0.66) translate({-cx:.1f} {-cyc:.1f})">')
        p.append(emblem(cx, cyc, c["frame"], c["primary"], f"url(#ac{i})", c["est"]))
        p.append('</g>')
        p.append(f'<text x="{gx+18}" y="{gy+ch-16}" font-family="{FONT}" font-size="13" '
                 f'font-weight="800" letter-spacing="1.5" fill="{c["primary"]}">{c["num"]} {esc(c["name"])}</text>')
    p.append('</svg>')
    return "".join(p)


def main():
    pages = [("H0_cover", cover_page())]
    for c in CONCEPTS:
        pages.append((f'{c["num"]}_{c["name"].split()[0].lower()}', concept_page(c)))
    pages.append(("H9_overview", overview_page()))

    writer = PdfWriter()
    for name, svg in pages:
        with open(f"logo/svg/{name}.svg", "w") as f:
            f.write(svg)
        pdf = cairosvg.svg2pdf(bytestring=svg.encode(), output_width=W * 2, output_height=H_PAGE * 2)
        writer.append(PdfReader(io.BytesIO(pdf)))
        print("ok:", name)

    with open("logo/FOMO_Marketing_Logo_Konzepte_Hybrid.pdf", "wb") as f:
        writer.write(f)
    print("PDF: logo/FOMO_Marketing_Logo_Konzepte_Hybrid.pdf")


if __name__ == "__main__":
    main()

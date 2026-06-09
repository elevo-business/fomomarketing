# -*- coding: utf-8 -*-
"""
FOMO MARKETING – Wort+Bild, Runde 2
Optimiert: die Bildidee erzaehlt 'Fear Of Missing Out' direkt (Verpassen,
aussen vor sein, Zeit laeuft ab). Sanfte, gedeckte, edle Farben – nichts Buntes.
"""
import io, math
import cairosvg
from pypdf import PdfWriter, PdfReader

from generate import (draw_word, tagline, card, swatches, wrap, esc,
                      FONT, W, H_PAGE, F_W, O_W, M_W, GAP)

TOTAL = (F_W + GAP + O_W + GAP + M_W + GAP + O_W)


def _pol(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def arc(cx, cy, r, a0, a1, color, w, cap="round"):
    x0, y0 = _pol(cx, cy, r, a0)
    x1, y1 = _pol(cx, cy, r, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return (f'<path d="M {x0:.2f} {y0:.2f} A {r:.2f} {r:.2f} 0 {large} 1 {x1:.2f} {y1:.2f}" '
            f'fill="none" stroke="{color}" stroke-width="{w:.2f}" stroke-linecap="{cap}"/>')


def dot(x, y, r, color, op=1.0):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{color}" opacity="{op}"/>'


def ring(x, y, r, color, w, op=1.0):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="none" '
            f'stroke="{color}" stroke-width="{w:.2f}" opacity="{op}"/>')


def geom(x0, y0, H):
    w = H * 0.1
    o1L = x0 + (F_W + GAP) * H
    mL = o1L + (O_W + GAP) * H
    o2L = mL + (M_W + GAP) * H
    R = H / 2 - w / 2
    cyc = y0 + H / 2
    return dict(w=w, R=R, top=y0, bot=y0 + H, cyc=cyc,
                o1=(o1L + O_W * H / 2, cyc), o2=(o2L + O_W * H / 2, cyc),
                end=o2L + O_W * H)


# ---------------------------------------------------------------------------
# Bildideen (Wort + Bild) – erzaehlen FOMO
# ---------------------------------------------------------------------------
def c_notify(g, ink, accent, bg):
    """Alert am letzten O: 'es passiert gerade etwas' (gedeckter Ton)."""
    cx, cy = g["o2"]
    bx, by = cx + g["R"] * 0.72, cy - g["R"] * 0.72
    r = g["w"] * 1.65
    over = dot(bx, by, r + 4, bg) + dot(bx, by, r, accent)
    return "", over, "FOMO"


def c_hourglass(g, ink, accent, bg):
    """Sanduhr im letzten O: die Zeit laeuft ab."""
    cx, cy = g["o2"]
    R = g["R"]
    ax, ay = R * 0.4, R * 0.5
    body = (f'<path d="M {cx-ax:.1f} {cy-ay:.1f} L {cx+ax:.1f} {cy-ay:.1f} '
            f'L {cx:.1f} {cy:.1f} L {cx+ax:.1f} {cy+ay:.1f} L {cx-ax:.1f} {cy+ay:.1f} '
            f'L {cx:.1f} {cy:.1f} Z" fill="none" stroke="{accent}" '
            f'stroke-width="{g["w"]*0.62:.1f}" stroke-linejoin="round"/>')
    top_sand = (f'<path d="M {cx-ax*0.78:.1f} {cy-ay*0.78:.1f} L {cx+ax*0.78:.1f} {cy-ay*0.78:.1f} '
                f'L {cx:.1f} {cy-ay*0.04:.1f} Z" fill="{accent}" opacity="0.5"/>')
    pile = (f'<path d="M {cx-ax*0.5:.1f} {cy+ay:.1f} L {cx+ax*0.5:.1f} {cy+ay:.1f} '
            f'L {cx:.1f} {cy+ay*0.45:.1f} Z" fill="{accent}"/>')
    caps = (f'<line x1="{cx-ax*1.1:.1f}" y1="{cy-ay:.1f}" x2="{cx+ax*1.1:.1f}" y2="{cy-ay:.1f}" '
            f'stroke="{accent}" stroke-width="{g["w"]*0.62:.1f}" stroke-linecap="round"/>'
            f'<line x1="{cx-ax*1.1:.1f}" y1="{cy+ay:.1f}" x2="{cx+ax*1.1:.1f}" y2="{cy+ay:.1f}" '
            f'stroke="{accent}" stroke-width="{g["w"]*0.62:.1f}" stroke-linecap="round"/>')
    return "", body + top_sand + pile + caps, "FOMO"


def c_missing(g, ink, accent, bg):
    """Letztes O hat eine Luecke; ein Punkt wartet aussen: das fehlende Stueck."""
    cx, cy = g["o2"]
    R, w = g["R"], g["w"]
    gap = arc(cx, cy, R, -37, 287, ink, w)             # kleine Luecke oben rechts -> bleibt O
    px, py = _pol(cx, cy, R * 1.22, -55)
    p2x, p2y = _pol(cx, cy, R * 1.95, -55)
    piece = dot(px, py, w * 1.45, accent) + dot(p2x, p2y, w * 0.8, accent, 0.4)
    return "", gap + piece, "FOM"


def c_leftout(g, ink, accent, bg):
    """Volle Gruppe im O, einer steht aussen vor: ausgeschlossen sein."""
    cx, cy = g["o2"]
    R, w = g["R"], g["w"]
    inside = []
    for ang in (90, 210, 330, 30, 150, 270):
        dx, dy = _pol(cx, cy, R * 0.46, ang)
        inside.append(dot(dx, dy, w * 0.78, accent))
    inside.append(dot(cx, cy, w * 0.78, accent))
    ox, oy = _pol(cx, cy, R * 1.8, 0)
    outside = ring(ox, oy, w * 1.25, ink, w * 0.55)     # leerer Ring = du, aussen vor
    return "", "".join(inside) + outside, "FOMO"


def c_fading(g, ink, accent, bg):
    """Letztes O loest sich rechts in Punkte auf: der Moment verfliegt."""
    cx, cy = g["o2"]
    R, w = g["R"], g["w"]
    # O bleibt vollstaendig (lesbar); Partikel loesen sich oben rechts ab -> der Moment verfliegt
    parts = []
    steps = [(1.16, 0.9, 0.85), (1.4, 0.72, 0.62), (1.66, 0.55, 0.45),
             (1.95, 0.42, 0.32), (2.28, 0.32, 0.22)]
    for i, (rf, sf, op) in enumerate(steps):
        ang = -42 - i * 7
        dx, dy = _pol(cx, cy, R * rf, ang)
        parts.append(dot(dx, dy, w * sf, ink, op))
    return "", "".join(parts), "FOMO"


def c_pull(g, ink, accent, bg):
    """Kleine Pfeile ziehen zum letzten O hin: der Sog, dabei sein zu wollen."""
    cx, cy = g["o2"]
    R, w = g["R"], g["w"]
    over = []
    for ang in (-90, 0, 90, 180):
        d = R * 1.7
        tipx, tipy = _pol(cx, cy, R * 1.32, ang)
        bx, by = _pol(cx, cy, d, ang)
        perp = ang + 90
        l1x, l1y = _pol(bx, by, w * 1.5, perp)
        l2x, l2y = _pol(bx, by, w * 1.5, ang - 90 + 180)
        wx1, wy1 = _pol(cx, cy, d + w * 1.1, ang + 7)
        wx2, wy2 = _pol(cx, cy, d + w * 1.1, ang - 7)
        over.append(f'<path d="M {wx1:.1f} {wy1:.1f} L {tipx:.1f} {tipy:.1f} L {wx2:.1f} {wy2:.1f}" '
                    f'fill="none" stroke="{accent}" stroke-width="{w*0.6:.1f}" '
                    f'stroke-linecap="round" stroke-linejoin="round"/>')
    return "", "".join(over), "FOMO"


COMBOS = dict(notify=c_notify, hourglass=c_hourglass, missing=c_missing,
              leftout=c_leftout, fading=c_fading, pull=c_pull)


# ---------------------------------------------------------------------------
CONCEPTS = [
    dict(num="F1", name="MISSING PIECE", tline="Das fehlende Stueck – du fehlst",
         combo="missing", cap="round", primary="#3B352D", accent="#CBB489",
         light_bg="#F1ECE2", dark_bg="#2E2920", dark_ink="#ECE3D2",
         desc="Das letzte O hat eine Luecke, ein Punkt wartet ausserhalb: genau "
              "dort gehoerst du hin. Die direkteste Darstellung von 'Fear Of "
              "Missing Out' – das Bild, das fehlt, bist du. Warmes Taupe & Champagner."),
    dict(num="F2", name="LEFT OUT", tline="Aussen vor",
         combo="leftout", cap="round", primary="#37413A", accent="#BFA97C",
         light_bg="#EDEAE0", dark_bg="#2A322C", dark_ink="#E8E4D5",
         desc="Im letzten O versammelt sich die Gruppe, ein leerer Ring steht "
              "ausserhalb – ausgeschlossen sein, nicht dazugehoeren. Das Kerngefuehl "
              "von FOMO, ruhig in gedecktem Salbei und Gold erzaehlt."),
    dict(num="F3", name="RUNNING OUT", tline="Die Zeit laeuft ab",
         combo="hourglass", cap="round", primary="#36414C", accent="#C7B488",
         light_bg="#EEEAE2", dark_bg="#2B333B", dark_ink="#E9E4D7",
         desc="Eine Sanduhr im letzten O: jetzt oder nie. Dringlichkeit und "
              "ablaufende Zeit sind der Motor jeder FOMO. Gedecktes Schiefer-Blau "
              "und warmer Sand wirken edel und seriös."),
    dict(num="F4", name="FADING", tline="Der Moment verfliegt",
         combo="fading", cap="round", primary="#3C3038", accent="#C2A07F",
         light_bg="#EFEAE6", dark_bg="#2E252B", dark_ink="#ECE2DE",
         desc="Vom letzten O steigen feine Partikel auf und vergehen – der Moment, "
              "der dir gerade entgleitet. Das O bleibt klar lesbar, das Verpassen "
              "wird leise spuerbar. Gedecktes Pflaume und Rosé-Gold, sehr zurueckhaltend."),
    dict(num="F5", name="THE PULL", tline="Der Sog, dabei zu sein",
         combo="pull", cap="round", primary="#2E3239", accent="#C3AC82",
         light_bg="#EEEBE4", dark_bg="#262A30", dark_ink="#E9E5DB",
         desc="Vier feine Pfeile ziehen zum letzten O hin – der Sog, Teil davon "
              "sein zu wollen. FOMO als Anziehung. Reduziert, edel, in gedecktem "
              "Schiefer und weichem Messing."),
    dict(num="F6", name="ALERT", tline="Es passiert gerade etwas",
         combo="notify", cap="round", primary="#2F2E2B", accent="#C19A6B",
         light_bg="#F1ECE4", dark_bg="#2A2825", dark_ink="#EDE6D8",
         desc="Ein gedeckter Signalpunkt am letzten O: da draussen passiert "
              "gerade etwas, sei dabei. Die vertraute Notification – aber in einem "
              "warmen, edlen Bernsteinton statt grellem Rot."),
]


def lockup(c, cx, cy, H, ink, accent, bg, tagcol, tag=True):
    w = H * 0.1
    ww = TOTAL * H
    x0 = cx - ww / 2
    tg = H * 0.42 if tag else 0
    y0 = cy - (H + tg) / 2
    g = geom(x0, y0, H)
    under, over, word = COMBOS[c["combo"]](g, ink, accent, bg)
    body = draw_word(word, x0, y0, H, w, ink, accent, c["cap"], "plain")
    out = [under, body, over]
    if tag:
        out.append(tagline(cx, y0 + H + tg * 0.8, H * 0.15, tagcol, spacing=H * 0.15 * 0.62))
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
             f'fill="#999">LOGO-KONZEPT {c["num"]} &#183; WORT + BILD</text>')
    p.append(f'<text x="{W-80}" y="92" font-family="{FONT}" font-size="42" font-weight="800" '
             f'text-anchor="end" fill="{c["primary"]}">{esc(c["name"])}</text>')
    p.append(f'<text x="{W-80}" y="116" font-family="{FONT}" font-size="14" font-style="italic" '
             f'text-anchor="end" fill="#888">{esc(c["tline"])}</text>')
    p.append(f'<line x1="80" y1="138" x2="{W-80}" y2="138" stroke="{gold}" stroke-width="2"/>')

    cw, ch, cy = 580, 560, 178
    lx, rx = 90, 730
    p.append(card(lx, cy, cw, ch, c["light_bg"], stroke="#0000000f"))
    p.append(card(rx, cy, cw, ch, c["dark_bg"]))
    ccy = cy + ch / 2
    p.append(lockup(c, lx + cw / 2, ccy, 116, c["primary"], gold, c["light_bg"], c["primary"]))
    p.append(lockup(c, rx + cw / 2, ccy, 116, c["dark_ink"], gold, c["dark_bg"], c["dark_ink"]))

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
    p.append(lockup(c, W / 2, H_PAGE / 2 - 30, 168, c["dark_ink"], c["accent"], c["dark_bg"], c["accent"]))
    p.append(f'<text x="{W/2}" y="{H_PAGE/2+185}" font-family="{FONT}" font-size="15" '
             f'letter-spacing="4" text-anchor="middle" fill="{c["dark_ink"]}">'
             f'FEAR OF MISSING OUT &#183; 6 KONZEPTE</text>')
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
             f'letter-spacing="4" fill="#2F2E2B">FOMO MARKETING</text>')
    p.append(f'<text x="80" y="112" font-family="{FONT}" font-size="13" letter-spacing="3" '
             f'fill="#999">UEBERSICHT &#183; FEAR OF MISSING OUT</text>')
    p.append(f'<line x1="80" y1="138" x2="{W-80}" y2="138" stroke="#2F2E2B" stroke-width="2"/>')
    cw, ch = 400, 250
    xs, ys = [90, 510, 930], [180, 490]
    for i, c in enumerate(CONCEPTS):
        gx, gy = xs[i % 3], ys[i // 3]
        p.append(card(gx, gy, cw, ch, c["light_bg"], stroke="#0000000f"))
        cx, cyc = gx + cw / 2, gy + ch / 2 - 16
        p.append(lockup(c, cx, cyc, 60, c["primary"], c["accent"], c["light_bg"], c["primary"], tag=False))
        p.append(f'<text x="{gx+18}" y="{gy+ch-16}" font-family="{FONT}" font-size="13" '
                 f'font-weight="800" letter-spacing="1.5" fill="{c["primary"]}">{c["num"]} {esc(c["name"])}</text>')
    p.append('</svg>')
    return "".join(p)


def main():
    pages = [("F0_cover", cover_page())]
    for c in CONCEPTS:
        pages.append((f'{c["num"]}_{c["combo"]}', concept_page(c)))
    pages.append(("F9_overview", overview_page()))
    writer = PdfWriter()
    for name, svg in pages:
        with open(f"logo/svg/{name}.svg", "w") as f:
            f.write(svg)
        pdf = cairosvg.svg2pdf(bytestring=svg.encode(), output_width=W * 2, output_height=H_PAGE * 2)
        writer.append(PdfReader(io.BytesIO(pdf)))
        print("ok:", name)
    with open("logo/FOMO_Marketing_Logo_Konzepte_FOMO.pdf", "wb") as f:
        writer.write(f)
    print("PDF: logo/FOMO_Marketing_Logo_Konzepte_FOMO.pdf")


if __name__ == "__main__":
    main()

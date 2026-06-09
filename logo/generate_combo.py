# -*- coding: utf-8 -*-
"""
FOMO MARKETING – Logo-Konzepte: KOMBINATIONSMARKEN (Wort + Bild)
Das Wort FOMO bleibt klar lesbar, verschmilzt aber mit einem bedeutungs-
tragenden Bildelement – die Buchstaben sind mit dem Bild 'verdrahtet'.
"""
import io, math
import cairosvg
from pypdf import PdfWriter, PdfReader

from generate import (letter_F, letter_O, letter_M, draw_word, tagline, card,
                      swatches, wrap, esc, FONT, W, H_PAGE,
                      F_W, O_W, M_W, GAP)

TOTAL = (F_W + GAP + O_W + GAP + M_W + GAP + O_W)   # Gesamtbreite / H


def _pol(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def arc(cx, cy, r, a0, a1, color, w, cap="round"):
    x0, y0 = _pol(cx, cy, r, a0)
    x1, y1 = _pol(cx, cy, r, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return (f'<path d="M {x0:.2f} {y0:.2f} A {r:.2f} {r:.2f} 0 {large} 1 {x1:.2f} {y1:.2f}" '
            f'fill="none" stroke="{color}" stroke-width="{w:.2f}" stroke-linecap="{cap}"/>')


def geom(x0, y0, H):
    w = H * 0.1
    o1L = x0 + (F_W + GAP) * H
    mL = o1L + (O_W + GAP) * H
    o2L = mL + (M_W + GAP) * H
    R = H / 2 - w / 2
    cyc = y0 + H / 2
    return dict(w=w, R=R, top=y0, bot=y0 + H, cyc=cyc,
                fL=x0, mL=mL, mW=M_W * H,
                o1=(o1L + O_W * H / 2, cyc), o2=(o2L + O_W * H / 2, cyc),
                end=o2L + O_W * H)


# ---------------------------------------------------------------------------
# Bildelemente (kombiniert mit der Wortmarke)
# ---------------------------------------------------------------------------
def combo_notify(g, ink, accent, bg):
    """Notification-Badge am letzten O – das universelle FOMO-Signal."""
    cx, cy = g["o2"]
    bx, by = cx + g["R"] * 0.72, cy - g["R"] * 0.72
    r = g["w"] * 1.7
    over = (f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{r+4:.1f}" fill="{bg}"/>'
            f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{r:.1f}" fill="{accent}"/>')
    return "", over


def combo_signal(g, ink, accent, bg):
    """Broadcast-/Signalwellen aus dem ersten O – Buzz & Reichweite."""
    cx, cy = g["o1"]
    over = [f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{g["w"]*1.2:.1f}" fill="{accent}"/>']
    for i, rr in enumerate((1.35, 1.7, 2.05)):
        over.append(arc(cx, cy, g["R"] * rr, -148, -32, accent, g["w"] * 0.62))
    return "", "".join(over)


def combo_play(g, ink, accent, bg):
    """Play-Dreieck im ersten O – Content, Video, Medien."""
    cx, cy = g["o1"]
    R = g["R"]
    over = (f'<path d="M {cx-R*0.32:.1f} {cy-R*0.46:.1f} L {cx-R*0.32:.1f} {cy+R*0.46:.1f} '
            f'L {cx+R*0.52:.1f} {cy:.1f} Z" fill="{accent}"/>')
    return "", over


def combo_speech(g, ink, accent, bg):
    """Wort in einer Sprechblase – Social Buzz / Gespraech."""
    padx, padyt, padyb = g["w"] * 2.4, g["w"] * 2.0, g["w"] * 2.0
    x = g["fL"] - padx
    y = g["top"] - padyt
    ww = (g["end"] - g["fL"]) + 2 * padx
    hh = (g["bot"] - g["top"]) + padyt + padyb
    tailx = x + ww * 0.26
    under = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{ww:.1f}" height="{hh:.1f}" rx="{hh*0.28:.1f}" '
             f'fill="none" stroke="{accent}" stroke-width="{g["w"]*0.85:.1f}"/>'
             f'<path d="M {tailx:.1f} {y+hh-2:.1f} l {-g["w"]*0.6:.1f} {g["w"]*2.6:.1f} '
             f'l {g["w"]*3.2:.1f} {-g["w"]*2.6:.1f} Z" fill="{bg}" stroke="{accent}" '
             f'stroke-width="{g["w"]*0.85:.1f}" stroke-linejoin="round"/>')
    return under, ""


def combo_network(g, ink, accent, bg):
    """Knoten & Leitungen entlang der Buchstaben-Oberkante – 'verdrahtet'."""
    pts = [(g["fL"] + g["w"] / 2, g["top"]),
           (g["o1"][0], g["o1"][1] - g["R"]),
           (g["mL"], g["top"]),
           (g["mL"] + g["mW"], g["top"]),
           (g["o2"][0], g["o2"][1] - g["R"])]
    ext = [(g["fL"] - g["w"] * 3, g["top"] - g["R"] * 0.7),
           (g["end"] + g["w"] * 3, g["top"] - g["R"] * 0.55)]
    line = [ext[0]] + pts + [ext[1]]
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in line)
    over = [f'<path d="{d}" fill="none" stroke="{accent}" stroke-width="{g["w"]*0.42:.1f}" '
            f'stroke-opacity="0.85" stroke-linejoin="round"/>']
    for x, y in line:
        over.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{g["w"]*0.75:.1f}" fill="{accent}"/>')
    return "", "".join(over)


def combo_timer(g, ink, accent, bg):
    """Uhr/Countdown im letzten O – Dringlichkeit, jetzt oder nie."""
    cx, cy = g["o2"]
    R = g["R"]
    hx, hy = _pol(cx, cy, R * 0.5, -90)        # Stundenzeiger (12 Uhr)
    mx, my = _pol(cx, cy, R * 0.72, -10)        # Minutenzeiger
    over = (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{g["w"]*0.7:.1f}" fill="{accent}"/>'
            f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{hx:.1f}" y2="{hy:.1f}" '
            f'stroke="{accent}" stroke-width="{g["w"]*0.7:.1f}" stroke-linecap="round"/>'
            f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{mx:.1f}" y2="{my:.1f}" '
            f'stroke="{accent}" stroke-width="{g["w"]*0.7:.1f}" stroke-linecap="round"/>')
    return "", over


COMBOS = dict(notify=combo_notify, signal=combo_signal, play=combo_play,
              speech=combo_speech, network=combo_network, timer=combo_timer)


# ---------------------------------------------------------------------------
CONCEPTS = [
    dict(num="K1", name="NOTIFICATION", tline="Das rote Signal am O",
         combo="notify", cap="round", primary="#0B1F3A", accent="#E5484D",
         light_bg="#F4F6F8", dark_bg="#0B1F3A", dark_ink="#EAF0F6",
         desc="Der rote Notification-Punkt am letzten O ist das universelle "
              "Zeichen fuer 'da passiert etwas, sei dabei' – die Essenz von FOMO. "
              "Klares Wort, ein praegnanter Bild-Akzent. Sofort verstanden."),
    dict(num="K2", name="SIGNAL", tline="Buzz & Reichweite",
         combo="signal", cap="round", primary="#0B1F3A", accent="#C9A24B",
         light_bg="#F7F3EA", dark_bg="#0B1F3A", dark_ink="#F1E9D6",
         desc="Aus dem ersten O senden Wellen wie von einem Sender – das O wird "
              "zur Quelle des Buzz. Verbindet das Wort mit der Idee von Reichweite "
              "und Aufmerksamkeit. Edel in Navy und Gold."),
    dict(num="K3", name="PLAY", tline="Content, der laeuft",
         combo="play", cap="butt", primary="#15110C", accent="#C9A24B",
         light_bg="#F4F1EA", dark_bg="#15110C", dark_ink="#EFE6D2",
         desc="Ein Play-Dreieck verwandelt das erste O in einen Start-Button – "
              "fuer eine Agentur, die Content und Kampagnen ins Laufen bringt. "
              "Schwarz-Gold, modern und mediennah."),
    dict(num="K4", name="BUZZ", tline="Wort in der Sprechblase",
         combo="speech", cap="round", primary="#0E3B2E", accent="#CDA75A",
         light_bg="#F1EEE3", dark_bg="#0A241B", dark_ink="#E9E3D2",
         desc="FOMO sitzt in einer Sprechblase – das Gespraech, ueber das alle "
              "reden. Wort und Bild verschmelzen zu einem Social-Zeichen. "
              "Smaragd und Gold geben eine wertige Note."),
    dict(num="K5", name="WIRED", tline="Verdrahtete Buchstaben",
         combo="network", cap="round", primary="#0B1F3A", accent="#C9A24B",
         light_bg="#F7F3EA", dark_bg="#0B1F3A", dark_ink="#F1E9D6",
         desc="Eine Leitung mit Knotenpunkten verbindet die Oberkanten der "
              "Buchstaben – FOMO als vernetztes System. Steht fuer Verbindung, "
              "Daten und Reichweite. Genau 'verdrahtet', aber klar lesbar."),
    dict(num="K6", name="COUNTDOWN", tline="Jetzt oder nie",
         combo="timer", cap="round", primary="#5E1F2E", accent="#C2A14A",
         light_bg="#F6EFE9", dark_bg="#2A0F16", dark_ink="#EBD9C7",
         desc="Im letzten O tickt eine Uhr – Dringlichkeit und limitierte Zeit, "
              "der Kern jeder FOMO. Das Bild erzaehlt die Markenidee direkt im "
              "Wort. Oxblood und Gold fuer einen souveraenen Auftritt."),
]


def lockup(c, cx, cy, H, ink, accent, bg, tagcol, tag=True):
    w = H * 0.1
    ww = TOTAL * H
    x0 = cx - ww / 2
    tg = H * 0.42 if tag else 0
    y0 = cy - (H + tg) / 2
    g = geom(x0, y0, H)
    under, over = COMBOS[c["combo"]](g, ink, accent, bg)
    word = draw_word("FOMO", x0, y0, H, w, ink, accent, c["cap"], "plain")
    out = [under, word, over]
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
    p.append(lockup(c, W / 2, H_PAGE / 2 - 30, 170, c["dark_ink"], c["accent"], c["dark_bg"], c["accent"]))
    p.append(f'<text x="{W/2}" y="{H_PAGE/2+185}" font-family="{FONT}" font-size="15" '
             f'letter-spacing="4" text-anchor="middle" fill="{c["dark_ink"]}">'
             f'WORT + BILD &#183; 6 KOMBINATIONSMARKEN</text>')
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
             f'fill="#999">UEBERSICHT &#183; WORT + BILD</text>')
    p.append(f'<line x1="80" y1="138" x2="{W-80}" y2="138" stroke="#0B1F3A" stroke-width="2"/>')
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
    pages = [("KB0_cover", cover_page())]
    for c in CONCEPTS:
        pages.append((f'{c["num"]}_{c["combo"]}', concept_page(c)))
    pages.append(("KB9_overview", overview_page()))
    writer = PdfWriter()
    for name, svg in pages:
        with open(f"logo/svg/{name}.svg", "w") as f:
            f.write(svg)
        pdf = cairosvg.svg2pdf(bytestring=svg.encode(), output_width=W * 2, output_height=H_PAGE * 2)
        writer.append(PdfReader(io.BytesIO(pdf)))
        print("ok:", name)
    with open("logo/FOMO_Marketing_Logo_Konzepte_WortBild.pdf", "wb") as f:
        writer.write(f)
    print("PDF: logo/FOMO_Marketing_Logo_Konzepte_WortBild.pdf")


if __name__ == "__main__":
    main()

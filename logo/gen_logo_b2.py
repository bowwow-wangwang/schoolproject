"""AIPHABESS mark B2 — refined grimoire with serif 'A' monogram.

Hand-authored SVG (no generative tool connected). Two variants:
  mono : single colour, follows CSS `color` via currentColor
  gilt : dark leather cover + gold-foil tooling (self-contained colours)
Usage: python gen_logo_b2.py <out_dir>
"""
import math, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."

def f(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s if s != "-0" else "0"

# geometry ------------------------------------------------------------------
W, H = 220, 260
X0, X1, Y0, Y1 = 54, 184, 20, 238          # front cover
SP = 18                                     # spine width
CX, CY = (X0 + X1) / 2, (Y0 + Y1) / 2       # medallion centre
RX, RY = 46, 64                             # lozenge half-diagonals


def lozenge(sx, sy=None):
    sy = sy if sy is not None else sx
    return (f"M{f(CX)},{f(CY-RY*sy)} L{f(CX+RX*sx)},{f(CY)} "
            f"L{f(CX)},{f(CY+RY*sy)} L{f(CX-RX*sx)},{f(CY)} Z")


def hatch(x0, y0, x1, y1, gap, angle_deg):
    """Parallel lines covering a box at the given angle (to be clipped)."""
    a = math.radians(angle_deg)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    R = math.hypot(x1 - x0, y1 - y0) / 2 + 2
    d = []
    k = -R
    while k <= R:
        px, py = cx + nx * k, cy + ny * k
        d.append(f"M{f(px-dx*R)},{f(py-dy*R)}L{f(px+dx*R)},{f(py+dy*R)}")
        k += gap
    return "".join(d)


# monogram A (filled shapes, thick-thin contrast, bracketed serifs) --------
def monogram_paths(cx=CX, base=CY + 30, top=CY - 30):
    h = base - top
    def P(x, y):  # local coords: x relative to centre, y from top 0..1*h scaled
        return f"{f(cx + x)},{f(top + y * h / 56)}"
    thick = (f"M{P(-3,0)} L{P(3.5,0)} L{P(20,53)} L{P(11,53)} Z")
    thin = (f"M{P(-3.2,1.5)} L{P(-1.4,5)} L{P(-16.2,53)} L{P(-18.6,53)} Z")
    bar = (f"M{P(-11.5,36.6)} L{P(8.2,36.6)} L{P(8.9,39)} L{P(-12.3,39)} Z")
    apex = (f"M{P(-8.5,0)} L{P(3.5,0)} L{P(3.2,1.6)} L{P(-7.6,1.6)} "
            f"C{P(-6.6,1.6)} {P(-5.6,2)} {P(-5,3)} Z")
    serif_l = (f"M{P(-25.5,56)} L{P(-9,56)} L{P(-9,54.4)} "
               f"C{P(-12.4,54.2)} {P(-14.6,53)} {P(-15.6,50)} "
               f"L{P(-18.9,50)} C{P(-19.8,53)} {P(-22,54.2)} {P(-25.5,54.4)} Z")
    serif_r = (f"M{P(4,56)} L{P(27.5,56)} L{P(27.5,54.4)} "
               f"C{P(23.6,54.2)} {P(21.2,53)} {P(19.6,49.5)} "
               f"L{P(10.6,49.5)} C{P(10.2,53)} {P(8.4,54.2)} {P(4,54.4)} Z")
    return [thick, thin, bar, apex, serif_l, serif_r]


def corner_path():
    # scalloped metal corner, local coords with corner at (0,0), symmetric on diagonal
    return ("M0,0 L34,0 C32,6 27.5,9.5 22,9.5 C15.5,9.5 9.5,15.5 9.5,22 "
            "C9.5,27.5 6,32 0,34 Z")


def build(variant):
    gilt = variant == "gilt"
    LINE = "url(#ab-gold)" if gilt else "currentColor"
    FILL = "url(#ab-gold)" if gilt else "currentColor"
    HATCH = "#140b06" if gilt else "currentColor"
    HATCH_OP = ".55" if gilt else ".5"
    defs, g = [], []

    if gilt:
        defs.append(
            '<linearGradient id="ab-gold" gradientUnits="userSpaceOnUse" x1="40" y1="20" x2="190" y2="240">'
            '<stop offset="0" stop-color="#f3dc97"/><stop offset=".28" stop-color="#c99d45"/>'
            '<stop offset=".5" stop-color="#f0d488"/><stop offset=".74" stop-color="#9c7432"/>'
            '<stop offset="1" stop-color="#e2c070"/></linearGradient>'
            '<linearGradient id="ab-leather" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#4a2c1c"/><stop offset=".55" stop-color="#3a2114"/>'
            '<stop offset="1" stop-color="#2a170d"/></linearGradient>'
            '<linearGradient id="ab-spine" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="#1f120a"/><stop offset=".6" stop-color="#3a2114"/>'
            '<stop offset="1" stop-color="#2c1910"/></linearGradient>'
            '<filter id="ab-grain" x="0" y="0" width="100%" height="100%">'
            '<feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="3"/>'
            '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .22 0"/>'
            '<feComposite in2="SourceGraphic" operator="in"/></filter>')

    # clip regions
    defs.append(f'<clipPath id="ab-{variant}-cover"><rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" rx="3"/></clipPath>')
    defs.append(f'<clipPath id="ab-{variant}-loz"><path d="{lozenge(.86, .87)}"/></clipPath>')
    defs.append(f'<clipPath id="ab-{variant}-corner"><path d="{corner_path()}"/></clipPath>')
    defs.append(f'<clipPath id="ab-{variant}-spine"><path d="M{X0},{Y0} C{X0-SP+2},{Y0+1} {X0-SP},{Y0+8} {X0-SP},{Y0+18} L{X0-SP},{Y1-18} C{X0-SP},{Y1-8} {X0-SP+2},{Y1-1} {X0},{Y1} Z"/></clipPath>')
    # border field = between frame insets 7 and 18
    defs.append(f'<clipPath id="ab-{variant}-border"><path clip-rule="evenodd" d="'
                f'M{X0+7},{Y0+7} H{X1-7} V{Y1-7} H{X0+7} Z '
                f'M{X0+18},{Y0+18} V{Y1-18} H{X1-18} V{Y0+18} Z"/></clipPath>')
    # halo around the monogram so the guilloché does not touch it
    mono = monogram_paths()
    halo = "".join(f'<path d="{d}"/>' for d in mono)
    defs.append(f'<mask id="ab-{variant}-halo" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
                f'<rect width="{W}" height="{H}" fill="#fff"/>'
                f'<g fill="#000" stroke="#000" stroke-width="7" stroke-linejoin="round">{halo}</g></mask>')

    # --- page block (fore-edge + tail) ---
    pb_fill = ' fill="#e9d7a6"' if gilt else ' fill="none"'
    g.append(f'<path d="M{X1-2},{Y0+4} L{X1+8},{Y0+9} L{X1+8},{Y1+4} L{X0+8},{Y1+4} L{X0+2},{Y1}"{pb_fill} stroke="{ "#6b4a22" if gilt else LINE}" stroke-width="1.2"/>')
    pl = "#8a6a3a" if gilt else LINE
    for i in range(1, 9):
        x = X1 + i * .95
        g.append(f'<path d="M{f(x)},{f(Y0+5+i*.55)} V{Y1+2}" stroke="{pl}" stroke-width=".35"/>')
    for i in range(1, 4):
        y = Y1 + i * 1.0
        g.append(f'<path d="M{X0+5},{f(y)} H{X1+7}" stroke="{pl}" stroke-width=".35"/>')

    # --- spine ---
    sp_d = (f"M{X0},{Y0} C{X0-SP+2},{Y0+1} {X0-SP},{Y0+8} {X0-SP},{Y0+18} "
            f"L{X0-SP},{Y1-18} C{X0-SP},{Y1-8} {X0-SP+2},{Y1-1} {X0},{Y1}")
    if gilt:
        g.append(f'<path d="{sp_d} Z" fill="url(#ab-spine)" stroke="none"/>')
    sh = []
    for i, x in enumerate([X0-SP+1.5, X0-SP+3, X0-SP+4.3, X0-SP+5.5, X0-SP+6.6, X0-SP+8, X0-3, X0-1.6]):
        sh.append(f'<path d="M{f(x)},{Y0} V{Y1}" stroke-width="{.55 if i < 5 else .35}"/>')
    g.append(f'<g clip-path="url(#ab-{variant}-spine)" stroke="{HATCH}" opacity="{HATCH_OP}">{"".join(sh)}</g>')
    g.append(f'<path d="{sp_d}" stroke="{LINE}" stroke-width="1.6"/>')
    for y in (58, 100, 142, 184, 214):
        g.append(f'<path d="M{X0-SP},{y} C{X0-SP+5},{y-3.2} {X0-6},{y-3.2} {X0},{y}" stroke="{LINE}" stroke-width="1.3"/>')
        g.append(f'<path d="M{X0-SP},{y+3.6} C{X0-SP+5},{y+.4} {X0-6},{y+.4} {X0},{y+3.6}" stroke="{LINE}" stroke-width=".6"/>')
    g.append(f'<path d="M{X0-SP+4},{f(Y0+38)} h{SP-8} M{X0-SP+4},{f(Y0+52)} h{SP-8}" stroke="{LINE}" stroke-width=".5"/>')

    # --- cover ---
    if gilt:
        g.append(f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" rx="3" fill="url(#ab-leather)"/>')
        g.append(f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" rx="3" fill="#fff" filter="url(#ab-grain)"/>')
    # tooled border field: dense hatching
    g.append(f'<g clip-path="url(#ab-{variant}-border)"><path d="{hatch(X0, Y0, X1, Y1, 2.1, 45)}" stroke="{HATCH}" stroke-width=".4" opacity="{HATCH_OP}"/></g>')
    g.append(f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" rx="3" stroke="{LINE}" stroke-width="1.8"/>')
    for ins, w in ((7, 1.1), (18, 1.0), (20.5, .45)):
        g.append(f'<rect x="{X0+ins}" y="{Y0+ins}" width="{X1-X0-2*ins}" height="{Y1-Y0-2*ins}" stroke="{LINE}" stroke-width="{w}"/>')
    # bead row along the inner field
    beads = []
    ins = 24.5
    bx0, bx1, by0, by1 = X0 + ins, X1 - ins, Y0 + ins, Y1 - ins
    step = 5.2
    def run(ax, ay, bx, by):
        L = math.hypot(bx - ax, by - ay); n = int(L // step)
        for i in range(n + 1):
            t = i / n
            x, y = ax + (bx - ax) * t, ay + (by - ay) * t
            if x > CX and any(abs(y - cy) < 8 for cy in (84, 174)):
                continue  # hidden under the clasp straps
            beads.append(f'<circle cx="{f(ax+(bx-ax)*t)}" cy="{f(ay+(by-ay)*t)}" r=".95"/>')
    run(bx0 + 30, by0, bx1 - 30, by0); run(bx0 + 30, by1, bx1 - 30, by1)
    run(bx0, by0 + 30, bx0, by1 - 30); run(bx1, by0 + 30, bx1, by1 - 30)
    g.append(f'<g fill="{FILL}" stroke="none">{"".join(beads)}</g>')

    # --- corner pieces (metal) ---
    for (tx, ty, sx, sy) in ((X0+1, Y0+1, 1, 1), (X1-1, Y0+1, -1, 1), (X0+1, Y1-1, 1, -1), (X1-1, Y1-1, -1, -1)):
        tr = f'translate({tx},{ty}) scale({sx},{sy})'
        part = [f'<g clip-path="url(#ab-{variant}-corner)"><path d="{hatch(0,0,34,34,1.9,-45)}" stroke="{HATCH if gilt else LINE}" stroke-width=".35" opacity="{".6" if gilt else ".55"}"/></g>']
        if gilt:
            part.insert(0, f'<path d="{corner_path()}" fill="url(#ab-gold)" opacity=".92"/>')
        part.append(f'<path d="{corner_path()}" stroke="{LINE if not gilt else "#2a170d"}" stroke-width="1.1"/>')
        part.append(f'<path d="M3,3 L27,3 C25,7.5 21.5,10 17.5,10.6 C13.5,11.2 11.2,13.5 10.6,17.5 C10,21.5 7.5,25 3,27 Z" stroke="{LINE if not gilt else "#2a170d"}" stroke-width=".5"/>')
        part.append(f'<circle cx="9" cy="9" r="2.6" fill="{"#2a170d" if gilt else FILL}" stroke="none"/>')
        part.append(f'<circle cx="8.3" cy="8.3" r=".8" fill="{"#f3dc97" if gilt else "none"}" stroke="none"/>')
        g.append(f'<g transform="{tr}">{"".join(part)}</g>')

    # --- medallion ---
    # guilloché: concentric lozenges
    gl = "".join(f'<path d="{lozenge(s)}"/>' for s in [i / 28 for i in range(3, 25)])
    g.append(f'<g clip-path="url(#ab-{variant}-loz)" mask="url(#ab-{variant}-halo)" stroke="{LINE}" stroke-width=".38" opacity=".7">{gl}</g>')
    g.append(f'<path d="{lozenge(1)}" stroke="{LINE}" stroke-width="1.5"/>')
    g.append(f'<path d="{lozenge(.93, .935)}" stroke="{LINE}" stroke-width=".55"/>')
    # finials at the four points
    for d in (-1, 1):
        y = CY + d * RY
        g.append(f'<path d="M{CX},{f(y+d*2)} V{f(y+d*16)}" stroke="{LINE}" stroke-width=".9"/>')
        # small lily: centre petal + two side curls
        g.append(f'<path d="M{CX},{f(y+d*16)} C{f(CX-3.4)},{f(y+d*20)} {f(CX-1.6)},{f(y+d*25)} {CX},{f(y+d*27)} '
                 f'C{f(CX+1.6)},{f(y+d*25)} {f(CX+3.4)},{f(y+d*20)} {CX},{f(y+d*16)} Z" fill="{FILL}" stroke="none"/>')
        for s in (-1, 1):
            g.append(f'<path d="M{CX},{f(y+d*9)} C{f(CX+s*5)},{f(y+d*7)} {f(CX+s*9)},{f(y+d*10)} {f(CX+s*7.5)},{f(y+d*14)} '
                     f'C{f(CX+s*6.5)},{f(y+d*16)} {f(CX+s*4)},{f(y+d*15)} {f(CX+s*4.6)},{f(y+d*13)}" stroke="{LINE}" stroke-width=".8"/>')
    for d in (-1, 1):
        x = CX + d * RX
        g.append(f'<path d="M{f(x+d*2)},{CY} H{f(x+d*8)}" stroke="{LINE}" stroke-width=".9"/>')
        g.append(f'<path d="M{f(x+d*8)},{CY} l{f(d*3)},-3 l{f(d*3)},3 l{f(-d*3)},3 Z" fill="{FILL}" stroke="none"/>')

    # monogram
    g.append(f'<g fill="{FILL}" stroke="none">' + "".join(f'<path d="{d}"/>' for d in mono) + '</g>')

    # --- clasps ---
    for y in (84, 174):
        strap = (f"M{X1+12},{y-6} L{X1-22},{y-6} C{X1-30},{y-6} {X1-34},{y-2} {X1-35},{y} "
                 f"C{X1-34},{y+2} {X1-30},{y+6} {X1-22},{y+6} L{X1+12},{y+6}")
        if gilt:
            g.append(f'<path d="{strap} Z" fill="#2a170d" stroke="none"/>')
        g.append(f'<path d="{strap}" stroke="{LINE}" stroke-width="1.2"/>')
        g.append(f'<path d="M{X1+10},{y-3.4} L{X1-22},{y-3.4} C{X1-27},{y-3.4} {X1-30},{y-1.5} {X1-31},{y} '
                 f'C{X1-30},{y+1.5} {X1-27},{y+3.4} {X1-22},{y+3.4} L{X1+10},{y+3.4}" stroke="{LINE}" stroke-width=".45" stroke-dasharray="1.6 1.4"/>')
        g.append(f'<path d="M{X1+12},{y-6} C{X1+15},{y-6} {X1+15},{y+6} {X1+12},{y+6}" stroke="{LINE}" stroke-width="1.2"/>')
        # metal catch
        g.append(f'<rect x="{X1-17}" y="{y-8}" width="9" height="16" rx="1.5" fill="{"url(#ab-gold)" if gilt else "none"}" stroke="{LINE if not gilt else "#2a170d"}" stroke-width="1"/>')
        g.append(f'<path d="M{X1-15},{y-5} V{y+5} M{X1-12.5},{y-5} V{y+5} M{X1-10},{y-5} V{y+5}" stroke="{"#2a170d" if gilt else LINE}" stroke-width=".35"/>')
        g.append(f'<circle cx="{X1-26}" cy="{y}" r="2.3" fill="{FILL}" stroke="none"/>')

    label = "아이파베스 문장: 머리글자 A가 새겨진 마법서"
    root_extra = '' if gilt else ' color="inherit"'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{label}" '
            f'fill="none" stroke-linecap="round" stroke-linejoin="round"{root_extra}>\n'
            f'<defs>{"".join(defs)}</defs>\n' + "\n".join(g) + "\n</svg>\n")


os.makedirs(OUT, exist_ok=True)
for v in ("mono", "gilt"):
    with open(os.path.join(OUT, f"mark_b2_{v}.svg"), "w", encoding="utf-8") as fh:
        fh.write(build(v))
print("ok")

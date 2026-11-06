"""Build the Aiphabess website into docs/ (book, newspaper, town map).

python build/build_site.py   (run from the project root)
Inputs : logo/mark_b2_*.svg, images/*.jpg + images/_sources.json, build/bgm.html, build/map_svg.py
Output : docs/index.html, docs/news.html, docs/map.html, docs/assets/
"""
import json, math, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda p: open(os.path.join(ROOT, p), encoding="utf-8").read()

def f(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s

# ------------------------------------------------------------------ assets
def strip_svg(s):
    return re.sub(r"\s*\n\s*", "", s.strip())

LOGO_GILT = strip_svg(rd("logo/mark_b2_gilt.svg"))
LOGO_MONO = strip_svg(rd("logo/mark_b2_mono.svg"))

def logo(prefix, variant="gilt", cls=""):
    s = LOGO_GILT if variant == "gilt" else LOGO_MONO
    s = s.replace("ab-", prefix + "-")
    return s.replace("<svg ", f'<svg class="{cls}" ', 1)

SRC = {d["key"]: d for d in json.load(open(os.path.join(ROOT, "images/_sources.json"), encoding="utf-8"))}
for _k, _v in {"np_reading": "작자 미상", "pm_street": "The Argosy", "pm_books": "작자 미상", "pm_inn": "Rijksmuseum 소장", "pm_fish": "Theo. R. Davis"}.items():
    if _k in SRC: SRC[_k]["artist"] = _v

def img_url(key):
    return f"assets/img/{key}.jpg"

GOLD_STOPS = ('<stop offset="0" stop-color="#f3dc97"/><stop offset=".3" stop-color="#c99d45"/>'
              '<stop offset=".52" stop-color="#f0d488"/><stop offset=".76" stop-color="#9c7432"/>'
              '<stop offset="1" stop-color="#e2c070"/>')

def medallion(idp, label_main, label_sub, size=104):
    """Gilt medallion: milled rim, bead ring, guilloché rosette, centred text."""
    c, R = 60, 56
    g = [f'<defs><linearGradient id="{idp}g" gradientUnits="userSpaceOnUse" x1="10" y1="6" x2="110" y2="114">{GOLD_STOPS}</linearGradient></defs>']
    g.append(f'<circle cx="{c}" cy="{c}" r="{R}" fill="url(#{idp}g)" stroke="#2a170d" stroke-width="1.2"/>')
    ticks = "".join(f'M{f(c+R*math.cos(a))},{f(c+R*math.sin(a))}L{f(c+(R-4)*math.cos(a))},{f(c+(R-4)*math.sin(a))}'
                    for a in [i * math.tau / 96 for i in range(96)])
    g.append(f'<path d="{ticks}" stroke="#5a3d17" stroke-width=".6"/>')
    g.append(f'<circle cx="{c}" cy="{c}" r="{R-5.5}" fill="none" stroke="#2a170d" stroke-width=".9"/>')
    beads = "".join(f'<circle cx="{f(c+(R-9)*math.cos(a))}" cy="{f(c+(R-9)*math.sin(a))}" r=".95"/>'
                    for a in [i * math.tau / 44 for i in range(44)])
    g.append(f'<g fill="#3b2410">{beads}</g>')
    g.append(f'<circle cx="{c}" cy="{c}" r="{R-12.5}" fill="none" stroke="#2a170d" stroke-width=".7"/>')
    # guilloché rosette (overlapping circles)
    ros = "".join(f'<circle cx="{f(c+9*math.cos(a))}" cy="{f(c+9*math.sin(a))}" r="30"/>'
                  for a in [i * math.tau / 18 for i in range(18)])
    g.append(f'<g fill="none" stroke="#6b4a1c" stroke-width=".35" opacity=".75">{ros}</g>')
    g.append(f'<circle cx="{c}" cy="{c}" r="27" fill="url(#{idp}g)" stroke="#2a170d" stroke-width=".9"/>')
    g.append(f'<text x="{c}" y="{c+4}" text-anchor="middle" font-family="Noto Serif KR,serif" font-weight="700" font-size="{17 if len(label_main)>2 else 19}" fill="#2a170d">{label_main}</text>')
    if label_sub:
        g.append(f'<text x="{c}" y="{c+16}" text-anchor="middle" font-family="IM Fell English SC,serif" font-size="6.5" letter-spacing="1.5" fill="#3b2410">{label_sub}</text>')
    return (f'<svg viewBox="0 0 120 120" width="{size}" height="{size}" role="img" aria-label="{label_main} 메달" '
            f'stroke-linecap="round">{"".join(g)}</svg>')

def coin(size=70):
    c, R = 40, 36
    g = [f'<defs><linearGradient id="cog" gradientUnits="userSpaceOnUse" x1="6" y1="4" x2="74" y2="76">{GOLD_STOPS}</linearGradient></defs>']
    g.append(f'<circle cx="{c}" cy="{c}" r="{R+1.5}" fill="#2a170d"/>')
    g.append(f'<circle cx="{c}" cy="{c}" r="{R}" fill="url(#cog)"/>')
    ticks = "".join(f'M{f(c+R*math.cos(a))},{f(c+R*math.sin(a))}L{f(c+(R-3.2)*math.cos(a))},{f(c+(R-3.2)*math.sin(a))}'
                    for a in [i * math.tau / 72 for i in range(72)])
    g.append(f'<path d="{ticks}" stroke="#5a3d17" stroke-width=".55"/>')
    g.append(f'<circle cx="{c}" cy="{c}" r="{R-5}" fill="none" stroke="#2a170d" stroke-width=".8"/>')
    g.append(f'<circle cx="{c}" cy="{c}" r="{R-8}" fill="none" stroke="#2a170d" stroke-width=".4" stroke-dasharray=".8 1.8"/>')
    for a in (0, 90, 180, 270):
        r = math.radians(a - 90); x, y = c + (R - 14.5) * math.cos(r), c + (R - 14.5) * math.sin(r)
        if a in (90, 270):
            g.append(f'<path d="M{f(x)},{f(y-2.4)}L{f(x+1)},{f(y)}L{f(x)},{f(y+2.4)}L{f(x-1)},{f(y)}Z" fill="#2a170d"/>')
    g.append(f'<text x="{c}" y="{c+9}" text-anchor="middle" font-family="IM Fell English,serif" font-size="27" fill="#2a170d">G</text>')
    g.append(f'<text x="{c}" y="{c-14}" text-anchor="middle" font-family="IM Fell English SC,serif" font-size="5.6" letter-spacing="1.2" fill="#2a170d">RECURAN</text>')
    g.append(f'<text x="{c}" y="{c+21}" text-anchor="middle" font-family="IM Fell English SC,serif" font-size="5.6" letter-spacing="1.2" fill="#2a170d">C · GOLD</text>')
    return f'<svg viewBox="0 0 80 80" width="{size}" height="{size}" aria-hidden="true" stroke-linecap="round">{"".join(g)}</svg>'

ROMAN = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII",
         "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI"]

def dial():
    c = 200; INK = "#2e2216"
    g = [f'<defs><linearGradient id="dlg" gradientUnits="userSpaceOnUse" x1="40" y1="40" x2="360" y2="360">{GOLD_STOPS}</linearGradient></defs>']
    for r, w in ((186, 1.8), (181, .5), (150, .8), (146, .4), (104, .8), (100, .4)):
        g.append(f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{INK}" stroke-width="{w}"/>')
    # minute ticks between 181 and 172
    t = []
    for i in range(22 * 5):
        a = math.radians(i * 360 / 110 - 90)
        r1 = 168 if i % 5 == 0 else 175
        t.append(f'M{f(c+181*math.cos(a))},{f(c+181*math.sin(a))}L{f(c+r1*math.cos(a))},{f(c+r1*math.sin(a))}')
    g.append(f'<path d="{"".join(t)}" stroke="{INK}" stroke-width=".6"/>')
    # current segment (18) gilded band
    a0, a1 = math.radians(18 * 360 / 22 - 90 - 360 / 44), math.radians(18 * 360 / 22 - 90 + 360 / 44)
    def arc(r, a, b):
        return f'{f(c+r*math.cos(a))},{f(c+r*math.sin(a))}', f'{f(c+r*math.cos(b))},{f(c+r*math.sin(b))}'
    p0, p1 = arc(150, a0, a1); q1, q0 = arc(104, a1, a0)
    g.append(f'<path d="M{p0} A150,150 0 0 1 {p1} L{q1} A104,104 0 0 0 {q0} Z" fill="url(#dlg)" stroke="{INK}" stroke-width=".6" opacity=".9"/>')
    # radial separators & numerals
    sep = []
    for i in range(22):
        a = math.radians(i * 360 / 22 - 90 + 360 / 44)
        sep.append(f'M{f(c+146*math.cos(a))},{f(c+146*math.sin(a))}L{f(c+104*math.cos(a))},{f(c+104*math.sin(a))}')
        b = math.radians(i * 360 / 22 - 90)
        x, y = c + 126 * math.cos(b), c + 126 * math.sin(b)
        now = i == 18
        fw = ' font-weight="700"' if now else ""
        g.append(f'<text x="{f(x)}" y="{f(y+4.5)}" text-anchor="middle" font-family="IM Fell English SC,serif" '
                 f'font-size="{14 if now else 12.5}" fill="{"#2a170d" if now else INK}"{fw}>{ROMAN[i]}</text>')
    g.append(f'<path d="{"".join(sep)}" stroke="{INK}" stroke-width=".45"/>')
    # inner rosette
    ros = "".join(f'<circle cx="{f(c+22*math.cos(a))}" cy="{f(c+22*math.sin(a))}" r="58"/>' for a in [i * math.tau / 22 for i in range(22)])
    g.append(f'<g fill="none" stroke="{INK}" stroke-width=".3" opacity=".45">{ros}</g>')
    g.append(f'<circle cx="{c}" cy="{c}" r="44" fill="#ecdcb4" stroke="{INK}" stroke-width=".9"/>')
    g.append(f'<circle cx="{c}" cy="{c}" r="40" fill="none" stroke="{INK}" stroke-width=".4"/>')
    # needle to XVIII
    a = math.radians(18 * 360 / 22 - 90)
    tipx, tipy = c + 98 * math.cos(a), c + 98 * math.sin(a)
    nx, ny = -math.sin(a), math.cos(a)
    bx, by = c + 46 * math.cos(a), c + 46 * math.sin(a)
    g.append(f'<path class="needle" d="M{f(bx+nx*3.2)},{f(by+ny*3.2)} L{f(tipx)},{f(tipy)} L{f(bx-nx*3.2)},{f(by-ny*3.2)} Z" fill="url(#dlg)" stroke="#2a170d" stroke-width=".7"/>')
    g.append(f'<text x="{c}" y="{c-4}" text-anchor="middle" font-family="IM Fell English,serif" font-size="30" fill="{INK}">95</text>')
    g.append(f'<text x="{c}" y="{c+16}" text-anchor="middle" font-family="Noto Serif KR,serif" font-size="12" fill="{INK}">회전</text>')
    # cardinal stars on outer ring
    for k in range(4):
        a = math.radians(k * 90 - 90 + 45)
        x, y = c + 192 * math.cos(a), c + 192 * math.sin(a)
        g.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="1.6" fill="{INK}"/>')
    return (f'<svg class="dial" viewBox="0 0 400 400" role="img" aria-label="22장의 타로로 이루어진 한 바퀴. 지금은 95회전 18번째, 달(XVIII)." '
            f'stroke-linecap="round">{"".join(g)}</svg>')

def alch(kind):
    """Classical alchemical element triangles (fine line)."""
    up = kind in ("fire", "air")
    pts = "M20,6 L34,32 L6,32 Z" if up else "M20,34 L34,8 L6,8 Z"
    bar = ""
    if kind == "air": bar = '<path d="M10,23 H30"/>'
    if kind == "earth": bar = '<path d="M10,17 H30"/>'
    return (f'<svg viewBox="0 0 40 40" width="34" height="34" aria-hidden="true" fill="none" stroke="currentColor" '
            f'stroke-width="1.4" stroke-linejoin="round"><path d="{pts}"/>{bar}</svg>')

# ornamental rule (used as CSS background)
ORN = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 16'>"
       "<g fill='none' stroke='%232e2216' stroke-width='.8' stroke-linecap='round'>"
       "<path d='M2,8 H44'/><path d='M76,8 H118'/>"
       "<path d='M44,8 C48,2 54,3 54,8 C54,12 50,12 49.5,9.5'/>"
       "<path d='M76,8 C72,2 66,3 66,8 C66,12 70,12 70.5,9.5'/></g>"
       "<path d='M60,2 L64,8 L60,14 L56,8 Z' fill='%232e2216'/></svg>")
ORN_GOLD = ORN.replace("%232e2216", "%23c9a24b")

NOISE = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 .3 0 0 0 0 .2 0 0 0 0 .08 0 0 0 .2 0'/></filter>"
         "<rect width='100%25' height='100%25' filter='url(%23n)'/></svg>")
FIBRE = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'>"
         "<filter id='f'><feTurbulence type='fractalNoise' baseFrequency='.012 .09' numOctaves='4' seed='9'/>"
         "<feColorMatrix values='0 0 0 0 .35 0 0 0 0 .22 0 0 0 0 .07 0 0 0 .14 0'/></filter>"
         "<rect width='100%25' height='100%25' filter='url(%23f)'/></svg>")

# ------------------------------------------------------------------ css
CSS = """
@import url('https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@0;1&family=IM+Fell+English+SC&family=Noto+Serif+KR:wght@400;600;700&display=swap');
.ap{--parch:#ecdcb4;--parch2:#e2cd9c;--ink:#2e2216;--sepia:#6b4a2a;--muted:#7a5f3e;--gold:#c9a24b;--gold2:#e6c97c;--leather:#3a2114;--desk:#1c1510;--wax:#7b2d22;
max-width:1180px;margin:0 auto;padding:26px 18px 0;color:var(--ink);font-family:'Noto Serif KR',serif;font-size:16px;line-height:1.95;word-break:keep-all;position:relative;
background-color:var(--desk);background-image:radial-gradient(ellipse at 50% 0,rgba(120,80,40,.18),transparent 60%),url("__NOISE__")}
.ap *{box-sizing:border-box}
.ap h1,.ap h2,.ap h3,.ap h4,.ap p,.ap ul,.ap ol,.ap dl,.ap table,.ap figure{margin:0;padding:0}
.ap ul{list-style:none}
.ap a{color:var(--wax);text-underline-offset:3px}
.ap .la{font-family:'IM Fell English','Noto Serif KR',serif;font-style:italic}
.ap .sc{font-family:'IM Fell English SC','Noto Serif KR',serif;letter-spacing:.14em}
.ap .rd{position:absolute;opacity:0;pointer-events:none}

/* ---------- frame: sidebar + main */
.ap .journal{display:grid;grid-template-columns:236px 1fr;border:1px solid #47331f;border-radius:4px;overflow:hidden;box-shadow:0 18px 40px rgba(0,0,0,.6)}
.ap .side{background:linear-gradient(90deg,#24160d,#311c11 70%,#2a170d);border-right:1px solid #120a05;color:#d9c08a;padding:26px 18px 28px;position:relative}
.ap .side:before{content:"";position:absolute;inset:8px;border:1px solid rgba(201,162,75,.35);pointer-events:none}
.ap .side:after{content:"";position:absolute;inset:11px;border:1px solid rgba(201,162,75,.15);pointer-events:none}
.ap .brand{text-align:center;padding:4px 0 16px;position:relative;z-index:1}
.ap .brand svg{width:92px;height:auto;display:block;margin:0 auto 10px;filter:drop-shadow(0 5px 6px rgba(0,0,0,.55))}
.ap .brand h1{font-size:24px;font-weight:700;color:#f0d792;letter-spacing:.06em;line-height:1.2}
.ap .brand .sc{display:block;font-size:12px;color:#c9a24b;margin-top:4px;letter-spacing:.34em}
.ap .brand .la{display:block;font-size:13px;color:#b59a68}
.ap .orn-g{height:14px;margin:14px 6px;background:url("__ORN_GOLD__") center/96px 13px no-repeat}
.ap .cur{position:relative;z-index:1;text-align:center;padding:4px 0 2px}
.ap .cur .sc{font-size:11px;color:#a98c58;display:block}
.ap .cur b{display:block;font-family:'IM Fell English',serif;font-weight:400;font-size:30px;color:#f0d792;line-height:1.1;margin-top:2px}
.ap .cur span{font-size:13px;color:#cdb382;line-height:1.6;display:block}
.ap .side h4{position:relative;z-index:1;font-family:'IM Fell English SC',serif;font-weight:400;font-size:12px;letter-spacing:.3em;color:#a98c58;margin:4px 6px 6px}
.ap .si{position:relative;z-index:1;display:grid;grid-template-columns:30px 1fr;align-items:baseline;padding:7px 8px;cursor:pointer;color:#d9c08a;border-bottom:1px solid rgba(201,162,75,.14);transition:background .2s}
.ap .si:hover{background:rgba(201,162,75,.08)}
.ap .si i{font-style:normal;font-family:'IM Fell English SC',serif;font-size:12px;color:#a98c58}
.ap .si b{font-weight:600;font-size:15px}
.ap .si em{grid-column:2;font-family:'IM Fell English',serif;font-size:12px;color:#9c8257}
.ap .main{background:#1e1610;padding:0 22px 26px;min-width:0}

/* ---------- index tabs */
.ap .tbar{display:flex;flex-wrap:wrap;gap:4px;padding:16px 0 0;margin-bottom:0}
.ap .tb{cursor:pointer;padding:7px 14px 6px;font-size:14px;color:#cdb382;background:linear-gradient(#3a2316,#2b190f);border:1px solid #4d3420;border-bottom:0;border-radius:6px 6px 0 0;position:relative;top:1px}
.ap .tb:hover{color:#f0d792}
.ap .pages{border-top:1px solid #4d3420;padding-top:22px}
.ap .pages>section{display:none}
#r-cov:checked~.main .pn-cov,#r-pro:checked~.main .pn-pro,#r-el:checked~.main .pn-el,#r-sch:checked~.main .pn-sch,#r-mag:checked~.main .pn-mag,#r-wld:checked~.main .pn-wld,#r-rum:checked~.main .pn-rum,#r-tm:checked~.main .pn-tm{display:block}
#r-cov:checked~.main #l-cov,#r-pro:checked~.main #l-pro,#r-el:checked~.main #l-el,#r-sch:checked~.main #l-sch,#r-mag:checked~.main #l-mag,#r-wld:checked~.main #l-wld,#r-rum:checked~.main #l-rum,#r-tm:checked~.main #l-tm{background:var(--parch);color:var(--ink);border-color:#a88b52;font-weight:600}
#r-cov:checked~.side .s-cov,#r-pro:checked~.side .s-pro,#r-el:checked~.side .s-el,#r-sch:checked~.side .s-sch,#r-mag:checked~.side .s-mag,#r-wld:checked~.side .s-wld,#r-rum:checked~.side .s-rum,#r-tm:checked~.side .s-tm{background:linear-gradient(90deg,rgba(201,162,75,.22),rgba(201,162,75,.04));color:#f6e2a6;box-shadow:inset 2px 0 0 #c9a24b}

/* ---------- open book spread */
.ap .sp{position:relative;display:grid;grid-template-columns:1fr 1fr;margin:0 0 30px;
box-shadow:0 14px 24px rgba(0,0,0,.55),2px 3px 0 -1px #d9c592,4px 6px 0 -2px #c7ae76,6px 9px 0 -3px #ae935c,8px 12px 0 -4px #8f7546}
.ap .pg{position:relative;padding:50px 46px 66px;min-height:500px;background-color:var(--parch);
background-image:radial-gradient(ellipse at 50% 45%,transparent 55%,rgba(120,80,30,.22) 100%),url("__FIBRE__"),url("__NOISE__")}
.ap .pg.l{border-radius:4px 0 0 4px}.ap .pg.r{border-radius:0 4px 4px 0}
.ap .pg:after{content:"";position:absolute;top:0;bottom:0;width:80px;pointer-events:none}
.ap .pg.l:after{right:0;background:linear-gradient(90deg,transparent,rgba(80,50,15,.12) 55%,rgba(60,35,10,.38))}
.ap .pg.r:after{left:0;background:linear-gradient(270deg,transparent,rgba(80,50,15,.12) 55%,rgba(60,35,10,.38))}
.ap .pg:before{content:"";position:absolute;inset:16px;border:1px solid rgba(46,34,22,.22);pointer-events:none}
.ap .pg>*{position:relative;z-index:1}
.ap .rh{position:absolute!important;top:22px;font-family:'IM Fell English',serif;font-style:italic;font-size:13px;color:var(--muted)}
.ap .pg.l .rh{left:46px}.ap .pg.r .rh{right:46px}
.ap .fo{position:absolute!important;bottom:28px;left:0;right:0;text-align:center;font-family:'IM Fell English',serif;font-size:14px;letter-spacing:.12em;color:var(--muted)}
.ap .cap{font-family:'IM Fell English SC',serif;font-size:13px;letter-spacing:.24em;color:var(--sepia);display:block;margin-bottom:6px}
.ap .pg h2{font-size:clamp(26px,3.2vw,36px);font-weight:700;line-height:1.25;letter-spacing:-.01em}
.ap .orn{height:16px;margin:14px 0 22px;background:url("__ORN__") left center/120px 16px no-repeat}
.ap .pg h3{font-size:19px;font-weight:700;line-height:1.45;margin-bottom:4px}
.ap .pg h3:before{content:"§ ";font-family:'IM Fell English',serif;font-weight:400;color:var(--sepia)}
.ap .pg article+article{margin-top:20px}
.ap .pg p+p{margin-top:1em}
.ap .drop:first-letter{float:left;font-size:3.3em;line-height:.95;font-weight:700;padding:.06em .1em 0 0;color:#4a2a14}
.ap .lead{font-size:21px;font-weight:600;line-height:1.65}

/* ---------- cover spread */
.ap .cover{background:linear-gradient(135deg,#4a2c1c,#3a2114 55%,#26150c)!important;color:#e9cf8c;text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center}
.ap .cover:before{inset:14px!important;border:1px solid rgba(201,162,75,.6)!important;box-shadow:inset 0 0 0 4px rgba(0,0,0,.18),inset 0 0 0 5px rgba(201,162,75,.35)}
.ap .cover:after{display:none}
.ap .cover .rh,.ap .cover .fo{color:#a98c58}
.ap .cover svg{width:150px;height:auto;filter:drop-shadow(0 8px 10px rgba(0,0,0,.6))}
.ap .cover h1{font-size:40px;letter-spacing:.12em;color:#f3dc97;margin-top:18px;font-weight:700;text-shadow:0 1px 0 #1a0e07}
.ap .cover .sc{font-size:15px;letter-spacing:.5em;color:#c9a24b;margin-top:2px}
.ap .cover .la{font-size:18px;color:#cdb382}
.ap .cover .ds{max-width:300px;margin:18px auto 0;font-size:14px;line-height:1.85;color:#d8c08e}
.ap .cover .orn-g{width:160px}
.ap .toc li{display:grid;grid-template-columns:auto 1fr auto;align-items:baseline;gap:8px;padding:7px 0}
.ap .toc label{cursor:pointer;font-weight:600}
.ap .toc label:hover{color:var(--wax)}
.ap .toc label .la{font-weight:400;font-size:13px;color:var(--muted);margin-left:8px}
.ap .toc i{border-bottom:1px dotted rgba(46,34,22,.5);transform:translateY(-4px)}
.ap .toc span{font-family:'IM Fell English',serif}
.ap .facts{display:grid;grid-template-columns:1fr 1fr;gap:0;margin-top:26px;border-top:1px solid rgba(46,34,22,.5);border-bottom:1px solid rgba(46,34,22,.5)}
.ap .facts div{padding:10px 12px;font-size:13px;line-height:1.6;color:var(--sepia)}
.ap .facts div:nth-child(odd){border-right:1px solid rgba(46,34,22,.25)}
.ap .facts div:nth-child(-n+2){border-bottom:1px solid rgba(46,34,22,.25)}
.ap .facts b{display:block;font-size:15px;color:var(--ink)}

/* ---------- engraved plates */
.ap .plate{background:#efe2bd;padding:9px;border:1px solid rgba(46,34,22,.55);box-shadow:0 1px 0 rgba(255,255,255,.4) inset,0 4px 10px rgba(60,35,10,.25);margin:4px 0 22px}
.ap .plate .im{position:relative;border:1px solid rgba(46,34,22,.6);outline:1px solid rgba(46,34,22,.35);outline-offset:3px;overflow:hidden;background:#d9c69a}
.ap .plate img{display:block;width:100%;height:auto;filter:sepia(.62) contrast(1.06) brightness(.97);mix-blend-mode:multiply}
.ap .plate .im:after{content:"";position:absolute;inset:0;box-shadow:inset 0 0 26px rgba(70,40,10,.35);pointer-events:none}
.ap .plate figcaption{display:flex;justify-content:space-between;gap:10px;align-items:baseline;padding:9px 2px 0;font-size:14px}
.ap .plate figcaption .sc{font-size:12px;color:var(--sepia);white-space:nowrap}
.ap .plate figcaption small{display:block;font-family:'IM Fell English',serif;font-style:italic;font-size:11.5px;color:var(--muted);text-align:right;line-height:1.4}
.ap .plate.crop .im{aspect-ratio:4/3}.ap .plate.crop img{height:100%;object-fit:cover}
.ap .plate.tall .im{aspect-ratio:4/5}.ap .plate.tall img{height:100%;object-fit:cover}

/* ---------- epigraph between spreads */
.ap .epi{text-align:center;margin:-6px auto 34px;max-width:620px;color:#e6c97c}
.ap .epi p{font-size:clamp(18px,2.4vw,23px);font-weight:600;line-height:1.6;letter-spacing:.02em}
.ap .epi .la{display:block;color:#a98c58;font-size:14px;margin-top:4px}
.ap .epi .orn-g{width:200px;margin:12px auto}

/* ---------- elements */
.ap .els{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid rgba(46,34,22,.55);outline:1px solid rgba(46,34,22,.25);outline-offset:3px;margin-top:8px}
.ap .el{padding:18px 16px 16px;text-align:center}
.ap .el:nth-child(odd){border-right:1px solid rgba(46,34,22,.3)}
.ap .el:nth-child(-n+2){border-bottom:1px solid rgba(46,34,22,.3)}
.ap .el svg{display:block;margin:0 auto 6px;color:#4a2a14}
.ap .el b{display:block;font-size:22px;line-height:1.2}
.ap .el .la{display:block;font-size:13px;color:var(--muted)}
.ap .el .gd{margin-top:8px;font-weight:600;font-size:15px}
.ap .el .kw{font-size:13.5px;color:var(--sepia);line-height:1.6}
.ap .note-sm{margin-top:18px;font-size:13.5px;color:var(--sepia);line-height:1.8;text-align:center}

/* ---------- lists / misc */
.ap .menu{margin-top:12px}
.ap .menu div{display:flex;align-items:baseline;gap:8px;padding:5px 0}
.ap .menu b{font-weight:600}
.ap .menu i{flex:1;border-bottom:1px dotted rgba(46,34,22,.5);transform:translateY(-4px)}
.ap .menu span{font-size:14px;color:var(--sepia)}
.ap .bq{border-left:2px solid var(--ink);padding:4px 0 4px 18px;margin-top:6px}
.ap .bq b{display:block;font-size:20px;line-height:1.55}
.ap .bq span{display:block;margin-top:8px;font-size:15px;color:var(--sepia)}
.ap .ranks{display:grid;gap:16px;margin-top:18px}
.ap .rk{display:grid;grid-template-columns:auto 1fr;gap:16px;align-items:center;padding:12px 14px;border-top:1px solid rgba(46,34,22,.35)}
.ap .rk:last-child{border-bottom:1px solid rgba(46,34,22,.35)}
.ap .rk svg{display:block;filter:drop-shadow(0 3px 3px rgba(60,35,10,.4))}
.ap .rk b{font-size:17px}.ap .rk p{font-size:14.5px;color:var(--sepia);line-height:1.7;margin-top:2px}
.ap .route{counter-reset:r;margin:18px 0 6px;border-left:1px solid rgba(46,34,22,.5);padding-left:18px}
.ap .route li{position:relative;padding:4px 0 8px}
.ap .route li:before{counter-increment:r;content:counter(r,upper-roman);position:absolute;left:-30px;top:6px;width:22px;height:22px;border-radius:50%;background:var(--parch);border:1px solid var(--ink);font-family:'IM Fell English SC',serif;font-size:10px;line-height:20px;text-align:center}
.ap .route b{display:block;font-weight:600}.ap .route span{font-size:14px;color:var(--sepia)}
.ap .ticket{display:grid;grid-template-columns:1fr auto;margin:16px 0 18px;background:#f3e7c6;border:1px solid rgba(46,34,22,.6);outline:1px solid rgba(46,34,22,.3);outline-offset:-5px;position:relative}
.ap .ticket .tl{padding:12px 16px}
.ap .ticket .tl .sc{font-size:11px;color:var(--sepia);display:block}
.ap .ticket .tl b{display:block;font-size:18px;letter-spacing:.06em}
.ap .ticket .tl span{font-size:13px;color:var(--sepia)}
.ap .ticket .tr{padding:12px 16px;border-left:1px dashed rgba(46,34,22,.6);text-align:center;font-family:'IM Fell English SC',serif;letter-spacing:.14em;font-size:12px;color:var(--sepia);display:flex;flex-direction:column;justify-content:center}
.ap .ticket .tr b{font-family:'Noto Serif KR',serif;font-size:15px;letter-spacing:.05em;color:var(--wax)}
.ap .trio>div+div{margin-top:16px}
.ap .goldrow{display:flex;align-items:center;gap:16px;margin-top:20px;padding:12px 0;border-top:1px solid rgba(46,34,22,.35);border-bottom:1px solid rgba(46,34,22,.35)}
.ap .goldrow svg{filter:drop-shadow(0 3px 3px rgba(60,35,10,.4))}
.ap .goldrow b{font-size:20px;display:block;line-height:1.3}.ap .goldrow span{font-size:13px;color:var(--sepia)}
.ap .cat{display:grid;margin-top:20px;border:1px solid rgba(46,34,22,.6)}
.ap .cat>div{padding:16px 18px}
.ap .cat .l{background:#f8f1de}
.ap .cat .d{background:#221812;color:#d9c08a}.ap .cat .d h3:before{color:#a98c58}
.ap .cat p{font-size:14.5px;line-height:1.8}
.ap .rum{display:grid;gap:18px}
.ap .rm{padding:2px 0 0 20px;border-left:3px double rgba(46,34,22,.7)}
.ap .rm .sc{font-size:11px;color:var(--sepia)}
.ap .rm p{font-size:15px}
.ap .fm{margin:16px 0;padding:14px 16px;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink);text-align:center}
.ap .fm .f{font-family:'IM Fell English',serif;font-size:24px}
.ap .fm p{font-size:13.5px;color:var(--sepia)}
.ap .qt{padding:14px 18px;background:rgba(46,34,22,.06);border-left:2px solid var(--ink);font-style:normal}
.ap .qt p{font-size:15px}
.ap .dialw{max-width:340px;margin:0 auto}
.ap .dial{width:100%;height:auto;display:block}
.ap .dcap{text-align:center;font-size:14px;color:var(--sepia);margin-top:6px}

/* ---------- tarot */
.ap table.tar{width:100%;border-collapse:collapse;font-size:13.5px;line-height:1.5}
.ap .tar th{font-family:'IM Fell English SC',serif;font-weight:400;letter-spacing:.12em;font-size:11.5px;color:var(--sepia);text-align:left;padding:4px 6px 6px;border-bottom:1px solid var(--ink)}
.ap .tar td{padding:7px 6px;border-bottom:1px solid rgba(46,34,22,.2);vertical-align:middle}
.ap .tar th:first-child{width:52px}.ap .tar th:nth-child(2){width:30%}
.ap .tar .rn{display:inline-block;min-width:38px;padding:3px 0 2px;text-align:center;font-family:'IM Fell English SC',serif;font-size:12px;border:1px solid rgba(46,34,22,.55);outline:1px solid rgba(46,34,22,.2);outline-offset:2px;background:rgba(255,250,235,.35)}
.ap .tar td:nth-child(2) b{display:block;font-weight:600;font-size:14px}
.ap .tar td:nth-child(2) .la{font-size:12px;color:var(--muted)}
.ap .tar td:nth-child(n+3){color:var(--sepia)}
.ap .tar tr.now td{background:rgba(201,162,75,.22)}
.ap .tar tr.now .rn{background:linear-gradient(135deg,#f3dc97,#c99d45 50%,#e2c070);border-color:#2a170d;font-weight:700}

/* ---------- footer */
.ap .foot2{margin-top:18px;color:#bfa77a;font-size:13px;padding:26px 8px 34px;border-top:1px solid #3a2a1c;text-align:center}
.ap .foot2 .mk{width:44px;height:auto;margin:0 auto 6px;display:block;color:#c9a24b;opacity:.9}
.ap .foot2 .mot{font-size:15px;color:#e6c97c;margin-bottom:16px}
.ap .foot2 details{max-width:900px;margin:0 auto;text-align:left}
.ap .foot2 summary{cursor:pointer;color:#e6c97c;text-align:center;font-family:'IM Fell English SC',serif;letter-spacing:.2em}
.ap .bgs{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin-top:14px}
.ap .bg h4{color:#e6c97c;font-size:14px;margin-bottom:4px;border-bottom:1px solid #3a2a1c;padding-bottom:4px}
.ap .bg li{display:flex;justify-content:space-between;gap:8px;padding:2px 0}
.ap .bg b{font-weight:400;color:#d6c094}.ap .bg a{color:#cdb382;font-size:12px}.ap .bg span{font-size:12px;opacity:.7}
.ap .cred{margin-top:22px;font-size:11.5px;line-height:1.8;color:#8f7a55}
.ap .cred a{color:#a98c58}

@media(max-width:860px){
.ap{padding:12px 8px 0}
.ap .journal{grid-template-columns:1fr}
.ap .side{border-right:0;border-bottom:1px solid #120a05;padding:20px 16px}
.ap .brand{display:grid;grid-template-columns:64px 1fr;gap:12px;align-items:center;text-align:left;padding:0}
.ap .brand svg{width:60px;margin:0}
.ap .side .si,.ap .side h4,.ap .side .orn-g,.ap .cur{display:none}
.ap .main{padding:0 8px 16px}
.ap .sp{grid-template-columns:1fr}
.ap .pg{padding:44px 24px 60px;min-height:0;border-radius:3px!important}
.ap .pg.l .rh{left:24px}.ap .pg.r .rh{right:24px}
.ap .pg:after{display:none}
.ap .pg.r{border-top:1px solid rgba(46,34,22,.25)}
.ap .tb{padding:6px 10px;font-size:13px}
.ap .els{grid-template-columns:1fr 1fr}
}
"""
CSS = (CSS.replace("__NOISE__", NOISE).replace("__FIBRE__", FIBRE)
          .replace("__ORN_GOLD__", ORN_GOLD).replace("__ORN__", ORN))
CSS = re.sub(r"\n/\*[^*]*\*/\n", "\n", CSS)

# ------------------------------------------------------------------ content
TABS = [("cov", "표지", "Cover", "I"), ("pro", "프롤로그", "Prologue", "II"), ("el", "네 학자", "Elements", "III"),
        ("sch", "학교", "School", "IV"), ("mag", "마법", "Magic", "V"), ("wld", "세계", "Worlds", "VI"),
        ("rum", "소문", "Rumors", "VII"), ("tm", "시간", "Time", "VIII")]

plate_no = [0]
def plate(key, title, cls="", alt=""):
    plate_no[0] += 1
    s = SRC[key]
    artist = s["artist"] or "Gustave Doré"
    artist = artist.split(" / ")[0]
    year = re.match(r"\D*(\d{4})", s["date"] or "")
    year = year.group(1) if year else ("1867" if "Idylls" in s["title"] else "")
    return (f'<figure class="plate {cls}"><div class="im"><img src="{img_url(key)}" alt="{alt or title}" loading="lazy"></div>'
            f'<figcaption><span class="sc">Pl. {ROMAN[plate_no[0]]}</span><span>{title}<small>{artist}{", " + year if year else ""} · Public Domain</small></span></figcaption></figure>')


def ticket_html():
    """Vintage rail ticket glued onto the page. Frame drawn in SVG (fixed 1200x555 ratio)."""
    W, H, X = 1200, 555, 930
    outer = (f"M36,0 H{X-22} A22,22 0 0 0 {X+22},0 H{W-36} A36,36 0 0 0 {W},36 V{H-36} A36,36 0 0 0 {W-36},{H} "
             f"H{X+22} A22,22 0 0 0 {X-22},{H} H36 A36,36 0 0 0 0,{H-36} V36 A36,36 0 0 0 36,0 Z")
    inner = (f"M48,14 H{X-33} A36,36 0 0 0 {X+33},14 H{W-48} A50,50 0 0 0 {W-14},48 V{H-48} A50,50 0 0 0 {W-48},{H-14} "
             f"H{X+33} A36,36 0 0 0 {X-33},{H-14} H48 A50,50 0 0 0 14,{H-48} V48 A50,50 0 0 0 48,14 Z")
    rules = (f"M34,132 H{X-26} M232,132 V412 M232,262 H{X-26} M34,412 H{X-26} M492,412 V{H-30}")
    svg = (f'<svg class="tk-bg" viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true">'
           '<defs><pattern id="tk-kraft" patternUnits="userSpaceOnUse" width="600" height="600">'
           '<image href="assets/tex/kraft.jpg" width="600" height="600"/></pattern>'
           '<filter id="tk-ink"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="5"/>'
           '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.1 1.45"/><feComposite in="SourceGraphic" operator="in"/></filter></defs>'
           f'<path d="{outer}" fill="#dcc59b"/><path d="{outer}" fill="url(#tk-kraft)" opacity=".55" style="mix-blend-mode:multiply"/>'
           f'<g filter="url(#tk-ink)" fill="none" stroke="#1d1712"><path d="{inner}" stroke-width="3"/>'
           f'<path d="{rules}" stroke-width="2.4"/><path d="M{X},40 V{H-40}" stroke-width="5" stroke-dasharray="16 12"/>'
           f'<path d="M{X+130},70 V{H-70}" stroke-width="2"/><path d="M{X+130},{H/2-26} l9,26 l-9,26 l-9,-26 Z" fill="#1d1712"/>'
           '</g>'
           '</svg>')
    stamp = ('<svg class="tk-stamp" viewBox="0 0 120 120" aria-hidden="true"><defs><filter id="tk-rough">'
             '<feTurbulence type="fractalNoise" baseFrequency=".55" numOctaves="2" seed="11"/>'
             '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.5 1.5"/><feComposite in="SourceGraphic" operator="in"/></filter></defs>'
             '<g filter="url(#tk-rough)" fill="none" stroke="#a8740f"><circle cx="60" cy="60" r="54" stroke-width="5"/><circle cx="60" cy="60" r="42" stroke-width="2"/>'
             '<text x="60" y="70" text-anchor="middle" font-family="IM Fell English SC,serif" font-size="21" letter-spacing="1" fill="#a8740f" stroke="none">Cleared</text></g></svg>')
    return (
        '<figure class="tk-glue"><div class="tk">' + svg +
        '<div class="tk-h"><i>You are cordially carried across the worlds</i>'
        '<span>by the <em>Dimensional Rail</em> of Recuran</span></div>'
        '<div class="tk-side"><span class="tk-list">Second Class</span><i>Bound for:</i></div>'
        '<div class="tk-top"><span>From · The Far Worlds</span><span>Via · Aiphabess</span>'
        '<em class="tk-gold">{ XVIII }</em></div>'
        '<div class="tk-big">Mortalia</div>'
        '<div class="tk-bl"><span>Immigration Check</span><small>Warp Zone <b>|</b> Gold Exchange</small></div>'
        '<div class="tk-br"><span>No. 2086 <b>|</b> XCV · XVIII</span><small>Present at the platform</small></div>'
        '<div class="tk-stub"><i>Admit One</i><span>Single Passage · No. 2086</span></div>'
        + stamp + '</div><figcaption>부록 · 차원열차 승차권 견본 — 인간계(Mortalia)행</figcaption></figure>')

SPREADS = []
def spread(left, right, lh="Aiphabess", rh_l="", fol=(0, 0), lcls="", rcls="", sid=""):
    SPREADS.append(dict(left=left, right=right, lh=lh, rh_l=rh_l, fol=fol, sid=sid))
    idattr = f' id="{sid}"' if sid else ""
    return (f'<div class="sp"{idattr}>'
            f'<div class="pg l {lcls}"><span class="rh">{rh_l}</span>{left}<span class="fo">— {fol[0]} —</span></div>'
            f'<div class="pg r {rcls}"><span class="rh">{lh}</span>{right}<span class="fo">— {fol[1]} —</span></div></div>')

def head(cap, title):
    return f'<span class="cap">{cap}</span><h2>{title}</h2><div class="orn"></div>'

H = []
# cover --------------------------------------------------------------------------
toc_items = [("pro", "프롤로그", "Prologue", 2), ("el", "네 명의 학자, 네 명의 여신", "The Four Scholars", 6),
             ("sch", "학교에서 지낸다는 것", "The School", 8), ("mag", "마력과 마법사", "Magic &amp; Rank", 12),
             ("wld", "세계와 차원열차", "Worlds", 14), ("rum", "아직 닿지 않은 것들", "Rumors", 18),
             ("tm", "태양이 도는 방식", "The Cycle of Suns", 20)]
toc = "".join(f'<li><a data-goto="@@{k}@@">{t}<span class="la">{e}</span></a><i></i><span>@@n:{k}@@</span></li>' for k, t, e, p in toc_items)
cover_l = (f'{logo("cv")}<h1>아이파베스</h1><p class="sc">AIPHABESS</p><p class="la">School of All Origins</p>'
           f'<div class="orn-g"></div>'
           f'<p class="ds">5개 명문 학교 중 하나. 마법 학교이자 대도서관. 모든 종족이 이해를 배우는 곳. 레큐란 대륙 남쪽, 삼면이 바다인 반도 위의 대도시.</p>')
cover_r = (head("Index", "차례") + f'<ul class="toc">{toc}</ul>'
           '<div class="facts"><div><b>레큐란 대륙</b><span class="la">Recuran Continent</span></div>'
           '<div><b>95회전 18번째</b>달의 태양, The Moon</div>'
           '<div><b>약 2,086년째</b>인간계 환산 기준</div>'
           '<div><b>5대 명문</b>아이파베스, 서양관</div></div>')
H.append(('cov', spread(cover_l, cover_r, lh="Contents", rh_l="Aiphabess", fol=("i", "ii"), lcls="cover")))

# prologue ------------------------------------------------------------------------
pro1_l = (head("Caput II · Prologue", "프롤로그") +
          plate("gate", "아이파베스의 문 앞", "crop", "언덕 위에 솟은 고성과 그 앞의 길") +
          '<p class="lead">처음 그 문 앞에 섰을 때, 당신은 아마 말문이 막혔을 것이다.</p>')
pro1_r = ('<p class="drop" style="margin-top:10px">웅장하다거나 화려하다는 표현으로는 부족한, 그저 오래되고 깊은 무언가가 그곳에 있었다.</p>'
          '<p>아이파베스. 대마법사와 네 명의 학자들이 함께 세운 이 학교는 처음엔 연구실과 대도서관에 불과했다고 전해진다. 하지만 지금 당신 앞에 서 있는 이 공간은, 단순한 배움의 장소라기엔 너무 많은 것을 품고 있었다.</p>'
          '<p>로비 한켠에 새겨진 그 문장을 당신은 천천히 읽는다. 누가 남긴 말인지, 처음엔 알 수 없었다.</p>'
          '<p>이 학교는 마력을 자유롭게 쓸 수 있는 공간인 동시에, 위대한 업적을 남긴 존재들의 흔적이 깃든 성소이기도 하다.</p>')
epi = ('<div class="epi"><div class="orn-g"></div><p>서로를 향한 이해가 곧 가장 위대한 힘이 되리니.</p>'
       '<span class="la">— inscribed in the lobby of Aiphabess</span><div class="orn-g"></div></div>')
pro2_l = ('<p style="margin-top:12px">로비에 놓인 책들은 네 명의 학자들이 직접 손으로 써내려간 기록들이다. 희생과 마법, 그리고 수많은 이들의 발자취.</p>'
          '<p>당신은 그 책들 사이를 천천히 눈으로 훑다가 문득 어딘가에서 들은 이야기를 떠올린다. 학교 어딘가에 각 여신의 가호가 깃든 책이 네 권 숨겨져 있다고. 아무도 본 적 없고, 실재하는지조차 확인된 바 없는 그것이.</p>')
pro2_r = ('<p style="margin-top:12px">당신은 시선을 들어 끝이 보이지 않는 복도를 바라본다. 이곳에서 무엇을 배우러 왔는가. 졸업과 함께 원하는 마법을 손에 넣으러 왔는가, 아니면 소문 속 여신의 책이 실존하는지 직접 확인하러 왔는가. 어떤 이유든 상관없다. 당신은 분명 무언가를 바라고 이 문을 넘었을 것이다.</p>'
          '<div class="orn c" style="width:40%;margin:1.6em auto 1.1em"></div><p>그리고 이제, 이 학교는 당신의 이야기가 되었다.</p>')
H.append(('pro', spread(pro1_l, pro1_r, rh_l="Prologue", fol=(2, 3), sid="pro") + epi + spread(pro2_l, pro2_r, rh_l="Prologue", fol=(4, 5))))

# elements -----------------------------------------------------------------------
el_l = (head("Caput III · The Four Scholars", "네 명의 학자, 네 명의 여신") +
        '<p>불·물·땅·바람을 연구한 네 명의 학자들은 각자의 원소 너머에 있는 것들을 탐구했다. 원소마다 사계절의 여신 한 명이 이어져 있다.</p>'
        '<p>학자들이 여신들로부터 직접 가르침을 받았는지, 그 흔적을 스스로 따라갔는지는 지금도 아무도 모른다. 학교 어딘가에는 <b>각 여신의 가호가 깃든 책 네 권</b>이 숨겨져 있다는 소문만 남아 있다.</p>')
els = [("fire", "불", "Ignis · Aestas", "여름의 여신", "열정과 소멸 뒤의 재생"),
       ("water", "물", "Aqua · Hiems", "겨울의 여신", "정화와 고요한 깊이"),
       ("earth", "땅", "Terra · Ver", "봄의 여신", "탄생과 뿌리의 성장"),
       ("air", "바람", "Ventus · Autumnus", "가을의 여신", "변화와 이별의 전달")]
el_r = (plate("library", "로비의 책장", "crop wide", "높은 서가가 늘어선 도서관 내부") +
        '<div class="els">' + "".join(f'<div class="el">{alch(k)}<b>{c}</b><span class="la">{l}</span><p class="gd">{g}</p><p class="kw">{w}</p></div>' for k, c, l, g, w in els) + '</div>')
H.append(('el', spread(el_l, el_r, rh_l="The Four Scholars", fol=(6, 7), sid="el")))

# school -------------------------------------------------------------------------
sch1_l = (head("Caput IV · The School", "학교에서 지낸다는 것") +
          '<article><h3>아이파베스와 마을</h3><p>5개의 명문 학교 중 하나인 아이파베스와 그 마을을 중심으로 이야기가 진행된다. 도서관이자 학교인 아이파베스 덕분에 반도 끝의 작은 마을은 대도시로 변할 수 있었다. 삼면이 바다인 이 대도시는 무역을 통틀어 다양한 종족이 먹을 수 있는 맛집과 볼거리가 많아 살고 싶은 마을 10위 안에 들기도 한다.</p></article>'
          '<article><h3>입학과 반 배정</h3><p>학교는 15세 이후 정식 입학이 가능하지만 필수는 아니다. 어떤 나이든 졸업할 의지가 있다면 입학을 허용하기 때문에, 같은 반 안에서도 학생들의 나이는 제각각이다.</p><p>반과 속성 배정은 교장이 아닌, 학생의 조상이나 그 종족이 섬기는 신수, 혹은 위대한 업적을 남기고 사라진 존재 중 하나가 결정한다. 입학 시 점성 선생님이 그 존재들과의 접점을 시도해주며, 점성 선생님을 통해 꾸는 꿈은 그들이 그려낸 환상이나 믿음 등 다양한 형태로 나타난다. 반의 이름 역시 그들이 직접 지정해준다.</p></article>'
          '<article><h3>졸업</h3><p>졸업 조건은 한 가지로 정해져 있지 않다. 그랑프리 대회에서 우승하거나, 담당 선생님에게 공식적으로 인정받는 등 조건은 학생마다 다양하다. 졸업이 확정된 학생은 현 교장 선생님으로부터 원하는 마법을 하나 직접 배울 수 있다. 어떤 마법이든 상관없다.</p></article>')
sch1_r = ('<article style="margin-top:8px"><h3>선생님</h3><p>선생님 대부분은 이 학교 출신 졸업생이다. 자신이 배운 곳에서 다시 가르치는 자리에 서는 것, 그 자체가 하나의 순환이기도 하다. 지금까지 언급된 선생님은 다음과 같다.</p>'
          '<div class="menu"><div><b>교장 선생님</b><i></i><span>저주 속성</span></div><div><b>점성 선생님</b><i></i><span>안내자</span></div><div><b>보건 · 연금술 선생님</b><i></i><span>둘 다 독 속성, 쌍둥이</span></div></div></article>'
          '<article><h3>기숙사</h3><p>기숙사 생활은 의무다. 입학하면 부모와 잠시 이별하고 학교 안에서 생활한다. 기숙사는 반마다 하나씩 배정되며, 같은 반 학생들이 한 공간에서 함께 지낸다. 단순한 규칙이 아니라 교우 관계를 자연스럽게 만들기 위한 학교의 방침이다.</p></article>'
          '<article><h3>동양관과 서양관</h3><p>본래 하나의 학교였으나 문화 차이로 인한 소통 문제가 잦아지면서 동양과 서양으로 나뉘었다. 가르치는 방식도 다르고 교장도 두 명이다. 서양관은 아이파베스, 동양관은 적월향, 줄여서 적월 학교라 불린다.</p></article>'
          '<article><h3>도서관으로서의 아이파베스</h3><p>초기에는 방대한 역사와 기록을 책으로 엮어 학생들에게 배포했으나, 대부분 전문 연구 자료 수준으로 난해했다. 이후 선생님들이 학생들과 함께 알기 쉽게 다시 쓰면서 지금은 모든 분류의 책이 구비되어 있다. 원본 자료와 중요 서적을 열람하려면 교장과의 약속뿐 아니라 대마법사의 맹약과 4원소 학자의 서약까지 필요하다. 연구에 흥미가 있는 학생은 교장과 함께 지하로 내려가 기록을 분석하고, 이해하기 쉬운 형태로 정리하는 작업에 참여할 수 있다.</p></article>')
sch2_l = (plate("harbour", "항구 마을", "", "돛단배가 오가는 항구와 부두의 마을") +
          '<article><h3>그랑프리 대회</h3><p>4년에 한 번 아이파베스가 여는 반 대항전이다. 선후배 구분 없이 자유롭게 참여할 수 있고, 우승하면 수석 졸업 자격 또는 상금과 아이템이 주어진다. 공정성을 위해 속성이 두 개인 반과 하나인 반을 나누어 두 경기를 진행하며, 두 우승 팀이 동의하면 결승전으로 이어지기도 한다. 대회 기간에는 친선전도 함께 열린다.</p></article>')
sch2_r = ('<article style="margin-top:8px"><h3>주신의 비서 · 보좌관 시험</h3><p>신들과 가까운 점성 선생님의 신뢰를 바탕으로, 아이파베스에서는 주신의 비서나 다른 신들의 보좌관을 지원할 수 있다. 공무원 시험과 비슷한 개념이다. 점성 선생님의 신뢰는 학생의 평소 행동에 달려 있어서 난이도가 상당히 높다. 이론 시험과 실전 시험을 모두 치러야 하며, 합격자 대부분은 판단력이 뛰어나고 올바르며 성실한 학생이라고 한다.</p></article>'
          '<article><h3>졸업 후의 길</h3><p>졸업 후의 길은 마법사만이 전부가 아니다. 공방을 열거나 무기제작사로 이름을 알리는 졸업생도 있고, 학교를 떠나지 않고 교장 선생님 곁에서 지하 서적 연구를 이어가는 이들도 있다.</p></article>')
_A = re.findall(r'<article.*?</article>', sch1_l + sch1_r + sch2_l + sch2_r, flags=re.S)
_A = [re.sub(r'^<article style="margin-top:8px">', '<article>', a) for a in _A]
_harbour = re.search(r'<figure.*?</figure>', sch2_l, flags=re.S).group(0)
H.append(('sch', spread(head("Caput IV · The School", "학교에서 지낸다는 것") + _A[0] + _A[1], _A[2] + _A[3], rh_l="The School", fol=(8, 9), sid="sch")
              + spread(_A[4] + _A[5], _A[6] + _A[7], rh_l="The School")
              + spread(_A[8] + _A[9], _harbour, rh_l="The School")))

# magic --------------------------------------------------------------------------
mag_l = (head("Caput V · Magic &amp; Rank", "마력과 마법사") +
         '<div class="bq"><b>마력이 없는 것이 아니다. 잠들어 있을 뿐이다.</b><span>이 세계의 시민들은 종족이 다양하며, 마력을 자각한 존재를 마법사라 부른다. 자각하는 순간 마력은 저마다 다른 방식으로 쓰인다.</span></div>'
         '<p style="margin-top:22px">자신만의 독특한 속성을 개발해 한층 발전시키는 것도 가능하다. 속성이 두 가지인 경우도 있는데, 유전적으로 타고나기도 하고 스스로의 힘을 각성시켜 새롭게 만들어내기도 한다.</p>'
         '<p style="font-weight:700">입학 후에도 속성이 늘어날 가능성이 있으며, 훗날 각성을 통해 새로운 속성이 깨어나는 경우도 있다.</p>')
mag_r = ('<h3 style="font-size:22px;margin-top:8px">마법사 등급과 졸업 후 진로</h3>'
         '<p>졸업과 동시에 마법사 등급이 부여되며, 등급은 졸업 방식에 따라 달라진다.</p>'
         '<div class="ranks">'
         f'<div class="rk">{medallion("m1", "1급", "PRIMA")}<div><b>마스터 반 · 그랑프리 우승</b><p>1급 마법사로 즉시 진급한다.</p></div></div>'
         f'<div class="rk">{medallion("m2", "2·3급", "SECUNDA")}<div><b>그 외의 조건으로 졸업</b><p>2급 또는 3급을 받고, 1급 시험 응시 자격이 함께 주어진다.</p></div></div>'
         '</div><div style="margin-top:24px">' + plate("scholar", "숲속의 노학자", "crop wide", "숲속에서 책을 펼쳐 든 노학자") + '</div>')
H.append(('mag', spread(mag_l, mag_r, rh_l="Magic &amp; Rank", fol=(12, 13), sid="mag")))

# worlds -------------------------------------------------------------------------
wld1_l = (head("Caput VI · Worlds", "세계와 차원열차") +
          '<p class="drop">아이파베스의 초대장은 경계를 가리지 않는다. 가까운 마을은 물론, 이름조차 낯선 머나먼 세계에서도 초대장을 받고 찾아오는 존재들이 있다. 그래서 학생들의 출신을 한마디로 단정하기는 어렵다. 단, 천사와 악마, 신은 입학할 수 없다.</p>'
          '<ol class="route"><li><b>머나먼 세계</b><span>초대장을 받은 존재들의 출발지</span></li><li><b>차원열차</b><span>대도시 한켠의 승강장</span></li><li><b>아이파베스</b><span>입학과 도서관의 도시</span></li><li><b>인간계</b><span>입국심사를 거쳐야 함</span></li></ol>'
          '<p>아무리 먼 곳에서 왔더라도 이곳에 닿을 수 있는 것은 대도시 한켠의 차원열차 덕분이다. 다만 인간계로 향하는 열차는 별도의 입국심사를 거쳐야 한다. 마법사가 인간계에 무분별하게 유입되는 것을 막기 위한 절차다.</p>')
wld1_r = ('<div class="trio" style="margin-top:8px">'
          '<div><h3>인간계 방문</h3><p>마법사가 인간계를 찾을 때는 인간의 향수를 쓴다. 뿌리면 인간들에게 평범한 인간으로 인식된다. 종류가 다양하며 주로 정령이 제조하고, 향이 은은하고 좋을수록 비싸다.</p></div>'
          '<div><h3>수호자</h3><p>소환자와 소환자의 마을, 집, 교실 등을 지키는 사명을 띠고 소환되는 존재. 동양의 성주신과 비슷하며 형태는 다양하다. 염원이 강할수록 더 강한 수호자를 소환하거나 만들어낼 수 있다. 이름이 부여된 수호자는 천사와 악마를 제외하면 극히 드물다.</p></div>'
          '<div><h3>골드</h3><p>공식 워프존으로 인간계에 가면 보유한 골드가 그 나라의 화폐로 자동 환전된다. 이 점을 이용해 환율 차익을 노리는 주식 마법사들도 적지 않다.</p></div></div>'
          f'<div class="goldrow">{coin()}<div><b>100골드 = 약 10,000원</b><span>한화 기준 환산</span></div></div>')
wld2_l = ('<h3 style="font-size:22px;margin-top:8px">천마계 통판북</h3>'
          '<p>천계와 마계의 물품을 정리한 카탈로그. 주 이용 연령층은 22세에서 80세까지다. 서명이 끝나면 보유 금액에서 자동으로 차감되고 5초 안에 배달된다.</p>'
          '<div class="cat"><div class="l"><h3>천계 상품</h3><p>흰 종이에 단정한 서체로 인쇄되어 있다. 흰 깃털 펜으로 서명한다.</p></div>'
          '<div class="d"><h3>마계 상품</h3><p>검은 종이에 강렬한 서체로 인쇄되어 있다. 검은 깃털 펜 또는 검은 볼펜으로 서명한다. 장난용이거나 위험한 물품이 섞여 있어 18세 미만은 사용할 수 없다.</p></div></div>')
wld2_r = plate("lighthouse", "포구의 등대", "crop wide", "폭풍 치는 해안에 선 등대") + ticket_html()
H.append(('wld', spread(wld1_l, wld1_r, rh_l="Worlds", fol=(14, 15), sid="wld") + spread(wld2_l, wld2_r, rh_l="Worlds", fol=(16, 17))))

# rumors -------------------------------------------------------------------------
rum_l = (head("Caput VII · Rumors", "아직 닿지 않은 것들") +
         '<div class="rum">'
         '<div class="rm"><span class="sc">Rumor · I</span><h3>대마법사의 행방</h3><p>아이파베스를 설계한 대마법사가 지금 어디에 있는지는 아무도 모른다. 4원소 학자들도 1000년이 넘는 시간 전에 세상을 떠났고, 지금은 그들이 남긴 기록과 흔적만이 학교 곳곳에 남아 있다.</p></div>'
         '<div class="rm"><span class="sc">Rumor · II</span><h3>여신의 가호가 깃든 책</h3><p>학교 어딘가에 네 권이 숨겨져 있다는 소문. 아무도 본 적이 없고, 실재하는지도 확인된 바 없다.</p></div>'
         '<div class="rm"><span class="sc">Rumor · III</span><h3>주선교와 죄악교</h3><p>최근 급증한 교단으로, 피해와 학살 사건이 여러 차례 발생했다. 교단마다 목적은 달랐지만, 무언가를 소환하는 것이 아니라 직접 만들어내려 한다는 점은 같았다. 확실한 증거 없이는 교단을 검거하기 어려워 수사는 난항을 겪고 있다.</p></div>'
         '</div>')
rum_r = plate("tower", "탑과 숨겨진 책", "tall", "달빛 아래 언덕 위에 선 탑")
H.append(('rum', spread(rum_l, rum_r, rh_l="Rumors", fol=(18, 19), sid="rum")))

# time ---------------------------------------------------------------------------
tm_l = (head("Caput VIII · The Cycle of Suns", "태양이 도는 방식") +
        f'<div class="dialw">{dial()}</div><p class="dcap">22개의 태양이 한 바퀴. 지금은 95회전 18번째, 달(XVIII)의 태양.</p>')
tm_r = ('<p style="margin-top:8px" class="drop">시간과 날짜는 인간계와 같이 0~24시, 1~12월로 적는다. 다만 연도는 2001년, 2002년 식으로 적지 않는다. 타로 카드의 순서대로 돌아간다. 예를 들어 2회전 12번째의 태양이라고 적는다. 태양이 바뀌는 날은 인간계 기준으로 1년이다.</p>'
        '<div class="fm"><div class="f">(95 − 1) × 22 + 18 = 2,086</div><p>(회전수 − 1) × 22 + 태양 번호. 1회전은 22년이다.</p></div>'
        '<p>현재 95회전 18번째 달의 태양은 인간계 기준으로 약 2,086년째. 월과 일은 인간계와 같고, 기준일은 3월 7일이다.</p>'
        '<div class="qt" style="margin-top:16px"><p>그 태양에 태어난 아이들은 정위치의 기운과 역위치의 기운이 흐른다.</p><p>이번 태양은 여교황의 태양이므로, 지식이 풍부한 아이들이 태어날 것이다.</p></div>'
        '<p style="margin-top:12px">마법사들은 이런 말을 주고받을 만큼 신앙이 깊다.</p>')
TAROT = [("The Fool", "광대", "모험, 무지(無知)", "경솔, 어리석음"), ("The Magician", "마술사", "창조, 수완", "겁많음, 기만"),
         ("The High Priestess", "여교황", "지식, 총명", "잔혹, 무례함"), ("The Empress", "여제", "풍양, 모성", "과잉, 허영"),
         ("The Emperor", "황제", "책임, 부성(父性)", "오만, 존대"), ("The Hierophant", "교황", "가르침, 관대함", "협량, 나태"),
         ("The Lovers", "연인", "연애, 쾌락", "질투, 배신"), ("The Chariot", "전차", "전진, 승리", "폭주, 좌절"),
         ("Strength", "힘", "힘, 용기", "본성, 자만"), ("The Hermit", "은둔자", "탐색, 사려깊음", "음습, 폐쇄적, 탐욕"),
         ("Wheel of Fortune", "운명", "기회, 일시적인 행운", "오산, 불운"), ("Justice", "정의", "균형, 정당함", "편견, 부정"),
         ("The Hanged Man", "매달린 사람", "자기희생, 인내", "무의미한 희생, 맹목"), ("Death", "죽음", "격변, 이별", "변화의 유보, 고착"),
         ("Temperance", "절제", "조화, 견실", "낭비, 불안정"), ("The Devil", "악마", "사심, 속박, 타락", "악순환으로부터의 각성"),
         ("The Tower", "탑", "파괴, 파멸", "필요로 하는 파괴"), ("The Star", "별", "희망, 동경", "환멸, 비애"),
         ("The Moon", "달", "불안, 애매함, 혼돈", "불안 해소, 명료함, 혼돈의 끝"), ("The Sun", "태양", "밝은 미래, 만족", "연기(延期), 실패"),
         ("Judgement", "심판", "부활, 개선", "재기불능, 후회"), ("The World", "세계", "완성, 완전", "미완성, 어중간함")]
def tarot_table(rng):
    rows = []
    for i in rng:
        en, ko, up, rv = TAROT[i]
        cls = ' class="now"' if i == 18 else ""
        rows.append(f'<tr{cls}><td><span class="rn">{ROMAN[i]}</span></td><td><b>{ko}</b><span class="la">{en}</span></td><td>{up}</td><td>{rv}</td></tr>')
    return ('<table class="tar"><thead><tr><th>No.</th><th>Arcana</th><th>정위치</th><th>역위치</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>')
tar_l = '<span class="cap" style="margin-top:6px">Arcana Maiora · 0 – X</span>' + tarot_table(range(0, 11))
tar_r = '<span class="cap" style="margin-top:6px">Arcana Maiora · XI – XXI</span>' + tarot_table(range(11, 22))
H.append(('tm', spread(tm_l, tm_r, rh_l="The Cycle of Suns", fol=(20, 21), sid="tm") + spread(tar_l, tar_r, lh="Tarot", rh_l="Tarot", fol=(22, 23))))

# footer -------------------------------------------------------------------------
BGM = rd("build/bgm.html").strip()
credits = " · ".join(
    f'<a href="{s["page"]}">{(s["artist"] or "Gustave Doré").split(" / ")[0]}</a>' for s in SRC.values())
footer = (f'<footer class="foot2" id="bgm">{logo("ft", "mono", "mk")}'
          '<p class="mot">서로를 향한 이해가 곧 가장 위대한 힘이 되리니.</p>'
          f'<details><summary>마학 BGM</summary>{BGM}</details>'
          f'<p class="cred">삽화: 퍼블릭 도메인 판화 (Wikimedia Commons) — {credits}</p></footer>')

# ------------------------------------------------------------------ site pages
import shutil, sys
sys.path.insert(0, os.path.join(ROOT, "build"))
from map_svg import town_map

CSS = CSS.replace("family=Noto+Serif+KR:wght@400;600;700", "family=Gowun+Batang:wght@400;700&family=Song+Myung&family=Hahmlet:wght@500;700;900&family=Diphylleia&family=Noto+Serif+KR:wght@400;700")
SITE_CSS = CSS + """
html,body{margin:0;background:#140e0a}
.ap{min-height:100vh}
.ap .snav{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin:0 0 18px;padding:10px 14px;background:linear-gradient(#2c1a10,#21130b);border:1px solid #47331f;border-radius:4px}
.ap .snav .sb{display:flex;align-items:center;gap:10px;margin-right:auto;color:#f0d792;text-decoration:none;font-weight:700;letter-spacing:.08em}
.ap .snav .sb svg{width:26px;height:auto}
.ap .snav>a:not(.sb){color:#cdb382;text-decoration:none;padding:6px 14px;border:1px solid transparent;border-radius:3px;font-size:15px}
.ap .snav>a:not(.sb):hover{color:#f6e2a6;border-color:rgba(201,162,75,.35)}
.ap .snav>a.on{color:#2a170d;background:linear-gradient(135deg,#f3dc97,#c99d45 55%,#e2c070);font-weight:600}
.ap .snav .la{font-size:12px;opacity:.75;margin-left:6px}

/* newspaper */
.ap .np{max-width:1120px;margin:0 auto 30px;padding:26px 34px 34px;color:#17130f;background-color:#efe9da;
background-image:radial-gradient(ellipse at 50% 40%,transparent 60%,rgba(90,70,40,.18)),url("__NOISE__");box-shadow:0 16px 30px rgba(0,0,0,.6)}
.ap .np *{color:inherit}
.ap .np-top{display:flex;justify-content:space-between;font-size:12.5px;border-bottom:1px solid #17130f;padding-bottom:6px;font-family:'IM Fell English SC',serif;letter-spacing:.12em}
.ap .np-title{text-align:center;padding:14px 0 6px}
.ap .np-title h1{font-size:clamp(46px,8vw,86px);font-weight:900;letter-spacing:.12em;line-height:1}
.ap .np-title .sc{display:block;font-size:15px;letter-spacing:.5em;margin-top:8px}
.ap .np-date{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;border-top:3px double #17130f;border-bottom:3px double #17130f;padding:6px 2px;font-size:13.5px;margin-bottom:18px}
.ap .np-front{display:grid;grid-template-columns:2fr 1fr;gap:0;border-bottom:1px solid #17130f;padding-bottom:18px;margin-bottom:18px}
.ap .np-front>.lead{padding-right:22px;border-right:1px solid #17130f}
.ap .np-front>aside{padding-left:22px}
.ap .np .kick{font-family:'IM Fell English SC',serif;letter-spacing:.18em;font-size:12px;display:block;margin-bottom:4px}
.ap .np h2{font-size:clamp(26px,3.4vw,38px);font-weight:900;line-height:1.25;letter-spacing:-.02em}
.ap .np h3{font-size:19px;font-weight:900;line-height:1.35;margin-bottom:6px}
.ap .np .deck{font-size:16px;font-weight:600;margin:8px 0 12px;line-height:1.6}
.ap .np p{font-size:14.5px;line-height:1.85;text-align:left}
.ap .np p+p{margin-top:.7em}
.ap .np figure{margin:4px 0 12px}
.ap .np figure img{display:block;width:100%;height:auto;filter:grayscale(1) contrast(1.12) brightness(1.02);mix-blend-mode:multiply}
.ap .np figure.crop{aspect-ratio:16/9;overflow:hidden}.ap .np figure.crop img{height:100%;object-fit:cover}
.ap .np figcaption{font-size:12px;font-style:italic;padding-top:4px;border-bottom:1px solid #17130f;padding-bottom:4px;display:flex;justify-content:space-between;gap:8px}
.ap .np .cols{columns:3 240px;column-gap:26px;column-rule:1px solid #17130f}
.ap .np .cols>figure{break-inside:avoid;display:block}
.ap .np .cols>article,.ap .np .cols>.box{break-inside:avoid;margin-bottom:20px;padding-bottom:18px;border-bottom:1px solid rgba(23,19,15,.4)}
.ap .np .box{border:1px solid #17130f;outline:1px solid #17130f;outline-offset:-5px;padding:16px 16px 14px!important;text-align:center}
.ap .np .box h3{font-size:20px;letter-spacing:.05em}
.ap .np .box p{text-align:center;font-size:13.5px}
.ap .np .box .big{font-size:26px;font-weight:900;margin:6px 0;display:block}
.ap .np .ad{background:#17130f;color:#efe9da;outline-color:#efe9da}
.ap .np .ad *{color:#efe9da}
.ap .np table{width:100%;border-collapse:collapse;font-size:13.5px;margin-top:6px}
.ap .np td{padding:4px 2px;border-bottom:1px dotted rgba(23,19,15,.5)}
.ap .np td:last-child{text-align:right;font-family:'IM Fell English',serif}
.ap .np-foot{border-top:3px double #17130f;padding-top:8px;font-size:12.5px;text-align:center;font-style:italic}

/* town map page */
.ap .mp{max-width:1180px;margin:0 auto 30px}
.ap .mp-head{text-align:center;color:#e6c97c;margin:6px 0 18px}
.ap .mp-head h1{font-size:clamp(28px,4vw,40px);color:#f3dc97;letter-spacing:.06em}
.ap .mp-head .la{color:#b59a68;font-size:16px}
.ap .mp-head p{color:#cdb382;font-size:14.5px;max-width:700px;margin:10px auto 0;line-height:1.8}
.ap .mp-map{background:#e4d3a6;padding:10px;box-shadow:0 16px 30px rgba(0,0,0,.6);border:1px solid #6b4a2a}
.ap .tmap{display:block;width:100%;height:auto}
.ap .tmap .dm{cursor:pointer}
.ap .tmap .dm:hover circle:first-child{fill:#f3dc97}
.ap .mp-dist{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px;margin-top:22px}
.ap .dcard{padding:18px 20px 16px;background-color:var(--parch);background-image:url("__NOISE__");border:1px solid rgba(46,34,22,.5);scroll-margin-top:20px;transition:box-shadow .3s}
.ap .dcard:target{box-shadow:0 0 0 3px #c9a24b,0 0 24px rgba(201,162,75,.5)}
.ap .dcard .no{display:inline-block;width:26px;height:26px;border-radius:50%;border:1px solid var(--ink);text-align:center;line-height:24px;font-family:'IM Fell English SC',serif;font-size:13px;margin-right:8px}
.ap .dcard h3{display:inline;font-size:18px}
.ap .dcard .la{display:block;font-size:13px;color:var(--muted);margin:2px 0 8px}
.ap .dcard p{font-size:14px;line-height:1.75}
.ap .dcard .tag{display:inline-block;margin-top:8px;font-size:11.5px;padding:1px 8px;border:1px solid rgba(46,34,22,.4);color:var(--sepia)}
.ap .mp-hist{margin-top:26px;padding:26px 30px;background-color:var(--parch);background-image:url("__NOISE__");border:1px solid rgba(46,34,22,.5)}
.ap .mp-hist h2{font-size:24px}
.ap .mp-hist ol{list-style:none;counter-reset:h;display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin-top:14px}
.ap .mp-hist li{counter-increment:h;border-top:2px solid var(--ink);padding-top:8px;font-size:14px;line-height:1.7}
.ap .mp-hist li:before{content:counter(h,upper-roman);font-family:'IM Fell English SC',serif;font-size:13px;color:var(--sepia);display:block}
.ap .mp-hist li b{display:block;font-size:16px}
@media(max-width:860px){.ap .np{padding:18px 16px}.ap .np-front{grid-template-columns:1fr}.ap .np-front>.lead{padding-right:0;border-right:0;border-bottom:1px solid #17130f;padding-bottom:16px;margin-bottom:16px}.ap .np-front>aside{padding-left:0}}

/* ===== typography ===== */
.ap{font-family:'Gowun Batang','Noto Serif KR',serif;font-size:16.5px}
.ap .pg h2,.ap .brand h1,.ap .cover h1,.ap .mp-head h1,.ap .dcard h3,.ap .mp-hist h2,.ap .np-title h1,.ap .el b,.ap .snav .sb span{font-family:'Song Myung','Noto Serif KR',serif;font-weight:400}
.ap .pg h2{font-size:clamp(30px,3.6vw,42px);letter-spacing:.01em}
.ap .pg h3{font-family:'Song Myung','Noto Serif KR',serif;font-weight:400;font-size:21px}
.ap .cover h1{font-size:46px}
.ap .brand h1{font-size:27px}
.ap .lead,.ap .epi p,.ap .bq b,.ap .qt p{font-family:'Diphylleia','Gowun Batang',serif;font-weight:400}
.ap .lead{font-size:23px}.ap .epi p{font-size:clamp(20px,2.6vw,27px)}.ap .bq b{font-size:22px}
.ap .toc label,.ap .menu b,.ap .route b,.ap .rk b,.ap .facts b,.ap .ticket .tl b,.ap .tar td:nth-child(2) b{font-family:'Song Myung','Gowun Batang',serif;font-weight:400;font-size:1.08em}
.ap .drop:first-letter{font-family:'Song Myung',serif;font-weight:400;font-size:3.6em}
.ap .np{font-family:'Gowun Batang',serif}
.ap .np h2,.ap .np h3,.ap .np .box .big{font-family:'Hahmlet','Gowun Batang',serif;font-weight:900;letter-spacing:-.03em}
.ap .np .deck{font-family:'Hahmlet',serif;font-weight:500}
.ap .np-title h1{font-size:clamp(54px,9vw,104px);letter-spacing:.08em}

/* ===== animation ===== */
@keyframes ap-rise{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:none}}
@keyframes ap-fade{from{opacity:0}to{opacity:1}}
@keyframes ap-turn{0%{transform:perspective(2200px) rotateY(-96deg);filter:brightness(.55)}55%{filter:brightness(1.06)}100%{transform:perspective(2200px) rotateY(0);filter:none}}
@keyframes ap-develop{from{opacity:.15;filter:sepia(.62) contrast(.5) brightness(1.6) blur(3px)}to{opacity:1;filter:sepia(.62) contrast(1.06) brightness(.97) blur(0)}}
@keyframes ap-glow{0%,100%{text-shadow:0 0 0 rgba(243,220,151,0)}50%{text-shadow:0 0 14px rgba(243,220,151,.55)}}
@keyframes ap-flicker{0%,100%{opacity:.9}42%{opacity:1}47%{opacity:.82}53%{opacity:.97}78%{opacity:.88}}
@keyframes ap-swing{from{transform:rotate(-220deg)}to{transform:rotate(0)}}
@keyframes ap-drop{from{opacity:0;transform:translateY(-40px) rotate(-1.6deg)}70%{transform:translateY(4px) rotate(.3deg)}to{opacity:1;transform:none}}
@keyframes ap-draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
@keyframes ap-pop{from{opacity:0;transform:scale(.2)}70%{transform:scale(1.15)}to{opacity:1;transform:none}}
@keyframes ap-drift{from{transform:translateX(-16px)}to{transform:translateX(16px)}}
@keyframes ap-beam{0%,100%{opacity:.15}50%{opacity:.9}}
@keyframes ap-sway{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(4deg)}}
.ap:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 50% 30%,rgba(255,190,110,.10),transparent 65%);animation:ap-flicker 5s infinite}
.ap>*{position:relative;z-index:1}
.ap .snav{animation:ap-fade .8s both}
.ap .journal,.ap .mp-head,.ap .mp-map{animation:ap-rise 1s cubic-bezier(.2,.7,.2,1) both}
.ap .cur b{animation:ap-glow 4s ease-in-out infinite}
.ap .pages>section .sp{perspective:2200px}
.ap .pages>section .pg.r{transform-origin:left center;animation:ap-turn 1.1s cubic-bezier(.3,.6,.15,1) both;backface-visibility:hidden}
.ap .pages>section .pg.l{animation:ap-fade .7s .15s both}
.ap .pages>section .sp+.sp .pg.r,.ap .pages>section .epi+.sp .pg.r{animation-delay:.25s}
.ap .pages>section .pg>*:not(.rh):not(.fo){animation:ap-rise .8s .45s both}
.ap .plate img{animation:ap-develop 2.2s .6s both}
.ap .epi{animation:ap-fade 1.6s .5s both}
.ap .dial .needle{transform-box:view-box;transform-origin:200px 200px;animation:ap-swing 2.6s cubic-bezier(.15,.85,.25,1) .5s both}
.ap .rk svg,.ap .goldrow svg{transition:transform .5s}.ap .rk:hover svg,.ap .goldrow:hover svg{transform:rotate(12deg) scale(1.06)}
.ap .si,.ap .tb{transition:background .25s,color .25s}
.ap .np{animation:ap-drop 1.1s cubic-bezier(.2,.7,.2,1) both}
.ap .np-front>*,.ap .np .cols>*{animation:ap-rise .8s both}
__NP_DELAYS__
.ap .np figure img{transition:filter .6s}.ap .np figure:hover img{filter:grayscale(.3) sepia(.4) contrast(1.05)}
.ap .tmap .coast{stroke-dasharray:1;animation:ap-draw 3.2s cubic-bezier(.4,.1,.2,1) .4s both}
.ap .tmap .wl{animation:ap-fade 2.4s 1.6s both}
.ap .tmap .dm{transform-box:fill-box;transform-origin:center;animation:ap-pop .6s both}
__DM_DELAYS__
.ap .tmap .fog{animation:ap-drift 7s ease-in-out infinite alternate}
.ap .tmap .beam{animation:ap-beam 2.6s ease-in-out infinite}
.ap .tmap .rose{transform-box:fill-box;transform-origin:center;animation:ap-sway 9s ease-in-out infinite}
.ap .tmap .rose.r2{animation-duration:12s;animation-direction:reverse}
.ap .dcard{animation:ap-rise .7s both}
.ap .dcard:hover{transform:translateY(-3px);transition:transform .3s}
@media (prefers-reduced-motion:reduce){.ap *,.ap:before{animation:none!important;transition:none!important}}
/* ===== objects on the desk (shared with the book page) ===== */
.desk .ap{background:none;padding-top:22px}
.desk .ap:before{display:none}
.ap .np{background:#efe8d6 url(tex/paper-creased.jpg) center/cover;background-blend-mode:multiply;rotate:-.5deg;box-shadow:0 22px 40px rgba(0,0,0,.65),0 2px 4px rgba(0,0,0,.4)}
.ap .mp-map{background:#e6d6ab url(tex/paper-creased.jpg) center/cover;background-blend-mode:multiply;rotate:.35deg;border:0;box-shadow:0 22px 40px rgba(0,0,0,.65)}
.ap .tmap{mix-blend-mode:multiply}
.ap .dcard,.ap .mp-hist{background:#efe2c4 url(tex/paper.jpg) center/420px;background-blend-mode:multiply;border:0;box-shadow:0 8px 16px rgba(0,0,0,.5)}
.ap .dcard:nth-child(3n+1){rotate:-.6deg}.ap .dcard:nth-child(3n+2){rotate:.4deg}.ap .dcard:nth-child(3n){rotate:-.2deg}
.ap .mp-head h1,.ap .mp-head .la,.ap .mp-head p{text-shadow:0 2px 4px #000}
.ap .foot2{border-top:0}
/* ===== tri-fold tourist pamphlet (two-colour print: ink + vermilion) ===== */
.pam-desk{padding:10px 0 20px}
.pamw{width:min(1080px,94vw);margin:20px auto 0;container-type:inline-size}
.pam{--red:#b0412a;--ink:#1f1a15;position:relative;width:100%;display:grid;grid-template-columns:repeat(3,1fr);aspect-ratio:3/2.12;perspective:2600px;transform-style:preserve-3d;rotate:-.4deg}
.pp{position:relative;transform-style:preserve-3d;transition:transform 1.1s cubic-bezier(.45,.05,.2,1)}
.p1{transform-origin:right center;z-index:3}.p3{transform-origin:left center;z-index:2}
.pam:not(.open) .p1{transform:rotateY(180deg) translateZ(-3px);transition-delay:.55s}
.pam:not(.open) .p3{transform:rotateY(-180deg) translateZ(-1.5px)}
.pam.open .p3{transition-delay:.6s}
.face{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;overflow:hidden;box-sizing:border-box;container-type:inline-size;
  padding:2.4cqw 2.4cqw 2cqw;color:var(--ink);font-family:'Gowun Batang',serif;font-size:calc(100cqw / 76);line-height:1.62;word-break:keep-all;
  background:#f3ead4 url(tex/paper.jpg) center/48cqw;background-blend-mode:multiply;box-shadow:0 18px 30px rgba(0,0,0,.55)}
.face.out{transform:rotateY(180deg)}
.p1 .in{box-shadow:inset -14px 0 18px -14px rgba(60,40,15,.45),0 18px 30px rgba(0,0,0,.55)}
.p2 .in{box-shadow:inset 14px 0 18px -14px rgba(60,40,15,.35),inset -14px 0 18px -14px rgba(60,40,15,.35),0 18px 30px rgba(0,0,0,.55)}
.p3 .in{box-shadow:inset 14px 0 18px -14px rgba(60,40,15,.45),0 18px 30px rgba(0,0,0,.55)}
.face h2{margin:0 0 .6em;font-family:'Song Myung',serif;font-weight:400;font-size:1.55em;line-height:1.2;color:var(--ink);border-bottom:2px solid var(--red);padding-bottom:.25em}
.face h2 i{font-style:normal;font-family:'IM Fell English SC',serif;color:var(--red);font-size:.7em;margin-right:.45em}
.face h2 small{display:block;font-family:'IM Fell English',serif;font-style:italic;font-size:.5em;color:#6b5a48;margin-top:.2em}
.face h3{margin:.7em 0 .1em;font-family:'Song Myung',serif;font-weight:400;font-size:1.12em;color:var(--red)}
.face p{margin:0}.face .small{font-size:.8em;color:#5a4a3a;margin-top:.3em}
.face ul{margin:.2em 0 0;padding:0;list-style:none}
.face li{position:relative;padding-left:.9em;margin:.25em 0;font-size:.9em}
.face li:before{content:"";position:absolute;left:0;top:.62em;width:.38em;height:.38em;background:var(--red);transform:rotate(45deg)}
.face li b{display:block;font-family:'Song Myung',serif;font-weight:400}
.pbox{margin:.9em 0 .4em;padding:.6em .8em .7em;border:1px solid var(--ink);outline:1px solid var(--ink);outline-offset:-4px}
.pbox h4{margin:0 0 .2em;font-family:'IM Fell English SC',serif;font-weight:400;letter-spacing:.14em;font-size:.85em;color:var(--red)}
.pbox.red{background:var(--red);color:#f6ead2;outline-color:#f6ead2;border-color:var(--red)}.pbox.red h4{color:#f6ead2}
.pbox p{font-size:.88em}
.pimg{margin:.6em 0 .2em}.pimg img{display:block;width:100%;height:auto;mix-blend-mode:multiply;filter:grayscale(1) sepia(.25) contrast(1.15)}
.pimg figcaption{font-family:'IM Fell English',serif;font-style:italic;font-size:.62em;color:#7a6a58;text-align:right}
.pimg.tall img{aspect-ratio:4/3;object-fit:cover}
.pimg.wide img{aspect-ratio:16/8;object-fit:cover}
.spot{display:grid;grid-template-columns:38% 1fr;gap:.7em;align-items:start;margin-top:.5em}
.spot .pimg{margin:.15em 0 0}.spot .pimg img{aspect-ratio:1;object-fit:cover}.spot h3{margin-top:0}.spot p{font-size:.88em}
/* cover */
.pcover{cursor:pointer;display:flex;flex-direction:column;align-items:center;text-align:center;padding:2.8cqw 2.8cqw 2.4cqw}
.pcover .pt{font-size:.78em;letter-spacing:.12em;color:#5a4a3a}
.pcover .pimg{width:100%;margin:.8em 0 .3em}
.pcover h1{margin:.2em 0 0;font-family:'Song Myung',serif;font-weight:400;font-size:3em;letter-spacing:.12em;line-height:1}
.pcover .ps{font-family:'Song Myung',serif;font-size:1.25em;color:var(--red);letter-spacing:.3em;margin-top:.35em}
.pcover .pr{width:60%;height:3px;margin:.8em auto;border-top:1px solid var(--red);border-bottom:1px solid var(--red)}
.pcover .tag{font-family:'Diphylleia',serif;font-size:1.05em;line-height:1.6}
.pcover .badge{margin-top:auto;display:inline-block;padding:.4em 1em;border:2px solid var(--red);color:var(--red);font-family:'Song Myung',serif;font-size:.9em;rotate:-4deg}
.pcover .badge b{display:block;font-size:1.9em;font-weight:400;line-height:1}
.pcover .pf{margin-top:.9em;font-family:'IM Fell English SC',serif;font-size:.65em;letter-spacing:.3em;color:#5a4a3a}
.pam:not(.open) .pcover:hover{filter:brightness(1.04)}
.pback{display:flex;height:100%;align-items:flex-end;justify-content:center;text-align:center;font-size:.8em;color:#6b5a48}
/* map panel */
.pmap{display:block;position:relative;width:100%;padding:0;border:1px solid var(--ink);background:none;cursor:zoom-in}
.pmap svg{display:block;width:100%;height:auto;mix-blend-mode:multiply}
.pmap span{position:absolute;right:.4em;bottom:.4em;font-size:.7em;background:var(--red);color:#f6ead2;padding:.1em .6em}
.legend{margin:.7em 0 0;padding:0;list-style:none;columns:1}
.legend li{display:grid;grid-template-columns:1.6em 1fr auto;align-items:baseline;gap:.3em;padding:.12em 0 .12em;margin:0;border-bottom:1px dotted rgba(31,26,21,.35);font-size:.86em}
.legend li:before{display:none}
.legend li b{font-family:'IM Fell English SC',serif;color:var(--red);font-weight:400;text-align:center}
.legend li span{font-family:'Song Myung',serif}.legend li em{font-style:normal;font-size:.82em;color:#6b5a48}
.legend li.hl{background:rgba(176,65,42,.15)}
.pam-hint{text-align:center;color:#cdb382;font-size:13px;margin:26px 0 0;text-shadow:0 1px 2px #000}.pam-hint a{color:#e6c97c}
.lightbox{position:fixed;inset:0;z-index:50;background:rgba(10,6,3,.82);display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:zoom-out}
.lightbox[hidden]{display:none}
.lb-in{width:min(1200px,94vw);background:#e6d6ab url(tex/paper-creased.jpg) center/cover;background-blend-mode:multiply;padding:10px;box-shadow:0 20px 40px #000}
.lb-in svg{display:block;width:100%;height:auto;mix-blend-mode:multiply}
.lightbox p{color:#cdb382;font-size:13px}
@media(max-width:760px){.pam{grid-template-columns:1fr;aspect-ratio:auto;rotate:0deg}.pp{transform:none!important}.face{position:relative;font-size:calc(100cqw / 25);padding:7cqw}.face.out{display:none}}
""".replace("__NOISE__", NOISE).replace("__NP_DELAYS__", "".join(
    f".ap .np-front>*:nth-child({i}),.ap .np .cols>*:nth-child({i}){{animation-delay:{.5 + i * .09:.2f}s}}" for i in range(1, 20))).replace(
    "__DM_DELAYS__", "".join(f".ap .tmap .dm:nth-of-type({i}){{animation-delay:{2.2 + i * .14:.2f}s}}" for i in range(1, 10)))

NAV_ITEMS = [("index.html", "세계관 책", "Liber"), ("news.html", "레큐란 석간", "Gazette"), ("map.html", "관광 안내", "Itinerarium")]
def shimmer_all(text):
    import re as _re
    anim = ('<animateTransform attributeName="gradientTransform" type="translate" '
            'values="-160 -60;160 60;-160 -60" dur="7s" repeatCount="indefinite"/>')
    def fix(m):
        g = m.group(0)
        g = g.replace('gradientUnits="userSpaceOnUse"', 'gradientUnits="userSpaceOnUse" spreadMethod="reflect"', 1)
        return g.replace('</linearGradient>', anim + '</linearGradient>')
    return _re.sub(r'<linearGradient id="[a-z0-9]+-gold"[^>]*>.*?</linearGradient>', fix, text)

def nav(active):
    on = ' class="on"'
    links = "".join(f'<a href="{h}"{on if h == active else ""}>{t}<span class="la">{e}</span></a>' for h, t, e in NAV_ITEMS)
    return f'<nav class="snav"><a class="sb" href="index.html">{logo("nv" + active[:2])}<span>아이파베스</span></a>{links}</nav>'

def page(fname, title, body):
    body = shimmer_all(body)
    html = (f'<!doctype html>\n<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title><link rel="icon" href="assets/logo.svg"><link rel="stylesheet" href="assets/site.css"><link rel="stylesheet" href="assets/book.css"></head>\n'
            f'<body class="desk">{topnav(fname)}<div class="ap">{body}{footer}</div></body></html>\n')
    open(os.path.join(SITE, fname), "w", encoding="utf-8").write(html)
    return len(html)

SITE = os.path.join(ROOT, "docs")
os.makedirs(os.path.join(SITE, "assets", "img"), exist_ok=True)
for k in SRC:
    shutil.copyfile(os.path.join(ROOT, "images", k + ".jpg"), os.path.join(SITE, "assets", "img", k + ".jpg"))
open(os.path.join(SITE, "assets", "site.css"), "w", encoding="utf-8").write(SITE_CSS)
open(os.path.join(SITE, "assets", "logo.svg"), "w", encoding="utf-8").write(rd("logo/mark_b2_gilt.svg"))

# ---- book (index): physical book with page turning ------------------------------
BOOK_SPREADS = SPREADS[1:]          # first recorded spread was the old cover/contents
pages_html = []
def pg(content, side, kind="soft", extra="", rh="", fo=""):
    dens = ' data-density="hard"' if kind == "hard" else ""
    rhs = f'<span class="rh">{rh}</span>' if rh else ""
    fos = f'<span class="fo">— {fo} —</span>' if fo != "" else ""
    pages_html.append(f'<div class="page {kind} {side} {extra}"{dens}><div class="pc">{rhs}{content}{fos}</div></div>')

mono = lambda pfx: logo(pfx, "mono")
pg(f'{logo("cv", "gilt", "mark")}<h1 class="gold">아이파베스</h1><p class="sc gold">AIPHABESS</p><p class="la gold">School of All Origins</p>'
   '<div class="rule"></div><small class="gold">Recuran · Anno XCV</small>', "r", "hard", "cover")
pg(f'<div class="exlibris"><span class="sc">Ex Libris</span>{mono("ex")}<p>아이파베스 대도서관 소장<br>함부로 지하 서고에 들고 내려가지 말 것</p></div>', "l", "soft", "endpaper")
pg(f'{mono("tt")}<h1>아이파베스</h1><p class="sc">AIPHABESS</p><p class="la">School of All Origins</p><div class="orn c" style="width:60%"></div>'
   '<p class="ds">5개 명문 학교 중 하나. 마법 학교이자 대도서관. 모든 종족이 이해를 배우는 곳.<br>레큐란 대륙 남쪽, 삼면이 바다인 반도 위의 대도시.</p>'
   '<p class="imp">아이파베스 대도서관 간행 · 95회전 18번째 달</p>', "r", "soft", "title")
pg(cover_r, "l", rh="Contents", fo="i")
pg('<div class="orn c" style="width:50%"></div><p class="q">서로를 향한 이해가<br>곧 가장 위대한 힘이 되리니.</p><p class="la">— inscribed in the lobby of Aiphabess</p><div class="orn c" style="width:50%"></div>',
   "r", "soft", "epigraph", fo="ii")
CHAP_PAGE = {}
for sp in BOOK_SPREADS:
    if sp["sid"]: CHAP_PAGE[sp["sid"]] = len(pages_html)
    pg(sp["left"], "l", rh=sp["rh_l"], fo=len(pages_html) - 3)
    pg(sp["right"], "r", rh=sp["lh"], fo=len(pages_html) - 3)
pg(f'<span class="cap">Musica</span><h2>마학 BGM</h2><div class="orn"></div><div class="bgm">{BGM}</div>', "l", rh="Musica")
src_items = "".join(f'<li>{(v["artist"] or "Gustave Doré").split(" / ")[0]} — <a href="{v["page"]}">{v["title"].replace("File:", "")}</a></li>' for v in SRC.values())
pg('<div class="colophon"><span class="cap">Colophon</span><h3>판권</h3>'
   '<p>삽화는 모두 퍼블릭 도메인 판화입니다 (Wikimedia Commons).</p><ul>' + src_items + '</ul>'
   '<p style="margin-top:.8em">가죽·종이·책상 질감: Poly Haven, ambientCG (CC0). 책장 넘김: StPageFlip (MIT).<br>'
   '글꼴: Song Myung, Gowun Batang, Diphylleia, Hahmlet, IM Fell English (SIL OFL).</p></div>', "r", rh="Colophon")
pg(mono("bk"), "l", "hard", "back")
assert len(pages_html) % 2 == 0, len(pages_html)

book_tabs = [("cov", "차례", 3)] + [(k, t, CHAP_PAGE[k]) for k, t, e, r in TABS if k in CHAP_PAGE]
tabs_html = "".join(f'<a class="tab" data-page="{n}" style="top:{8 + i * 9.5:.1f}%">{t}</a>' for i, (k, t, n) in enumerate(book_tabs))
book_body = "".join(pages_html)
for k, n in CHAP_PAGE.items():
    book_body = book_body.replace(f"@@{k}@@", str(n)).replace(f"@@n:{k}@@", str(n - 3))

FONTS = ("https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Song+Myung&family=Diphylleia&family=Hahmlet:wght@500;700;900"
         "&family=IM+Fell+English:ital@0;1&family=IM+Fell+English+SC&display=swap")
def topnav(active):
    return '<nav class="topnav">' + "".join(
        f'<a href="{h}"{" class=on" if h == active else ""}>{t}<span class="la">{e}</span></a>' for h, t, e in NAV_ITEMS) + '</nav>'
NAV_ITEMS_LOCAL = None
index_html = (f'<!doctype html>\n<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
              f'<title>아이파베스 · 세계관 책</title><link rel="icon" href="assets/logo.svg"><link rel="stylesheet" href="{FONTS}">'
              f'<link rel="stylesheet" href="assets/book.css"></head>\n<body class="desk">'
              f'{{TOPNAV}}<main class="stage"><div class="bookwrap closed"><div class="stack l"></div><div class="stack r"></div>'
              f'<div id="book">{shimmer_all(book_body)}</div><nav class="tabs">{tabs_html}</nav><i class="ribbon"></i></div>'
              f'<p class="hint">책장 모서리를 끌거나 눌러서 넘기세요 · <kbd>←</kbd> <kbd>→</kbd></p></main>'
              f'<script src="assets/vendor/page-flip.browser.js"></script><script src="assets/book.js"></script></body></html>\n')
# ---- newspaper -------------------------------------------------------------------
def npimg(key, cap, cls=""):
    s = SRC[key]; a = (s["artist"] or "Gustave Doré").split(" / ")[0]
    return f'<figure class="{cls}"><img src="{img_url(key)}" alt="{cap}" loading="lazy"><figcaption><span>{cap}</span><span>판화: {a}</span></figcaption></figure>'

news = f'''<div class="np">
<div class="np-top"><span>Specimen Issue · 견본호</span><span>세계관 안내판</span><span>값 1골드</span></div>
<div class="np-title"><h1>레큐란 석간</h1><span class="sc">The Recuran Evening Post</span></div>
<div class="np-date"><span>95회전 18번째 달의 태양 · 첫날 (3월 7일)</span><span>인간계 기준 약 2,086년째</span><span>아이파베스 대도시 서항 인쇄소 발행</span></div>
<div class="np-front">
 <div class="lead"><span class="kick">School · 학교</span>
  <h2>새 태양 첫날, 아이파베스 정문에 입학 행렬</h2>
  <p class="deck">나이 제한은 "졸업할 의지"뿐 … 반과 속성은 올해도 조상과 신수가 정한다</p>
  {npimg("np_square", "입학 첫날, 사람들로 붐비는 광장", "crop")}
  <p>달의 태양이 뜬 첫날, 아이파베스 정문 앞은 새 학생들로 붐볐다. 정식 입학은 15세부터 가능하지만 필수는 아니어서, 줄 선 이들의 나이는 제각각이었다. 학교는 어떤 나이든 졸업할 의지만 있으면 입학을 허용한다.</p>
  <p>반과 속성은 교장이 정하지 않는다. 학생의 조상, 그 종족이 섬기는 신수, 혹은 위대한 업적을 남기고 사라진 존재 가운데 하나가 정한다. 입학생은 점성 선생님의 도움으로 그 존재와의 접점을 시도하며, 이때 꾸는 꿈은 환상이나 믿음 등 저마다 다른 모습으로 나타난다. 반의 이름도 그 존재가 직접 지어 준다.</p>
  <p>입학이 확정되면 부모와 잠시 헤어져 기숙사에 들어간다. 기숙사는 반마다 하나씩이며 생활은 의무다. 학교는 "교우 관계를 자연스럽게 만들기 위한 방침"이라고 설명했다.</p>
 </div>
 <aside>
  <div class="box" style="margin-bottom:16px"><span class="kick">Calendarium</span><h3>오늘의 태양</h3><span class="big">XVIII · 달</span>
   <p>95회전 18번째 태양. 정위치는 불안·애매함·혼돈, 역위치는 불안 해소·명료함·혼돈의 끝.</p>
   <p style="margin-top:6px;font-family:'IM Fell English',serif;font-size:16px">(95 − 1) × 22 + 18 = 2,086</p></div>
  <div class="box" style="margin-bottom:16px"><span class="kick">Cambium</span><h3>골드 시세</h3>
   <table><tr><td>100골드</td><td>≈ 10,000원</td></tr><tr><td>환전 방법</td><td>공식 워프존 자동</td></tr></table>
   <p style="margin-top:8px">인간계 화폐로 자동 환전된다. 환율 차익을 노리는 "주식 마법사"도 적지 않다.</p></div>
  <article><span class="kick">Rumor · 소문란</span><h3>여신의 책 네 권, 올해는 찾을까</h3>
   <p>학교 어딘가에 사계절 여신의 가호가 깃든 책이 네 권 숨겨져 있다는 소문은 올해도 신입생 사이에서 가장 먼저 퍼졌다. 본 사람도, 실재를 확인한 사람도 없다. 아이파베스를 설계한 대마법사의 행방 역시 여전히 알려지지 않았다.</p></article>
 </aside>
</div>
<div class="cols">
 <article><span class="kick">Graduation · 졸업</span><h3>졸업생 특전 "원하는 마법 하나"</h3>
  <p>아이파베스의 졸업 조건은 하나로 정해져 있지 않다. 그랑프리 우승, 담당 선생님의 공식 인정 등 학생마다 다르다. 졸업이 확정되면 현 교장 선생님에게서 원하는 마법 하나를 직접 배울 수 있다. 어떤 마법이든 상관없다.</p>
  <p>마스터 반 출신이나 그랑프리 우승자는 곧바로 1급 마법사가 되고, 그 밖의 졸업생은 2급 또는 3급을 받으며 1급 시험 응시 자격을 함께 얻는다.</p></article>
 <article><span class="kick">Grand Prix</span><h3>4년에 한 번, 반 대항 그랑프리</h3>
  <p>선후배 구분 없이 참가하는 반 대항전이다. 공정성을 위해 속성이 두 개인 반과 하나인 반을 나눠 두 경기를 치르고, 두 우승 팀이 동의하면 결승전이 열린다. 우승하면 수석 졸업 자격 또는 상금과 아이템을 받는다. 대회 기간에는 친선전도 함께 열린다.</p></article>
 <div class="box ad"><span class="kick">Advertisement</span><h3>천마계 통판북</h3><span class="big">서명 5초, 배달 5초</span>
  <p>천계 상품은 흰 종이·흰 깃털 펜으로, 마계 상품은 검은 종이·검은 깃털 펜으로 서명하십시오. 보유 금액에서 자동 차감됩니다.</p>
  <p style="margin-top:6px;font-size:12px">※ 마계 상품은 18세 미만 이용 불가</p></div>
 {npimg("np_alley", "항구 뒷골목")}
 <article><span class="kick">Society · 사회</span><h3>주선교·죄악교 사건, 수사 여전히 난항</h3>
  <p>최근 급증한 두 교단과 관련된 피해·학살 사건 수사가 진척을 보이지 못하고 있다. 교단마다 목적은 다르지만, 무언가를 소환하는 것이 아니라 직접 만들어내려 한다는 점은 같다는 것이 지금까지의 분석이다. 확실한 증거 없이는 검거가 어렵다.</p></article>
 {npimg("np_station", "차원열차 승강장")}
 <article><span class="kick">Transit · 교통</span><h3>인간계행 차원열차, 입국심사 필수</h3>
  <p>머나먼 세계에서 오는 학생들도 대도시 한켠의 차원열차 승강장을 통해 아이파베스에 닿는다. 다만 인간계로 가는 열차는 별도의 입국심사를 거쳐야 한다. 마법사의 무분별한 유입을 막기 위한 절차다. 천사와 악마, 신은 입학할 수 없다는 점도 다시 안내되었다.</p></article>
 <div class="box"><span class="kick">Advertisement</span><h3>정령 조향소 · 인간의 향수</h3>
  <p>한 번 뿌리면 인간에게 평범한 인간으로 보입니다. 향이 은은하고 좋을수록 오래, 그리고 비쌉니다.</p><p style="margin-top:6px"><b>인간계 방문 전 필수품</b></p></div>
 <article><span class="kick">Notice · 공고</span><h3>주신의 비서·신들의 보좌관 시험 접수</h3>
  <p>점성 선생님의 신뢰를 바탕으로 지원할 수 있다. 공무원 시험과 비슷하며 이론과 실전 시험을 모두 치른다. 점성 선생님의 신뢰는 평소 행동에 달려 있어 난이도가 높다. 합격자 대부분은 판단력이 뛰어나고 성실한 학생이었다.</p></article>
 {npimg("np_reading", "대열람실. 지하 서고는 이 아래에 있다")}
 <article><span class="kick">Library · 도서관</span><h3>지하 서고 원본 열람, 세 겹의 허락 필요</h3>
  <p>원본 자료와 중요 서적을 보려면 교장과의 약속, 대마법사의 맹약, 4원소 학자의 서약이 모두 필요하다. 연구에 흥미가 있는 학생은 교장과 함께 지하로 내려가 기록을 분석하고 쉽게 정리하는 작업에 참여할 수 있다.</p></article>
 <article><span class="kick">Column · 칼럼</span><h3>달의 태양에 태어난 아이들</h3>
  <p>이 세계의 연도는 타로 22장의 순서대로 돈다. 태양 하나가 인간계의 1년이고, 22개가 돌면 한 회전이다. 마법사들은 "그 태양에 태어난 아이에게는 정위치와 역위치의 기운이 흐른다"고 믿는다. 올해 태어날 아이들에게는 달의 기운, 곧 혼돈과 그 끝이 함께 흐를 것이다.</p></article>
 <div class="box"><span class="kick">Advertisement</span><h3>졸업생 공방 거리</h3>
  <p>무기 제작 · 연금 재료 · 맞춤 마도구<br>아이파베스 졸업생이 직접 만듭니다.</p></div>
</div>
<div class="np-foot">이 신문은 아이파베스 세계관을 소개하기 위한 견본호입니다. 실제 발행 일정은 없습니다.</div>
</div>'''
index_html = index_html.replace('{TOPNAV}', topnav('index.html'))
open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8').write(index_html)
n1 = len(index_html)
n2 = page("news.html", "레큐란 석간 · 견본호", news)

# ---- town map ----------------------------------------------------------------
DIST = [
    (1, "학원 언덕", "Collis Academiae", "반도 남부 중앙, 도시에서 가장 높은 곳. 아이파베스 본관과 대도서관, 반별 기숙사, 점성탑이 있고 지하 서고 입구도 이곳에 있다.", "학교 · 행정"),
    (2, "필사가 골목", "Vicus Scribarum", "언덕 북쪽 기슭의 가장 오래된 골목. 유학생들이 처음 자리 잡은 곳으로 서점, 제본소, 잉크·깃펜 상점, 번역소가 늘어서 있다.", "지식 산업"),
    (3, "만족(萬族) 시장", "Forum Omnium Gentium", "구시가와 항구 사이의 광장. 여러 종족이 먹을 수 있는 음식 거리로 \"살고 싶은 마을 10위\"를 만든 주인공. 그랑프리 때는 노점이 들어선다.", "상업 · 관광"),
    (4, "서항", "Portus Occidentalis", "서쪽 만의 큰 항구. 책과 종이, 잉크를 실어 나르며 커졌다. 부두, 세관, 창고, 어시장이 있다.", "무역"),
    (5, "역전 신시가지", "Nova Urbs", "대륙과 이어지는 북쪽 길목. 차원열차 승강장과 입국심사소, 환전소, 여관, 인간의 향수 상점이 반듯한 격자 거리에 모여 있다.", "교통 · 외부인"),
    (6, "공방 거리", "Vicus Fabrorum", "북동쪽. 졸업생들이 연 공방과 무기제작사, 연금술 재료상이 모여 있다.", "생산"),
    (7, "동쪽 언덕 주택가", "Colles Orientales", "동쪽 절벽 위의 조용한 주택가. 선생님들의 사택과 오래된 가문의 저택이 있다.", "상류층 주거"),
    (8, "항구 뒷골목", "Angiportus", "서항 북쪽. 선원과 일꾼들의 숙소, 싼 술집이 모인 골목.", "서민 주거"),
    (9, "안개 곶", "Promontorium Nebulae", "반도 남쪽 끝. 안개 속에 돌탑이 서 있고 폐쇄된 옛 예배당이 있다. 여신의 책이 숨겨져 있다는 소문이 도는 곳.", "경계 · 소문"),
]
def pimg(key, cls=""):
    a = (SRC[key]["artist"] or "").split(" / ")[0]
    return f'<figure class="pimg {cls}"><img src="{img_url(key)}" alt="" loading="lazy"><figcaption>{a}</figcaption></figure>'

legend = "".join(f'<li id="d{i}"><b>{i}</b><span>{n}</span><em>{t}</em></li>' for i, n, la, d, t in DIST)
cover = (f'<div class="pt">레큐란 대륙 남쪽 · 삼면이 바다인 반도</div>{pimg("pm_street", "tall")}'
         '<h1>아이파베스</h1><div class="ps">대도시 관광 안내</div><div class="pr"></div>'
         '<p class="tag">배움의 언덕과 서쪽 바다,<br>그리고 온갖 종족의 식탁</p>'
         '<div class="badge">살고 싶은 마을<b>10위</b></div><div class="pf">AIPHABESS · GUIDE TO THE CITY</div>')
p1 = ('<h2><i>I</i>오시는 길<small>Accessus</small></h2>'
      '<h3>차원열차</h3><p>이름조차 낯선 머나먼 세계에서도 닿을 수 있습니다. 북쪽 역전 신시가지의 승강장에서 내리세요. '
      '인간계로 가는 열차는 별도의 입국심사를 거칩니다.</p>'
      '<h3>대륙 가도</h3><p>레큐란 대륙과 이어진 유일한 육로입니다. 반도의 북쪽 끝에서 시작해 학원 언덕까지 이어집니다.</p>'
      '<h3>서항 항로</h3><p>서쪽 만의 항구로 배가 드나듭니다. 책과 종이, 잉크를 실은 배가 가장 많습니다.</p>'
      '<div class="pbox"><h4>도착하면</h4><ul><li><b>환전</b>100골드 ≈ 10,000원 (한화 기준)</li>'
      '<li><b>인간계 방문</b>정령이 만든 인간의 향수를 준비하세요. 향이 은은할수록 값이 나갑니다.</li></ul></div>'
      + pimg("pm_inn", "wide") + '<p class="small">묵을 곳은 역전 신시가지와 항구 뒷골목에 많습니다.</p>')
p2 = ('<h2><i>II</i>한눈에 보는 대도시<small>Charta</small></h2>'
      f'<button class="pmap" type="button" aria-label="지도 크게 보기">{town_map()}<span>크게 보기</span></button>'
      f'<ol class="legend">{legend}</ol>')
p3 = ('<h2><i>III</i>꼭 들러 볼 곳<small>Visenda</small></h2>'
      f'<div class="spot">{pimg("pm_books")}<div><h3>필사가 골목</h3><p>유학생들이 처음 자리 잡은 가장 오래된 골목. 서점과 제본소, 잉크·깃펜 상점이 이어집니다.</p></div></div>'
      f'<div class="spot">{pimg("pm_fish")}<div><h3>서항 어시장</h3><p>삼면의 바다에서 올라온 생선이 아침마다 부두에 깔립니다.</p></div></div>'
      '<h3>만족(萬族) 시장</h3><p>여러 종족이 함께 먹을 수 있는 음식 거리. 이 도시가 "살고 싶은 마을 10위"에 드는 이유입니다.</p>'
      '<div class="pbox red"><h4>그랑프리 시즌</h4><p>4년에 한 번 열리는 아이파베스 반 대항전. 친선전도 함께 열려 도시 전체가 들썩입니다.</p></div>'
      '<div class="pbox"><h4>여행자 유의사항</h4><ul>'
      '<li>대도서관 지하 서고의 원본은 교장의 약속, 대마법사의 맹약, 4원소 학자의 서약 없이는 볼 수 없습니다.</li>'
      '<li>천마계 통판북의 마계 상품은 18세 미만 이용 불가.</li>'
      '<li>안개 곶의 돌탑에 얽힌 소문을 좇아 밤에 홀로 가지 마십시오.</li></ul></div>')
back = '<div class="pback"><p>아이파베스 대도시 관광 안내<br><small>견본 · 95회전 18번째 달</small></p></div>'
pam = (f'<div class="pam-desk"><div class="pamw"><div class="pam" id="pam">'
       f'<div class="pp p1"><div class="face in">{p1}</div><div class="face out pcover" role="button" tabindex="0" aria-label="팸플릿 펼치기">{cover}</div></div>'
       f'<div class="pp p2"><div class="face in">{p2}</div></div>'
       f'<div class="pp p3"><div class="face in">{p3}</div><div class="face out">{back}</div></div>'
       '</div></div><p class="pam-hint">표지를 누르면 펼쳐집니다 · <a href="#" id="pam-close">다시 접기</a></p>'
       '<div class="lightbox" id="lb" hidden><div class="lb-in"></div><p>지도 밖을 누르면 닫힙니다</p></div></div>'
       '<script>(function(){var pam=document.getElementById("pam"),cov=pam.querySelector(".pcover"),lb=document.getElementById("lb"),'
       'box=lb.querySelector(".lb-in"),btn=pam.querySelector(".pmap"),svg=btn.querySelector("svg");'
       'function open(){pam.classList.add("open")}cov.addEventListener("click",open);'
       'cov.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" ")open()});'
       'document.getElementById("pam-close").addEventListener("click",function(e){e.preventDefault();pam.classList.remove("open")});'
       'btn.addEventListener("click",function(){box.appendChild(svg);lb.hidden=false});'
       'lb.addEventListener("click",function(e){if(e.target.closest("a"))return;btn.insertBefore(svg,btn.firstChild);lb.hidden=true});'
       'svg.addEventListener("click",function(e){var a=e.target.closest("a");if(!a)return;e.preventDefault();open();'
       'if(!lb.hidden){btn.insertBefore(svg,btn.firstChild);lb.hidden=true}var t=document.querySelector(a.getAttribute("href"));'
       'document.querySelectorAll(".legend li").forEach(function(l){l.classList.remove("hl")});if(t){t.classList.add("hl")}});'
       'if(/^#d\\d/.test(location.hash))open();})();</script>')
n3 = page("map.html", "아이파베스 대도시 관광 안내", pam)
print("site:", n1, n2, n3, "bytes")

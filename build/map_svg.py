"""Engraved-style town map of the Aiphabess peninsula city (sea on three sides).

town_map() -> SVG string. Deterministic (seeded). Hand-authored generator:
coastline by midpoint displacement, water-lining by alternating ink/paper strokes,
hill hachures, streets, building blocks, compass rose with rhumb lines, cartouche.
"""
import math, random

W, H = 1200, 900
INK = "#2e2216"
SEA = "#e4d3a6"
LAND = "#efe2bd"

def f(v):
    s = f"{v:.1f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s

def P(pts, close=False):
    return "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts) + (" Z" if close else "")

# ------------------------------------------------------------------ coastline
BASE = [(240, -40), (262, 60), (292, 150), (318, 240), (345, 318),
        (392, 342), (452, 352), (492, 388), (488, 440), (446, 470), (388, 486), (352, 520),
        (346, 572), (372, 624), (404, 664), (446, 676), (492, 690), (530, 728), (566, 782), (598, 846),
        (632, 806), (676, 752), (726, 700), (782, 640), (822, 572), (846, 498), (872, 412),
        (896, 330), (922, 238), (944, 140), (966, 40), (986, -40)]

def displace(pts, rng, levels=4, rough=.16):
    for _ in range(levels):
        out = [pts[0]]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            L = math.hypot(x1 - x0, y1 - y0)
            nx, ny = -(y1 - y0) / (L or 1), (x1 - x0) / (L or 1)
            d = rng.uniform(-1, 1) * L * rough
            out += [(mx + nx * d, my + ny * d), (x1, y1)]
        pts = out
        rough *= .62
    return pts

def coast():
    rng = random.Random(11)
    pts = displace(BASE, rng)
    pts += [(1000, -60), (220, -60)]
    return pts

def inside(poly, x, y):
    c = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            c = not c
    return c

# ------------------------------------------------------------------ pieces
def compass(cx, cy, r):
    g = []
    # rhumb lines (drawn separately under land)
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r+10}" fill="none" stroke="{INK}" stroke-width=".8"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r+6}" fill="none" stroke="{INK}" stroke-width=".4"/>')
    ticks = "".join(f"M{f(cx+(r+6)*math.cos(a))},{f(cy+(r+6)*math.sin(a))}L{f(cx+(r+10)*math.cos(a))},{f(cy+(r+10)*math.sin(a))}"
                    for a in [i * math.tau / 64 for i in range(64)])
    g.append(f'<path d="{ticks}" stroke="{INK}" stroke-width=".5"/>')
    for k, (rr, wid) in enumerate(((r, .2), (r * .72, .16), (r * .5, .12))):
        n = 4 if k == 0 else (4 if k == 1 else 8)
        off = 0 if k == 0 else (45 if k == 1 else 22.5)
        for i in range(n):
            a = math.radians(i * 360 / n + off - 90)
            tip = (cx + rr * math.cos(a), cy + rr * math.sin(a))
            l = (cx + rr * wid * math.cos(a - math.pi / 2), cy + rr * wid * math.sin(a - math.pi / 2))
            rt = (cx + rr * wid * math.cos(a + math.pi / 2), cy + rr * wid * math.sin(a + math.pi / 2))
            g.append(f'<path d="{P([(cx, cy), tip, l], True)}" fill="{INK}" stroke="{INK}" stroke-width=".5"/>')
            g.append(f'<path d="{P([(cx, cy), tip, rt], True)}" fill="{LAND}" stroke="{INK}" stroke-width=".5"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{LAND}" stroke="{INK}" stroke-width=".7"/>')
    g.append(f'<text x="{cx}" y="{f(cy-r-16)}" text-anchor="middle" font-family="IM Fell English,serif" font-size="20" fill="{INK}">N</text>')
    return "".join(g)

def hill(cx, cy, rng):
    s = []
    for ring, (r0, n, L) in enumerate(((60, 80, 9), (76, 104, 11), (94, 128, 12))):
        for i in range(n):
            a = i * math.tau / n + rng.uniform(-.02, .02)
            rr = r0 * (1 + .12 * math.sin(a * 3 + 1)) + rng.uniform(-2, 2)
            l = L * rng.uniform(.6, 1.1)
            x0, y0 = cx + rr * math.cos(a), cy + rr * .78 * math.sin(a)
            x1, y1 = cx + (rr + l) * math.cos(a), cy + (rr + l) * .78 * math.sin(a)
            s.append(f"M{f(x0)},{f(y0)}L{f(x1)},{f(y1)}")
    return f'<path d="{"".join(s)}" stroke="{INK}" stroke-width=".55" opacity=".75"/>'

def blocks_along(path, rng, poly, every=13, off=7, size=(5, 9), avoid=()):
    out = []
    for (x0, y0), (x1, y1) in zip(path, path[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        if L < 1: continue
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        nx, ny = -uy, ux
        ang = math.degrees(math.atan2(uy, ux))
        t = rng.uniform(0, every)
        while t < L:
            for side in (-1, 1):
                if rng.random() < .18: continue
                w, h = rng.uniform(*size), rng.uniform(size[0], size[1] * .8)
                cx = x0 + ux * t + nx * side * (off + h / 2)
                cy = y0 + uy * t + ny * side * (off + h / 2)
                if not inside(poly, cx, cy) or any(math.hypot(cx - ax, cy - ay) < ar for ax, ay, ar in avoid):
                    continue
                out.append(f'<rect x="{f(cx-w/2)}" y="{f(cy-h/2)}" width="{f(w)}" height="{f(h)}" transform="rotate({f(ang)} {f(cx)} {f(cy)})"/>')
            t += every * rng.uniform(.8, 1.2)
    return out

def wobble(pts, rng, amt=4, n=3):
    out = [pts[0]]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for k in range(1, n):
            t = k / n
            out.append((x0 + (x1 - x0) * t + rng.uniform(-amt, amt), y0 + (y1 - y0) * t + rng.uniform(-amt, amt)))
        out.append((x1, y1))
    return out

def smooth(pts):
    """Catmull-Rom to cubic bezier path."""
    d = f"M{f(pts[0][0])},{f(pts[0][1])}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(p2[0])},{f(p2[1])}"
    return d

# district anchors: (id, x, y, label, label_dx, label_dy)
DISTRICTS = [
    (1, 596, 560, "학원 언덕", 0, 56),
    (2, 612, 420, "필사가 골목", 60, 4),
    (3, 520, 492, "만족 시장", -10, 30),
    (4, 452, 418, "서항", -64, -26),
    (5, 640, 150, "역전 신시가지", 0, -54),
    (6, 812, 300, "공방 거리", 0, -30),
    (7, 744, 580, "동쪽 언덕 주택가", 18, 30),
    (8, 404, 300, "항구 뒷골목", -10, -26),
    (9, 600, 786, "안개 곶", 46, 0),
]

def town_map():
    rng = random.Random(5)
    land = coast()
    land_d = P(land, True)
    out = [f'<svg class="tmap" viewBox="0 0 {W} {H}" role="img" aria-label="아이파베스 대도시 구성도. 북쪽만 대륙에 이어지고 동·서·남이 바다인 반도." '
           f'stroke-linecap="round" stroke-linejoin="round">']
    out.append('<defs><clipPath id="tm-frame"><rect x="18" y="18" width="1164" height="864"/></clipPath>'
               '<clipPath id="tm-land"><path d="' + land_d + '"/></clipPath>'
               f'<pattern id="tm-hatch" width="2.6" height="2.6" patternUnits="userSpaceOnUse" patternTransform="rotate(40)"><rect width="2.6" height="2.6" fill="{LAND}"/><path d="M0,0V2.6" stroke="{INK}" stroke-width=".75"/></pattern>'
               f'<pattern id="tm-hatch2" width="1.8" height="1.8" patternUnits="userSpaceOnUse" patternTransform="rotate(-40)"><rect width="1.8" height="1.8" fill="{LAND}"/><path d="M0,0V1.8" stroke="{INK}" stroke-width=".7"/></pattern>'
               '<filter id="tm-grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="4"/>'
               '<feColorMatrix values="0 0 0 0 .3 0 0 0 0 .2 0 0 0 0 .08 0 0 0 .16 0"/></filter></defs>')
    out.append(f'<rect width="{W}" height="{H}" fill="{SEA}"/>')
    out.append('<g clip-path="url(#tm-frame)">')
    # rhumb lines from two roses
    rh = []
    for cx, cy in ((190, 700), (1040, 170)):
        for i in range(16):
            a = math.radians(i * 22.5)
            rh.append(f"M{cx},{cy}L{f(cx+1600*math.cos(a))},{f(cy+1600*math.sin(a))}")
    out.append(f'<path d="{"".join(rh)}" stroke="{INK}" stroke-width=".35" opacity=".35"/>')
    # water-lining
    out.append('<g class="wl">')
    for i in range(9, 0, -1):
        dist = i * 6.5
        op = max(.08, .55 - i * .055)
        out.append(f'<path d="{land_d}" fill="none" stroke="{INK}" stroke-opacity="{f(op)}" stroke-width="{f(2*dist+.9)}"/>')
        out.append(f'<path d="{land_d}" fill="none" stroke="{SEA}" stroke-width="{f(2*dist-.6)}"/>')
    out.append('</g>')
    # land
    out.append(f'<path d="{land_d}" fill="{LAND}"/>')
    out.append('<g clip-path="url(#tm-land)">')
    # fields (hatched parcels) in the north outside the grid
    fields = []
    for _ in range(26):
        x, y = rng.uniform(300, 940), rng.uniform(20, 300)
        if 500 < x < 800 and y < 250: continue
        w, h, ang = rng.uniform(30, 60), rng.uniform(20, 40), rng.uniform(-25, 25)
        if not inside(land, x, y): continue
        lines = "".join(f"M{f(x)},{f(y+k)}h{f(w)}" for k in range(0, int(h), 4 if rng.random() < .5 else 3))
        fields.append(f'<g transform="rotate({f(ang)} {f(x+w/2)} {f(y+h/2)})"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="none" stroke="{INK}" stroke-width=".5"/>'
                      f'<path d="{lines}" stroke="{INK}" stroke-width=".3" opacity=".6"/></g>')
    out.append(f'<g opacity=".55">{"".join(fields)}</g>')
    # cliffs on east coast: short strokes perpendicular inland
    cl = []
    for (x0, y0), (x1, y1) in zip(land, land[1:]):
        if x0 > 760 and 180 < y0 < 700:
            L = math.hypot(x1 - x0, y1 - y0) or 1
            nx, ny = -(y1 - y0) / L, (x1 - x0) / L
            for t in (0, .5):
                px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
                l = rng.uniform(5, 11)
                cl.append(f"M{f(px)},{f(py)}L{f(px-nx*l)},{f(py-ny*l)}")
    out.append(f'<path d="{"".join(cl)}" stroke="{INK}" stroke-width=".6" opacity=".7"/>')
    # hill (hachures start outside the school wall)
    out.append(hill(596, 552, rng))
    # ---- roads: organic, following terrain
    roads = [
        [(642, -10), (630, 60), (648, 128), (640, 200), (622, 270), (606, 340), (614, 400), (602, 462), (596, 506)],
        [(604, 446), (572, 436), (540, 452), (508, 440), (480, 424)],
        [(626, 560), (668, 588), (712, 578), (760, 596), (806, 584)],
        [(598, 590), (612, 640), (590, 700), (604, 752), (598, 790)],
        [(566, 574), (528, 600), (482, 630), (446, 650), (420, 660)],
        [(612, 400), (650, 380), (700, 352), (744, 322), (790, 296), (840, 262)],
        [(480, 424), (452, 384), (426, 330), (408, 262), (396, 190), (378, 110), (366, -10)],
    ]
    roads = [wobble(r, rng, 2.5, 2) for r in roads]
    lanes = []
    for cx, cy, n, spread in ((585, 440, 12, 34), (640, 168, 6, 46), (420, 300, 4, 28), (520, 478, 4, 22)):
        for _ in range(n):
            x, y = cx + rng.gauss(0, spread), cy + rng.gauss(0, spread * .7)
            a = rng.uniform(0, math.tau); pts = [(x, y)]
            for _ in range(4):
                a += rng.uniform(-.7, .7); x += 12 * math.cos(a); y += 12 * math.sin(a); pts.append((x, y))
            lanes.append(pts)
    segs = [(a, b) for r in roads + lanes for a, b in zip(r, r[1:])]
    main_segs = [(a, b) for r in roads for a, b in zip(r, r[1:])]

    def seg_dist(x, y, a, b):
        (x0, y0), (x1, y1) = a, b
        dx, dy = x1 - x0, y1 - y0
        t = max(0, min(1, ((x - x0) * dx + (y - y0) * dy) / ((dx * dx + dy * dy) or 1)))
        return math.hypot(x - x0 - t * dx, y - y0 - t * dy), math.atan2(dy, dx)

    def nearest(x, y, pool):
        best = (1e9, 0)
        for a, b in pool:
            d = seg_dist(x, y, a, b)
            if d[0] < best[0]: best = d
        return best

    placed = []
    def cluster(cx, cy, rx, ry, n, wmin, wmax, hmin, hmax, court=0.0, gap=3.2, clear=4.5):
        out_b = []
        tries = 0
        while len(out_b) < n and tries < n * 80:
            tries += 1
            x, y = cx + rng.gauss(0, rx / 2), cy + rng.gauss(0, ry / 2)
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 > 1: continue
            if not inside(land, x, y): continue
            dm, ang = nearest(x, y, main_segs)
            if dm < clear + 2.5: continue
            dl, ang_l = nearest(x, y, segs)
            if dl < clear: continue
            if math.hypot(x - 596, y - 548) < 62 or math.hypot(x - 528, y - 486) < 16: continue
            if dl < dm: ang = ang_l
            w, h = rng.uniform(wmin, wmax), rng.uniform(hmin, hmax)
            r = max(w, h) / 2
            if any(math.hypot(x - px, y - py) < r + pr + gap for px, py, pr in placed): continue
            ang += rng.uniform(-.12, .12)
            c, s_ = math.cos(ang), math.sin(ang)
            def pt(u, v): return (x + u * c - v * s_, y + u * s_ + v * c)
            j = lambda: rng.uniform(-.9, .9)
            outer = [pt(-w/2 + j(), -h/2 + j()), pt(w/2 + j(), -h/2 + j()), pt(w/2 + j(), h/2 + j()), pt(-w/2 + j(), h/2 + j())]
            if rng.random() < .3 and w > 9:
                k = rng.uniform(.35, .6)
                outer = [pt(-w/2, -h/2), pt(w/2, -h/2), pt(w/2, h/2), pt(-w/2 + w*k, h/2), pt(-w/2 + w*k, h*.05), pt(-w/2, h*.05)]
            d = P(outer, True)
            if court and w > 14 and h > 12 and rng.random() < court:
                iw, ih = w * .45, h * .4
                d += " " + P([pt(-iw/2, -ih/2), pt(-iw/2, ih/2), pt(iw/2, ih/2), pt(iw/2, -ih/2)], True)
            placed.append((x, y, r))
            out_b.append(f'<path d="{d}"/>')
        return out_b

    blocks = []
    blocks += cluster(586, 438, 100, 74, 240, 6, 13, 5, 10, gap=1.6, clear=3.6)
    blocks += cluster(530, 470, 60, 50, 60, 6, 11, 5, 9, gap=1.6, clear=3.6)
    blocks += cluster(494, 410, 40, 52, 40, 12, 22, 6, 9, gap=2, clear=3.6)
    blocks += cluster(420, 300, 46, 84, 80, 5, 10, 5, 8, gap=1.8, clear=3.4)
    blocks += cluster(636, 176, 110, 96, 100, 13, 22, 11, 17, court=.6, gap=2.6)
    blocks += cluster(796, 296, 70, 48, 44, 8, 15, 6, 10, gap=2.2)
    blocks += cluster(748, 588, 56, 36, 12, 7, 11, 6, 9, gap=9)
    blocks += cluster(516, 604, 50, 30, 26, 5, 9, 5, 8, gap=2.6)
    blocks += cluster(604, 760, 24, 26, 4, 5, 8, 5, 7, gap=6)
    for hx, hy in ((330, 120), (880, 120), (760, 60), (470, 230), (860, 420)):
        blocks += cluster(hx, hy, 26, 20, 4, 5, 8, 4, 7, gap=5)
    out.append(f'<g fill="url(#tm-hatch)" stroke="{INK}" stroke-width=".6" fill-rule="evenodd">{"".join(blocks)}</g>')

    tr = []
    def trees(cx, cy, rx, ry, n):
        for _ in range(n):
            x, y = cx + rng.uniform(-rx, rx), cy + rng.uniform(-ry, ry)
            if not inside(land, x, y) or nearest(x, y, segs)[0] < 4: continue
            if any(math.hypot(x - px, y - py) < pr + 1 for px, py, pr in placed): continue
            if math.hypot(x - 596, y - 548) < 56: continue
            r = rng.uniform(1.6, 2.8)
            tr.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/><circle cx="{f(x+r*.5)}" cy="{f(y+r*.6)}" r="{f(r*.45)}" fill="{INK}" stroke="none"/>')
    trees(752, 592, 66, 44, 60); trees(690, 520, 40, 30, 22); trees(520, 560, 40, 30, 20)
    trees(600, 700, 30, 40, 26); trees(860, 200, 60, 90, 40); trees(360, 220, 30, 70, 26)
    out.append(f'<g fill="{LAND}" stroke="{INK}" stroke-width=".55">{"".join(tr)}</g>')

    road_d = "".join(smooth(r) for r in roads)
    out.append(f'<path d="{road_d}" fill="none" stroke="{INK}" stroke-width="4"/>')
    out.append(f'<path d="{road_d}" fill="none" stroke="{LAND}" stroke-width="2.3"/>')
    out.append(f'<path d="{"".join(smooth(l) for l in lanes)}" fill="none" stroke="{INK}" stroke-width=".55" opacity=".55"/>')
    out.append(f'<path d="{P([(514,474),(540,472),(546,494),(522,502),(510,490)], True)}" fill="none" stroke="{INK}" stroke-width=".8" stroke-dasharray="2 2"/>')
    rail = [(560, -10), (556, 50), (566, 100), (574, 142)]
    out.append(f'<path d="{smooth(rail)}" fill="none" stroke="{INK}" stroke-width="4"/><path d="{smooth(rail)}" fill="none" stroke="{LAND}" stroke-width="2.2" stroke-dasharray="5 4"/>')

    sc = []
    wall = []
    for i in range(28):
        a = i * math.tau / 28
        wall.append((596 + 50 * math.cos(a) * (1 + .05 * math.sin(3 * a)), 548 + 38 * math.sin(a) * (1 + .04 * math.cos(2 * a))))
    sc.append(f'<path d="{P(wall, True)}" fill="{LAND}" stroke="{INK}" stroke-width="2.2"/>')
    sc.append(f'<path d="{P(wall, True)}" fill="none" stroke="{INK}" stroke-width=".5" transform="translate(596 548) scale(.93) translate(-596 -548)"/>')
    for i in range(0, 28, 4):
        x, y = wall[i]; sc.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="3.2" fill="{LAND}" stroke="{INK}" stroke-width="1.1"/>')
    sc.append(f'<path d="M590,508 h12 v6 h-12 Z" fill="{INK}"/>')
    H2 = 'fill="url(#tm-hatch2)" stroke="' + INK + '" stroke-width=".8" fill-rule="evenodd"'
    sc.append(f'<path d="M570,526 H612 V552 H570 Z M580,532 V546 H602 V532 Z" {H2}/>')
    sc.append(f'<path d="M560,556 H604 V566 H560 Z" {H2}/>')
    sc.append(f'<path d="M616,532 H630 V560 H616 Z" {H2}/>')
    sc.append(f'<path d="M560,532 H566 V550 H560 Z M610,566 H624 V574 H610 Z" {H2}/>')
    sc.append(f'<circle cx="632" cy="524" r="6" {H2}/><circle cx="632" cy="524" r="2" fill="{INK}"/>')
    sc.append(f'<circle cx="591" cy="539" r="1.6" fill="{INK}"/>')
    out.append("".join(sc))
    out.append('</g>')  # end land clip
    # coastline
    out.append(f'<path class="coast" pathLength="1" d="{land_d}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    # piers in the bay
    piers = "".join(f"M{x},{y} L{x-28},{y+6}" for x, y in ((470, 392), (480, 414), (476, 438), (458, 458)))
    out.append(f'<path d="{piers}" stroke="{INK}" stroke-width="2.2"/>')
    # lighthouse (SW cape)
    lx, ly = 412, 664
    rays = "".join(f"M{f(lx+8*math.cos(a))},{f(ly-18+8*math.sin(a))}L{f(lx+22*math.cos(a))},{f(ly-18+22*math.sin(a))}" for a in [math.radians(d) for d in range(150, 391, 20)])
    out.append(f'<path class="beam" d="{rays}" stroke="{INK}" stroke-width=".5" opacity=".7"/>'
               f'<path d="M{lx-4},{ly} L{lx-2.4},{ly-16} L{lx+2.4},{ly-16} L{lx+4},{ly} Z" fill="{LAND}" stroke="{INK}" stroke-width="1"/>'
               f'<path d="M{lx-3.2},{ly-6} H{lx+3.2} M{lx-2.8},{ly-11} H{lx+2.8}" stroke="{INK}" stroke-width=".6"/>'
               f'<circle cx="{lx}" cy="{ly-18}" r="2.4" fill="{INK}"/>')
    # fog + tower at the south cape
    tx, ty = 598, 812
    fog = "".join(f'<path d="M{f(tx-60+k*8)},{f(ty-10+k*6)} c14,-6 28,6 42,0 s28,-6 42,0" fill="none"/>' for k in range(5))
    out.append(f'<g class="fog" stroke="{INK}" stroke-width=".6" opacity=".5" stroke-dasharray="2 3">{fog}</g>')
    out.append(f'<path d="M{tx-4},{ty} L{tx-3},{ty-22} L{tx+3},{ty-22} L{tx+4},{ty} Z M{tx-4},{ty-22} h8 v-3 h-8 Z" fill="{LAND}" stroke="{INK}" stroke-width="1"/>'
               f'<path d="M{tx-3},{ty-8}H{tx+3}M{tx-3},{ty-15}H{tx+3}" stroke="{INK}" stroke-width=".5"/>')
    # station
    out.append(f'<path d="M560,140 H592 V154 H560 Z" fill="url(#tm-hatch2)" stroke="{INK}" stroke-width="1.1"/>'
               f'<path d="M558,140 C566,128 586,128 594,140" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    # compass roses
    out.append('<g class="rose">' + compass(190, 700, 58) + '</g>')
    out.append('<g class="rose r2">' + compass(1040, 170, 34) + '</g>')
    # sea & land labels
    lab = []
    def T(x, y, s, size=16, it=True, rot=0, ls=".2em", op="1", fam=None):
        fam = fam or ("IM Fell English,serif" if it else "Song Myung,serif")
        st = ' font-style="italic"' if it else ""
        tr = f' transform="rotate({rot} {x} {y})"' if rot else ""
        lab.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="{fam}" font-size="{size}"{st} letter-spacing="{ls}" fill="{INK}" opacity="{op}"{tr}>{s}</text>')
    T(130, 330, "서쪽 바다", 19, False, -78, ".5em"); T(162, 330, "Mare Occidentale", 14, True, -78, ".3em", ".8")
    T(1080, 470, "동쪽 바다", 19, False, 78, ".5em"); T(1048, 470, "Mare Orientale", 14, True, 78, ".3em", ".8")
    T(820, 820, "남쪽 바다", 19, False, 0, ".5em"); T(820, 842, "Mare Australe", 14, True, 0, ".3em", ".8")
    T(780, 44, "레큐란 대륙 ↑", 15, False, 0, ".3em"); T(780, 62, "Continens Recuranus", 12, True, 0, ".2em", ".8")
    T(510, 152, "차원열차 →", 11, False, 0, ".1em", ".9")
    T(412, 690, "포구의 등대", 11, False, 0, ".05em", ".9")
    T(400, 452, "서항 만", 12, False, 0, ".2em", ".75")
    out.append("".join(lab))
    # district markers (clickable)
    for i, x, y, name, dx, dy in DISTRICTS:
        out.append(f'<a href="#d{i}" class="dm"><circle cx="{x}" cy="{y}" r="11" fill="{LAND}" stroke="{INK}" stroke-width="1.2"/>'
                   f'<circle cx="{x}" cy="{y}" r="8.5" fill="none" stroke="{INK}" stroke-width=".4"/>'
                   f'<text x="{x}" y="{y+4.5}" text-anchor="middle" font-family="IM Fell English SC,serif" font-size="13" fill="{INK}">{i}</text>'
                   f'<text x="{x+dx}" y="{y+dy}" text-anchor="middle" font-family="Song Myung,serif" font-size="15" fill="{INK}" '
                   f'paint-order="stroke" stroke="{LAND}" stroke-width="4">{name}</text></a>')
    out.append('</g>')
    # cartouche
    out.append(f'<g><rect x="44" y="44" width="300" height="118" fill="{LAND}" stroke="{INK}" stroke-width="1.4"/>'
               f'<rect x="50" y="50" width="288" height="106" fill="none" stroke="{INK}" stroke-width=".5"/>'
               f'<text x="194" y="92" text-anchor="middle" font-family="Song Myung,serif" font-size="28" fill="{INK}">아이파베스 대도시</text>'
               f'<text x="194" y="116" text-anchor="middle" font-family="IM Fell English SC,serif" font-size="13" letter-spacing=".22em" fill="{INK}">Aiphabess · Urbis Descriptio</text>'
               f'<text x="194" y="140" text-anchor="middle" font-family="IM Fell English,serif" font-style="italic" font-size="12" fill="{INK}" opacity=".8">mensurata anno XCV · luna XVIII</text></g>')
    # scale bar (walking time)
    sb = []
    for k in range(4):
        sb.append(f'<rect x="{900+k*50}" y="852" width="50" height="6" fill="{INK if k % 2 == 0 else LAND}" stroke="{INK}" stroke-width=".8"/>')
    out.append("".join(sb) + f'<text x="1000" y="844" text-anchor="middle" font-family="Gowun Batang,serif" font-size="11" fill="{INK}">걸어서 반 시간</text>')
    # neatline with ticks
    ticks = "".join(f"M{x},18v-6M{x},882v6" for x in range(30, 1180, 20)) + "".join(f"M18,{y}h-6M1182,{y}h6" for y in range(30, 880, 20))
    out.append(f'<rect x="18" y="18" width="1164" height="864" fill="none" stroke="{INK}" stroke-width="1.6"/>'
               f'<rect x="8" y="8" width="1184" height="884" fill="none" stroke="{INK}" stroke-width=".8"/>'
               f'<path d="{ticks}" stroke="{INK}" stroke-width=".5"/>')
    out.append(f'<rect width="{W}" height="{H}" filter="url(#tm-grain)" pointer-events="none"/>')
    out.append('</svg>')
    return "".join(out)

if __name__ == "__main__":
    import sys
    open(sys.argv[1], "w", encoding="utf-8").write(town_map())

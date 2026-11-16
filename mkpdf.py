#!/usr/bin/env python3
"""A4 landscape one-sheet (photo strip + chevron timeline + route maps with arrows) -> valeska-akihabara-nov17.pdf/.png
Same design as the adopted model-course sheet (Sample-shibuya.pdf). Needs: Pillow, qrcode, playwright chromium.
Run with /usr/local/bin/python3 (the python that has playwright)."""
import io, os, json, math, time, base64, urllib.request, tempfile
from PIL import Image, ImageDraw, ImageFont
import qrcode

from data import URL, PDF, P as PP, IMG
UA = {'User-Agent': 'route-sheet/1.0'}
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.mapcache'); os.makedirs(CACHE, exist_ok=True)

# ---- data (shared with build.py via data.py) -----------------------------------------------------
STOPS = {i: (PP[i][3], PP[i][0], PP[i][1]) for i in range(1, 8)}
NAMES = {i: PP[i][2] for i in range(1, 8)}
HOURS = {1: 'BiTO AKIBA PLAZA 1F, Electric Town exit', 2: 'Figure and hobby shops', 3: 'Character goods, 4th floor', 4: 'Crane games and prizes', 5: 'Figures and toys', 6: 'Anime goods, open 10:00-21:00', 7: 'Used manga, figures and games'}
PHOTOS = [IMG['figuarts'], IMG['manga'], IMG['trader'], IMG['anim']]
BAND = [(p[5], t) for p, t in zip(PP[1:], ['Meet, Vie de France', 'Radio Kaikan, figures', 'COSPA, goods', 'GiGO 3, crane games', 'Trader, toys', 'Animate, goods', 'BOOKOFF, used manga'])] + [('14:00', 'Done, near the station')]
WALK = {1: 'walk 3 min', 2: 'walk about 2 min', 3: 'walk about 3 min', 4: 'walk about 4 min', 5: 'walk about 3 min', 6: 'walk about 8 min'}

# ---- map rendering (PIL, OSM tiles, red route + arrows + numbered labelled pins) ----------------
def get(url, binary=False):
    for _ in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read()
            return r if binary else json.loads(r)
        except Exception: time.sleep(2)
def px(lat, lon, z):
    n = 2 ** z * 256
    return (lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
def tile(z, x, y):
    p = f'{CACHE}/t_{z}_{x}_{y}.png'
    if not os.path.exists(p):
        data = get(f'https://tile.openstreetmap.org/{z}/{x}/{y}.png', True)
        if not data: raise SystemExit(f'tile download failed: {z}/{x}/{y}')  # don't leave a 0-byte tile in the cache
        open(p, 'wb').write(data); time.sleep(0.15)
    return Image.open(p).convert('RGB')
def foot(a, b):
    p = f'{CACHE}/r_{a[0]:.5f}_{a[1]:.5f}_{b[0]:.5f}_{b[1]:.5f}.json'
    if not os.path.exists(p):
        r = get(f'https://routing.openstreetmap.de/routed-foot/route/v1/foot/{a[1]},{a[0]};{b[1]},{b[0]}?overview=full&geometries=geojson')
        try: line = [[y, x] for x, y in r['routes'][0]['geometry']['coordinates']]
        except Exception:
            print(f'warn: walking route failed, straight line used (not cached): {a} -> {b}')
            return [list(a), list(b)]
        json.dump(line, open(p, 'w'))
    return json.load(open(p))
def font(sz):
    for f in ['/System/Library/Fonts/Helvetica.ttc', '/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc']:
        try: return ImageFont.truetype(f, sz)
        except Exception: pass
    return ImageFont.load_default()

def dashed(d, xy, fill, width, on=16, off=12):
    for a, b in zip(xy, xy[1:]):
        L = math.dist(a, b)
        if L == 0: continue
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L; t = 0
        while t < L:
            e = min(t + on, L); d.line([(a[0] + ux * t, a[1] + uy * t), (a[0] + ux * e, a[1] + uy * e)], fill=fill, width=width); t += on + off
def arrows(d, xy, fill, every=150, size=17):
    acc = every / 2
    for a, b in zip(xy, xy[1:]):
        L = math.dist(a, b)
        if L == 0: continue
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L; pos = 0
        while pos + acc <= L:
            pos += acc; acc = every
            cx, cy = a[0] + ux * pos, a[1] + uy * pos
            tip = (cx + ux * size, cy + uy * size); l = (cx - ux * size * .6 - uy * size * .8, cy - uy * size * .6 + ux * size * .8); r = (cx - ux * size * .6 + uy * size * .8, cy - uy * size * .6 - ux * size * .8)
            d.polygon([tip, l, r], fill=fill, outline='white')
        acc -= (L - pos)

def render(out, W, H, pins, legs, stations, dots=()):
    """pins [(n,label,lat,lon)], legs [(kind,[(lat,lon)..])] kind foot|train, stations [(name,lat,lon)], dots [(letter,lat,lon)]"""
    allpts = [(p[2], p[3]) for p in pins] + [(s[1], s[2]) for s in stations] + [(x[1], x[2]) for x in dots]
    for _, line in legs: allpts += [tuple(q) for q in line]
    lats = [p[0] for p in allpts]; lons = [p[1] for p in allpts]
    z = 17
    while z > 4:
        x0, y1 = px(min(lats), min(lons), z); x1, y0 = px(max(lats), max(lons), z)
        if x1 - x0 < W - 150 and y1 - y0 < H - 150: break
        z -= 1
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; ox, oy = cx - W / 2, cy - H / 2
    img = Image.new('RGB', (W, H), '#ddd')
    for tx in range(int(ox // 256), int((ox + W) // 256) + 1):
        for ty in range(int(oy // 256), int((oy + H) // 256) + 1): img.paste(tile(z, tx, ty), (int(tx * 256 - ox), int(ty * 256 - oy)))
    img = img.convert('RGBA'); d = ImageDraw.Draw(img)
    P = lambda la, lo: (px(la, lo, z)[0] - ox, px(la, lo, z)[1] - oy)
    for kind, line in legs:
        xy = [P(*q) for q in line]
        if kind == 'train': dashed(d, xy, '#444', 7)
        else:
            d.line(xy, fill='white', width=14, joint='curve'); d.line(xy, fill='#e60012', width=8, joint='curve'); arrows(d, xy, '#e60012')
    pinpos = []
    for n, label, la, lo in pins:
        x, y = P(la, lo); pinpos.append((x, y))
        d.ellipse([x - 21, y - 21, x + 21, y + 21], fill='#111', outline='white', width=4); d.text((x, y), str(n), fill='white', font=font(27), anchor='mm')
    occ = [(x - 24, y - 24, x + 24, y + 24) for x, y in pinpos]
    def put(text, x, y, fill, ink, fs, outline):
        ft = font(fs); l, t, r, b = d.textbbox((0, 0), text, font=ft); w, h = r - l + 16, b - t + 10
        for dx, dy in [(26, -h / 2), (-w - 26, -h / 2), (-w / 2, 26), (-w / 2, -h - 26), (26, 10), (-w - 26, 10), (26, -h - 10), (-w - 26, -h - 10)]:
            bx = (x + dx, y + dy, x + dx + w, y + dy + h)
            if bx[0] < 4 or bx[1] < 4 or bx[2] > W - 4 or bx[3] > H - 30: continue
            if any(not (bx[2] < o[0] or bx[0] > o[2] or bx[3] < o[1] or bx[1] > o[3]) for o in occ): continue
            d.rounded_rectangle(bx, radius=8, fill=fill, outline=outline, width=2); d.text((bx[0] + 8, bx[1] + 4 - t), text, fill=ink, font=ft); occ.append(bx); return
    for ltr, la, lo in dots:
        x, y = P(la, lo); d.ellipse([x - 17, y - 17, x + 17, y + 17], fill='white', outline='#e60012', width=5); d.text((x, y), ltr, fill='#e60012', font=font(25), anchor='mm'); occ.append((x - 19, y - 19, x + 19, y + 19))
    for nm, la, lo in stations:
        x, y = P(la, lo); d.ellipse([x - 8, y - 8, x + 8, y + 8], fill='#1d4f91', outline='white', width=3); occ.append((x - 9, y - 9, x + 9, y + 9)); put(nm, x, y, '#1d4f91', 'white', 20, 'white')
    for (n, label, la, lo), (x, y) in zip(pins, pinpos): put(label, x, y, 'white', '#111', 23, '#111')
    d.rectangle([W - 250, H - 24, W, H], fill=(255, 255, 255, 210)); d.text((W - 6, H - 12), '© OpenStreetMap contributors', fill='#333', font=font(16), anchor='rm')
    img.convert('RGB').save(out)

S = lambda n: (STOPS[n][1], STOPS[n][2])
def make_maps():
    legs = [('foot', foot(S(i), S(i + 1))) for i in range(1, 7)]
    render(f'{CACHE}/map_aki.png', 1000, 1000, [(i, STOPS[i][0], *S(i)) for i in range(1, 8)], legs, [])

# ---- html ---------------------------------------------------------------------------------------
def leg(txt): return f'<li class="leg"><u></u>{txt}</li>'
def build_html():
    b64 = lambda p: ('data:image/jpeg;base64,' if p.endswith('.jpg') else 'data:image/png;base64,') + base64.b64encode(open(p, 'rb').read()).decode()
    q = qrcode.make(URL, box_size=6, border=1); bb = io.BytesIO(); q.save(bb, 'PNG'); qr = base64.b64encode(bb.getvalue()).decode()
    band = ''.join(f'<div class="s{" first" if i == 0 else " last" if i == len(BAND) - 1 else ""}"><b>{t}</b>{x}</div>' for i, (t, x) in enumerate(BAND))
    photos = ''.join(f'<div><img src="{b64(os.path.join(os.path.dirname(os.path.abspath(__file__)), u))}" alt=""></div>' for u in PHOTOS)
    rows = ''
    for i in range(1, 8):
        rows += f'<li><i>{i}</i>{NAMES[i]}<small>{HOURS[i]}</small></li>'
        if i in WALK: rows += leg(WALK[i])
    rows += '<li class="back"><span>Done around 14:00, near JR Akihabara Station (BOOKOFF is 2 min from the station).</span></li>'
    css = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sheet.css')).read()
    return f'''<!doctype html><meta charset=utf-8><title>Akihabara Anime Tour, Tuesday November 17</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&display=swap" rel="stylesheet">
<style>{css}</style>
<article><header><h1>Akihabara Anime Tour</h1><div class="meta">For Valeska, Stefano &amp; Carolina · Tuesday, November 17<br>Guide: Yuuki · meet 11:00, done about 14:00<div class="chips"><span>Figures</span><span>Manga</span><span>Toys</span><span>Crane games</span></div></div></header>
<div class="ph">{photos}</div><div class="band">{band}</div>
<div class="low"><img class="map" src="{b64(CACHE + '/map_aki.png')}" alt="">
<div class="side"><h2>Route</h2><ul>{rows}</ul><h2>Meeting point</h2><p class="mp">Vie de France Dining, BiTO AKIBA PLAZA 1F, in front of the Electric Town exit of JR Akihabara Station.</p>
<div class="foot"><img src="data:image/png;base64,{qr}"><div><p><b>Full plan and maps:</b> yukitchy.github.io/valeska-akihabara-nov17</p><p>Times are approximate and can move on the day.</p></div></div></div></div></article>'''

def main():
    make_maps()
    html = build_html(); tmp = os.path.join(tempfile.gettempdir(), 'valeska-sheet.html'); open(tmp, 'w').write(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1123, 'height': 794}); pg.goto('file://' + tmp); pg.wait_for_load_state('networkidle'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(2500)
        over = pg.evaluate("(()=>{const a=document.querySelector('article'),s=document.querySelector('.side');return [a.scrollHeight>a.clientHeight+1, s.scrollHeight>s.clientHeight+1]})()")
        pg.pdf(path=PDF, format='A4', landscape=True, print_background=True, prefer_css_page_size=True)
        pg.screenshot(path=PDF[:-4] + '.png', full_page=False); b.close()
    import re; d = open(PDF, 'rb').read()
    print('pages', len(re.findall(rb'/Type\s*/Page[^s]', d)), 'overflow(article,side)', over)

if __name__ == '__main__': main()

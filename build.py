#!/usr/bin/env python3
"""Valeska, Tue Nov 17: Akihabara tour page, hero layout (same template as akiba-anime-day-kids). python3 build.py -> index.html"""
import re, os
from data import *
css = open('style.css').read()
src = open(os.path.expanduser('~/akiba-where-to-eat/index.html')).read()
svg0 = re.search(r'<svg id="map".*?</svg>', src, flags=re.S).group(0)
base = svg0[:svg0.index('<line x1="376" y1="231"')].rstrip().replace('Simple sketch map of the 14 places', 'Simple sketch map of the route')
lat0, lon0 = 35.69836, 139.77311
def xy(la, lo): return round(425 + (lo - lon0) * 90350 * 0.44), round(249 - (la - lat0) * 111200 * 0.44)
# n, tag, short, name, img, genre, jp, text, hours, hrs line, maps query
S = [
 (1, 'Figures', 'RADIO KAIKAN', 'AKIHABARA RADIO KAIKAN', 'radio-kaikan.jpg', 'Figures, cards, character goods', '秋葉原ラジオ会館',
  'Glass cases of figures on every floor, from Dragon Ball Z and Evangelion to Demon Slayer and Jujutsu Kaisen. Look into the small shops and see what you can find. The photo shows a figure case in an Akihabara shop.', None, None, 'Akihabara Radio Kaikan'),
 (2, 'Goods', 'COSPA 4F', 'COSPA G-STORE AKIBA, 4TH FLOOR', 'cospa.jpg', 'Character clothes and goods', 'コスパ ジーストア・アキバ店',
  'Character apparel and goods on the 4th floor of the Onoden main building, a few minutes from Radio Kaikan. Take the lift to the 4th floor. The photo shows the building.', '10:00 to 20:00', '10:00 to 20:00, no regular day off (official site, checked on 5 Nov 2026)', 'COSPA G-STORE Akiba Onoden'),
 (3, 'Crane games', 'GIGO 3', 'GIGO AKIHABARA 3', 'gigo.jpg', 'Arcade and crane games', 'GiGO 秋葉原3号館',
  'Rows and rows of crane games filled with anime prizes. Try a few machines and win something to take home. You do not need to win to enjoy it.', None, None, 'GiGO Akihabara 3'),
 (4, 'Treasure', 'TRADER', 'TRADER', 'trader.jpg', 'Figures and toys, packed to the ceiling', 'トレーダー',
  'A bright shop crammed with figures and toys. Take your time and look at every shelf: this is where Carolina can hunt for Mazinger Z. The photo shows a case of vintage robot toys, the kind of thing we look for.', None, None, 'Trader Akihabara main store'),
 (5, 'Goods', 'ANIMATE', 'ANIMATE AKIHABARA', 'animate.jpg', 'Anime goods, many series', 'アニメイト秋葉原',
  'Several floors of current anime and manga goods: Demon Slayer, SPY&times;FAMILY, Jujutsu Kaisen, HUNTER&times;HUNTER, Dandadan and more. The photo shows the shop front on Chuo-dori. A good place for souvenirs.', '10:00 to 21:00', '10:00 to 21:00, open daily (official site, checked on 5 Nov 2026)', 'Animate Akihabara'),
 (6, 'Manga', 'BOOKOFF', 'BOOKOFF AKIHABARA EKIMAE', 'manga.jpg', 'Used manga, figures and games', 'ブックオフ 秋葉原駅前店',
  'A treasure hunt for second-hand manga: long shelves of Dragon Ball, Naruto, Jujutsu Kaisen and more, plus used figures and games at small prices. It is right by the station, so it is a good last stop. The photo shows a manga shop in Japan, the kind of shelf we look at.', None, None, 'BOOKOFF Akihabara Ekimae'),
]
N = {p[0]: p for p in S}
clock = '<svg viewBox="0 0 16 16" width="15" height="15" aria-hidden="true"><circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 4.5V8l2.5 1.8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
def tile(p): return f'<a class="tile" href="#p{p[0]}"><img src="img/{p[4]}" alt="" loading="lazy"><b class="no">{p[0]:02d}</b><span class="tt">{p[1]}</span><span class="tn">{p[2]}</span></a>'
def card(p):
    n, _, _, title, img, genre, jp, tx, hours, hrs, maps = p
    strip = f'<p class="strip"><span class="hr">{clock}<b class="today">{hours}</b></span></p><p class="hrs">{hrs}</p>' if hours else ''
    return (f'<article class="card" id="p{n}"><div class="hd"><span class="big">{n:02d}</span><div><span class="genre">{genre}</span><h3>{title}</h3></div></div>'
            f'<img class="ph" src="img/{img}" alt="" loading="lazy"><p class="jp" lang="ja">{jp}</p><p class="tx">{tx}</p>{strip}'
            f'<div class="bt"><a class="btn" href="https://www.google.com/maps/search/?api=1&amp;query={maps.replace(" ", "+")}">Google Maps <i>&rarr;</i></a></div></article>')
# map: route line + pins (meeting = M, stops 1-6)
pts = [xy(p[0], p[1]) for p in P[1:]]
line = '<polyline points="' + ' '.join(f'{x},{y}' for x, y in pts) + '" fill="none" stroke="#D9342B" stroke-width="5" stroke-dasharray="12 8" stroke-linecap="round"/>'
pins = ''
for k, p in enumerate(P[1:]):
    x, y = pts[k]; nm = p[3]; w = len(nm) * 9 + 24; lab = 'M' if k == 0 else str(k)
    a0, a1 = ('<a class="pin" href="#route" data-n="0">', '</a>') if k == 0 else (f'<a class="pin" href="#p{k}" data-n="{k}">', '</a>')
    pins += f'{a0}<circle cx="{x}" cy="{y}" r="16" fill="#121212" stroke="#fff" stroke-width="3"/><text x="{x}" y="{y+6}" text-anchor="middle" font-size="16" font-weight="900" fill="#fff">{lab}</text><g class="lbl"><rect x="{x-w//2}" y="{y-46}" width="{w}" height="28" fill="#121212"/><text x="{x}" y="{y-27}" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">{nm}</text></g>{a1}'
mapsvg = base + line + pins + '</svg>'
R = [('11:00', 'Meet inside Vie de France', 'The bakery caf&eacute; near Akihabara Station. I will be there at 11:00, and use the map link in my message.', None),
     ('11:10', 1, 'figures, about 20 min', None), ('11:35', 2, 'goods, about 20 min', None), ('12:00', 3, 'crane games, about 30 min', None),
     ('12:40', 4, 'figures and toys, about 25 min', None), ('13:10', 5, 'goods and souvenirs, about 20 min', None), ('13:40', 6, 'used manga and figures, about 20 min', None), ('14:00', 'Goodbye, near the station', 'We finish around 14:00.', None)]
tl = ''
for t, a, b, _ in R:
    if isinstance(a, int): tl += f'<li><b>{t}</b><span><a href="#p{a}" style="color:inherit;font-weight:800">{a:02d} {N[a][3].title().replace('Cospa','COSPA').replace('Gigo','GiGO')}</a><em>{b}</em></span></li>'
    else: tl += f'<li><b>{t}</b><span>{a}<em>{b}</em></span></li>'
route = (f'<section class="route" id="route"><div class="hd"><span class="big">&rarr;</span><div><span class="genre">Tuesday, November 17</span><h3>THE ROUTE</h3></div></div>'
         f'<p class="tx">Meet at 11:00, finish around 14:00. All on foot, all within a small area.</p><ul class="tl">{tl}</ul></section>')
credits = ('The photo for COSPA shows the building. Photos for Radio Kaikan, Trader, BOOKOFF and the hero show the kind of place, not the shop itself. The photo for GiGO is from a GiGO Akihabara arcade, and the Animate photo is the shop itself. All from Wikimedia Commons except the large figure photo in the hero, which I took in Akihabara: ' + '; '.join(CREDITS) + '. Animate hours come from its official site, checked on November 5. BOOKOFF is shown as open 10:00 to 22:00 on OpenStreetMap, not checked on its own site. Other hours were not confirmed. The map is a simple sketch, not to scale, and the positions of Trader, COSPA and BOOKOFF are approximate. Times are approximate and can move on the day.')
html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Akihabara Anime Tour for Valeska, Stefano &amp; Carolina</title><meta name="robots" content="noindex,nofollow">
<meta name="description" content="Six stops in Akihabara for figures and manga: Radio Kaikan, COSPA, GiGO 3, Trader, Animate and BOOKOFF. Tuesday, November 17, 11:00 to 14:00.">
<meta property="og:type" content="website"><meta property="og:url" content="{URL}"><meta property="og:site_name" content="Akihabara Anime Tour">
<meta property="og:title" content="Akihabara Anime Tour for Valeska, Stefano and Carolina"><meta property="og:description" content="Figures, manga and anime goods. Tuesday, November 17, 11:00 to 14:00."><meta property="og:image" content="{URL}og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="Akihabara Anime Tour for Valeska, Stefano and Carolina"><meta name="twitter:description" content="Figures, manga and anime goods. Tuesday, November 17, 11:00 to 14:00."><meta name="twitter:image" content="{URL}og.jpg">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Noto+Sans+JP:wght@500;700;900&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<div class="col"><div class="top"><span>GUEST GUIDE</span><span>AKIHABARA &middot; 6 STOPS</span></div>
<h1>Hunt for treasure in <em>Akihabara</em></h1></div>
<div class="col" style="padding:0"><div class="hero"><img src="img/hero-collage.jpg" alt="Three real photos: anime figures, a manga shelf, a figure display case"><div class="vt">秋葉原</div></div>
<div class="hb"><span>Tue 17 Nov &middot; 11:00 to 14:00</span><b>Meet inside Vie de France</b></div></div>
<div class="col"><p class="gp" style="margin-top:18px">Valeska, Stefano and Carolina, this is our route: figures and manga first. We look at figure cases, shelves of used manga, old toys, crane games and anime goods. Dragon Ball Z, Demon Slayer, SPY&times;FAMILY, Jujutsu Kaisen, HUNTER&times;HUNTER, Evangelion, Dandadan, Ghibli, Rurouni Kenshin, and Mazinger Z for Carolina. You do not need to buy anything.</p>
<div class="maphd"><h2 class="map">The map</h2></div><p class="gp">Tap a pin to see the name, tap again to jump to the place.</p>{mapsvg}<div class="lg"><span><i class=""></i>M is where we meet. Everything is within about 10 minutes on foot.</span></div>
<div class="bar"><h2>FIGURES AND GOODS</h2><span>1-2</span></div><div class="wall w2">{tile(N[1])}{tile(N[2])}</div>
<div class="bar r"><h2>GAMES AND TOYS</h2><span>3-4</span></div><div class="wall w2">{tile(N[3])}{tile(N[4])}</div>
<div class="bar"><h2>GOODS AND MANGA</h2><span>5-6</span></div><div class="wall w2">{tile(N[5])}{tile(N[6])}</div>
<div class="bar"><h2>THE DAY</h2><span>11:00 &middot; 14:00</span></div><p class="gp">Times are approximate and we can change as we go.</p>{route}
{''.join(card(p) for p in S)}<p class="gp"><a class="btn" href="{PDF}" target="_blank" rel="noopener">Open the PDF (A4, 1 page) <i>&rarr;</i></a></p></div>
<details class="crd"><summary>Photo credits and sources</summary><p class="cr">{credits}</p></details>
<script>
(function(){{var coarse=matchMedia('(pointer:coarse)').matches,onPin=null;
document.querySelectorAll('.pin').forEach(function(a){{a.addEventListener('click',function(ev){{ev.preventDefault();if(coarse&&onPin!==a){{if(onPin)onPin.classList.remove('on');onPin=a;a.classList.add('on');return}}var c=document.getElementById(a.dataset.n==='0'?'route':'p'+a.dataset.n);if(!c)return;c.scrollIntoView({{behavior:'smooth',block:'start'}});c.classList.add('hit');setTimeout(function(){{c.classList.remove('hit')}},1600);if(onPin){{onPin.classList.remove('on');onPin=null}}}})}});
document.getElementById('map').addEventListener('click',function(ev){{if(!ev.target.closest('.pin')&&onPin){{onPin.classList.remove('on');onPin=null}}}});}})();
</script></body></html>'''
open('index.html', 'w').write(html); print('built', len(html))

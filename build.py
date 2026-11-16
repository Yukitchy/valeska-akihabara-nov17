#!/usr/bin/env python3
"""Valeska, Tue Nov 17: Akihabara anime tour page (same format as patrick-tokyo-day). python3 build.py -> index.html"""
import json
from data import *
gm = lambda q: 'https://www.google.com/maps/search/?api=1&query=' + q.replace(' ', '+')
A = lambda u, t: f'<a href="{u}" target="_blank" rel="noopener">{t}</a>'
def links(*ls): return '<ul class="links">' + ''.join('<li>' + A(u, t) + '</li>' for t, u in ls) + '</ul>'
def nums(*ns): return '<dl class="nums">' + ''.join(f'<div><dt>{a}</dt><dd class="n">{b}</dd><dd class="s">{c}</dd></div>' for a, b, c in ns) + '</dl>'
def pts(*ps): return '<ul class="pts">' + ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in ps) + '</ul>'
def ph(k, alt): return f'<div class="ph"><img src="{IMG[k]}" alt="{alt}"></div>'
def nxt(*rows): return '<div class="next"><p class="nl">Next</p>' + ''.join(f'<p>{r}</p>' for r in rows) + '</div>'
TT = [('11:00', 'Meet at JR Akihabara'), ('11:10', 'Akihabara Radio Kaikan'), ('12:00', 'Mandarake Complex'), ('12:40', 'Super Potato'),
      ('13:10', 'Animate Akihabara'), ('13:35', 'Kanda Myojin Shrine'), ('14:00', 'Done, at JR Akihabara')]
tt = ''.join(f'<tr class="st-plain"><td class="v">{t}</td><td><span class="k">{k}</span></td></tr>' for t, k in TT)
def step(i, h, body): return f'<article class="step" data-i="{i}"><p class="no"><i>{i}</i>{P[i][5]}</p><h2>{h}</h2>{body}</article>'
S = []
S.append('<article class="step" data-i="0"><p class="no"><i>0</i>The whole day</p><h2>Akihabara, <span class="l2">11:00 to <em>14:00</em></span></h2>'
 '<p class="lead">Three hours in the heart of anime and manga Tokyo: figures, retro manga, retro games, anime goods, and one famous shrine from the anime. All on foot, all within a small area.</p>'
 f'<div class="tt"><p class="cap">The day</p><table>{tt}</table></div>'
 + pts(('Made for you', 'Dragon Ball Z, Demon Slayer, SPY×FAMILY, Jujutsu Kaisen, HUNTER×HUNTER, Evangelion, Dandadan, Ghibli and Rurouni Kenshin. And Mazinger Z for Carolina.'),
       ('Keep in mind', 'Times are approximate and can move on the day. Shops are small and busy, so we take it at your pace.'))
 + links(('Open the whole route in Google Maps', 'https://www.google.com/maps/dir/?api=1&origin=JR+Akihabara+Station&destination=Kanda+Myojin&waypoints=Akihabara+Radio+Kaikan%7CMandarake+Complex+Akihabara%7CSuper+Potato+Akihabara%7CAnimate+Akihabara&travelmode=walking')) + '</article>')
S.append(step(1, 'We meet at <em>Akihabara</em>', ph('stn', 'The Electric Town exit of JR Akihabara Station')
 + '<p class="lead">Meet at Vie de France Dining on the 1st floor of BiTO AKIBA PLAZA, right in front of the Electric Town exit of JR Akihabara Station. I will be there at 11:00.</p>'
 + nums(('Time', '11:00', 'Tuesday, November 17'), ('Finish', '14:00', 'JR Akihabara'))
 + links(('Meeting point on Google Maps', gm('Vie de France Dining BiTO AKIBA PLAZA Akihabara')))
 + nxt('Walk 3 min to Radio Kaikan')))
S.append(step(2, '<em>Radio Kaikan</em>, figures', ph('radio', 'Akihabara Radio Kaikan building')
 + '<p class="lead">A landmark building packed with figure and hobby shops, floor after floor. A great place to find Dragon Ball Z and Evangelion figures, and we can look for Demon Slayer and Jujutsu Kaisen too.</p>'
 + links(('Radio Kaikan on Google Maps', gm('Akihabara Radio Kaikan')))
 + nxt('Walk about 8 min to Mandarake')))
S.append(step(3, '<em>Mandarake</em> Complex', ph('mand', 'The Mandarake Complex building in Akihabara')
 + '<p class="lead">Mandarake is a famous second-hand shop for manga, figures and collectibles. Look for old manga volumes, vintage toys and retro anime goods: Rurouni Kenshin, Dragon Ball, and for Carolina, Mazinger Z. It opens at 12:00, so we arrive right on time.</p>'
 + nums(('Open', '12:00 to 20:00', 'Daily'))
 + links(('Mandarake on Google Maps', gm('Mandarake Complex Akihabara')), ('Official site', 'https://www.mandarake.co.jp/dir/cmp/index-en.html'))
 + nxt('Walk 2 min to Super Potato')))
S.append(step(4, '<em>Super Potato</em>, retro games', ph('pot', 'The Super Potato retro game shop')
 + '<p class="lead">Retro games from the Famicom, Super Famicom and beyond, over several floors of the Kitabayashi Building. There is also an arcade on the top floor, so we can see classic games, including Dragon Ball Z games, if they have them.</p>'
 + nums(('Open', '11:00 to 20:00', 'Daily'))
 + links(('Super Potato on Google Maps', gm('Super Potato Akihabara')))
 + nxt('Walk about 5 min to Animate')))
S.append(step(5, '<em>Animate</em> Akihabara', ph('anim', 'The Animate Akihabara store')
 + '<p class="lead">Animate is Japan\'s biggest anime shop chain. This is where to look for current goods and apparel: Demon Slayer, SPY×FAMILY, Jujutsu Kaisen, HUNTER×HUNTER, Dandadan and more. A good stop for souvenirs.</p>'
 + links(('Animate on Google Maps', gm('Animate Akihabara')), ('Official site', 'https://www.animate.co.jp/shop/akihabara/'))
 + nxt('Walk about 6 min to Kanda Myojin')))
S.append(step(6, '<em>Kanda Myojin</em>, and done', ph('myo', 'Kanda Myojin Shrine')
 + '<p class="lead">A shrine just up the hill from Akihabara, loved by anime fans. It has appeared in anime such as Love Live! and Steins;Gate, and it is known for charms for electronics and IT. A calm end to the day.</p>'
 + '<p class="note" style="font-size:13px;color:var(--mute)">From here it is about 15 min on foot back to JR Akihabara Station, where we say goodbye around 14:00.</p>'
 + links(('Kanda Myojin on Google Maps', gm('Kanda Myojin')), ('Official site', 'https://www.kandamyoujin.or.jp/'))
 + nxt('Walk about 15 min back to JR Akihabara, 14:00')))
credit = ('<footer class="credit"><p class="note" style="margin:0 0 10px">Times are approximate and can move on the day. Message Yuuki if you want to change anything.</p><details><summary>Photo credits</summary><ul>'
 + ''.join(f'<li>{c}</li>' for c in CREDITS) + '</ul><p>Photos via Wikimedia Commons. Map: Tiles © Esri / © ' + A('https://www.openstreetmap.org/copyright', 'OpenStreetMap') + '</p></details></footer>')
dn = ''.join(f'<button type="button" class="dn" data-i="{i}" aria-label="{"The whole day" if i == 0 else P[i][5]}">{i}</button>' for i in range(len(P)))
head = ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><meta name="robots" content="noindex,nofollow"><title>Akihabara Anime Tour for Valeska, Stefano &amp; Carolina</title>'
 '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700;900&display=swap">'
 '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"><script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script><style>' + open('style.css').read() + '</style></head><body>')
intro = ('<div class="wrap"><div class="mapbox"><div id="map" aria-label="Map of the day"></div><p class="where"><small>Tue, November 17</small><b>The whole day</b></p>'
 '<nav class="dial" aria-label="Switch stop"><button type="button" class="ar" data-d="-1" aria-label="Previous stop">&lsaquo;</button><div class="nums-r">' + dn + '</div><button type="button" class="ar" data-d="1" aria-label="Next stop">&rsaquo;</button></nav></div>'
 '<main class="story"><header class="intro"><p class="date">Tuesday, November 17 · 11:00 to 14:00</p><h1>Akihabara Anime Tour</h1><p class="who">For Valeska, Stefano and Carolina, with Yuuki. Figures, retro manga, retro games, anime goods and a famous shrine.</p>'
 '<dl class="cn"><div><dt>Meet</dt><dd class="n">11:00</dd><dd class="s">Vie de France Dining, BiTO AKIBA PLAZA 1F</dd></div><div><dt>Finish</dt><dd class="n">14:00</dd><dd class="s">JR Akihabara</dd></div></dl>'
 f'<div class="tools"><a class="tool" href="{PDF}" target="_blank" rel="noopener">Open the PDF (A4, 1 page)</a></div></header>')
js = ('<script>const LI=-1,LUNCH=[[35.7,139.77,"x","t"]],DAYS=%s,P=%s,GEO=[];' % (json.dumps(['The whole day'] + [p[5] for p in P[1:]]), json.dumps([None] + [[p[0], p[1], p[2], p[3], p[4], 0] for p in P[1:]])))
js += open('map.js').read() + '</script>'
open('index.html', 'w').write(head + intro + ''.join(S) + credit + '</main></div>' + js + '</body></html>')

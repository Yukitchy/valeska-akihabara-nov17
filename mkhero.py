# Hero collage 1280x960: big left = own S.H.Figuarts figure photo, right top = manga shelf (Wikimedia), right bottom = figure case (Wikimedia)
from PIL import Image
W,H,G,LW=1280,960,4,760
def fit(p,w,h,cx=.5,cy=.5):
    im=Image.open(p).convert('RGB'); r=max(w/im.width,h/im.height); im=im.resize((round(im.width*r),round(im.height*r)),Image.LANCZOS)
    x=round((im.width-w)*cx); y=round((im.height-h)*cy); return im.crop((x,y,x+w,y+h))
c=Image.new('RGB',(W,H),'#121212'); rh=(H-G)//2; rw=W-LW-G
c.paste(fit('ogp-src.jpg',LW,H,.42,.5),(0,0))
c.paste(fit('img/manga.jpg',rw,rh,.72,.1),(LW+G,0))
c.paste(fit('img/figurecase.jpg',rw,H-rh-G),(LW+G,rh+G))
c.save('img/hero-collage.jpg',quality=88,optimize=True)

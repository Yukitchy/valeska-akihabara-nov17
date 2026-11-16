# Builds og.jpg (1200x630) from ogp-src.jpg (own photo, S.H.Figuarts case, Akihabara) + favicon.svg is hand-written.
from PIL import Image, ImageDraw, ImageFont
W, H, PH = 1200, 630, 372
RED, INK = (229, 56, 43), (26, 26, 26)
F = lambda i, s: ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', s, index=i)
src = Image.open('ogp-src.jpg').convert('RGB')
c = Image.new('RGB', (W, H), INK)
r = max(W / src.width, PH / src.height)
p = src.resize((round(src.width * r), round(src.height * r)), Image.LANCZOS)
c.paste(p.crop(((p.width - W) // 2, round((p.height - PH) * 0.8), (p.width - W) // 2 + W, round((p.height - PH) * 0.8) + PH)), (0, 0))
d = ImageDraw.Draw(c)
d.rectangle((0, PH, W, PH + 8), fill=RED)
d.text((60, PH + 30), 'Akihabara Anime Tour', font=F(1, 78), fill='white')
d.text((60, PH + 120), 'for Valeska, Stefano & Carolina', font=F(0, 38), fill=(235, 235, 235))
chip, fw = 'TUE, NOV 17  ·  11:00-14:00', F(1, 30)
tw = d.textlength(chip, font=fw)
d.rectangle((60, PH + 188 - 4, 60 + tw + 36, PH + 188 + 36), fill=RED)
d.text((78, PH + 188), chip, font=fw, fill='white')
c.save('og.jpg', quality=90, optimize=True)

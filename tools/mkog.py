"""OG-картинка визитки i.seedwave.pt (1200×630). Запуск: python3 tools/mkog.py photo-hero.jpg og-card.jpg
v2 (10.10.2026): текст не заходит на фото, затемнение только по краю фото (бамбук), лицо чистое."""
import sys, math
from PIL import Image, ImageDraw, ImageFont
src, out = sys.argv[1], sys.argv[2]
W, H = 1200, 630
BG = (6, 34, 43); INK = (240, 248, 250); MUTED = (170, 204, 211); ACC = (25, 168, 196)
F = '/usr/share/fonts/opentype/inter/'
f = lambda n, s: ImageFont.truetype(F + n, s)
im = Image.new('RGB', (W, H), BG)
# фото справа: панель 480 px, лицо по центру панели
ph = Image.open(src).convert('RGB')
sc = 700 / ph.height
ph = ph.resize((int(ph.width * sc), int(ph.height * sc)), Image.LANCZOS)
pw = 480
left = max(0, min(ph.width - pw, int(430 * sc - pw / 2)))
top = 18
im.paste(ph.crop((left, top, left + pw, top + H)), (W - pw, 0))
# короткий переход только по левому краю фото (40 px, там бамбук)
fade = 40
mask = Image.new('L', (fade, H), 0); md = ImageDraw.Draw(mask)
for x in range(fade):
    md.line([(x, 0), (x, H)], fill=int(255 * (1 - x / fade) ** 1.5))
im.paste(Image.new('RGB', (fade, H), BG), (W - pw, 0), mask)
d = ImageDraw.Draw(im)
x0 = 70
def spaced(xy, text, font, fill, sp):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill); x += d.textlength(ch, font=font) + sp
spaced((x0, 70), 'IGOR KARTUZOV · SEEDWAVE', f('Inter-Bold.otf', 22), MUTED, 1.4)
big = f('Inter-ExtraBold.otf', 88)
d.text((x0 - 3, 128), 'СУБСИДИИ', font=big, fill=INK)
d.text((x0 - 3, 236), 'МАДЕЙРЫ', font=big, fill=ACC)
d.text((x0, 378), 'чекер · табло программ · заявки', font=f('Inter-Medium.otf', 31), fill=INK)
d.text((x0, 426), 'apoios às empresas da Madeira', font=f('Inter-Regular.otf', 28), fill=MUTED)
pf = f('Inter-Bold.otf', 28); t = 'i.seedwave.pt'; tw = d.textlength(t, font=pf)
d.rounded_rectangle((x0 - 4, 512, x0 + tw + 30, 566), radius=27, fill=(14, 53, 63))
d.text((x0 + 13, 520), t, font=pf, fill=ACC)
d.line([(x0 + i, 596 + 5 * math.sin(i / 40.0)) for i in range(0, 300, 2)], fill=ACC, width=4)
# контроль: правый край текста не заходит на фото
right = max(x0 - 3 + d.textlength('СУБСИДИИ', font=big), x0 + d.textlength('чекер · табло программ · заявки', font=f('Inter-Medium.otf', 31)))
assert right < W - pw - 30, right
im.save(out, 'JPEG', quality=90, optimize=True)
print(im.size, 'text right edge', int(right), 'photo starts', W - pw)

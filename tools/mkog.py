import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
src, out = sys.argv[1], sys.argv[2]
W,H=1200,630
BG=(6,34,43); INK=(240,248,250); MUTED=(170,204,211); ACC=(25,168,196)
F='/usr/share/fonts/opentype/inter/'
def f(name,size): return ImageFont.truetype(F+name,size)
im=Image.new('RGB',(W,H),BG)
# photo right
ph=Image.open(src).convert('RGB')
scale=720/ph.height
ph=ph.resize((int(ph.width*scale),int(ph.height*scale)),Image.LANCZOS)
pw=430
left=int(ph.width*0.235); top=int(ph.height*0.06)
crop=ph.crop((left,top,left+pw,top+H))
im.paste(crop,(W-pw,0))
# gradient fade from bg to photo
grad=Image.new('L',(pw,H),0); gd=ImageDraw.Draw(grad)
for x in range(pw):
    a=255 if x>120 else int(255*(x/120)**1.6)
    gd.line([(x,0),(x,H)],fill=255-a)
ov=Image.new('RGB',(pw,H),BG)
im.paste(ov,(W-pw,0),grad)
d=ImageDraw.Draw(im)
x0=74
def spaced(xy,text,font,fill,sp):
    x,y=xy
    for ch in text:
        d.text((x,y),ch,font=font,fill=fill); x+=d.textlength(ch,font=font)+sp
spaced((x0,64),'IGOR KARTUZOV · SEEDWAVE',f('Inter-Bold.otf',25),MUTED,1.6)
big=f('Inter-ExtraBold.otf',106)
d.text((x0-4,128),'СУБСИДИИ',font=big,fill=INK)
d.text((x0-4,246),'МАДЕЙРЫ',font=big,fill=ACC)
d.text((x0,402),'чекер · табло программ · заявки',font=f('Inter-Medium.otf',35),fill=INK)
d.text((x0,456),'apoios às empresas da Madeira',font=f('Inter-Regular.otf',33),fill=MUTED)
# pill
pf=f('Inter-Bold.otf',31); t='i.seedwave.pt'; tw=d.textlength(t,font=pf)
d.rounded_rectangle((x0-4,538,x0+tw+34,596),radius=29,fill=(14,53,63))
d.text((x0+15,548),t,font=pf,fill=ACC)
# wave
import math
pts=[(410+i, 604+6*math.sin(i/46.0)) for i in range(0,290,2)]
d.line(pts,fill=ACC,width=4)
im.save(out,'JPEG',quality=90,optimize=True)
print(im.size)

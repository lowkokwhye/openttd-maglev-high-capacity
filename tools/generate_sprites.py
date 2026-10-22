from PIL import Image, ImageDraw
from pathlib import Path
OUT=Path("graphics"); OUT.mkdir(exist_ok=True)
NAMES=["passengers","steel","armoured","oil","coal","livestock","grain","goods","iron_ore"]
COLORS=[(70,138,218),(119,130,145),(107,105,143),(205,73,58),(88,85,77),(190,158,85),(82,150,103),(145,107,75),(112,122,135)]
def wagon(name,index,view):
 im=Image.new("RGBA",(40,24));d=ImageDraw.Draw(im)
 base=COLORS[index]; dark=tuple(max(0,c-55) for c in base);light=tuple(min(255,c+60) for c in base)
 d.rounded_rectangle((2,15,37,19),radius=2,fill=(67,79,91),outline=(31,42,53))
 d.rectangle((5,19,35,20),fill=(32,50,61));d.line((5,20,35,20),fill=(69,212,239))
 d.polygon([(1,14),(4,12),(4,18),(1,17)],fill=(132,217,229))
 d.polygon([(38,14),(35,12),(35,18),(38,17)],fill=(132,217,229))
 if name=="passengers":
  d.rounded_rectangle((3,6,36,16),radius=3,fill=(224,231,236),outline=(59,83,104))
  d.rectangle((5,12,35,15),fill=base)
  for x in range(8,33,6):d.rectangle((x,8,x+4,11),fill=(44,109,157))
  d.line((17,8,17,15),fill=(68,77,86))
 elif name=="oil":
  d.rounded_rectangle((4,5,35,16),radius=5,fill=(203,213,220),outline=(68,77,86))
  d.line((6,8,33,8),fill=(255,255,255),width=2)
  d.rectangle((4,13,35,15),fill=base)
  for x in (12,28):d.line((x,5,x,16),fill=dark)
  d.rectangle((19,3,23,5),fill=(67,77,86))
 elif name in ("coal","iron_ore"):
  d.polygon([(4,8),(35,8),(33,17),(6,17)],fill=(136,151,165),outline=(52,65,79))
  d.rectangle((5,12,34,15),fill=base)
  for x in range(7,34,4):
   h=(x*7+index)%4
   d.ellipse((x,5+h,x+5,11+h),fill=(34,37,42) if name=="coal" else (119,91,73))
 elif name=="steel":
  d.rectangle((5,12,35,16),fill=base,outline=dark)
  for y in (7,9,11):d.rounded_rectangle((6,y,33,y+3),radius=1,fill=(145+y,155+y,170+y),outline=(69,78,87))
  for x in (10,30):d.line((x,6,x,15),fill=(224,147,43),width=2)
 elif name=="livestock":
  d.rounded_rectangle((4,5,35,16),radius=2,fill=(209,218,209),outline=dark)
  for y in (8,11,14):d.line((5,y,34,y),fill=base)
  for x in range(7,35,5):d.line((x,7,x,15),fill=(49,85,62))
 elif name=="grain":
  d.polygon([(4,7),(10,5),(30,5),(35,7),(33,17),(6,17)],fill=(224,205,160),outline=(101,96,79))
  for x in (12,20,28):d.line((x,5,x,16),fill=(153,135,91))
  d.rectangle((6,12,33,15),fill=base)
 elif name=="armoured":
  d.rounded_rectangle((4,5,35,17),radius=2,fill=base,outline=(35,43,57),width=2)
  for x in range(8,34,7):d.line((x,7,x,15),fill=light)
  d.rectangle((17,8,23,13),fill=(45,51,74),outline=(223,216,167))
 else:
  d.rounded_rectangle((4,5,35,17),radius=2,fill=base,outline=dark)
  for x in range(8,36,5):d.line((x,6,x,16),fill=dark)
  d.rectangle((5,6,34,7),fill=light)
 if view%2:d.line((5,18,35,18),fill=(135,169,186))
 return im
for i,name in enumerate(NAMES):
 sheet=Image.new("RGBA",(320,24))
 for view in range(8):sheet.paste(wagon(name,i,view),(view*40,0))
 sheet.save(OUT/(name+".png"))
print("Generated nine cargo-specific 32bpp sprite sheets")

# NML's bundled DOS palette provides valid 8bpp company-colour mask indices.
# 0 is transparent; 0xC6..0xCD are the primary company-colour ramp.
from nml.palette import raw_palette_data
for name in NAMES:
 mask=Image.new("P",(320,24),0)
 mask.putpalette(raw_palette_data[0])
 pen=ImageDraw.Draw(mask)
 for direction in range(8):
  x=direction*40
  if name=="passengers":
   pen.rectangle((x+5,12,x+35,14),fill=0xCA)
  elif name=="oil":
   pen.rectangle((x+5,13,x+34,15),fill=0xCA)
  elif name in ("coal","iron_ore","steel","grain"):
   pen.rectangle((x+6,13,x+33,15),fill=0xCA)
  elif name=="livestock":
   pen.rectangle((x+5,5,x+34,7),fill=0xCA)
  else:
   pen.rectangle((x+5,7,x+34,8),fill=0xCA)
 mask.save(OUT/(name+"_mask.png"))
print("Generated nine company-colour recolour masks")

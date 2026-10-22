"""Pixel-art Maglev wagons: eight perspective-correct views, company-colour masks."""
from pathlib import Path
from math import hypot
from PIL import Image, ImageDraw
from nml.palette import raw_palette_data

OUT = Path("graphics")
OUT.mkdir(exist_ok=True)
NAMES = ("passengers","steel","armoured","oil","coal","livestock","grain","goods","iron_ore")
BASE = {
 "passengers":(220,231,239), "steel":(118,132,147), "armoured":(112,117,145),
 "oil":(198,208,217), "coal":(113,130,146), "livestock":(189,206,195),
 "grain":(214,193,151), "goods":(175,145,117), "iron_ore":(121,135,150),
}
W,H=48,32
# Each view is a genuinely different 3D projection. 1/3/5/7 are diagonals.
AXES=((0,1),(-1,.48),(-1,0),(-1,-.48),(0,-1),(1,-.48),(1,0),(1,.48))
def shade(rgb,k):
 return tuple(min(255,max(0,int(v*k))) for v in rgb)+(255,)

def render(name,view):
 im=Image.new("RGBA",(W,H),(0,0,0,0))
 mask=Image.new("P",(W,H),0); mask.putpalette(raw_palette_data[0])
 d=ImageDraw.Draw(im); m=ImageDraw.Draw(mask)
 ax,ay=AXES[view]
 # Keep cardinal end-on views short; side-on and diagonal views long.
 length=6 if view in (0,4) else (16 if view in (2,6) else 16)
 breadth=5 if view in (0,4) else (4 if view in (2,6) else 4)
 cx,cy=24,21
 def p(a,b,z=0):
  return (round(cx+ax*a-ay*b),round(cy+ay*a+ax*b-z))
 def polygon(coords,fill,outline=None):
  pts=[p(*c) for c in coords];d.polygon(pts,fill=fill)
  if outline:d.line(pts+[pts[0]],fill=outline,width=1)
 def face(a,b,z1,z2):
  return [(a,-breadth,z1),(b,-breadth,z1),(b,-breadth,z2),(a,-breadth,z2)]
 dark=(42,54,68,255); metal=(85,103,118,255)
 # Low Maglev skirt and continuous underbody (no conventional wheels).
 polygon([(-length-1,-breadth-1,-1),(length+1,-breadth-1,-1),
          (length+1,breadth+1,-1),(-length-1,breadth+1,-1)],dark)
 polygon([(-length,-breadth,1),(length,-breadth,1),(length,breadth,1),(-length,breadth,1)],
         (77,94,109,255))
 # The body is a proper extruded prism, with visible end face and roof.
 polygon(face(-length,length,1,8),shade(BASE[name],.79),dark)
 polygon([(length,-breadth,1),(length,breadth,1),(length,breadth,8),(length,-breadth,8)],
         shade(BASE[name],.61),dark)
 polygon([(-length,-breadth,8),(length,-breadth,8),(length,breadth,8),(-length,breadth,8)],
         shade(BASE[name],1.13),dark)
 # Structural edge, and a narrow company-colour accent (mask is the recolour layer).
 d.line([p(-length+1,-breadth,3),p(length-1,-breadth,3)],fill=(128,128,128,255),width=2)
 m.line([p(-length+1,-breadth,3),p(length-1,-breadth,3)],fill=0xC8,width=2)
 d.line([p(-length+1,-breadth,8),p(length-1,-breadth,8)],fill=(234,243,247,255))
 # Rail-facing cyan guide lights at the two ends.
 for a in (-length,length):
  x,y=p(a,0,0);d.line([(x-2,y),(x+2,y)],fill=(42,201,231,255))
 if name=="passengers":
  # Individual dark-glass windows across the actual near side, not across the ground.
  for a in range(-length+3,length-2,5):
   polygon([(a,-breadth-.12,5),(a+3,-breadth-.12,5),
            (a+3,-breadth-.12,7),(a,-breadth-.12,7)],(35,104,152,255))
  d.line([p(0,-breadth,2),p(0,-breadth,7)],fill=(66,83,98,255))
 elif name=="oil":
  # Long silver tank with dark end caps, top inspection hatches.
  d.line([p(-length+3,0,10),p(length-3,0,10)],fill=(235,241,244,255),width=5)
  d.line([p(-length+3,0,11),p(length-3,0,11)],fill=(153,172,185,255),width=1)
  for a in (-length+5,length-5):
   d.line([p(a,-2,10),p(a,2,10)],fill=(77,93,105,255),width=1)
 elif name in ("coal","iron_ore"):
  # Open-top hopper with visible uneven material inside raised rim.
  ore=(32,37,43,255) if name=="coal" else (138,84,58,255)
  polygon([(-length+2,-breadth+1,9),(length-2,-breadth+1,9),
           (length-2,breadth-1,9),(-length+2,breadth-1,9)],ore)
  for a in range(-length+3,length-2,4):
   for b in (-2,1):
    x,y=p(a,b,10+(a+b)%2)
    d.ellipse((x-1,y-1,x+1,y+1),fill=shade(ore[:3],1.2))
  d.line([p(-length,-breadth,9),p(length,-breadth,9)],fill=(215,226,231,255))
 elif name=="steel":
  # Exposed parallel steel sections, secured with orange transverse straps.
  for b in (-2,0,2):
   d.line([p(-length+2,b,10),p(length-2,b,10)],fill=(185,199,212,255),width=2)
   d.line([p(-length+2,b,11),p(length-2,b,11)],fill=(96,113,128,255))
  for a in (-length+6,length-6):
   d.line([p(a,-breadth+1,12),p(a,breadth-1,12)],fill=(235,147,43,255),width=2)
 elif name=="grain":
  # Grain silo hatches on the rounded roof.
  for a in range(-length+5,length-2,7):
   x,y=p(a,0,10)
   d.ellipse((x-3,y-2,x+3,y+1),fill=(237,219,173,255),outline=(129,112,79,255))
 elif name=="livestock":
  # Ventilated slatted walls.
  for a in range(-length+3,length-1,4):
   d.line([p(a,-breadth-.2,5),p(a,-breadth-.2,7)],fill=(44,91,71,255))
  d.line([p(-length+2,-breadth,6),p(length-2,-breadth,6)],fill=(70,112,88,255))
 elif name=="armoured":
  # Reinforced container and small secure hatch.
  for a in range(-length+5,length-2,7):
   d.line([p(a,-breadth-.2,2),p(a,-breadth-.2,8)],fill=(65,70,93,255))
  polygon([(-2,-breadth-.2,5),(2,-breadth-.2,5),(2,-breadth-.2,7),(-2,-breadth-.2,7)],
          (57,64,85,255),(194,188,147,255))
 elif name=="goods":
  # Ribbed container wall.
  for a in range(-length+3,length-2,4):
   d.line([p(a,-breadth-.2,4),p(a,-breadth-.2,8)],fill=(110,78,56,255))
 return im,mask

for name in NAMES:
 sheet=Image.new("RGBA",(W*8,H),(0,0,0,0))
 masks=Image.new("P",(W*8,H),0); masks.putpalette(raw_palette_data[0])
 for view in range(8):
  sprite,recolour=render(name,view)
  sheet.paste(sprite,(view*W,0))
  masks.paste(recolour,(view*W,0))
 sheet.save(OUT/(name+".png"))
 masks.save(OUT/(name+"_mask.png"))
print("Generated nine eight-view Maglev wagons, 48x32px per sprite, with recolour masks")

# Goods wagon proof-of-concept: hand-authored pixel geometry with
# OpenTTD-like 8-view silhouettes (end, diagonal, side, diagonal, ...).
def render_goods_prototype(view):
 im=Image.new("RGBA",(W,H),(0,0,0,0))
 mask=Image.new("P",(W,H),0);mask.putpalette(raw_palette_data[0])
 d=ImageDraw.Draw(im);m=ImageDraw.Draw(mask)
 outline=(49,57,67,255);roof=(168,132,93,255)
 side=(136,94,61,255);end=(105,75,57,255)
 light=(202,164,120,255);skirt=(59,75,88,255)
 # A conventional OpenTTD vehicle is low and ~28 px long in side views.
 # Diagonals are sloped parallelograms, NOT upright platforms.
 if view in (0,4):
  # End views are narrow, upright silhouettes, with a sloping roof.
  d.polygon([(20,13),(24,11),(28,13),(28,24),(20,24)],fill=side)
  d.line([(20,13),(24,11),(28,13)],fill=light,width=1)
  d.rectangle((19,23,29,25),fill=skirt)
  d.line([(21,18),(27,18)],fill=outline)
  d.line([(21,21),(27,21)],fill=outline)
  m.line([(20,22),(28,22)],fill=0xC8,width=1)
 elif view in (2,6):
  # Long near-horizontal profile with 2px roof, 8px cargo body.
  d.polygon([(9,14),(12,12),(37,12),(40,14),(40,23),(9,23)],fill=side,outline=outline)
  d.polygon([(12,12),(37,12),(40,14),(9,14)],fill=roof)
  d.line([(11,15),(38,15)],fill=light)
  for x in range(14,39,5):
   d.line([(x,16),(x,21)],fill=end)
  d.rectangle((9,23,40,25),fill=skirt)
  d.line([(12,25),(38,25)],fill=(51,189,211,255))
  m.line([(11,22),(38,22)],fill=0xC8,width=1)
 else:
  # True 2:1 isometric diagonals: 28px along x, 14px along y.
  # Keep the wagon body below 12px high and aligned with the rail.
  falling=view in (1,5)
  if falling:
   roofpoly=[(9,13),(32,23),(38,20),(15,10)]
   near=[(9,13),(32,23),(32,28),(9,18)]
   far=[(32,23),(38,20),(38,25),(32,28)]
   rail=[(8,20),(32,30),(39,27)]
   accents=[(11,18),(32,27)]
  else:
   roofpoly=[(9,23),(32,12),(38,15),(15,26)]
   near=[(9,23),(32,12),(32,18),(9,29)]
   far=[(32,12),(38,15),(38,21),(32,18)]
   rail=[(8,30),(32,19),(39,23)]
   accents=[(11,28),(32,17)]
  d.polygon(near,fill=side)
  d.polygon(far,fill=end)
  d.polygon(roofpoly,fill=roof)
  d.line(roofpoly+[roofpoly[0]],fill=outline,width=1)
  d.line(rail,fill=skirt,width=2)
  d.line(accents,fill=light,width=1)
  m.line(accents,fill=0xC8,width=1)
 return im,mask

# Overwrite only Goods: leave the other eight existing sprite sets unchanged
# until this prototype is approved visually in-game.
goods_sheet=Image.new("RGBA",(W*8,H),(0,0,0,0))
goods_mask=Image.new("P",(W*8,H),0);goods_mask.putpalette(raw_palette_data[0])
for view in range(8):
 sprite,recolour=render_goods_prototype(view)
 goods_sheet.paste(sprite,(view*W,0))
 goods_mask.paste(recolour,(view*W,0))
goods_sheet.save(OUT/"goods.png")
goods_mask.save(OUT/"goods_mask.png")
print("Goods proof-of-concept sprite sheet generated")

# Goods prototype: source-aligned OpenGFX goods wagon artwork.
# OpenGFX is GPL-2.0; keep attribution and license when redistributing.
# Original sprites: sprites/png/trains/temperatemonolev.png,
# tmpl_train_4view_88length_28px(0,220), x=(0,16,48,96).
from urllib.request import urlopen
from io import BytesIO
URL="https://raw.githubusercontent.com/OpenTTD/OpenGFX/master/sprites/png/trains/temperatemonolev.png"
original=Image.open(BytesIO(urlopen(URL,timeout=30).read()))
print("OpenGFX reference:",original.mode,original.size)
if original.mode!="P":
 raise RuntimeError("Expected indexed OpenGFX source artwork")
# The 8bpp palette carries OpenTTD's native company-colour ramps.
# Do not convert to RGBA, which would bake the recolour indices.
views=[(0,220,8,18,-3,-12),(16,220,20,16,-13,-9),
       (48,220,28,12,-15,-8),(96,220,20,16,-5,-9)]
sheet=Image.new("P",(8*32,20),0)
sheet.putpalette(original.getpalette())
for i in range(8):
 x,y,w,h,ox,oy=views[i%4]
 sprite=original.crop((x,y,x+w,y+h))
 sheet.paste(sprite,(i*32,0))
sheet.save(OUT/"goods_opengfx_reference.png")
print("Saved OpenGFX-aligned Goods reference sprites (8bpp)")

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

from PIL import Image, ImageDraw
from pathlib import Path
from math import sqrt
from nml.palette import raw_palette_data

OUT=Path("graphics")
OUT.mkdir(exist_ok=True)
NAMES=["passengers","steel","armoured","oil","coal","livestock","grain","goods","iron_ore"]
BASE={"passengers":(205,217,229),"steel":(113,127,143),"armoured":(106,111,138),"oil":(186,198,209),"coal":(106,122,137),"livestock":(172,190,178),"grain":(199,181,135),"goods":(163,137,111),"iron_ore":(118,132,144)}
# OpenTTD sprite order: short end, diagonal, long side, diagonal, opposite end, diagonal, opposite long side, diagonal.
VECTORS=[(0,1),(-1,0.47),(-1,0),(-1,-0.47),(0,-1),(1,-0.47),(1,0),(1,0.47)]
W,H=64,40
def tint(c,n):
 return tuple(max(0,min(255,int(v*n))) for v in c)
def draw_one(name,direction):
 im=Image.new("RGBA",(W,H),(0,0,0,0))
 mask=Image.new("P",(W,H),0)
 mask.putpalette(raw_palette_data[0])
 d=ImageDraw.Draw(im);m=ImageDraw.Draw(mask)
 ux,uy=VECTORS[direction]
 mag=sqrt(ux*ux+uy*uy);ux/=mag;uy/=mag
 # Screen-space width axis. End-on sprites remain short and narrow.
 vx,vy=-uy,ux
 half=22 if direction in (2,6) else (18 if direction%2 else 7)
 width=5 if direction in (0,4) else 6
 cx,cy=32,23
 def pt(along,across,z=0):
  return (round(cx+ux*along+vx*across),round(cy+uy*along+vy*across-z))
 def quad(a,b,w,z=0):
  return [pt(a,-w,z),pt(b,-w,z),pt(b,w,z),pt(a,w,z)]
 base=BASE[name]
 # Maglev running gear, dark low profile with cyan levitation rail
 d.polygon(quad(-half-1,half+1,width+1,-2),fill=(43,54,65,255))
 d.line([pt(-half,0,-3),pt(half,0,-3)],fill=(58,202,229,255),width=2)
 # Solid side and roof polygons: correct orientation per sprite
 d.polygon(quad(-half,half,width,2),fill=tint(base,.73)+(255,))
 d.polygon(quad(-half,half,width,8),fill=tint(base,1.12)+(255,))
 d.line([pt(-half,-width,8),pt(half,-width,8)],fill=(239,246,247,255),width=1)
 for end in (-half,half):
  d.line([pt(end,-width,2),pt(end,-width,8),pt(end,width,8),pt(end,width,2)],fill=(55,70,83,255),width=1)
 # Recolourable stripe on side: NML palette index 0xC8 in mask, transparent elsewhere.
 stripe=[pt(-half+2,-width-.1,4),pt(half-2,-width-.1,4)]
 d.line(stripe,fill=(135,135,135,255),width=2)
 m.line(stripe,fill=0xC8,width=2)
 if name=="passengers":
  for i in range(-half+4,half-2,6):
   d.polygon([pt(i,-width-.2,5),pt(i+4,-width-.2,5),pt(i+4,-width-.2,7),pt(i,-width-.2,7)],fill=(35,101,152,255))
 elif name=="oil":
  d.line([pt(-half+3,0,9),pt(half-3,0,9)],fill=(243,248,250,255),width=5)
  for i in range(-half+6,half-3,9):
   d.line([pt(i,-width+1,8),pt(i,width-1,8)],fill=(76,86,94,255),width=1)
 elif name in ("coal","iron_ore"):
  d.polygon(quad(-half+2,half-2,width-1,9),fill=(45,45,48,255) if name=="coal" else (133,91,66,255))
  for i in range(-half+3,half-2,5):
   d.ellipse((pt(i,0,10)[0]-2,pt(i,0,10)[1]-1,pt(i,0,10)[0]+2,pt(i,0,10)[1]+1),fill=(22,26,29,255) if name=="coal" else (169,108,70,255))
 elif name=="steel":
  for a in (-2,0,2):
   d.line([pt(-half+3,a,10),pt(half-3,a,10)],fill=(190,201,213,255),width=2)
  for i in (-half+7,half-7):
   d.line([pt(i,-width,11),pt(i,width,11)],fill=(226,146,46,255),width=2)
 elif name=="livestock":
  for i in range(-half+4,half-2,5):
   d.line([pt(i,-width-.1,5),pt(i,-width-.1,7)],fill=(42,75,59,255),width=1)
 elif name=="grain":
  for i in range(-half+6,half-2,8):
   d.line([pt(i,-width+1,9),pt(i,width-1,9)],fill=(134,116,79,255),width=1)
 elif name=="armoured":
  for i in range(-half+5,half-2,8):
   d.line([pt(i,-width-.1,3),pt(i,-width-.1,8)],fill=(59,61,85,255),width=1)
 elif name=="goods":
  for i in range(-half+4,half-2,4):
   d.line([pt(i,-width-.1,3),pt(i,-width-.1,8)],fill=(103,76,56,255),width=1)
 return im,mask

for name in NAMES:
 sheet=Image.new("RGBA",(W*8,H),(0,0,0,0))
 masks=Image.new("P",(W*8,H),0);masks.putpalette(raw_palette_data[0])
 for direction in range(8):
  sprite,mask=draw_one(name,direction)
  sheet.paste(sprite,(direction*W,0))
  masks.paste(mask,(direction*W,0))
 sheet.save(OUT/(name+".png"))
 masks.save(OUT/(name+"_mask.png"))
print("Generated eight-direction isometric wagon sprites and recolour masks for nine cargo types.")

"""Generate original placeholder sprite sheets for the nine Maglev wagons."""
import os, struct, zlib
names = ["passengers","steel","armoured","oil","coal","livestock","grain","goods","iron_ore"]
os.makedirs("graphics", exist_ok=True)
def png(path, pixels, width, height):
    raw=b"".join(b"\x00"+bytes(sum((list(rgb) for rgb in row),[])) for row in pixels)
    def chunk(kind,data):
        return struct.pack(">I",len(data))+kind+data+struct.pack(">I",zlib.crc32(kind+data)&0xffffffff)
    data=b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",width,height,8,2,0,0,0))+chunk(b"IDAT",zlib.compress(raw))+chunk(b"IEND",b"")
    with open(path,"wb") as f:f.write(data)
for index,name in enumerate(names):
    width,height=320,24
    pixels=[]
    base=(40+index*13%130,85+index*17%120,130+index*19%110)
    for y in range(height):
        row=[]
        for x in range(width):
            xx=x%40
            body=(4<=xx<=35 and 7<=y<=17)
            window=(7<=xx<=32 and 9<=y<=11 and name=="passengers")
            wheel=(xx in range(9,14) or xx in range(26,31)) and y in (18,19)
            rgb=(0,0,255) if not (body or wheel) else ((40,40,40) if wheel else ((205,220,235) if window else base))
            row.append(rgb)
        pixels.append(row)
    png("graphics/"+name+".png",pixels,width,height)

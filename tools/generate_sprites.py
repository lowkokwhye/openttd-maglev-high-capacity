"""Build native OpenGFX 8bpp wagon sprite sheets with original geometry.

Source: OpenTTD/OpenGFX sprites/png/trains/temperatemonolev.png
License: GPL-2.0 (OpenGFX contributors).
Uses original four directional views repeated for reverse-facing directions,
matching the Goods reference approved in-game.
"""
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from PIL import Image

OUT = Path("graphics")
OUT.mkdir(exist_ok=True)
SOURCE = ("https://raw.githubusercontent.com/OpenTTD/OpenGFX/master/"
          "sprites/png/trains/temperatemonolev.png")
original = Image.open(BytesIO(urlopen(SOURCE, timeout=45).read()))
if original.mode != "P":
    raise RuntimeError("Expected original indexed 8bpp OpenGFX sprites")

# OpenGFX base-2733-rail-vehicles-wagons.pnml:
# monorail rows correspond to passenger, mail, valuables, coal,
# oil, livestock, goods, grain, steel and iron ore.
# Mail serves as the closest original enclosed carriage for passengers
# only where needed; passengers use the actual passenger row.
ROWS = {
    "passengers": 0,
    "steel": 320,
    "armoured": 80,
    "oil": 140,
    "coal": 120,
    "livestock": 180,
    "grain": 260,
    "goods": 220,
    "iron_ore": 380,
}
# Native 28px OpenGFX sprite geometry. See tmpl_trains.nml.
VIEWS = ((0, 8, 18), (16, 20, 16), (48, 28, 12), (96, 20, 16))
for name, y in ROWS.items():
    if y + 18 > original.height:
        raise ValueError(f"Sprite row for {name} is outside source image")
    sheet = Image.new("P", (8 * 32, 20), 0)
    sheet.putpalette(original.getpalette())
    for view in range(8):
        x, w, h = VIEWS[view % 4]
        sprite = original.crop((x, y, x+w, y+h))
        sheet.paste(sprite, (view * 32, 0))
    sheet.save(OUT / f"{name}_opengfx.png")
    print(f"{name}: original OpenGFX 8bpp artwork, row {y}")

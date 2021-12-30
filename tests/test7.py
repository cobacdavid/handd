import cairo
from handd import HDD
import sys
import math
import colorsys


HDD.debug = not True

H = 2_400
W = 1_080

img = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = HDD(img)

ctx.set_source_rgb(0, 0, 0)
ctx.rectangle(0, 0, W, H)
ctx.fill()

HDD.deviation = 10

offset = 100
ctx.set_line_width(9)
ctx.translate(W / 2, H / 2)
for i in range(7):
    couleur_hsv = (200 / 360, 1 - 1 / 1.3 ** i, 1)
    couleur = colorsys.hsv_to_rgb(*couleur_hsv)
    ctx.set_source_rgb(*couleur)
    p, bb = ctx.rectangle_hdd(-W / 2 + offset, - H / 2 + offset,
                               W - 2 * offset, H - 2 * offset)
    ctx.hatch_hdd(p, bb, angle=-math.pi / 5, nb=10 + 10 * i)
    ctx.stroke()
    ctx.rotate(.25)
    ctx.scale(0.65, 0.65)

img.write_to_png(f"{sys.argv[0].split('.')[0]}.png")

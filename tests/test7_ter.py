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
info_rect = []
for i in range(2):
    ctx.save()
    ctx.translate(W / 2, H / 2)
    ctx.rotate(.25 * i)
    ctx.scale(0.65 ** i, 0.65 ** i)
    couleur_hsv = (200 / 360, 1 - 1 / 1.3 ** i, 1)
    couleur = colorsys.hsv_to_rgb(*couleur_hsv)
    ctx.set_source_rgb(*couleur)
    p, bb = ctx.rectangle_hdd(-W / 2 + offset, - H / 2 + offset,
                               W - 2 * offset, H - 2 * offset)
    M = ctx.get_matrix()
    new_p = []
    new_bb = []
    for xy in p:
        new_p.append(M.transform_point(*xy))
    for xy in bb:
        new_bb.append(M.transform_point(*xy))
    info_rect.append((new_p, new_bb))
    # ctx.hatch_hdd(p, bb, angle=-math.pi / 5, nb=10 + 10 * i)
    ctx.stroke()
    ctx.restore()

ctx.translate(W / 2, H / 2)
for i in range(len(info_rect)):
    print(info_rect[i][0])
    if i != len(info_rect) - 1:
        condition = lambda x, y: not HDD.is_in(x, y, info_rect[i][0])
    else:
        condition = lambda x, y: True
    ctx.set_source_rgb(1, 0, 0)
    ctx.hatch_hdd(p, bb,
                  angle=-math.pi / 5,
                  n=10 + 10 * i,
                  condition=condition)
    ctx.stroke()


img.write_to_png(f"{sys.argv[0].split('.')[0]}.png")

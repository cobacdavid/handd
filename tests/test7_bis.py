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

M = cairo.Matrix.init_rotate(.25)
M.scale(.65, .65)


def trace_rectangle(i):
    if i == 0:
        condition = lambda x, y: True
    else:
        pi = trace_rectangle(i - 1)
        condition = lambda x, y: not HDD.is_in(x, y, pi)
    #
    ctx.save()
    if i == 0:
        new_M = cairo.Matrix()
    else:
        new_M = M
    for _ in range(i - 1):
        new_M = new_M.multiply(M)
    ctx.transform(new_M)
    couleur_hsv = (200 / 360, 1 - 1 / 1.3 ** i, 1)
    couleur = colorsys.hsv_to_rgb(*couleur_hsv)
    ctx.set_source_rgb(*couleur)
    p, bb = ctx.rectangle_hdd(-W / 2 + offset, - H / 2 + offset,
                               W - 2 * offset, H - 2 * offset)
    ctx.hatch_hdd(p, bb,
                  angle=-math.pi / 5,
                  nb=10 + 10 * i,
                  condition=condition)
    ctx.stroke()
    ctx.restore()
    new_p = []
    for xy in p:
        new_p.append(new_M.transform_point(xy[0], xy[1]))
    return new_p



HDD.deviation = 10

offset = 100
ctx.set_line_width(9)
ctx.translate(W / 2, H / 2)
trace_rectangle(2)
    
img.write_to_png(f"{sys.argv[0].split('.')[0]}.png")

import cairo
from handd import HDD
import sys
import math

HDD.debug = not True

H = 2_400
W = 1_080

img = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = HDD(img)

ctx.set_source_rgb(0, 0, 0)
ctx.rectangle(0, 0, W, H)
ctx.fill()

ctx.set_source_rgb(1, 0, 0)
ctx.set_line_width(5)
ctx.translate(W / 2, H / 2)
ctx.rotate(.3)
p, bb = ctx.rectangle_hdd([(-W / 7, - H / 6), (W / 7, H / 6)])
ctx.hatch_hdd(p, bb, angle=-math.pi / 5, nb=50)

img.write_to_png(f"{sys.argv[0].split('.')[0]}.png")

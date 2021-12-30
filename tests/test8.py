import cairo
from handd import HDD
import math


img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
ctx = HDD(img)


ctx.set_source_rgb(0, 0, 0)
ctx.rectangle(0, 0, 500, 500)
ctx.fill()

HDD.deviation = 0
ctx.set_source_rgb(1, 0, 0)
pc, bbc = ctx.rectangle_hdd(130, 130, 240, 240)
p, bb = ctx.circle_hdd(315, 315, 100)
ctx.set_source_rgba(0, 0, 1)
HDD.debug = not True
ctx.hatch_hdd(p, bb,
              angle=math.radians(1),
              nb=10,
              condition=lambda x, y: not HDD.is_in_polygon(x, y, pc))

img.write_to_png("test8.png")

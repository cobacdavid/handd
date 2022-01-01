import cairo
from handd import HDD
import math

img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 800)
ctx = HDD(img)


ctx.set_source_rgb(1, 1, 1)
ctx.rectangle(0, 0, 800, 800)
ctx.fill()

# HDD.deviation = 0
ctx.set_source_rgb(0, 0.8, 1)
ctx.set_line_width(10)
p, bb = ctx.circle_hdd(400, 400, 350, step=.008, dev=10)
ctx.stroke()
ctx.set_source_rgba(1, 0, 0, .9)
q, cc = ctx.regular_polygon_hdd(400, 400, 350, 3, - math.pi / 2)
ctx.set_source_rgba(238 / 255, 130 / 255, 238 / 255, .9)
r, dd = ctx.sector_hdd(400, 575, 303, -math.pi, 0)

ctx.set_source_rgba(238 / 255, 130 / 255, 238 / 255, .9)
ctx.hatch_hdd(q, cc,
              angle=math.radians(115),
              n=30,
              condition=lambda x, y: not HDD.is_in(x, y, r))
ctx.hatch_hdd(r, dd,
              angle=math.radians(115),
              n=35,
              condition=lambda x, y: not HDD.is_in(x, y, q))

img.write_to_png("catriona38.png")

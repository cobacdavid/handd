import cairo
from handd import HDD
import math

img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 800)
ctx = HDD(img)


ctx.set_source_rgb(1, 1, 1)
ctx.rectangle(0, 0, 800, 800)
ctx.fill()


ctx.set_source_rgba(0, 0, 0, 0)
ctx.set_line_width(10)
p, bb = ctx.regular_polygon_hdd(470, 530, 270, 6)
ctx.stroke()
q, cc = ctx.circle_hdd(*p[-3], 270)
ctx.stroke()
r, dd = ctx.circle_hdd(*p[-3], 180)
ctx.stroke()
s, ee = ctx.circle_hdd(*p[-3], 90)
ctx.stroke()

ctx.set_source_rgba(0, 172 / 255, 32 / 255, .9)
ctx.hatch_hdd(q, cc,
              angle=0,
              n=60,
              condition=lambda x, y: not HDD.is_in(x, y, p)
              and not HDD.is_in(x, y, r))
ctx.hatch_hdd(r, dd,
              angle=0,
              n=40,
              condition=lambda x, y: HDD.is_in(x, y, p)
              and not HDD.is_in(x, y, s))
ctx.hatch_hdd(s, ee,
              angle=0,
              n=20,
              condition=lambda x, y: not HDD.is_in(x, y, p))
ctx.stroke()

ctx.set_source_rgba(11 / 255, 168 / 255, 133 / 255, .85)
ctx.circle_hdd(*p[-3], 270)
ctx.stroke()
ctx.circle_hdd(*p[-3], 180)
ctx.stroke()
ctx.circle_hdd(*p[-3], 90)
ctx.stroke()

ctx.set_source_rgba(0, 0, 0, .9)
ctx.set_line_width(10)
ctx.regular_polygon_hdd(470, 530, 270, 6)
ctx.stroke()

img.write_to_png("catriona57.png")

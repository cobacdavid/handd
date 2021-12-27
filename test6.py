import cairo
from handd import HDD

W = H = 800

img = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
calque = HDD(img)
ctx = calque.ctx

ctx.set_source_rgb(0, 0, 0)
ctx.rectangle(0, 0, W, H)
ctx.fill()

ctx.set_source_rgba(1, 1, 0, .95)
ctx.set_line_width(10)
p, bb = calque.sector_hdd((350, 400), 300, 45, 315)
calque.hatch_hdd(p, bb, nb=50)
ctx.stroke()

ctx.set_source_rgba(0, 0, 0, 0)
p, bb = calque.circle_hdd((400, 250), 40)
ctx.set_source_rgb(0, 0, 0)
calque.hatch_hdd(p, bb, angle=20, nb=7)
ctx.stroke()

pilules = {"rouge": [(1, 0, 0), (550, 400)],
           "bleue": [(0, 0, 1), (730, 400)]}

for pill in pilules:
    ctx.set_source_rgb(0, 0, 0)
    p, bb = calque.circle_hdd(pilules[pill][1], 70)
    ctx.set_source_rgba(*pilules[pill][0], .90)
    ctx.set_line_width(5)
    calque.hatch_hdd(p, bb, angle=-30, nb=20)
    calque.hatch_hdd(p, bb, angle=-50, nb=20)
    ctx.stroke()

img.write_to_png("test6.png")

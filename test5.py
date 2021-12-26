from handd import HDD
import math
import cairo


class Rectangle:
    def __init__(self, xy, calque):
        self.xy = xy
        self.calque = calque

    def affiche(self, gris=0, width=0):
        self.calque.ctx.set_line_width(width)
        self.calque.ctx.set_source_rgb(gris, gris, gris)
        p = self.calque.rectangle_hdd(self.xy)
        self.calque.ctx.stroke()
        return p


offset = 60
W = 800 - offset
H = 800 - offset

img = cairo.ImageSurface(cairo.FORMAT_ARGB32, W + offset, H + offset)
calque = HDD(img)
ctx = calque.ctx
ctx.set_line_cap(cairo.LINE_CAP_ROUND)

# fond blanc
ctx.set_source_rgb(1, 1, 1)
ctx.rectangle(0, 0, W + offset, H + offset)
ctx.fill()

ctx.save()
ctx.translate((W + offset) / 2, (H + offset) / 2)
ctx.set_line_width(3)
N = 6
for _ in range(N):
    angle = math.tau / N
    ctx.rotate(angle)
    rectangle = Rectangle([(0, 0), (200, 200)], calque)
    ctx.set_source_rgb(0, 0, 0)
    p, bb = rectangle.affiche(width=10)
    ctx.stroke()
    ctx.set_source_rgba(0, 0, 1, .5)
    calque.hatch_hdd(p, bb, nb=30)
    ctx.stroke()
ctx.restore()

img.write_to_png("test5.png")

import cairo
from handd import HDD
import math


class Rectangle:
    def __init__(self, x, y, w, h, calque):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.calque = calque

    def affiche(self, gris=0, width=0):
        self.calque.set_line_width(width)
        self.calque.set_source_rgb(gris, gris, gris)
        p = self.calque.rectangle_hdd(self.x, self.y, self.w, self.h)
        self.calque.stroke()
        return p


offset = 60
W = 800 - offset
H = 800 - offset

img = cairo.ImageSurface(cairo.FORMAT_ARGB32, W + offset, H + offset)
ctx = HDD(img)

# fond blanc
ctx.set_source_rgb(1, 1, 1)
ctx.rectangle(0, 0, W + offset, H + offset)
ctx.fill()

M = cairo.Matrix()
ctx.save()
M.translate((W + offset) / 2, (H + offset) / 2)
N = 6
infos = []
for _ in range(N):
    angle = math.tau / N
    M.rotate(angle)
    ctx.set_matrix(M)
    rectangle = Rectangle(0, 0, 280, 280, ctx)
    ctx.set_source_rgb(0, 0, 0)
    p, bb = rectangle.affiche(width=10)
    new_p = []
    new_bb = []
    for xy in p:
        new_p.append(M.transform_point(*xy))
    infos.append((new_p, HDD._bbox(new_p)))
    ctx.stroke()
ctx.restore()

ctx.set_source_rgba(0, 0, 1, .5)
ctx.set_line_width(15)
N = len(infos)

ctx.set_dash([5, 30])
for i, (p, bb) in enumerate(infos):
    ctx.hatch_hdd(p, bb,
                  n=20,
                  condition=lambda x, y:
                  not HDD.is_in(x, y, infos[(i - 1) % N][0]) and
                  not HDD.is_in(x, y, infos[(i + 1) % N][0]))


img.write_to_png("test5.png")

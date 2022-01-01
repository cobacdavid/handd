import cairo
from handd import HDD
from opensimplex import OpenSimplex
import math

HDD.debug = not True
HDD.debug_color = (.25, 0.25, 0.25)
HDD.deviation = 0

class Rectangle:
    def __init__(self, x, y, w, h, calque):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.calque = calque

    def affiche(self, gris=1, width=0):
        self.calque.set_line_width(width)
        self.calque.set_source_rgb(gris, gris, gris)
        p = self.calque.rectangle_hdd(self.x, self.y, self.w, self.h)
        self.calque.stroke()
        return p


offset = 0
H = 2_400 - offset
W = 1_080 - offset

img = cairo.ImageSurface(cairo.FORMAT_RGB24, W + offset, H + offset)
ctx = HDD(img)


# les rectangles:
dimw = W // 5
dimh = H // 5
ratio = dimw / dimh
rectangles = []
for l in range(H // dimh + 2):
    for c in range(W // dimw + 2):
        A = (offset / 2 + c * dimw, offset / 2 + l * dimh)
        rectangles.append(Rectangle(A[0], A[1], dimw, dimh, ctx))

info_rectangles = []
for c in rectangles:
    info_rectangles.append((c, c.affiche()))

noise = OpenSimplex()
for i, pack_r in enumerate(info_rectangles):
    r, (p, bb) = pack_r
    n = noise.noise2d(r.x, r.y)
    angle = n * math.pi / 2
    nb = max(3, int((n + 1) * 30))
    width = 1 + int(10 * (150 - (nb - 3)) / 150)
    ctx.set_line_width(width)
    ctx.set_source_rgb(1, 1, 1)
    ctx.hatch_hdd(p, bb, angle=angle, n=nb)
    ctx.stroke()

for c in rectangles:
    c.affiche(width=4, gris=0)

img.write_to_png("test4.png")

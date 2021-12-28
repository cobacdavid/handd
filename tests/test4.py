import cairo
from handd import HDD
from opensimplex import OpenSimplex
import math

HDD.debug = True
HDD.debug_color = (.25, 0.25, 0.25)

class Rectangle:
    def __init__(self, xy, calque):
        self.xy = xy
        self.calque = calque

    def affiche(self, gris=1, width=0):
        self.calque.set_line_width(width)
        self.calque.set_source_rgb(gris, gris, gris)
        p = self.calque.rectangle_hdd(self.xy)
        self.calque.stroke()
        return p


offset = 20
H = 2_400 - offset
W = 1_080 - offset

img = cairo.ImageSurface(cairo.FORMAT_RGB24, W + offset, H + offset)
ctx = HDD(img)


# les rectangles:
dimw = W // 5
dimh = H // 5
ratio = dimw / dimh
rectangles = []
for l in range(H // dimh):
    for c in range(W // dimw):
        A = (offset / 2 + c * dimw, offset / 2 + l * dimh)
        B = (offset / 2 + (c + 1) * dimw, offset / 2 + (l + 1) * dimh)
        rectangles.append(Rectangle([A, B], ctx))

info_rectangles = []
for c in rectangles:
    info_rectangles.append((c, c.affiche()))

noise = OpenSimplex()
for i, pack_r in enumerate(info_rectangles):
    r, (p, bb) = pack_r
    n = noise.noise2d(r.xy[0][0], r.xy[0][1])
    angle = n * math.pi / 2
    nb = max(3, int((n + 1) * 8))
    width = 1 + int(10 * (150 - (nb - 3)) / 150)
    ctx.set_line_width(width)
    ctx.set_source_rgb(1, 1, 1)
    ctx.hatch_hdd(p, bb, angle=angle, nb=nb)
    ctx.stroke()

for c in rectangles:
    c.affiche(width=4, gris=0)

img.write_to_png("test4.png")

from handd import HDD
from opensimplex import OpenSimplex
import cairo


class Rectangle:
    def __init__(self, xy, calque):
        self.xy = xy
        self.calque = calque

    def affiche(self, gris=1, width=0):
        self.calque.ctx.set_line_width(width)
        self.calque.ctx.set_source_rgb(gris, gris, gris)
        p = self.calque.rectangle_hdd(self.xy)
        self.calque.ctx.stroke()
        return p


offset = 100
W = 1_080 - offset
H = 1_920 - offset

img = cairo.ImageSurface(cairo.FORMAT_RGB24, W + offset, H + offset)
calque = HDD(img)
ctx = calque.ctx


# les rectangles:
dimw = W // 5
dimh = H // 5
ratio = dimw / dimh
rectangles = []
for l in range(H // dimh):
    for c in range(W // dimw):
        A = (offset / 2 + c * dimw, offset / 2 + l * dimh)
        B = (offset / 2 + (c + 1) * dimw, offset / 2 + (l + 1) * dimh)
        rectangles.append(Rectangle([A, B], calque))

info_rectangles = []
for c in rectangles:
    info_rectangles.append((c, c.affiche()))

noise = OpenSimplex()
for i, pack_r in enumerate(info_rectangles):
    r, (p, bb) = pack_r
    n = noise.noise2d(r.xy[0][0], r.xy[0][1])
    angle = int(n * 90) / 2
    nb = max(3, int((n + 1) * 50))
    width = 1 + int(10 * (150 - (nb - 3)) / 150)
    ctx.set_line_width(width)
    ctx.set_source_rgb(1, 1, 1)
    calque.hatch_hdd(p, bb, angle=angle, nb=nb)
    ctx.stroke()

for c in rectangles:
    c.affiche(width=4, gris=0)

img.write_to_png("test4.png")

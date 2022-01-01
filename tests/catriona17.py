from handd import HDD
import cairo
import math

W = H = 800

img = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = HDD(img)

ctx.set_source_rgb(1, 1, 1)
ctx.rectangle(0, 0, W, H)
ctx.fill()

color = (219, 112, 147)
normalized_color = [c / 255 for c in color]

ctx.set_line_width(9)
ctx.set_source_rgb(*normalized_color)
poly, bb = ctx.regular_polygon_hdd(W / 2, H / 2, 300, 8, -math.tau / 16)
points = poly[1:3] + poly[6:8][::-1]
poly, bb = ctx.lpolygon_hdd(points)
ctx.stroke()
ctx.set_line_width(15)
ctx.set_source_rgba(*normalized_color, .8)
ctx.hatch_hdd(poly, bb, nb=50, angle=90)
ctx.stroke()
img.write_to_png("catriona17.png")

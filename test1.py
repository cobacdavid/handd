import cairo
from handd import HDD
import math


img = cairo.ImageSurface(cairo.FORMAT_RGB24, 800, 800)
calque = HDD(img)
ctx = calque.ctx

ctx.set_source_rgb(1, 0, 0)
poly, bb_poly = calque.regular_polygon_hdd((100, 100, 50), 4)
ctx.stroke()
ctx.set_source_rgb(0, 0, 1)
ctx.set_line_width(3)
calque.hatch_hdd(poly, bb_poly, angle=30, nb=10)
ctx.stroke()

ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1)
poly, bb_poly = calque.polygon_hdd([(700, 100), (400, 400),
                                   (600, 300), (650, 500)])
ctx.stroke()
ctx.set_source_rgb(1, 0, 0)
ctx.set_line_width(2)
calque.dot_hdd(poly, bb_poly, sep=15)
ctx.stroke()


ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1)
calque.axes_hdd((400, 700), units=(100, 100))
ctx.stroke()
ctx.set_source_rgb(1, 0, 0)
ctx.set_line_width(3)
calque.function_hdd(lambda x: math.sin(x),
                   -2 * math.pi, 2 * math.pi,
                   nb=100)
ctx.stroke()

img.write_to_png("test1.png")

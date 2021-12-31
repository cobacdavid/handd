import cairo
from handd import HDD
import math


img = cairo.ImageSurface(cairo.FORMAT_RGB24, 800, 800)
ctx = HDD(img)

ctx.set_source_rgb(1, 0, 0)
poly, bb_poly = ctx.regular_polygon_hdd(100, 100, 50, 4)
ctx.stroke()
ctx.set_source_rgb(0, 0, 1)
ctx.set_line_width(3)
ctx.hatch_hdd(poly, bb_poly, angle=math.pi / 6, nb=10)
ctx.stroke()

ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1)
poly, bb_poly = ctx.lpolygon_hdd([(700, 100), (400, 400),
                                   (600, 300), (650, 500)])
ctx.stroke()
ctx.set_source_rgb(1, 0, 0)
ctx.set_line_width(2)
ctx.dot_hdd(poly, bb_poly, sep=15)
ctx.stroke()


HDD.deviation = 5
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1)
ctx.axes_hdd(400, 700, units=(100, 100))
ctx.stroke()
ctx.set_source_rgb(1, 0, 0)
ctx.set_line_width(3)
HDD.deviation = 50
ctx.function_hdd(lambda x: math.sin(x),
                   -2 * math.pi, 2 * math.pi,
                   nb=50)
ctx.stroke()

img.write_to_png("test1.png")

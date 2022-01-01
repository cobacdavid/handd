# HANDD

HAND-Drawn like Context extension for [pycairo](https://pycairo.readthedocs.io/)

## Installation

`pip3 install handd`

_Dependancy:_

- `pycairo`


## The new Context methods

### classmethod

- `HDD.is_in(x, y, close_path)`

### methods on tuple lists

- `hdd.lpolygon_hdd(xy)` (returns `(p, bb)` path and bounding box)
- `hdd.lround_point_hdd(xy)`
- `hdd.lpoint_hdd(xy)`
- `hdd.lline_hdd(xy)`
- 
### basic figures methods

- `hdd.rectangle_hdd(x, y, w, h)` (returns `(p, bb)` path and bounding box)
- `hdd.regular_polygon_hdd(x, y, radius, n_sides, angle_radian=0)` (returns `(p, bb)` path and bounding box)
- `hdd.disc_hdd(x, y, radius, a_debut, a_fin=None)` (returns `(p, bb)` path and bounding box)
- `hdd.sector_hdd(x, y, radius, a_debut, a_fin, dev=3)` (returns `(p, bb)` path and bounding box)
- `hdd.real_circle_hdd(self, xc, yc, r, step=.005)` (returns `(p, bb)` path and bounding box)
- `hdd.circle_hdd(x, y, radius, dev=3, step=.01)` (returns `(p, bb)` path and bounding box)

### various methods

- `hdd.hatch_hdd(closed_path, bbox, nb=10, angle=math.pi / 4, condition=lambda x, y: True)`
- `hdd.dot_hdd(closed_path, bbox, sep=5)`
- `hdd.axes_hdd(x, y, units=None)`
- `hdd.function_hdd(function, xmin, xmax, nb=15)`
- `hdd.data_hdd(file)`

## Images from examples (see tests section)

### test1
![](https://github.com/cobacdavid/handd/blob/master/tests/test1.png?raw=true)

### test2
![](https://github.com/cobacdavid/handd/blob/master/tests/test2.png?raw=true)

### test4_svg
![](https://raw.githubusercontent.com/cobacdavid/handd/1ca655088d3bc009c79651ca81ec72daa359f5eb/tests/test4_svg.svg)

### test5
![](https://github.com/cobacdavid/handd/blob/master/tests/test5.png?raw=true)

### test6
![](https://github.com/cobacdavid/handd/blob/master/tests/test6.png?raw=true)

### catriona57

![](https://github.com/cobacdavid/handd/blob/master/tests/catriona57.png?raw=true)

_figure from Catriona Shearer's book "geometry puzzle"_




## Copyright

2022 / D. COBAC / CC-BY-NC-SA

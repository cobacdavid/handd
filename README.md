# HANDD

HAND-Drawn like Context extension for [pycairo](https://pycairo.readthedocs.io/)

## Installation

`pip3 install handd`

_Dependancy:_

- `pycairo`


## The new Context methods

### classmethod

- `HDD.is_in(x, y, closed_path)`

### methods on tuple lists

- `hdd.lline_hdd(xy)` (return points list used to draw Bezier line)
- `hdd.lpolygon_hdd(xy)` (returns `(p, bb)` path and bounding box)
- `hdd.lround_point_hdd(xy)`
- `hdd.lpoint_hdd(xy, radius=5)`

### basic figures methods

- `hdd.rectangle_hdd(x, y, w, h)` (returns `(p, bb)` path and bounding box)
- `hdd.regular_polygon_hdd(x, y, radius, n_sides, angle=0)` (returns `(p, bb)` path and bounding box)
- `hdd.disc_hdd(x, y, radius, a_start, a_end=None)` (returns `(p, bb)` path and bounding box)
- `hdd.sector_hdd(x, y, radius, a_start, a_end, dev=3)` (returns `(p, bb)` path and bounding box)
- `hdd.real_circle_hdd(x, y, radius, step=.005)` (returns `(p, bb)` path and bounding box)
- `hdd.circle_hdd(x, y, radius, dev=3, step=.01)` (returns `(p, bb)` path and bounding box)

### various methods

- `hdd.hatch_hdd(path, bbox, n=10, angle=math.pi / 4, condition=lambda x, y: True)`
- `hdd.dot_hdd(path, bbox, sep=5)`
- `hdd.axes_hdd(x, y, units=None)`
- `hdd.function_hdd(f, xmin, xmax, n=15)`
- `hdd.data_hdd(a_file)` (functionnality actually not tested)

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

### test7
![](https://github.com/cobacdavid/handd/blob/master/tests/test7.png?raw=true)

### test8
![](https://github.com/cobacdavid/handd/blob/master/tests/test8.png?raw=true)


### catriona17
![](https://github.com/cobacdavid/handd/blob/master/tests/catriona17.png?raw=true)

### catriona38
![](https://github.com/cobacdavid/handd/blob/master/tests/catriona38.png?raw=true)

### catriona57
![](https://github.com/cobacdavid/handd/blob/master/tests/catriona57.png?raw=true)

_Catriona figures from [Catriona Shearer](https://twitter.com/Cshearer41)'s book "geometry puzzle"_




## Copyright

2022 / D. COBAC / CC-BY-NC-SA

#!/usr/bin/env python

'''
    Attractor Visualizer
    ~~~~~~~~~~~~~~~~~~~~~

    Parameters used are from Paul Bourke's fractal page.
    See also: "The Pattern Book" by Clifford A. Pickover.
    
    Requires the PyDye graphics library for rendering.

    :copyright: Copyright (c) 2012 Saumitro Dasgupta
    :license: MIT License [http://opensource.org/licenses/MIT]
'''

import dye
from math import ceil, sin, cos

# -----------------------------
#   Common Utility
# -----------------------------

def make_set_explorer(func, n, x0=0, y0=0):
    def set_explorer():
        x, y = x0, y0
        for i in xrange(n):
            x, y = func(x, y)
            yield (x, y)
    return set_explorer

def get_bounds(explorer):
    bounds = dye.BoundingBox()
    for p in explorer():
        bounds.expand(*p)
    return bounds

def plot_points(explorer, scale, alpha=40):
    b = dye.BoundingBox(points=explorer())
    w, h = int(ceil(scale*(b.max_x - b.min_x))), int(ceil(scale*(b.max_y - b.min_y)))
    bmp = dye.BitmapContext(w, h)
    for x, y in explorer():
        x, y = int(scale*(x-b.min_x)), int(scale*(y-b.min_y))
        bmp.composite_pixel(x, y, 0, 0, 0, alpha)
    bmp.preview()

# -----------------------------
#   The Attractors
# -----------------------------

def de_jong_attractor(a, b, c, d):
    return lambda x, y: (sin(a*y) - cos(b*x), sin(c*x) - cos(d*y))

def de_jong_variant_attractor(a, b, c, d):
    return lambda x, y: (d*sin(a*x) - sin(b*y), c*cos(a*x) + cos(b*y))

def clifford_attractor(a, b, c, d):
    return lambda x, y: (sin(a*y) + c*cos(a*x), sin(b*x) + d*cos(b*y))

# -----------------------------
#   Test Parameters
# -----------------------------

de_jong_params = (1.4, -2.3, 2.4, -2.1)
de_jong_variant_params = (1.4, 1.56, 1.4, -6.56)
clifford_params = (1.5, -1.8, 1.6, 0.9)

if __name__=='__main__':
    attractor = de_jong_attractor(*de_jong_params)
    explorer = make_set_explorer(attractor, n=1000000)
    plot_points(explorer, scale=100)

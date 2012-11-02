#!/usr/bin/env python
'''
    Sample L-Systems
    ~~~~~~~~~~~~~~~~~

    Many of the sample L-Systems below are from the book:
    "The Algorithmic Beauty of Plants" by Przemyslaw Prusinkiewicz and Aristid Lindenmayer.
    [1990, Springer-Verlag, New York]

    Requires the PyDye graphics library.

    :copyright: Copyright (c) 2012 Saumitro Dasgupta
    :license: MIT License [http://opensource.org/licenses/MIT]
'''

import dye
from Lsystem import Lsystem
from BezierSynthesizer import BezierSynthesizer
from TreeSynthesizer import TreeSynthesizer
from TreeRenderer import render_tree, preprocess_tree

ISLAND_AND_LAKES = Lsystem(axiom='F+F+F+F', rules={'F': 'F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF', 'f': 'ffffff'}, theta=90, n=2)
KOCH_ISLAND = Lsystem(axiom='F-F-F-F', rules={'F':'F+FF-FF-F-F+F+FF-F-F+F+FF+FF-F'}, theta=90, n=2)
DRAGON_CURVE = Lsystem(axiom='A', rules={'A':'A+B+', 'B':'-A-B'}, theta=90, n=10)
SIERPINSKI_GASKET = Lsystem(axiom='B', rules={'A':'B+A+B', 'B':'A-B-A'}, theta=60, n=8)
HEX_GOSPER = Lsystem(axiom='A', rules={'A':'A+B++B-A--AA-B+', 'B':'-A+BB++B+A--A-B'}, theta=60, n=4)
PLANT_1 = Lsystem(axiom ='F', rules={'F':'F[+F]F[-F]F'}, theta=25.7, n=5)
PLANT_2 = Lsystem(axiom='F', rules={'F':'FF-[-F+F+F]+[+F-F-F]'}, theta=22.5, n=4)
PLANT_3 = Lsystem(axiom='A', rules={'A':'F[+A][-A]FA', 'F':'FF'}, theta=25.7, n=7)

palettes = (dye.Gradient(start=dye.RGB(0.007, 0.469, 0.085), stop=dye.RGBA(0.000, 0.990, 0.664, 0.4)),
            dye.Gradient(start=dye.RGB(1.000, 0.769, 0), stop=dye.RGBA(1.000, 0.312, 0.000, 0.8)))

def preview_simple_curve(sys):
    synth = BezierSynthesizer()
    synth.synthesize(sys)
    path = synth.path
    path.normalize_origin(stroked=True)
    r = path.bounds()
    with dye.Image(r.w, r.h) as img:
        dye.Gray(0.8).set()
        path.stroke()
    img.preview()

def preview_shaded_curve(sys):
    synth = TreeSynthesizer()
    synth.synthesize(sys, step_size=2)
    root_node = synth.root_node
    preprocess_tree(root_node)
    with dye.Image(*root_node.bounds.size()) as img:
        render_tree(root_node, gradient=palettes[1])
    img.preview()

if __name__=='__main__':
    preview_shaded_curve(PLANT_3)

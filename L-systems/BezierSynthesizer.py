'''
    L-system Bezier Path Synthesizer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Requires the PyDye graphics library.

    :copyright: Copyright (c) 2012 Saumitro Dasgupta
    :license: MIT License [http://opensource.org/licenses/MIT]
'''

import Lsystem
import dye

class BezierSynthesizer(Lsystem.AbstractSynthesizer):

    def prepare(self):
        self.path = dye.BezierPath()
        self.path.move_to(self.x, self.y)

    def move_to(self, x, y):
        self.path.move_to(x, y)

    def line_to(self, x, y):
        self.path.line_to(x, y)
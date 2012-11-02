'''
    Lindenmayer system producer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright (c) 2012 Saumitro Dasgupta
    :license: MIT License [http://opensource.org/licenses/MIT]
'''

import math

class Lsystem(object):

    def __init__(self, axiom, rules, theta, n):
        self.axiom = axiom
        self.rules = rules.copy()
        self.theta = theta
        self.n = n

    def rewrite(self, s):
        return ''.join([self.rules.setdefault(c, c) for c in s])

    def iterate(self, idx=0):
        s = self.axiom
        for i in xrange(idx):
            s = self.rewrite(s)        
        return s

    def string(self):
        return self.iterate(self.n)

class AbstractSynthesizer(object):
    
    op_lookup = {'f':'move_forward',
                 'F':'draw_forward',
                 'A':'draw_forward',
                 'B':'draw_forward',
                 '+':'turn_left',
                 '-':'turn_right',
                 '[':'push',
                 ']':'pop',}

    def synthesize(self, lsys, step_size=5, x=0, y=0):
        self.x, self.y = x, y
        self.heading = math.pi/2.0
        self.step_size = step_size
        self.stack = []
        self.prepare()
        self.theta = lsys.theta*(math.pi/180)
        s = lsys.string()
        for c in s:
            try:
                method = self.op_lookup[c]
                getattr(self, method)()
            except KeyError:
                raise ValueError('Invalid symbol encountered: %s'%c)

    def update_position(self):
        self.x += self.step_size*math.cos(self.heading)
        self.y += self.step_size*math.sin(self.heading)

    def move_forward(self):
        self.update_position()
        self.move_to(self.x, self.y)

    def draw_forward(self):
        self.update_position()
        self.line_to(self.x, self.y)

    def turn_left(self):
        self.heading += self.theta

    def turn_right(self):
        self.heading -=  self.theta

    def push(self):
        self.stack.append((self.x, self.y, self.heading))

    def pop(self):
        self.x, self.y, self.heading = self.stack.pop()
        self.move_to(self.x, self.y)


    def prepare(self): raise NotImplementedError

    def move_to(self, x, y): raise NotImplementedError

    def line_to(self, x, y): raise NotImplementedError


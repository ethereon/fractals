#!/usr/bin/env python

'''
    Diffusion-Limited Aggregation (DLA) Simulation in 2D
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Requires the PyDye graphics library for rendering.

    :copyright: Copyright (c) 2012 Saumitro Dasgupta
    :license: MIT License [http://opensource.org/licenses/MIT]
'''

import dye
import math, random

# --------------------------------------------------------------------
# Vector Operations. We use plain-old Python tuples for vectors.
# --------------------------------------------------------------------

vec_negate = lambda v : (-v[0], -v[1])
vec_add = lambda a, b: (a[0]+b[0], a[1]+b[1])
vec_scale = lambda v, s:  (s*v[0], s*v[1])

def vec_distance(a, b):
    x, y = a[0] - b[0], a[1] - b[1]
    return math.sqrt(x*x + y*y)

def vec_normalize(v):
    norm = math.sqrt(v[0]*v[0] + v[1]*v[1])
    return (v[0]/norm, v[1]/norm) if norm!=0 else (0, 0)

# --------------------------------------------------------------------
# A single node in the DLA network.
# --------------------------------------------------------------------

class Node(object):
    def __init__(self, pos, parent=None):
        self.pos = pos
        self.parent = parent

# --------------------------------------------------------------------
# The core DLA class
# --------------------------------------------------------------------

class DLA(object):

    def __init__(self):
        # DLA Parameters
        self.step_size = 5                            
        self.bounds_radius = 3*self.step_size
        self.collision_distance = 2*self.step_size
        # Drawing Parameters
        self.draw_nodes = True
        self.node_color = dye.RGB(0.251, 0.078, 0.098)
        self.line_color = dye.RGB(1.000, 0.119, 0.059)
        self.line_thickness = 2.0
        self.node_marker_radius = 2.0
        self.image_margin = 30.0

    def detect_collision(self):
        ''' A straight-forward but inefficient linear collision search. '''
        for n in self.nodes:
            if vec_distance(n.pos, self.loc)<=self.collision_distance:
                self.nodes.append(Node(self.loc, n))
                # If we are one step away from the bound, expand it by a step.
                if vec_distance(self.loc, (0, 0)) >= (self.bounds_radius-self.step_size):
                    self.bounds_radius += self.step_size
                # Move to a point on the bounding curve
                theta = random.uniform(0, 2*math.pi)
                self.loc = (self.bounds_radius*math.cos(theta), self.bounds_radius*math.sin(theta))
                break
            
    def generate(self, num_nodes=400):
        self.nodes = [Node((0.0, 0.0))]
        self.loc = (0.0, 0.0)
        rv = lambda: random.uniform(-1, 1)        
        while len(self.nodes)<num_nodes:
            # Random walk
            random_vec = vec_scale(vec_normalize((rv(), rv())), self.step_size)
            self.loc = vec_add(self.loc, random_vec)
            if vec_distance(self.loc, (0, 0))>self.bounds_radius:
                # We've stepped outside the bounds. Walk back in.
                self.loc = vec_add(self.loc, vec_negate(random_vec))
            self.detect_collision()

    def draw_network(self):
        for n in self.nodes:
            if n.parent is not None:
                dye.draw_line(n.parent.pos, n.pos, color=self.line_color, thickness=self.line_thickness)
        if self.draw_nodes:
            for n in self.nodes:
                dye.Oval(center=n.pos, radius=self.node_marker_radius).stroke(color=self.node_color)

    def render(self):
        w, h =  2*(2*(self.bounds_radius + self.image_margin),)
        tx, ty = 2*(self.bounds_radius + self.image_margin,)
        with dye.Image(w, h) as img:            
            with dye.translation(tx, ty):
                self.draw_network()
        return img

# --------------------------------------------------------------------
# TracingDLA: For visualizing the simulation process
# --------------------------------------------------------------------

class TracingDLA(DLA):

    def __init__(self):
        super(TracingDLA, self).__init__()
        self.walk_trace = []
        self.base_radius = self.bounds_radius
        self.trace_color = dye.RGBA(0, 0, 0, 0.1)        
        self.bound_color = dye.RGBA(0, 0, 0, 0.2)
        self.tracing_enabled = True

    def detect_collision(self):
        if (len(self.walk_trace)==0) or (self.walk_trace[-1]!=self.loc):
            self.walk_trace.append(self.loc)
        super(TracingDLA, self).detect_collision()

    def draw_network(self):
        if self.tracing_enabled:
            for point in self.walk_trace:
                dye.Oval(center=point, radius=self.node_marker_radius).fill(color=self.trace_color)
            for i in xrange(1+(self.bounds_radius - self.base_radius)/self.step_size):
                dye.Oval(center = (0, 0), radius=self.base_radius+(i*self.step_size)).stroke(self.bound_color)
        super(TracingDLA, self).draw_network()

if __name__=='__main__':
    dla = TracingDLA()
    dla.generate()
    dla.render().preview()

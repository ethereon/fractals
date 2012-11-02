'''
    Tree Synthesizer
    ~~~~~~~~~~~~~~~~~

    Creates a tree structure from an L-system string.
    This will fail in spectacular ways for systems with cycles.

    :copyright: Copyright (c) 2012 Saumitro Dasgupta
    :license: MIT License [http://opensource.org/licenses/MIT]
'''

import Lsystem
from collections import deque

class Node(object):
    
    def __init__(self, x, y, parent=None):
        self.x, self.y = x, y
        self.children = []
        self.parent = parent
        if parent is not None:
            parent.children.append(self)        

    def __str__(self):
        return "Node at (%d, %d) with %d children."%(self.x, self.y, len(self.children))

class TreeSynthesizer(Lsystem.AbstractSynthesizer):

    def prepare(self):
        self.root_node = Node(self.x, self.y)
        self.nodes = { (self.x, self.y) : self.root_node }
        self.curr_parent = self.root_node
        
    def move_to(self, x, y):
        try:
            self.curr_parent = self.nodes[(x, y)]
        except KeyError:
            raise ValueError("Unsupported tree structure.")

    def line_to(self, x, y):
        node = Node(x, y, parent=self.curr_parent)
        self.nodes[(x, y)] = node
        self.curr_parent = node

def walk(root_node):
    queue = deque(root_node.children)
    while len(queue)!=0:
        node = queue.popleft()
        yield node
        queue.extend(node.children)
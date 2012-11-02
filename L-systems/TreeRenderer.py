'''
    Tree Renderer
    ~~~~~~~~~~~~~~

    Draws L-system tree graphs generated using TreeSynthesizer
    Requires the PyDye graphics library.

    :copyright: Copyright (c) 2012 Saumitro Dasgupta
    :license: MIT License [http://opensource.org/licenses/MIT]
'''

import dye
import math
from TreeSynthesizer import walk

def preprocess_tree(root_node):
    root_node.weight = 0
    root_node.leaf_dist = None
    # Step 1: Calculate each node's distance to the farthest leaf node
    for node in walk(root_node):
        if len(node.children)==0:
            node.leaf_dist = 0
            while node.parent and ((node.parent.leaf_dist is None) or node.parent.leaf_dist<(node.leaf_dist+1)):
                node.parent.leaf_dist = node.leaf_dist+1
                node = node.parent
        else:
            node.leaf_dist = None
    # Step 2: Calculate the node weights + tree bounds
    bounding_box = dye.BoundingBox()
    for node in walk(root_node):
        bounding_box.expand(node.x, node.y)
        if node.leaf_dist==0:
            node.weight = 1
        else:
            node.weight = node.parent.weight+((1 - node.parent.weight)/float(node.leaf_dist + 1))
    root_node.bounds = bounding_box.rect()

def render_tree(root_node, gradient):    
    with dye.translation(-root_node.bounds.x, -root_node.bounds.y):
        for node in walk(root_node):
            if node.parent is not None:
                x0, y0, x1, y1 = (node.parent.x, node.parent.y, node.x, node.y)
                seg_gradient = dye.Gradient(start = gradient.get_interpolated_color(node.parent.weight),
                                            stop = gradient.get_interpolated_color(node.weight))
                seg = dye.BezierPath()
                seg.move_to(x0, y0)
                seg.line_to(x1, y1)
                with dye.ContextFrame():
                    seg.clip_to_outline()
                    seg_gradient.draw_linear_in_rect(seg.bounds(), math.atan2(x1 - x0, y1 - y0))
# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

from graphviz import Digraph
import cPickle as pickle
import itertools
from DialogContainer import DialogContainer

class DialogAnalyzer:
    def __init__(self, dialog_container):
        self.container = dialog_container
        self.index = dialog_container.index
        self.roots = dialog_container.root_nodes

    def __r_draw(self, parent):
        ret = []
        if parent in self.index:
            for child in self.index[parent]:
                ret.append((parent,child))
                ret += self.__r_draw(child)
        return ret

    def draw(self, root, filename):
        dot = Digraph(format = 'pdf')
        for parent, child in self.__r_draw(root):
            dot.edge(str(parent), str(child))
        dot.render(filename)

    """ Returns a list of all subordinated nodes to a given parent node """
    def subordinated_nodes(self, root):
        ret = []
        if root in self.index:
            for child in self.index[root]:
                ret.append(child)
                ret += self.subordinated_nodes(child)
        return ret

    """ Returns the max. depth of the graph"""
    def depth (self, root):
        score = 0
        if root in self.index:
            for child in self.index[root]:
                child_score = self.depth(child)
                if child_score > score:
                    score = child_score
        return score + 1

    """ Returns the max. width of a tree under a given root node"""
    def width(self, root):
        if root in self.index:
            score = len(self.index[root])
            for child in self.index[root]:
                child_score = self.width(child)
                if child_score > score:
                    score = child_score
            return score
        else:
            return 0


##Steve: AllDialogs-DialogContainer.bin can be found on daphne in /tmp/AllDialogs-DialogContainer.bin
##Remember to use cPickle instead of pickle.
if __name__ == '__main__':
    dialog_container = pickle.load(open("AllDialogs-DialogContainer.bin", "rb"))
    analyzer = DialogAnalyzer(dialog_container)
    print analyzer.roots[0]
    analyzer.draw(analyzer.roots[0],"/Users/johannes/Desktop/1")


#
#
# d = DialogContainer()
# d.add_relation(0,1)
# d.add_relation(0,2)
# d.add_relation(2,3)
# d.add_relation(3,4)
# d.add_relation(3,5)
# d.add_relation(4,6)
#
# a = DialogAnalyzer(d)
# print a.subordinated_nodes(0)
# print a.width(0)
# print a.depth(0)
# a.draw(0, "/Users/johannes/Desktop/a.pdf")
# print d.depth()
# d.draw("/Users/johannes/Desktop/a.pdf")
# """
#         0
#        / \
#       1   2
#           |
#           3
#          / \
#         4   5
#         |
#         6
# """
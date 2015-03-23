# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

import itertools

class DialogContainer:
    def __init__ (self):
        self.index = {}  # stores a list
        self.root_nodes = [] # node, that has no incoming edges

    def add_relation (self, parent, child):
        self.index.setdefault(parent, []).append(child)

    def find_roots (self):
        # Make a set difference between the keys and the values of the index. The root-node will not appear as a value, only as a key.
        self.root_nodes = list(set(self.index.keys()).difference(set(itertools.chain.from_iterable(self.index.values()))))

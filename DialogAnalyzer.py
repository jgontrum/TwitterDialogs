# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

from graphviz import Digraph
import cPickle as pickle
from operator import itemgetter
from DialogContainer import DialogContainer

"""Analyzes dialog-graphs."""
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

    def getMostDistantChild(self, root):
        return self.__r_getMostDistantChild(root)[1]

    def __r_getMostDistantChild (self, root):
        score = 0
        deep_id = root
        if root in self.index:
            for child in self.index[root]:
                child_score, child_id = self.__r_getMostDistantChild(child)
                if child_score > score:
                    score = child_score
                    deep_id = child_id
        return (score + 1, deep_id)

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

    def getDialogMembers(self, root):
        ret = [root]
        ret += self.__r_getDialogMembers(root)
        return set(ret)

    def __r_getDialogMembers(self, parent):
        ret = []
        if parent in self.index:
            for child in self.index[parent]:
                ret.append(child)
                ret += self.__r_getDialogMembers(child)
        return ret


#Steve: AllDialogs-DialogContainer.bin can be found on daphne in /tmp/AllDialogs-DialogContainer.bin
#Remember to use cPickle instead of pickle.
if __name__ == '__main__':
    dialog_container = pickle.load(open("AllDialogs-DialogContainer.bin", "rb"))
    id_to_data = pickle.load(open("IDtoData.pickle", "rb"))
    analyzer = DialogAnalyzer(dialog_container)


    '''Dialogteilnehmer -> Breite / Länge '''
    members_to_width = {}
    members_to_height = {}

    for root in analyzer.roots:
        if root in id_to_data:
            mem = len(analyzer.getDialogMembers(root))
            members_to_width.setdefault(mem, []).append(analyzer.width(root))
            members_to_height.setdefault(mem, []).append(analyzer.depth(root))

    for mems, widths in sorted(members_to_width.iteritems(), key=itemgetter(0)):
        print str(mems) + "\t" + str((sum(widths) / float(len(widths)))) + "\t" + str(len(widths))
    print "\n\n\n"

    for mems, height in sorted(members_to_height.iteritems(), key=itemgetter(0)):
        print str(mems) + "\t" + str((sum(height) / float(len(height)))) + "\t" + str(len(height))

    # '''Followeranzahl -> Breite '''
    # follower_to_width = {}
    #
    # for root in analyzer.roots:
    #     if root in id_to_data:
    #         follower_to_width.setdefault(analyzer.width(root), []).append(id_to_data[root][1])
    #
    # for width, followers in sorted(follower_to_width.iteritems(), key=itemgetter(0)):
    #     print str(width) + "\t" + str(int(sum(followers) / float(len(followers)))) + "\t" + str(len(followers))

    # """ Dialoglänge -> Zeitdifferenz """
    # length_to_time = {}
    #
    # for root in analyzer.roots:
    #     latest_reply = analyzer.getMostDistantChild(root)
    #     if latest_reply in id_to_data and root in id_to_data:
    #         length_to_time.setdefault(analyzer.depth(root), []).append(id_to_data[latest_reply][0] -
    #                                                                   id_to_data[root][0])
    #
    #
    # for length, times in sorted(length_to_time.iteritems(), key=itemgetter(0)):
    #     print str(length) + "\t" + str(int(sum(times) / float(len(times)))) + "\t" + str(len(times))


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
# print a.get_dialog_members(0)
# a.draw(0, "/Users/johannes/Desktop/a.pdf")
# print a.getMostDistantChild(0)

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
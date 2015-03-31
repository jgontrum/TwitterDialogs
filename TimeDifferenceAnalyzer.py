# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

import cPickle as pickle
from operator import itemgetter
from pylab import *
import numpy as np
hour_to_timediff, follower_to_timediff = pickle.load(open("TimeDiff.pickle", "rb"))
from scipy.interpolate import spline


def avg_list(data, interval=100):
    ret = []
    for i in range(0,len(data),interval):
        x_avg = 0
        y_avg = 0
        for x,y in data[i : i+interval]:
            x_avg += x
            y_avg += y
        x_avg = int(x_avg / float(interval))
        y_avg = int(y_avg / float(interval))
        ret.append((x_avg, y_avg))
        # for i in range(interval):
        #     ret.append((x_avg, y_avg))
    return ret

# for hour, diff in sorted(hour_to_timediff.iteritems(), key=itemgetter(0), reverse=True):
#     print(hour + "\t" + str(int(sum(diff)/float(len(diff)))))

follower_to_avg_timediff = {}
for follower, diff in sorted(follower_to_timediff.iteritems(), key=itemgetter(0)):
    follower_to_avg_timediff[follower] = int(sum(diff) / float(len(diff)))

s = sorted(follower_to_avg_timediff.iteritems(), key=itemgetter(0))
s_sub_500 = [x for x in sorted(follower_to_avg_timediff.iteritems(), key=itemgetter(0)) if x[0] < 1000]

for follower, time in avg_list(s, 80):
    print str(follower) + "\t" + str(time)


# plot([x_avg[0] for x in avg_list(s_sub_500, 50)], [x[1] for x in avg_list(s_sub_500, 50)], color='b')
# plot([x[1] for x in avg_list(s, 425)], color='b')

# show()

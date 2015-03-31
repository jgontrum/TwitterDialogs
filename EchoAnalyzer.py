# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

import cPickle as pickle
from operator import itemgetter

scores = []

for tweet, reply, tweetid, replyid, score in pickle.load(open("EchoScore.pickle", "rb")):
    scores.append((score[0][1], tweet, tweetid, reply, replyid))

for score, tweet, tweetid, reply, replyid in sorted(scores, key=itemgetter(0), reverse=True):
    if score > 0.8:
        print "Frage: \t" + tweet + "\t(ID: " + str(tweetid) + ")\nAntwort: \t" + reply + "\t(ID: " + str(replyid) + ")\nScore: \t" + str(score) + "\n"
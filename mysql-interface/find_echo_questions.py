# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'
import ConfigParser
import MySQLdb
import MySQLdb.cursors
import sys
import cPickle as pickle
    
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity  

# <editor-fold desc="SQL Connect">
# Read in config:
config = ConfigParser.RawConfigParser()
config.read('config.properties')

dbHostDB = config.get('MySQL', 'mySQLHost')
dbUser = config.get('MySQL', 'mySQLUser')
dbPassword = config.get('MySQL', 'mySQLPassword')
dbTable = config.get('MySQL', 'mySQLTablePrefix')
dbHost = dbHostDB[:dbHostDB.find("/")]
dbDB = dbHostDB[dbHostDB.find("/") + 1:]

# Connect to database
connection = MySQLdb.connect(host = dbHost, user = dbUser, passwd = dbPassword, db = dbDB)

# Create a server sided cursor: http://stackoverflow.com/a/3788777/4587312
readCursor = connection.cursor(MySQLdb.cursors.SSCursor)

# </editor-fold>

readCursor.execute("SELECT Replies.text as reply, April2013.text as tweet, Replies.childid, April2013.id FROM April2013, (SELECT `text`, `id` as `childid`,  `in_reply_to_status_id` as `id` FROM April2013 WHERE `valid` = 1 and `direct_replies_count` > 0 and `in_reply_to_status_id` != -1 and `question_mark` = 1 ) AS Replies WHERE April2013.valid = 1 and April2013.question_mark IS NULL and April2013.id = Replies.id")

stats = []
tfidf_vectorizer = TfidfVectorizer()

for reply, tweet, replyid, tweetid in readCursor:
   tfidf_matrix = tfidf_vectorizer.fit_transform((reply, tweet))
   stats.append((tweet, reply, tweetid, replyid, cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)))

pickle.dump(stats, open("EchoScore.pickle", "wb"))


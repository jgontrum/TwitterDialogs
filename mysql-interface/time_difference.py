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

readCursor.execute("""
        SELECT from_unixtime(April2013.created_at,'%a%H') as question_timestamp, (Replies.created_at - April2013.created_at) as difference, followers_count
        FROM April2013,
            (   SELECT `created_at`, `in_reply_to_status_id` as `id`
                FROM April2013 
                WHERE `valid` = 1 and `in_reply_to_status_id` != -1
            ) AS Replies
        WHERE April2013.valid = 1 and April2013.question_mark = 1
              and April2013.id = Replies.id 
         """)

day_hour_to_time_diff = {}
follower_to_time_diff = {}
for day_hour, time_diff, followers in readCursor:
    day_hour_to_time_diff.setdefault(day_hour, []).append(time_diff)
    follower_to_time_diff.setdefault(followers,[]).append(time_diff)

pickle.dump((day_hour_to_time_diff,follower_to_time_diff), open("/tmp/TimeDiff.pickle", "wb"))


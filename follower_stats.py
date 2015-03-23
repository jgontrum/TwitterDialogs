# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'
import ConfigParser
import MySQLdb
import MySQLdb.cursors
import sys
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

print "Creating statistics about twitter users, the number of their followers and the amount of tweets and questions they write."

userid_to_followercnt = {}
userid_to_tweets = {}
userid_to_questions = {}

readCursor.execute("SELECT user_id, followers_count, question_mark FROM " + dbTable + " WHERE valid = 1")

for user_id, follow_cnt, question in readCursor:
    userid_to_followercnt.setdefault(user_id, follow_cnt)
    userid_to_tweets.setdefault(user_id, 0)
    userid_to_tweets[user_id] += 1
    userid_to_questions.setdefault(user_id, 0)
    userid_to_questions[user_id] += 1

print "Question/Tweet Ratio per user"
follower_file = open('question-tweet-ratio.txt','w')
for i in sorted(userid_to_followercnt.values()):
    if i in userid_to_questions.keys():
        ret = str(int(userid_to_questions[i] / float(userid_to_tweets[i])))
        follower_file.write(ret + "\n")




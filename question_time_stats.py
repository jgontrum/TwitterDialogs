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

print "Finding dialog initializing questions and how they are answered."

followers_to_reply_list = {}

readCursor.execute("SELECT direct_replies_count, indirect_replies_count, created_at, followers_count FROM " + dbTable + " WHERE question_mark = 1 and is_base_tweet = 1 and valid = 1")


for direct_cnt, indirect_cnt, created, follower_cnt in readCursor:
    followers_to_reply_list.setdefault(follower_cnt / 1000 * 1000, list()).append(indirect_cnt)

print "Output:"
for follower, list_of_replies in sorted(followers_to_reply_list.iteritems()):
    print follower, ";", sum(list_of_replies)/float(len(list_of_replies))


# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'
import ConfigParser
import MySQLdb
import MySQLdb.cursors
import sys
import cPickle as pickle
from operator import itemgetter

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
        SELECT CHAR_LENGTH(`text`), indirect_replies_count
        FROM April2013
        WHERE question_mark = 1
            and valid = 1
            and direct_replies_count > 0
        """)

length_to_replies = {}
for length, count in readCursor:
    length_to_replies.setdefault(length,[]).append(count)

for length, counts in sorted(length_to_replies.iteritems(), key=itemgetter(0)):
    print str(length) + "\t" + str(float(sum(counts)) / len(counts)) + "\t" + str(len(counts))

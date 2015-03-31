# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'
import ConfigParser
import MySQLdb
import MySQLdb.cursors
import sys
import cPickle as pickle
    
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

readCursor.execute("SELECT id, created_at, followers_count, CHAR_LENGTH(text)  FROM " + dbTable + " WHERE indirect_replies_count > 0 and valid = 1")

id_to_data = {}

for tweet_id, created_at, followers, length in readCursor:
    id_to_data[tweet_id] = (created_at, followers, length)

pickle.dump(id_to_data,  open("/tmp/IDtoData.pickle","wb"))


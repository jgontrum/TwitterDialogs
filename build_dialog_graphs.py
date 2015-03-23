# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'
import ConfigParser
import MySQLdb
import MySQLdb.cursors
import sys
import cPickle as pickle
from DialogContainer import DialogContainer

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

print "Iterate over the tweet ids and the ids that they reply to. Then integrate this parent-child relation into the dialog structure."


readCursor.execute("SELECT id, in_reply_to_status_id FROM " + dbTable + " WHERE direct_replies_count > 0 and in_reply_to_status_id != -1 and valid = 1")

container = DialogContainer()
for status_id, reply_to in readCursor:
    container.add_relation(reply_to, status_id)

print "Now find the root-nodes."
container.find_roots()

print "Writing to a pickled file."
pickle.dump(container, open("AllDialogs-DialogContainer.bin","wb"))






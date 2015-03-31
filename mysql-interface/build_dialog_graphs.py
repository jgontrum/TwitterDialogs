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

readCursor.execute("SELECT text, in_reply_to_status_id, id FROM " + dbTable + " WHERE question_mark = 1 and in_reply_to_status_id != -1 and valid = 1")

possible_echo_frage = [] # (parentid, text)

for text, parent, me_id in readCursor:
    possible_echo_frage.append((parent, text, me))

print "Moegliche echofragen gefunden"

readCursor.execute("SELECT text, id  FROM " + dbTable + " WHERE question_mark IS NULL and valid = 1")
id_to_text = {}

for text, pid in readCursor:
    id_to_text[pid] = text

text_to_compare = []
for parentid, text, me_id in possible_echo_frage :
    if parentid in id_to_text.keys():
        text_to_compare.append(((text, me_id), (id_to_text[parentid], parentid)))

print "Writing to a pickled file."
pickle.dump(text_to_compare,  open("TextParentText.bin","wb"))






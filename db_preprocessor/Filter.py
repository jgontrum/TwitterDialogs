# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'
import ConfigParser
import itertools
import MySQLdb


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
connectionInsert = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPassword, db=dbDB)
connectionInsert.autocommit(True)
insertCursor = connectionInsert.cursor()
# </editor-fold>

print "Set default value for `valid`"

insertCursor.execute("UPDATE `" + dbTable + "` SET `valid` = 1")
connectionInsert.commit()

print "Find invalid tweets"

keywords = ["@YouTube","Gutschein","#4sq","#androidgames","#nowplaying","#np","Verkehrsmeldungen","Wetterdaten"]

print "UPDATE `" + dbTable + "` SET `valid` = 0 WHERE `text` REGEXP '[[:<:]](" + "|".join(keywords) +  ")[[:>:]]'"

insertCursor.execute(
    "UPDATE `" + dbTable + "` SET `valid` = 0 WHERE `text` REGEXP '[[:<:]](" + "|".join(keywords) +  ")[[:>:]]'") 
connectionInsert.commit()

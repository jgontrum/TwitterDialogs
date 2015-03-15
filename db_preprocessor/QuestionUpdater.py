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

#print "Finding questionmarks"
# http://dev.mysql.com/doc/refman/5.1/en/regexp.html
# Set question_mark = 1 IF a '?' is found:
#insertCursor.execute(
#    'UPDATE `" + dbTable + "` SET `question_mark` = 1 WHERE `text` LIKE "%?%"')
#connectionInsert.commit()

print "Find wh-questions"
# Set is_wh_question = 1 IF it contains a word that marks a question
keywords = ["wer","welche","welcher","wen","wem","welchen","welchem","was","welches","warum","weshalb","weswegen","wieso","wozu","womit","wodurch","wo","wohin","woher","woran","worin","worauf","worunter","wovor","wohinter","wann"]

print "UPDATE `" + dbTable + "` SET `is_wh_question` = 1 WHERE `text` REGEXP '[[:<:]](" + "|".join(keywords) +  ")[[:>:]]'"
# create query (text begins with the word or is BLANK+WORD+BLANK to avoid partial matches:
insertCursor.execute(
    "UPDATE `" + dbTable + "` SET `is_wh_question` = 1 WHERE `text` REGEXP '[[:<:]](" + "|".join(keywords) +  ")[[:>:]]'") 
connectionInsert.commit()

print "Set is_question"
# Set is_question
insertCursor.execute(
    "UPDATE `" + dbTable + "` SET `is_question` = 1 WHERE `is_wh_question` = 1 OR `question_mark` = 1")
connectionInsert.commit()

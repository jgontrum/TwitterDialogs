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
dbTable = "testDB"
dbHost = dbHostDB[:dbHostDB.find("/")]
dbDB = dbHostDB[dbHostDB.find("/") + 1:]

# Connect to database
connectionInsert = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPassword, db=dbDB)
connectionInsert.autocommit(True)
insertCursor = connectionInsert.cursor()
# </editor-fold>

# http://dev.mysql.com/doc/refman/5.1/en/regexp.html
# Set question_mark = 1 IF a '?' is found:
regex = ".+[[.question-mark.]].*"
insertCursor.execute(
    "UPDATE `" + dbTable + "` SET `question_mark` = 1 WHERE `id` IN ( SELECT * FROM ( SELECT `id` FROM `" + dbTable + "` WHERE `text` RLIKE '" + regex + "' ) tblTmp )")
connectionInsert.commit()

# Set is_wh_question = 1 IF it contains a word that marks a question
regex2 = ".*(was|wie|warum)[[:blank:]].*"
insertCursor.execute(
    "UPDATE `" + dbTable + "` SET `is_wh_question` = 1 WHERE `id` IN ( SELECT * FROM ( SELECT `id` FROM `" + dbTable + "` LOWER(`text`) RLIKE '" + regex2 + "' ) tblTmp )")
connectionInsert.commit()

# Set is_question
insertCursor.execute(
    "UPDATE `" + dbTable + "` SET `is_question` = 1 WHERE `is_wh_question` = 1 OR `question_mark` = 1")
connectionInsert.commit()
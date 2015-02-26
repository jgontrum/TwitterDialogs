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
connection = MySQLdb.connect(host = dbHost, user = dbUser, passwd = dbPassword, db = dbDB)
connection.autocommit(False)
dbCursor = connection.cursor()

connectionInsert = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPassword, db=dbDB)
connectionInsert.autocommit(True)
insertCursor = connectionInsert.cursor()
# </editor-fold>

# <editor-fold desc="Read DB content">
""" Read MySQL database in chunks """
dbCursor.execute('SELECT COUNT(*) FROM ' + dbTable)
max_rows = float(dbCursor.fetchone()[0])

current_top_row = 0
step_fetch = 500

def getNextDBChunk ():
    global current_top_row
    global step_fetch
    global max_rows
    global dbCursor
    if current_top_row > max_rows:
        print "Finished!"
        return None
    dbCursor.execute(
        'SELECT id, in_reply_to_status_id FROM ' + dbTable + ' WHERE in_reply_to_status_id > 0 ORDER BY created_at DESC LIMIT ' + str(
            current_top_row) + ',' + str(step_fetch))
    rp = dbCursor.fetchall()
    print "[DEBUG] Returning range from", current_top_row, "to", (current_top_row + step_fetch)
    current_top_row += step_fetch
    return rp
# </editor-fold>

# <editor-fold desc="Create datastructures">
# Map tweet ids to a list of their replies.
direct_replies = {}

# Fill the dictionary with values from the DB
while True:
    rp = getNextDBChunk()
    if rp == None:
        break
    for tweetid, reply_to in rp:
        direct_replies.setdefault(reply_to, []).append(tweetid)

# Base tweets = tweets that are the root of a conversation tree.
# A tweet is a base tweet iff there are tweets that reply to it and the base tweet is not a reply.
# The base tweets are found by creating the difference between the set of tweets that have tweets replying to them
#  (keys of the dict) and the set of tweets that reply to other tweets.
base_tweets = set(direct_replies.keys()).difference(set(itertools.chain.from_iterable(direct_replies.values())))

# Find indirect replies.
# Map tweets to a list of their indirect replies, including the id of the tweet itself.
indirect_replies = {}

# Recursive function. Returns a list of all tweet ids that are id or subordinated to it in the tree.
def find_replies_rec (id):
    ret = [id]
    if id in direct_replies.keys():
        for reply in direct_replies[id]:
            ret += find_replies_rec(reply)
    indirect_replies[id] = ret
    return ret

# Iterate over all root nodes
for tweet in base_tweets:
    find_replies_rec(tweet)

# Key: counts, value: list of ids
direct_counter = {}
indirect_counter = {}

for id, replies in direct_replies.iteritems():
    l = len(replies)
    direct_counter.setdefault(l, []).append(str(id))

for id, replies in indirect_counter.iteritems():
    l = len(replies)
    indirect_counter.setdefault(l, []).append(str(id))

# </editor-fold>

# Create a MySQL value string for a list.
# [1,2,3] => ' "1","2","3" '
def list_to_string (lst):
    ret = ""
    for l in lst:
        ret += "\"" + str(l) + "\","
    return ret[:-1]

# <editor-fold desc="Add direct replies">
# Add to DB
# See: http://blog.bubble.ro/how-to-make-multiple-updates-using-a-single-query-in-mysql/
insert_step = 500
insert_count = 0
insert_query = None
insert_id_list = []
for id, replies in direct_replies.iteritems():
    # Create the head of the query if its empty
    if insert_query is None:
        insert_query = "UPDATE `" + dbTable + "` SET `direct_replies_list` = CASE "

    # Add to query:
    insert_id_list.append(str(id))
    insert_query += "WHEN id = " + str(id) + " THEN '" + list_to_string(replies) + "' "
    insert_count += 1

    # Send to DB
    if insert_count == insert_step:
        # Add footer to query
        insert_query += "ELSE `direct_replies_list` END WHERE id IN ("
        insert_query += ",".join(insert_id_list)
        insert_query += ");"

        print insert_query
        insertCursor.execute(insert_query)
        connectionInsert.commit()
        insert_id_list = []
        insert_count = 0
        insert_query = None
# </editor-fold>

# <editor-fold desc="Add indirect replies">
# Add to DB
# See: http://blog.bubble.ro/how-to-make-multiple-updates-using-a-single-query-in-mysql/
insert_step = 500
insert_count = 0
insert_query = None
insert_id_list = []
for id, replies in indirect_replies.iteritems():
    # Create the head of the query if its empty
    if insert_query is None:
        insert_query = "UPDATE `" + dbTable + "` SET `indirect_replies_list` = CASE "

    # Add to query:
    insert_id_list.append(str(id))
    insert_query += "WHEN id = " + str(id) + " THEN '" + list_to_string(replies) + "' "
    insert_count += 1

    # Send to DB
    if insert_count == insert_step:
        # Add footer to query
        insert_query += "ELSE `indirect_replies_list` END WHERE id IN ("
        insert_query += ",".join(insert_id_list)
        insert_query += ");"

        print insert_query
        insertCursor.execute(insert_query)
        connectionInsert.commit()
        insert_id_list = []
        insert_count = 0
        insert_query = None
# </editor-fold>

# <editor-fold desc="Set Counters">
# from http://stackoverflow.com/a/23148997/4587312
def list_split (arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs

# Set counter for direct replies
max_list_size = 1000
for length, ids in direct_counter.iteritems():
    for sub_lists in list_split(ids, max_list_size):
        insert_query = "UPDATE `" + dbTable + "` SET `direct_replies_count` = " + str(length) + " WHERE id IN ("
        insert_query += ",".join(sub_lists)
        insert_query += ");"

        print insert_query
        insertCursor.execute(insert_query)
        connectionInsert.commit()

# Set counter for indirect replies
max_list_size = 1000
for length, ids in indirect_counter.iteritems():
    for sub_lists in list_split(ids, max_list_size):
        insert_query = "UPDATE `" + dbTable + "` SET `indirect_replies_count` = " + str(length) + " WHERE id IN ("
        insert_query += ",".join(sub_lists)
        insert_query += ");"

        print insert_query
        insertCursor.execute(insert_query)
        connectionInsert.commit()
# </editor-fold>

# Base ids:
max_list_size = 1000
for sub_list in list_split(list(base_tweets), max_list_size):
    insert_query = "UPDATE `" + dbTable + "` SET `is_base_tweet` = 1 WHERE id IN ("
    insert_query += ",".join([str(i) for i in sub_list])
    insert_query += ");"

    print insert_query
    insertCursor.execute(insert_query)
    connectionInsert.commit()
#This module allows me to not need a ton of database query/update code 
#   in the rest of the server, by making a mini interface between the
#   database and the serve

import sqlite3
import json

def initDB():
    sql_users =                     """ CREATE TABLE IF NOT EXISTS users ( 
                                            username text NOT NULL,
                                            salt     text NOT NULL,
                                            hash     text NOT NULL,
                                            PRIMARY KEY(username)
                                        );
                                        """     

    sql_chats =                     """ CREATE TABLE IF NOT EXISTS chats ( 
                                            chatID      number NOT NULL,
                                            name        text NOT NULL,
                                            creator     text NOT NULL,
                                            createdAt   text NOT NULL,
                                            persistant  text NOT NULL,
                                                check (persistant in (\'true\', \'false\')),
                                            PRIMARY KEY(chatID)
                                        );
                                        """  
    sql_msgs =                     """ CREATE TABLE IF NOT EXISTS msgs ( 
                                            chatID      number NOT NULL,
                                            msgID       number NOT NULL,
                                            username    text NOT NULL,
                                            sentAt      text NOT NULL,
                                            img         text NOT NULL,
                                            PRIMARY KEY(msgID),
                                            FOREIGN KEY(chatID) REFERENCES chats(chatID)
                                            FOREIGN KEY(username) REFERENCES users(username)
                                        );
                                        """ 


    dbconn = sqlite3.connect("user.db")
    cursor = dbconn.cursor()
    cursor.execute(sql_users)
    cursor.execute(sql_chats)
    cursor.execute(sql_msgs)
    dbconn.close()

def insert(table, values):
    vals = ''
    for value in values:
        vals+=value+','
    vals = vals[:-1]

    sql_insert= """INSERT INTO {t} VALUES({v});""".format(t=table, v=vals)
    dbconn = sqlite3.connect("user.db")
    cursor = dbconn.cursor()
    cursor.execute(sql_insert)
    dbconn.commit()
    dbconn.close()

def query(table, columns='*', args=''):
    sql_query= """SELECT {c} FROM {t} {a};""".format(c=columns, t=table, a=args)  
    dbconn = sqlite3.connect("user.db")
    cursor = dbconn.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    dbconn.close()

    return result

def delete(table, args):
    sql_query= """DELETE FROM {t} WHERE {a};""".format(t = table, a = args)
    dbconn = sqlite3.connect("user.db")
    cursor = dbconn.cursor()
    cursor.execute(sql_query)
    dbconn.commit()
    dbconn.close()

def update(table, args):
    sql_query= """UPDATE {t} {a};""".format(t = table, a = args)
    dbconn = sqlite3.connect("user.db")
    cursor = dbconn.cursor()
    cursor.execute(sql_query)
    dbconn.commit()
    dbconn.close()
    
def toJSON(table, query, exceptfor=()):
    dbconn = sqlite3.connect("user.db")
    cursor = dbconn.cursor()
    column_info = cursor.execute("""PRAGMA table_info({t})""".format(t = table)).fetchall()

    jsonstr = ""
    for i in range(len(query)):
        jsonatt = ["\"{c}\" : \"{v}\",".format(c = cname[1], v = cvalue) for cname, cvalue in zip(column_info, query[i]) if cname[1] not in exceptfor]
        jsonrow = ""
        for entry in jsonatt:
            jsonrow+=entry
        jsonrow="{"+jsonrow[:-1]+"},"
        jsonstr+=jsonrow
    jsonstr = "["+jsonstr[:-1]+"]"
    return jsonstr
import sqlite3
import json

def initDB():
    dbconn = sqlite3.connect("pixel.db")
    cursor = dbconn.cursor()

    messages_table =        """ CREATE TABLE IF NOT EXISTS messages (
                                            messageID INTEGER NOT NULL,
                                            userID test NOT NULL,
                                            bucket INTEGER NOT NULL,
                                            time INTEGER NOT NULL,
                                            filename text NOT NULL,

                                            PRIMARY KEY (messageID) 
                                        ); """

    users_table =           """ CREATE TABLE IF NOT EXISTS users (
                                            id text NOT NULL,
                                            name text,
                                            priv text NOT NULL
                                                check (priv in (\'user\', \'admin\')),
                                            account_associated INTEGER NOT NULL,
                                            account_id text,

                                            PRIMARY KEY(id)
                                        ); """
    dbconn.execute(messages_table)
    dbconn.execute(users_table)
    dbconn.close()

    if len(query('messages', args='WHERE userID =\"alpha\"')) == 0:
        insert('messages', '0, \"alpha\", 0, 0, \"\\\"')

def insert(table, vals):
    
    sql_insert= """INSERT INTO {t} VALUES({v});""".format(t=table, v=vals)
    # sql_log = """ INSERT INTO dblog VALUES (\'{c}\', \'insert\', (SELECT datetime())); """.format(c = table + ", " + vals.replace("\'", ""))
    # print(sql_log)
    dbconn = sqlite3.connect("pixel.db")
    cursor = dbconn.cursor()
    cursor.execute(sql_insert)
    # cursor.execute(sql_log)
    dbconn.commit()
    dbconn.close()

def query(table, columns='*', args=''):
    sql_query= """SELECT {c} FROM {t} {a};""".format(c=columns, t=table, a=args)  
    dbconn = sqlite3.connect("pixel.db")
    cursor = dbconn.cursor()    
    cursor.execute(sql_query)
    result = cursor.fetchall()
    dbconn.close()

    return result

def delete(table, args):
    sql_query= """DELETE FROM {t} WHERE {a};""".format(t = table, a = args)
    dbconn = sqlite3.connect("pixel.db")
    cursor = dbconn.cursor()
    cursor.execute(sql_query)
    dbconn.commit()
    dbconn.close()

def update(table, args):
    sql_query= """UPDATE {t} {a};""".format(t = table, a = args)
    dbconn = sqlite3.connect("pixel.db")
    cursor = dbconn.cursor()
    cursor.execute(sql_query)
    dbconn.commit()
    dbconn.close()
    
def tableToJSON(table, query, exceptfor=()):
    dbconn = sqlite3.connect("pixel.db")
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
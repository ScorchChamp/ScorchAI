import sqlite3
import os
from typing import List, Tuple

NO_DATA_ERROR = "<b>No data found!</b>"
INSERT_SUCCEEDED = "Insertion succeedeed!"
ERROR_1 = "<b>ERROR 1: Please report this message</b>"
ERROR_2 = "<b>ERROR 2: </b>Data type is not List!"


class ScorchDB:
    SETUP_FILE = "./queries/Setup.sql"
    DATABASE_FILE = "./clipData/ScorchDB.db"

    def __init__(self):
        self.setupDB()

    def setupDB(self):
        with sqlite3.connect(self.DATABASE_FILE) as con:
            try:
                cur = con.cursor()
                sql_file = open(self.SETUP_FILE)
                sql_as_string = sql_file.read()
                cur.executescript(sql_as_string)
            except Exception as e:
                print(e)
                pass

    def runQuery(self, query, with_headers = False):
        with sqlite3.connect(self.DATABASE_FILE) as con:
            try:
                cur = con.cursor()
                result = cur.execute(query).fetchall()
                returnal = []
                if with_headers:
                    headers = [tpl[0] for tpl in cur.description]
                    returnal.append(tuple(headers))
                returnal.append(result)
                return returnal
            except Exception as e:
                return "{} ({})".format(ERROR_1, e)

    def generateTableFromTupleList(self, tupleList):
        data = tupleList
        print(type(data))
        if type(data) != list:
            return ERROR_2

        returnal = "<table border='1'><tr>"

        for index in data:
            if type(index) == tuple:
                for header in index:
                    returnal += "<th>" + str(header) + "</th>"
            else:
                for row in index:
                    returnal += "<tr>"
                    for column in row: returnal += "<td>" + str(column) + "</td>"
                    returnal += "</tr>"

        returnal += "</table>"
        return returnal

    def getAllTables(self):
        return self.runQuery("SELECT name FROM sqlite_master")

    def getParametersForPriority(self, channel_id, priority):
        return self.runQuery("SELECT game_id, twitch_channel_id FROM categories WHERE youtube_channel_id = '%s' AND prio = %s" % (channel_id, priority))

    def createHTMLFormInsertToDB(self, table_name):
        page = '''
        <style>
            label {
                display: block; 
                margin-bottom: 10px;
            }
            form {max-width: 20%;}
            input {float: right;}
        </style>
        <form method="post"><br>
        '''
        for header in self.runQuery("SELECT * FROM %s" % (table_name), True)[0]:
            page += "<label>{}: <input type=text name={} /></label>".format(header, header)
        page += '''<input type=submit value=submit></form>'''
        return page

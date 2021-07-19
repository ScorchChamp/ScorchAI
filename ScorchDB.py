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

    def generateTableFromQuery(self, query):
        data = self.runQuery(query)
        return self.generateTableFromCursor(data)

    def runQuery(self, query):
        with sqlite3.connect(self.DATABASE_FILE) as con:
            try:
                sel_cur = con.cursor()
                sel_cur.execute(query) 
                return sel_cur
            except Exception as e:
                return "{} ({})".format(ERROR_1, e)

    def generateTableFromCursor(self, cur):
        if type(cur) is str:
            return cur
        data = cur.fetchall()
        if len(data) == 0:
            return self.makeTableFromTupleList([(0,NO_DATA_ERROR)])
        print(data)
        headers = [tuple[0] for tuple in cur.description]
        returnal = headers + data
        returnal = self.makeTableFromTupleList(returnal)
        return returnal
    
    def getTableHeaders(self, table_name):
        with sqlite3.connect(self.DATABASE_FILE) as con:
            try:
                sel_cur = con.cursor()
                sel_cur.execute("SELECT * FROM " + str(table_name)) 
                returnal = sel_cur.fetchall()
                if len(returnal) == 0:
                    returnal = [(0,NO_DATA_ERROR)]
                return [tuple[0] for tuple in sel_cur.description]
            except Exception as e:
                return "{} ({})".format(ERROR_1, e)

    def setupDB(self):
        with sqlite3.connect(self.DATABASE_FILE) as con:
            try:
                cur = con.cursor()
                sql_file = open(self.SETUP_FILE)
                sql_as_string = sql_file.read()
                cur.executescript(sql_as_string)
            except Exception as e:
                print(e)
                # print(e)
                pass

    def makeTableFromTupleList(self, tupleList):
        data = tupleList
        print(type(data))
        if type(data) != list:
            return ERROR_2

        returnal = "<table border='1'><tr>"

        for row in data:
            if type(row) == str:
                returnal += "<th>" + str(row) + "</th>"
            else:
                returnal += "<tr>"
                for column in row:
                    returnal += "<td>" + str(column) + "</td>"
                returnal += "</tr>"

        returnal += "</table>"
        return returnal

    def getAllTables(self):
        return self.runQuery("SELECT name FROM sqlite_master")

    def getParametersForPriority(self, channel_id, priority):
        return self.runQuery("SELECT game_id, twitch_channel_id FROM categories WHERE youtube_channel_id = '%s' AND prio = %s", (channel_id, priority))

    def getHTMLTableFromTable(self, table_name):
        query = "SELECT * FROM" + str(table_name)
        return self.generateTableFromCursor(self.runQuery(query))






    def createHTMLFormInsertToDB(self, table_name):
        page = '''
        <style>
            label, input {
                display: block;
            }
            label {
                margin-bottom: 10px;
            }
        </style>
        <form method="post"><br>
        '''
        for header in self.getTableHeaders(table_name):
            page += "<label>{}: <input type=text name={}></label>".format(header, header)
        page += '''<input type=submit value=submit></form>'''
        return page
        
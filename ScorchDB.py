import sqlite3
import os


class ScorchDB:
    SETUP_FILE = "./queries/Setup.sql"
    DATABASE_FILE = "./clipData/ScorchDB.db"

    def __init__(self):
        self.setupDB()

    def runSELECT(self, query):
        with sqlite3.connect(self.DATABASE_FILE) as con:
            try:
                sel_cur = con.cursor()
                sel_cur.execute(query) 
                return sel_cur.fetchall()
            except Exception as e:
                return "ERROR 1 {}".format(e)

    def setupDB(self):
        with sqlite3.connect(self.DATABASE_FILE) as con:
            try:
                cur = con.cursor()
                sql_file = open(self.SETUP_FILE)
                sql_as_string = sql_file.read()
                cur.executescript(sql_as_string)
                print(sql_as_string)
            except Exception as e:
                print(e)
                # print(e)
                pass

    def getAllTables(self):
        return self.runSELECT("SELECT name FROM sqlite_master")


    def getParametersForPriority(self, channel_id, priority):
        return self.runSELECT("SELECT game_id, twitch_channel_id FROM categories WHERE youtube_channel_id = '%s' AND prio = %s", (channel_id, priority))

from distutils.util import execute
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE_FILE = BASE_DIR + '/database.db'
QUERY_FILE_BASE_DIR = BASE_DIR + "/queries/"


def serializeCursor(cursor):
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results

def selectQuery(query: str, *, params:list = []):
    cursor = executeQuery(query, params=params)
    return serializeCursor(cursor)

def executeQuery(query: str, *, params:list = []):
    with sqlite3.connect(DATABASE_FILE) as connection:
        connection.execute("PRAGMA foreign_keys = 1;")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(query, params)
    return cursor


def runFileQuery(file: str, *, params: list = []):
    with open(QUERY_FILE_BASE_DIR + file, 'r') as f:
        queries = f.read()
        for query in queries.split(";"):
            try:
                executeQuery(query, params=params)
            except Exception as e:
                print(e)
                pass

if not os.path.isfile(DATABASE_FILE):
    runFileQuery("Setup.sql")
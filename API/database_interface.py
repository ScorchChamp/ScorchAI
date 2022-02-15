import sqlite3


def serializeCursor(cursor):
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results

def selectQuery(query: str, *, params:list = []):
    with sqlite3.connect('database.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(query, params)
    return serializeCursor(cursor)


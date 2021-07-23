from flask import Flask, redirect, url_for, request, session
import os
from ScorchDB import ScorchDB

db = ScorchDB()

app = Flask(__name__)
app.secret_key = os.urandom(16)

is_admin = False

@app.route("/", methods=['GET'])
def index():
    resultList = db.runQuery("SELECT * FROM youtube_channel", True)
    page = db.generateTableFromTupleList(resultList)
    page += "<br><br><br>"
    page += db.createHTMLFormInsertToDB("youtube_channel")
    return page

@app.route("/", methods=['POST'])
def insert():
    data = request.data
    page = ""
    
    return page



@app.route('/test')
def testPage():
    resultList = db.runQuery("SELECT * FROM sqlite_master", True)
    page = db.generateTableFromTupleList(resultList)
    return page


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6969', debug=True)
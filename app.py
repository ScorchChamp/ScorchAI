from flask import Flask, redirect, url_for, request, session
import os
from ScorchDB import ScorchDB

db = ScorchDB()

app = Flask(__name__)
app.secret_key = os.urandom(16)

is_admin = False

@app.route("/")
def index():
    page = db.generateTableFromQuery("SELECT DISTINCT * FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'")
    page += "<br><br><br>"
    page += db.createHTMLFormInsertToDB("sqlite_master")
    return page
    
@app.route('/insertpage', methods=['GET', 'POST'])
def runInsert():
    if request.method == 'POST':
        session['query'] = request.form['query']
        returnal = db.generateTableFromQuery(session['query'])
        return returnal
    return '''
        <form method="post">
            <p><input type=text name=query>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/getTables', methods=['GET', 'POST'])
def runSelect():
    if request.method == 'GET':
        page = db.generateTableFromQuery("SELECT * FROM {}".format(request.form['table']))
        return page

@app.route('/test')
def testPage():
    page = db.generateTableFromQuery("SELECT * FROM sqlite_master")
    return page


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6969', debug=True)
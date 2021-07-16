from flask import Flask, redirect, url_for, request, session
import os
from ScorchDB import ScorchDB

db = ScorchDB()

app = Flask(__name__)
app.secret_key = os.urandom(16)

is_admin = False

@app.route("/")
def index():
    page = db.makeTableFromSelect("SELECT DISTINCT * FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'")
    page += "<br><br><br>"
    page += db.createHTMLFormInsertToDB("sqlite_master")
    return page
    
@app.route('/runinsert', methods=['GET', 'POST'])
def runInsert():
    if request.method == 'POST':
        session['query'] = request.form['query']
        returnal = db.runINSERT(session['query'])
        return returnal
    return '''
        <form method="post">
            <p><input type=text name=query>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/runselect', methods=['GET', 'POST'])
def runSelect():
    page = db.makeTableFromSelect("SELECT * FROM twitch_channel")
    return 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug=True)
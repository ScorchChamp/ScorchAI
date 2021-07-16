from flask import Flask, redirect, url_for, request, session
import os
from ScorchDB import ScorchDB

db = ScorchDB()

app = Flask(__name__)
app.secret_key = os.urandom(16)

is_admin = False

@app.route("/")
def index():
    res = db.getAllTables()
    if res is None:
        res = ""
    return res

@app.route('/runselect', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['query'] = request.form['query']
        returnal = ""
        for r in db.runSELECT(session['query']):
            returnal += r[1]
            print(r)
        return returnal
    return '''
        <form method="post">
            <p><input type=text name=query>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
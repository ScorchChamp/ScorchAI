from flask import Flask, send_from_directory
from flask_restful import Resource, Api
from endpoints import *
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
api = Api(app)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 
                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

api.add_resource(Categories.Categories, '/categories')
api.add_resource(Channels.Channel, '/channel/<id>')
api.add_resource(Channels.Channels, '/channels')
api.add_resource(Clips.Clips, '/clips')
api.add_resource(Clips.Clip, '/clips/<id>')
api.add_resource(Clips.NextClipForChannel, '/nextclipforchannel')
api.add_resource(Users.Users, '/users')
api.add_resource(Users.User, '/user/<id>')
api.add_resource(Main.Main, '/')

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
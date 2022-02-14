from flask import Flask
from flask_restful import Resource, Api
import pandas as pd
import ast
from endpoints import *

class Main(Resource):
    def get(self):
        return {"status": "Ready for take-off!"}





app = Flask(__name__)
api = Api(app)
api.add_resource(Broadcasters.Broadcasters, '/broadcasters')
api.add_resource(Categories.Categories, '/categories')
api.add_resource(Channels.Channel, '/channel')
api.add_resource(Channels.Channels, '/channels')
api.add_resource(Clips.Clips, '/clips')
api.add_resource(Main, '/')



if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0')
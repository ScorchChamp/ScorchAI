import database_interface as db
from flask_restful import Resource
from flask import request

class Broadcasters(Resource):
    def get(self):
        return {"data": db.selectQuery("SELECT * FROM Broadcasters")}

class Broadcaster(Resource):
    def get(self):
        id = request.args.get('id')  
        return {"given_id": id}
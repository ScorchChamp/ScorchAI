import database_interface as db
from flask_restful import Resource
from flask import request

class Channels(Resource):
    def get(self):
        return {"data": db.selectQuery("SELECT * FROM Channels")} # TODO: Update with sql file

class Channel(Resource):
    def get(self, id):
        if id: params = id
        else: params = "%"
        return {
            "data": db.selectQuery("SELECT * FROM Channels WHERE Channel_ID LIKE ?", params=(params,)) # TODO: Update with sql file
        }

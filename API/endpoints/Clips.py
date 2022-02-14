import database_interface as db
from flask_restful import Resource, Api, reqparse

class Clips(Resource):
    def get(self):
        return {"data": db.selectQuery("SELECT * FROM Clips")}

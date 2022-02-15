import database_interface as db
from flask_restful import Resource

class Users(Resource):
    def get(self):
        return {"data": db.selectQuery("SELECT * FROM Users")} # TODO: Update with sql file

class User(Resource):
    def get(self, id):
        if id: params = id
        else: params = "%"
        return {
            "data": db.selectQuery("SELECT * FROM Users WHERE User_ID LIKE ?", params=(params,)) # TODO: Update with sql file
        }

import database_interface as db
from flask_restful import Resource

class Categories(Resource):
    def get(self):
        return {"data": db.selectQuery("SELECT * FROM Categories")} # TODO: Update with sql file

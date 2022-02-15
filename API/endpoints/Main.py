import database_interface as db
from flask_restful import Resource

class Main(Resource):
    def get(self):
        return {"status": "Ready for take-off!"}, 200

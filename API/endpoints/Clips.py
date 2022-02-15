import database_interface as db
from flask_restful import Resource, Api, reqparse

class Clips(Resource):
    def get(self):
        return {"data": db.runFileQuery("selectClips.sql")} # TODO: Update with sql file

class Clip(Resource):
    def get(self, id):
        if id: params = id
        else: params = "%"
        return {
            "data": db.selectQuery("SELECT * FROM Clips WHERE Clip_ID LIKE ?", params=(params,)) # TODO: Update with sql file
        }
class NextClipForChannel(Resource):
    def get(self):
        return {"data": db.runFileQuery("selectNotUploadedClip.sql", ('a', 'a'))} # TODO: Update with sql file



import database_interface as db
from flask_restful import Resource, Api, reqparse

class Clips(Resource):
    def get(self):
        return {"data": db.selectQuery("SELECT * FROM Clips")} # TODO: Update with sql file

class Clip(Resource):
    def get(self, id):
        if id: params = id
        else: params = "%"
        return {
            "data": db.selectQuery("SELECT * FROM Clips WHERE Clip_ID LIKE ?", params=(params,)) # TODO: Update with sql file
        }

class NextClipForChannel(Resource):
    def get(self, id):
        return {"data": db.runFileQuery("selectNotUploadedClip.sql", params=(id, id))} # TODO: Update with sql file


parser = reqparse.RequestParser()
parser.add_argument('Clip_ID')
parser.add_argument('Channel_ID')
parser.add_argument('upload_date')

class ClipUploaded(Resource):
    def post(self):
        args = parser.parse_args()
        db.executeQuery("INSERT INTO Clips_Uploaded_To_Channel VALUES (?, ?, ?)", params=(args['Clip_ID'],args['Channel_ID'],args['upload_date'])) # TODO: Update with sql file
        return {"message": "success"}
import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
import os
import sys
from assets import constants

class YoutubeAPI:
    def __init__(self): 
        self.SERVICE = Create_Service(constants.CLIENTSECRETS_FILE, constants.API_NAME, constants.API_VERSION, constants.SCOPES)

    def uploadVideo(self, file, title, description, tags, uploadDate = datetime.datetime.now()):
        request_body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': 20
            },
            'status': self.generateStatus(uploadDate),
            'notifySubscribers': True
        }
        self.insert(request_body, file)

    def generateStatus(self, uploadDate, forKids = False):
         status = constants.VIDEO_STATUS
         status["publishAt"] = uploadDate.isoformat()
         return status

    def insert(self, request_body, file):
        print(file)
        mediaFile = MediaFileUpload(file)
        response_upload = self.SERVICE.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body= mediaFile
        ).execute()

    def upload_thumbnail(video_id, file):
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=file
        ).execute()
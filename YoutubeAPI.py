import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
import os
import sys

class YoutubeAPI:
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    CLIENT_SECRET_FILE = ''
    SERVICE = ''
        
    def __init__(self, CLIENT_SECRET_FILE): 
        self.CLIENT_SECRET_FILE = CLIENT_SECRET_FILE
        self.SERVICE = Create_Service(self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES)

    def uploadVideo(self, file, title, description, tags, uploadDate = datetime.datetime.now()):
        request_body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags
            },
            'status': self.generateStatus(uploadDate),
            'notifySubscribers': True
        }
        self.insert(request_body, file)

    def generateStatus(self, uploadDate, forKids = False):
         return {
                'privacyStatus': 'private',
                'publishAt': uploadDate.isoformat(),
                'selfDeclaredMadeForKids': forKids
            }

    def insert(self, request_body, file):
        print(file)
        mediaFile = MediaFileUpload(file)
        response_upload = self.SERVICE.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body= mediaFile
        ).execute()
import datetime
from assets.Google import Create_Service
from googleapiclient.http import MediaFileUpload
import os
import sys

class YoutubeAPI:
    def __init__(self, clientSecretsFile): 
        self.SERVICE = Create_Service(clientSecretsFile, 'youtube', 'v3', ['https://www.googleapis.com/auth/youtube.upload'])

    def uploadVideo(self, file, title, description, tags):
        request_body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': 20
            },
            'status': self.generateStatus(),
            'notifySubscribers': True
        }
        self.insert(request_body, file)

    def generateStatus(self):
         status = {
            'privacyStatus': 'private',
            'selfDeclaredMadeForKids': False
        }
         return status

    def insert(self, request_body, file):
        print(request_body, file)
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
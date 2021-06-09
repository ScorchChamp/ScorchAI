import datetime
import random
import time

from urllib.error import HTTPError
import httplib2
import http

from assets.Google import Create_Service
from googleapiclient.http import MediaFileUpload
import os
import sys

class YoutubeAPI:
    status = {
        'privacyStatus': 'public',
        'selfDeclaredMadeForKids': False
    }
    def __init__(self, clientSecretsFile): 
        self.SERVICE = Create_Service(clientSecretsFile, 'youtube', 'v3', ['https://www.googleapis.com/auth/youtube.upload'])

    def uploadVideo(self, file, title, description, tags):
        request_body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': 10
            },
            'status': self.status,
            'notifySubscribers': True
        }
        self.insert(request_body, file)

    def insert(self, request_body, file):
        mediaFile = MediaFileUpload(file, chunksize=-1, resumable=True)
        response_upload = self.SERVICE.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body= mediaFile
        )

        httplib2.RETRIES = 1
        MAX_RETRIES = 10
        RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
        RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
            http.client.IncompleteRead, http.client.ImproperConnectionState,
            http.client.CannotSendRequest, http.client.CannotSendHeader,
            http.client.ResponseNotReady, http.client.BadStatusLine)
        response = None
        error = None
        retry = 0
        video_id = ''
        while response is None:
            try:
                print("Uploading file " + file)
                print(response_upload)
                status, response = response_upload.next_chunk()
                if response is not None:
                    if 'id' in response:
                        video_id = response['id']
                        print("Video id '%s' was successfully uploaded." % response['id'])
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
            except HTTPError as e:
                if e.resp.status in RETRIABLE_STATUS_CODES:
                    error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,e.content)
                else:
                    raise
            except RETRIABLE_EXCEPTIONS as e:
                error = "A retriable error occurred: %s" % e

            if error is not None:
                print(error)
                retry += 1
                if retry > MAX_RETRIES:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print("Sleeping %f seconds and then retrying..." % sleep_seconds)
                time.sleep(sleep_seconds)
                
    def upload_thumbnails(self, thumbnail = False):
        if not thumbnail:
            print("No thumbnail specified, skipping upload")
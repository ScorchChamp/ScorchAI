import pickle
import os
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import random
import time
from urllib.error import HTTPError
import httplib2
import http
from googleapiclient.http import MediaFileUpload

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
httplib2.RETRIES = 1
MAX_RETRIES = 10
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
http.client.IncompleteRead, http.client.ImproperConnectionState,
http.client.CannotSendRequest, http.client.CannotSendHeader,
http.client.ResponseNotReady, http.client.BadStatusLine)

def Create_Service(channel, client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'{BASE_DIR}/auth/{channel}.pickle'
    print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(api_name, api_version, credentials=cred)
        print(api_name, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def Upload_Video(request_body, file, channel):
        print(f"Uploading {file}")
        service = Create_Service(channel, f"{BASE_DIR}/auth/client_secrets.json", 'youtube', 'v3', ['https://www.googleapis.com/auth/youtube.upload'])
        mediaFile = MediaFileUpload(file, chunksize=-1, resumable=True)
        response_upload = service.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body= mediaFile
        )
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


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt


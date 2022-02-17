import requests
import datetime

API_SOCKET = 'http://localhost:8000'

def getChannelData(Channel_ID: str):
    try:
        return requests.get(f'{API_SOCKET}/channel/{Channel_ID}').json()['data'][0]
    except:
        print("Channel does not exist!")
        exit(-1)
        
def getCategories(Channel_ID: str):
    try:
        return requests.get(f'{API_SOCKET}/categories/{Channel_ID}').json()['data']
    except:
        print("Channel does not have a category!")
        exit(-1)
        
def getNextClip(Channel_ID: str, *, game_id: str = None, broadcaster_id: str = None):
    assert game_id or broadcaster_id
    valid_clips = []
    try:
        clips = requests.get(f'{API_SOCKET}/nextclipforchannel/{Channel_ID}').json()['data']
        for clip in clips:
            
            if game_id and clip['Game_id'] == game_id: valid_clips.append(clip)
            if broadcaster_id and clip['Broadcaster_id'] == broadcaster_id: valid_clips.append(clip)
        return valid_clips
    except:
        print("Channel does not have a valid clip!")

        
def insertUpload(Clip_ID: str, Channel_ID: str):
    requests.post(f'{API_SOCKET}/clipuploaded', params={
        "Clip_ID": Clip_ID,
        "Channel_ID": Channel_ID,
        "upload_date": datetime.datetime.now()
    }).json()
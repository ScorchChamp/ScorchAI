import API.Authorizer as Authorizer
import requests
import urllib
import time
CLIPS_FOLDER = './videos/clips/'
PREP_STAGE = './videos/prepstage/'
READY_STAGE = './videos/ready_to_upload/'
UPLOADED_STAGE = './videos/uploaded_clips/'

def getChannelID(name):
    parameters = {
        "login": name
    }
    while True: 
        res = requests.get("https://api.twitch.tv/helix/users", parameters, headers=Authorizer.getHeaders()).json()
        if "error" in res:
            time.sleep(1)
            print(f"Error code: {res['status']}")
            if res["status"] == 401:
               Authorizer.refreshOAUTH()
            else:
                print(f"SOMETHING WENT WRONG: {res}")
        else:
            if len(res['data']):
                print(res['data'][0])
                return res['data'][0]["id"]
            else:
                return "-1"


def downloadClip(clip):
    try:    
        download_url(getMp4UrlFromClip(clip), f"{READY_STAGE}{clip['id']}.mp4", clip['id']) 
        return True
    except: 
        print("Download failed.")
        return False

def getClipsList(parameters):
    while True: 
        res = requests.get("https://api.twitch.tv/helix/clips", parameters, headers=Authorizer.getHeaders()).json()
        if "error" in res:
            time.sleep(1)
            print(f"Error code: {res['status']}")
            if res["status"] == 401:
               Authorizer.refreshOAUTH()
            else:
                print(f"SOMETHING WENT WRONG: {res}")
        else:
            return res['data']

def download_url(url, output_path, title):
        print(f"Downloading {title}")
        urllib.request.urlretrieve(url, filename=output_path)
        print("Download done!")


def getMp4UrlFromClip(clip):
    return clip['thumbnail_url'].split("-preview")[0] + ".mp4"


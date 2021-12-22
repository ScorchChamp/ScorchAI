import API.Authorizer as Authorizer
import requests
import urllib
import time

def downloadClip(clip):
    try:    
        download_url(getMp4UrlFromClip(clip), f"./videos/clips/{clip['id']}.mp4", clip['id']) 
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
            return res

def download_url(url, output_path, title):
        print(f"Downloading {title}")
        urllib.request.urlretrieve(url, filename=output_path)
        print("Download done!")


def getMp4UrlFromClip(clip):
    return clip['thumbnail_url'].split("-preview")[0] + ".mp4"


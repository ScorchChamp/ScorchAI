from assets.Authorizer import Authorizer
import requests
import urllib
import time

class TwitchAPI:
    def __init__(self, authFile): 
        self.authorizer = Authorizer("./auth/auth.json")

    def downloadClip(self, clip):
        try:    
            download_url(getMp4UrlFromClip(clip), f"./videos/clips/{clip['id']}.mp4", clip['id']) 
            return True
        except: 
            print("Download failed.")
            return False

    def getClipsList(self, parameters):
        while True: 
            res = requests.get("https://api.twitch.tv/helix/clips", parameters, headers=self.authorizer.getHeaders()).json()
            if "error" in res:
                time.sleep(1)
                print(f"Error code: {res['status']}")
                if res["status"] == 401:
                    self.authorizer.refreshOAUTH()
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


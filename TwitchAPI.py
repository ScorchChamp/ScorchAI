from assets.Authorizer import Authorizer
import requests
import urllib

class TwitchAPI:
    def __init__(self, authFile): 
        self.authorizer = Authorizer("./auth/auth.json")

    def downloadClip(self, clipID, downloadURL):
        try:    
            download_url(downloadURL, "./videos/clips/{}.mp4".format(clipID), clipID) 
        except: 
            print("Download failed...{}".format(downloadURL))

    def getClipsList(self, parameters):
        return requests.get("https://api.twitch.tv/helix/clips", parameters, headers=self.authorizer.getHeaders()).json()

def download_url(url, output_path, title):
        print("Downloading {}".format(title))
        urllib.request.urlretrieve(url, filename=output_path)
        print("Download done!")


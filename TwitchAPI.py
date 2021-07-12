from assets.Authorizer import Authorizer
import requests
import urllib

class TwitchAPI:
    def __init__(self, authFile): 
        self.authorizer = Authorizer("./auth/auth.json")

    def downloadClip(self, clipID, downloadURL):
        try:    
            download_url(downloadURL, "./videos/clips/{}.mp4".format(clipID), clipID) 
            return True
        except: 
            print("Download failed...{}".format(downloadURL))
            return False

    def getClipsList(self, parameters):
        while True: 
            res = requests.get("https://api.twitch.tv/helix/clips", parameters, headers=self.authorizer.getHeaders()).json()
            if "error" in res:
                print("Error code: {}".format(res['status']))
                if res["status"] == 401:
                    self.authorizer.refreshOAUTH()
                else:
                    print("SOMETHING WENT WRONG: {}".format(res))
            else:
                return res

def download_url(url, output_path, title):
        print("Downloading {}".format(title))
        urllib.request.urlretrieve(url, filename=output_path)
        print("Download done!")


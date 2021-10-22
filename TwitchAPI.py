from assets.Authorizer import Authorizer
import requests
import urllib

class TwitchAPI:
    def __init__(self, authFile): 
        self.authorizer = Authorizer("./auth/auth.json")

    def downloadClip(self, clipID, downloadURL):
        try:    
            download_url(downloadURL, f"./videos/clips/{clipID}.mp4", clipID) 
            return True
        except: 
            print(f"Download failed...{downloadURL}")
            return False

    def getClipsList(self, parameters):
        while True: 
            res = requests.get("https://api.twitch.tv/helix/clips", parameters, headers=self.authorizer.getHeaders()).json()
            if "error" in res:
                print(f"Error code: {res['status']}")
                if res["status"] == 401:
                    self.authorizer.refreshOAUTH()
                else:
                    print(f"SOMETHING WENT WRONG: {res}")
            else:
                return res
    
    def getIDFromName(self, id):
        parameters = {
            "login": id
        }
        while True: 
            res = requests.get("https://api.twitch.tv/helix/users", parameters, headers=self.authorizer.getHeaders()).json()
            if "error" in res:
                print(f"Error code: {res['status']}")
                if res["status"] == 401:
                    self.authorizer.refreshOAUTH()
                else:
                    print(f"SOMETHING WENT WRONG: {res}")
            else:
                return res["data"][0]["id"]

def download_url(url, output_path, title):
        print(f"Downloading {title}")
        urllib.request.urlretrieve(url, filename=output_path)
        print("Download done!")


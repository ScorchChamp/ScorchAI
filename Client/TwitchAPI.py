import requests
import time
import Authorizer

def getClipsList(parameters):
    while True: 
        res = requests.get("https://api.twitch.tv/helix/clips", parameters, headers=Authorizer.getHeaders()).json()
        if "error" in res:
            time.sleep(1)
            print(f"Error code: {res['status']}")
            if res["status"] == 401: Authorizer.refreshOAUTH()
            else: print(f"SOMETHING WENT WRONG: {res}")
        else: return res['data']
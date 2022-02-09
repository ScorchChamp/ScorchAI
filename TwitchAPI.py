import requests
import Authorizer
import time

class TwitchAPI:
    def getAPICallData(self, url, parameters):
        max_retries = 3
        current_tries = 0
        while True: 
            res = requests.get(url, parameters, headers=Authorizer.getHeaders()).json()
            print(parameters)
            if "error" in res:
                time.sleep(1)
                print(f"Error code: {res['status']}")
                if res["status"] == 401:
                    Authorizer.refreshOAUTH()
                else:
                    current_tries += 1
                    print(f"SOMETHING WENT WRONG: {res}")
                    if current_tries > max_retries:
                        break
            else:
                return res

    def getClipsList(self, parameters):
        data = self.getAPICallData("https://api.twitch.tv/helix/clips", parameters)
        if data: return data['data']
        else: return {}

    def getGameData(self, *, game_id: int = None, game_name: str = None):
        data = {"data": []}
        if game_id:
            data = self.getAPICallData("https://api.twitch.tv/helix/games", {"id": game_id})
        elif game_name:
            data = self.getAPICallData("https://api.twitch.tv/helix/games", {"name": game_name})
        if data: return data['data']
        else: return {}

    def getUserData(self, *, user_id: int = None, user_name: str = None):
        data = {"data": []}
        if user_id:
            data = self.getAPICallData("https://api.twitch.tv/helix/users", {"id": user_id})
        if user_name:
            data = self.getAPICallData("https://api.twitch.tv/helix/users", {"login": user_name})
        if data: return data['data']
        else: return {}

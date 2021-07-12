import json
import requests

class Authorizer:
    OAUTH = ""
    CLIENT_ID = ""
    AUTH_DATA = ""

    def __init__(self, authDataFile): 
        self.authDataFile = authDataFile
        self.generateData()
    
    def generateData(self):
        self.AUTH_DATA  = self.readAuthFile()
        self.OAUTH      = self.AUTH_DATA['twitch']['OAUTH']
        self.CLIENT_ID  = self.AUTH_DATA['twitch']['client-id']
        self.CLIENT_SECRET  = self.AUTH_DATA['twitch']['client-secret']
        self.REFRESH_TOKEN  = self.AUTH_DATA['twitch']['refresh-token']
        self.REDIRECT_URI = self.AUTH_DATA['twitch']['redirect-uri']

    def getHeaders(self):
        self.generateData()
        return {
            "Authorization": self.OAUTH, 
            "Client-Id": self.CLIENT_ID
        }
 
    def readAuthFile(self):
        with open(self.authDataFile) as authData:
            return json.load(authData)

    def refreshOAUTH(self):
        print("GENERATING NEW OAUTH TOKEN")
        self.generateData()
        url = "https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&redirect_uri={}&refresh_token={}&grant_type=refresh_token"
        res = requests.post(url.format(self.CLIENT_ID,self.CLIENT_SECRET,self.REDIRECT_URI,self.REFRESH_TOKEN)).json()
        print(res)
        self.saveRefresh(res['token_type'].capitalize() + " " + res['access_token'], res['refresh_token'])
    
    def saveRefresh(self, oauth_token, refresh_token):
        with open(self.authDataFile) as f:
            data = json.load(f)

        data["twitch"]["refresh-token"] = refresh_token
        data["twitch"]["OAUTH"] = oauth_token
        with open(self.authDataFile, 'w') as f:
            json.dump(data, f)

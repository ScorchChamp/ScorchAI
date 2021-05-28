import json

class Authorizer:
    OAUTH = ""
    CLIENT_ID = ""
    AUTH_DATA = ""

    def __init__(self, authDataFile): 
        self.AUTH_DATA  = self.readAuthFile(authDataFile)
        self.OAUTH      = self.AUTH_DATA['twitch']['OAUTH']
        self.CLIENT_ID  = self.AUTH_DATA['twitch']['client-id']
    
    def getHeaders(self):
        return {
            "Authorization": self.OAUTH, 
            "Client-Id": self.CLIENT_ID
        }
 
    def readAuthFile(self, authDataFile):
        with open(authDataFile) as authData:
            return json.load(authData)

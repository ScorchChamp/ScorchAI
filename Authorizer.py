
import json
class Authorizer:
    OAUTH = ""
    CLIENT_ID = ""
    AUTH_DATA = ""

    def __init__(self, authDataFile): 
        self.AUTH_DATA = self.readAuthFile(authDataFile)
        self.OAUTH = self.getTOAUTHFromAuthData(self.AUTH_DATA)
        self.CLIENT_ID = self.getClientIdFromAuthData(self.AUTH_DATA)
    
    def getHeaders(self):
        return {"Authorization": self.OAUTH, "Client-Id": self.CLIENT_ID}
        
    def getClientIdFromAuthData(self, authData):  
        return authData['twitch']['client-id']

    def getTOAUTHFromAuthData(self, authData): 
        return authData['twitch']['OAUTH']

    def readAuthFile(self, authDataFile):
        with open(authDataFile) as authData:
            return json.load(authData)

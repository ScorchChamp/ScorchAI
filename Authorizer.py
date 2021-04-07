
import json
class Authorizer:
    OAUTH = ""
    ClientId = ""
    authorisationData = ""

    def __init__(self, authDataFile): 
        self.authorisationData = self.readAuthFile(authDataFile)
        self.OAUTH = self.getTOAUTHFromAuthData(self.authorisationData)
        self.ClientId = self.getClientIdFromAuthData(self.authorisationData)
    
    def getHeaders(self):
        return {"Authorization": self.OAUTH, "Client-Id": self.ClientId}
        
    def getClientIdFromAuthData(self, authData):  
        return authData['twitch']['client-id']

    def getTOAUTHFromAuthData(self, authData): 
        return authData['twitch']['OAUTH']

    def readAuthFile(self, authDataFile):
        with open(authDataFile) as authData:
            return json.load(authData)

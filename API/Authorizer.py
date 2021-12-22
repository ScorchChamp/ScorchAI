import json
import requests

OAUTH = ""
CLIENT_ID = ""
AUTH_DATA = ""
CLIENT_SECRET = ""
REFRESH_TOKEN  = ""
REDIRECT_URI = ""
authDataFile = "./auth/auth.json"
    
def generateData():
    AUTH_DATA  = readAuthFile()
    OAUTH      = AUTH_DATA['twitch']['OAUTH']
    CLIENT_ID  = AUTH_DATA['twitch']['client-id']
    CLIENT_SECRET  = AUTH_DATA['twitch']['client-secret']
    try:
        REFRESH_TOKEN  = AUTH_DATA['twitch']['refresh-token']
        REDIRECT_URI = AUTH_DATA['twitch']['redirect-uri']
    except:
        REFRESH_TOKEN = ""
        REDIRECT_URI = "https://localhost"
    return {
        'client_id': AUTH_DATA['twitch']['client-id'],
        'client_secret': AUTH_DATA['twitch']['client-secret'],
        'redirect_uri': AUTH_DATA['twitch']['redirect-uri'],
        'refresh_token': AUTH_DATA['twitch']['refresh-token'],
        'oauth': AUTH_DATA['twitch']['OAUTH']
    }

def getHeaders():
    data = generateData()
    return {
        "Authorization": data['oauth'], 
        "Client-Id": data['client_id']
    }

def readAuthFile():
    with open(authDataFile) as authData:
        return json.load(authData)

def refreshOAUTH():
    print("GENERATING NEW OAUTH TOKEN")
    data = generateData()
    res = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={data['client_id']}&client_secret={data['client_secret']}&redirect_uri={data['redirect_uri']}&refresh_token={data['refresh_token']}&grant_type=refresh_token").json()
    print(res)
    saveRefresh(res['token_type'].capitalize() + " " + res['access_token'], res['refresh_token'])

def saveRefresh(oauth_token, refresh_token):
    with open(authDataFile) as f:
        data = json.load(f)

    data["twitch"]["refresh-token"] = refresh_token
    data["twitch"]["OAUTH"] = oauth_token
    with open(authDataFile, 'w') as f:
        json.dump(data, f)

generateData()
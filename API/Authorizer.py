import json
import requests

OAUTH = ""
CLIENT_ID = ""
AUTH_DATA = ""
CLIENT_SECRET = ""
REFRESH_TOKEN  = ""
REDIRECT_URI = ""
AUTH_DATA_FILE = "./auth/auth.json"
    
def generateData():
    AUTH_DATA  = readAuthFile()
    return {
        'client_id': AUTH_DATA['client_id'],
        'client_secret': AUTH_DATA['client_secret'],
        'redirect_uri': AUTH_DATA['redirect_uri'],
        'refresh_token': AUTH_DATA['refresh_token'],
        'oauth': AUTH_DATA['oauth']
    }

def getHeaders():
    data = generateData()
    return {
        "Authorization": data['oauth'], 
        "Client-Id": data['client_id']
    }

def readAuthFile():
    return json.load(open(AUTH_DATA_FILE))

def refreshOAUTH():
    print("GENERATING NEW OAUTH TOKEN")
    data = generateData()
    res = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={data['client_id']}&client_secret={data['client_secret']}&redirect_uri={data['redirect_uri']}&refresh_token={data['refresh_token']}&grant_type=refresh_token").json()
    print(res)
    saveRefresh(res['token_type'].capitalize() + " " + res['access_token'], res['refresh_token'])

def saveRefresh(oauth_token, refresh_token):
    data = generateData()
    data["refresh_token"] = refresh_token
    data["oauth"] = oauth_token

    with open(AUTH_DATA_FILE, 'w') as f:
        json.dump(data, f)
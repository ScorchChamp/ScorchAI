import json
import requests
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
AUTH_DATA_FILE = f'{BASE_DIR}/auth/auth.json'
    
def getHeaders():
    data = readAuthFile()
    return {
        'Authorization': data['oauth'], 
        'Client-Id': data['client_id']
    }

def readAuthFile():
    return json.load(open(AUTH_DATA_FILE))

def refreshOAUTH():
    print('GENERATING NEW OAUTH TOKEN')
    data = readAuthFile()
    res = requests.post(f'https://id.twitch.tv/oauth2/token', params = {
        'client_id': data['client_id'],
        'client_secret': data['client_secret'],
        'redirect_uri': data['redirect_uri'],
        'refresh_token': data['refresh_token'],
        'grant_type': 'refresh_token'
    }).json()
    print(res)
    saveRefresh(res['token_type'].capitalize() + ' ' + res['access_token'], res['refresh_token'])

def saveRefresh(oauth_token, refresh_token):
    data = readAuthFile()
    data['refresh_token'] = refresh_token
    data['oauth'] = oauth_token

    with open(AUTH_DATA_FILE, 'w') as f:
        json.dump(data, f)
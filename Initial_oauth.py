import webbrowser
import requests
import API.Authorizer as Authorizer
import json

AUTH_FILE = "./auth/auth.json"

data = Authorizer.generateData()
webbrowser.open(f"https://id.twitch.tv/oauth2/authorize?response_type=code&client_id={data['client_id']}&redirect_uri={data['redirect_uri']}&scope=channel:moderate&state=c3ab8aa609ea11e793ae92361f002671")

code = input("Paste code after ?code=\n")
res = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={data['client_id']}&client_secret={data['client_secret']}&code={code}&grant_type=authorization_code&redirect_uri={data['redirect_uri']}").json()
print(res)

with open(AUTH_FILE) as f:
    data = json.load(f)

data["twitch"]["refresh-token"] = res["refresh_token"]
data["twitch"]["OAUTH"] = f"{res['token_type']} {res['access_token']}"

with open(AUTH_FILE, 'w') as f:
    json.dump(data, f)
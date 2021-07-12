import webbrowser
import requests
from assets.Authorizer import Authorizer
import json

AUTH_FILE = "./auth/auth.json"

authorizer = Authorizer(AUTH_FILE)

url = "https://id.twitch.tv/oauth2/authorize?response_type=code&client_id={}&redirect_uri={}&scope=channel:moderate&state=c3ab8aa609ea11e793ae92361f002671"
webbrowser.open(url.format(authorizer.CLIENT_ID, authorizer.REDIRECT_URI))  # Go to example.com
code = input("Paste code after ?code=\n")

url = "https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&code={}&grant_type=authorization_code&redirect_uri={}"
res = requests.post(url.format(authorizer.CLIENT_ID, authorizer.CLIENT_SECRET, code,authorizer.REDIRECT_URI)).json()

print(res)
with open(AUTH_FILE) as f:
    data = json.load(f)

data["twitch"]["refresh-token"] = res["refresh_token"]
data["twitch"]["OAUTH"] = "{} {}".format(res["token_type"], res["access_token"])
with open(AUTH_FILE, 'w') as f:
    json.dump(data, f)
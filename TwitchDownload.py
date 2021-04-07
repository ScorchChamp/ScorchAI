import requests
import json
from datetime import datetime, timezone 
import urllib.request
import sys
from DataCollector import DataCollector
import datetime
import os

uploaded_folder = "./clips/uploaded/"
dc = DataCollector("./assets/auth.json", './assets/client_secrets.json', "./clips/", "./clipData/")
try:
    for file in os.listdir(uploaded_folder):
        os.remove(uploaded_folder + file)
except:
    pass

yesterday_date_iso = datetime.datetime.now() - datetime.timedelta(days=1)
yesterday_date_formatted = yesterday_date_iso.strftime("%Y-%m-%dT%H:%M:%SZ")


 # JUST CHATTING = 509658 || MINECRAFT = 27471 || AMONG US = 510218 || CHESS = 743
dc.generateClipsFromData("https://api.twitch.tv/helix/clips", {"game_id": "509658",  "first": "8", "started_at": yesterday_date_formatted}) # JUST CHATTING
dc.generateClipsFromData("https://api.twitch.tv/helix/clips", {"game_id": "27471",  "first": "8", "started_at": yesterday_date_formatted}) # MINECRAFT
dc.generateClipsFromData("https://api.twitch.tv/helix/clips", {"game_id": "510218",  "first": "4", "started_at": yesterday_date_formatted}) # AMONG US
dc.generateClipsFromData("https://api.twitch.tv/helix/clips", {"game_id": "743",  "first": "4", "started_at": yesterday_date_formatted}) # CHESS
dc.downloadClipsListToFolder()


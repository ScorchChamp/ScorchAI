import requests
import json
from datetime import datetime, timezone 
import urllib.request
import sys
from DataCollector import DataCollector
import datetime
import os

CLIPS_LINK = "https://api.twitch.tv/helix/clips"
UPLOADED_FOLDER = "./clips/uploaded/"

YESTERDAY_DATE_ISO = datetime.datetime.now() - datetime.timedelta(days=1)
YESTERDAY_DATE_FORMATTED = YESTERDAY_DATE_ISO.strftime("%Y-%m-%dT%H:%M:%SZ")

try:
    for file in os.listdir(UPLOADED_FOLDER):
        os.remove(UPLOADED_FOLDER + file)
except:
    pass


dc = DataCollector("./assets/auth.json", './assets/client_secrets.json', "./clips/", "./clipData/")
dc.generateClipsFromData(CLIPS_LINK, {
    "game_id": "509658",   # JUST CHATTING
    "first": "8", 
    "started_at": YESTERDAY_DATE_FORMATTED
})
dc.generateClipsFromData(CLIPS_LINK, {
    "game_id": "27471",   # MINECRAFT
    "first": "8", 
    "started_at": YESTERDAY_DATE_FORMATTED
})
dc.generateClipsFromData(CLIPS_LINK, {
    "game_id": "510218",   # AMONG US
    "first": "4", 
    "started_at": YESTERDAY_DATE_FORMATTED
})
dc.generateClipsFromData(CLIPS_LINK, {
    "game_id": "743",   # CHESS
    "first": "4",
    "started_at": YESTERDAY_DATE_FORMATTED
})

dc.downloadClipsListToFolder()


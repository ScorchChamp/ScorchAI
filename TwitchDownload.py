import json
from datetime import datetime, timezone 
from DataCollector import DataCollector
import datetime
import os
from assets import constants


YESTERDAY_DATE_ISO = datetime.datetime.now() - datetime.timedelta(days=1)
YESTERDAY_DATE_FORMATTED = YESTERDAY_DATE_ISO.strftime("%Y-%m-%dT%H:%M:%SZ")

dc = DataCollector()

try:
    for file in os.listdir(constants.UPLOADED_FOLDER):
        os.remove(constants.UPLOADED_FOLDER + file)
except:
    print("removal failed")
    pass

with open(constants.CATEGORIES_FILE, encoding="utf8") as file:
    categories = json.load(file)
    for category in categories['download_categories']:
        category["started_at"] = YESTERDAY_DATE_FORMATTED
        dc.generateClipsFromData(constants.CLIPS_LINK, category)

dc.downloadClipsListToFolder()


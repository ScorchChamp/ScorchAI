import json
from datetime import datetime, timezone 
import datetime
import os, glob
from TwitchAPI import TwitchAPI
import time

class Twitch:
    def __init__(self): 
        self.API = TwitchAPI("./auth/auth.json")

    def getGames(self):    
        with open("assets/categories.json", encoding="utf8") as file:
            categories = json.load(file)
            return categories['games']

    def getBroadcasters(self):    
        with open("assets/categories.json", encoding="utf8") as file:
            categories = json.load(file)
            return categories['broadcasters']

    def generateClips(self, amount):
        self.cleanFolder('./videos/uploaded_clips/')
        clips_left = amount
        prio = 1
        days = 1
        while clips_left > 0:
            category = self.getNextcategory(prio)

            print(f"clips_left: {clips_left}")
            print(f"prio: {prio}")
            print(f"day: {days}")
            print(f"category: {category}")
            if days > 10:
                print("Too many days... Quitting")
                exit()
            if not category:
                print(f'No priority number: {prio}, expanding range to {days} days')
                days += 1
                prio = 1
            else:
                clips_left = self.downloadClipsList(category['parameters'], category['min_views'], clips_left, days)
                prio += 1
    
    def getNextcategory(self, priority):
        for category in self.getBroadcasters():
            category = self.getBroadcasters()[category]
            if category['priority'] == priority:
                return category
        for category in self.getGames():
            category = self.getGames()[category]
            if category['priority'] == priority:
                return category
        return False

    def downloadClipsList(self, parameters, min_views = 0, amount_left = 10, days = 1):
        if not "first" in parameters:
            parameters['first'] = 10
        parameters["started_at"] = self.getTimeWithDelay(days)
        for clip in self.API.getClipsList(parameters)['data']:
            if amount_left < 1:
                return amount_left
            if os.path.isfile(f"./clipData/{clip['id']}.json"):
                print("Clip already used, skipping...")
                continue
            if not clip['view_count'] > min_views:
                print('Not enough views, skipping...')
                continue

            if not 'en' in clip['language']:
                print('Clip not in english... Skipping')
                continue

            elif clip['broadcaster_id'] in self.getBlacklistedCreators():
                print('Broadcaster blacklisted... Skipping')
                continue
            
            self.dumpClipData(clip)

            if self.API.downloadClip(clip['id'], clip['thumbnail_url'].split("-preview")[0] + ".mp4"):
                amount_left -=1

        return amount_left
    
    def dumpClipData(self, clip):
        file = f"./clipData/{clip['id']}.json"
        with open(file, 'w') as fp:
            json.dump(clip, fp)

    def getBlacklistedCreators(self):
        with open("assets/categories.json", encoding="utf8") as file:
            categories = json.load(file)
            return categories['blacklisted_broadcasters']
        

    def cleanFolder(self, dir):
        for f in os.listdir(dir):
            print(f'Cleaning clip in folder: {f}')
            os.remove(os.path.join(dir, f))

    def getTimeWithDelay(self, days = 1):
        YESTERDAY_DATE_ISO = datetime.datetime.now() - datetime.timedelta(days=days)
        YESTERDAY_DATE_FORMATTED = YESTERDAY_DATE_ISO.strftime("%Y-%m-%dT%H:%M:%SZ")
        return YESTERDAY_DATE_FORMATTED


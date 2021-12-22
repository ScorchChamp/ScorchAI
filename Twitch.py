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
        cleanFolder('./videos/uploaded_clips/')
        clips_left = amount
        prio = 1
        days = 1
        while clips_left > 0:
            category = self.getNextcategory(prio)

            print(f"clips_left: {clips_left}")
            print(f"prio: {prio}")
            print(f"day: {days}")
            print(f"category: {category}")
            if daysTooHigh(days): exit()
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
        if not "first" in parameters: parameters['first'] = 10
        parameters["started_at"] = getTimeWithDelay(days)

        for clip in self.API.getClipsList(parameters)['data']:
            if amount_left < 1: return amount_left
            if     clipAlreadyUploaded(clip):           continue
            if     clipAlreadyUploaded(clip):           continue
            if not clipHasEnoughViews(clip, min_views): continue
            if not clipIsInRightLanguage(clip):         continue
            if     clipBroadcasterIsBlacklisted(clip):  continue

            dumpClipData(clip)
            if self.API.downloadClip(clip): amount_left -=1

        return amount_left






def clipBroadcasterIsBlacklisted(clip):
    if clip['broadcaster_id'] in getBlacklistedCreators():
        print('Broadcaster blacklisted')
        return True
    return False

def clipIsInRightLanguage(clip, language = 'en'):
    if 'en' in clip['language']:
        return True
    print('Clip not in english')
    return False

def daysTooHigh(days):
    if days > 10:
        print("Too many days")
        return True
    return False


def clipHasEnoughViews(clip, min_views):
    if clip['view_count'] > min_views:
        return True
    print('Not enough views')
    return False
    

def clipAlreadyUploaded(clip):
    if os.path.isfile(f"./clipData/{clip['id']}.json"):
        print(f"Clip {clip['id']} already used")
        return True
    return False

def dumpClipData(clip):
    file = f"./clipData/{clip['id']}.json"
    with open(file, 'w') as fp:
        json.dump(clip, fp)

def getBlacklistedCreators():
    with open("assets/categories.json", encoding="utf8") as file:
        categories = json.load(file)
        return categories['blacklisted_broadcasters']
    

def cleanFolder( dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


def getTimeWithDelay( days = 1):
    YESTERDAY_DATE_ISO = datetime.datetime.now() - datetime.timedelta(days=days)
    YESTERDAY_DATE_FORMATTED = YESTERDAY_DATE_ISO.strftime("%Y-%m-%dT%H:%M:%SZ")
    return YESTERDAY_DATE_FORMATTED


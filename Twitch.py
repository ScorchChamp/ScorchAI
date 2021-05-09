import json
from datetime import datetime, timezone 
import datetime
import os, glob
from TwitchAPI import TwitchAPI

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
        while clips_left > 0:
            print("clips_left: {}".format(clips_left))
            print("prio: {}".format(prio))
            category = self.getNextcategory(prio)
            print("category: {}".format(category))
            if not category:
                print('No priority number: {}'.format(prio))
                exit()
            clips_left = self.downloadClipsList(category['parameters'], category['min_views'], clips_left)
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

    def downloadClipsList(self, parameters, min_views = 0, amount_left = 10):
        if not "first" in parameters:
            parameters['first'] = 10
        parameters["started_at"] = self.getTimeWithDelay(1)
        print(parameters)
        print(self.API.getClipsList(parameters))
        for clip in self.API.getClipsList(parameters)['data']:
            if amount_left < 1:
                return amount_left
            if os.path.isfile('./clipData/{}.json'.format(clip['id'])):
                print("Clip already used, skipping...")
            else:
                if not clip['view_count'] > min_views:
                    print('Not enough views, skipping...')
                elif not 'en' in clip['language']:
                    print('Clip not in english... Skipping')
                else:
                    self.dumpClipData(clip)
                    self.API.downloadClip(
                        clip['id'],
                        clip['thumbnail_url'].split("-preview")[0] + ".mp4"
                    )
                    amount_left -=1
        return amount_left
    
    def dumpClipData(self, clip):
        file = "./clipData/{}.json".format(clip['id'])
        with open(file, 'w') as fp:
            json.dump(clip, fp)

    def cleanFolder(self, dir):
        for f in os.listdir(dir):
            print('Cleaning clip in folder: {}'.format(f))
            os.remove(os.path.join(dir, f))

    def getTimeWithDelay(self, hours = 1):
        YESTERDAY_DATE_ISO = datetime.datetime.now() - datetime.timedelta(days=1)
        YESTERDAY_DATE_FORMATTED = YESTERDAY_DATE_ISO.strftime("%Y-%m-%dT%H:%M:%SZ")
        return YESTERDAY_DATE_FORMATTED


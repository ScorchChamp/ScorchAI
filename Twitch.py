import json
from datetime import datetime, timezone 
import datetime
import os, glob
from TwitchAPI import TwitchAPI
from moviepy.editor import *

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

    def generateCompilation(self, amount):
        self.cleanFolder('./videos/ready_compilations/')
        self.generateClips(amount)
        self.compileClips()


    def generateClips(self, amount):
        clips_left = amount
        prio = 1
        while clips_left > 0:
            category = self.getNextcategory(prio)
            if not category:
                print('No clips left...')
                break
            clips_left = self.downloadClipsList(category['parameters'], clips_left)
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

    def downloadClipsList(self, parameters, amount_left = 10):
        parameters['first'] = 10
        parameters["started_at"] = self.getYesterdayFormatted()
        for clip in self.API.getClipsList(parameters)['data']:
            # print("Clips left: {}".format(amount_left))
            if amount_left < 1:
                return amount_left
            if os.path.isfile('./clipData/{}.json'.format(clip['id'])):
                print("Clip already used, skipping...")
            else:
                # if not 'en' in clip['language'] or not clip['view_count'] > 500:
                # print("Clip didnt reach requirements, skipping...")
                # else:
                self.dumpClipFile(clip)
                self.API.downloadClip(
                    clip['id'],
                    clip['thumbnail_url'].split("-preview")[0] + ".mp4"
                )
                amount_left -=1
        return amount_left

    def dumpClipFile(self, clip):
        file = "./clipData/{}.json".format(clip['id'])
        with open(file, 'w') as fp:
            json.dump(clip, fp)

    def compileClips(self):
        L = []
        for root, dirs, files in os.walk("./videos/clips/"):
            for file in files:
                if os.path.splitext(file)[1] == '.mp4':
                    filePath = os.path.join(root, file)
                    video = VideoFileClip(filePath)
                    L.append(video)

        final_clip = concatenate_videoclips(L, method='compose')
        final_clip.to_videofile("./videos/ready_compilations/{}.mp4".format(self.getYesterdayFormatted()).replace(":", "-"), fps=24, remove_temp=True)
    
    def cleanFolder(self, dir):
        for f in os.listdir(dir):
            print('Cleaning clip in folder: {}'.format(f))
            os.remove(os.path.join(dir, f))

    def getYesterdayFormatted(self):
        YESTERDAY_DATE_ISO = datetime.datetime.now() - datetime.timedelta(days=1)
        YESTERDAY_DATE_FORMATTED = YESTERDAY_DATE_ISO.strftime("%Y-%m-%dT%H:%M:%SZ")
        return YESTERDAY_DATE_FORMATTED


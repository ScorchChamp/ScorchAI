from YoutubeAPI import YoutubeAPI
import os
import datetime
import json
from Twitch import Twitch
import shutil

class Youtube:
    def __init__(self): 
        self.API = YoutubeAPI("./auth/client_secrets.json")
        self.twitch = Twitch()

    def uploadClip(self, generateWhenNoneFound):
        videos = self.getVideos('./videos/clips/')
        while len(videos) == 0:
            if generateWhenNoneFound:
                print('Getting clips')
                self.twitch.generateClips(1)
                videos = self.getVideos('./videos/clips/')
            else:
                print("No clips found... Use -g tag to generate anyway")
                return False

        vidData = self.generateVidData(videos[0])
        self.uploadVideo(
            vidData['videourl'], 
            vidData['title'], 
            vidData['description'], 
            vidData['tags']
        )
        
    def generateVidData(self, vidData):
        vidData = {
            'videourl': './videos/clips/{}.mp4'.format(vidData),
            'title': self.generateTitle(vidData),
            'description': self.generateDescription(vidData, "#{}".format(self.getBroadcaster(vidData))),
            'tags': self.generateTags(vidData)
        }
        return vidData

    def uploadVideo(self, video, title, description, tags):
        newDir = "./videos/uploaded_clips/{}".format(video.split("/")[-1])
        shutil.move(video, newDir)
        print("Uploading {}".format(title))
        self.API.uploadVideo(newDir, title, description, tags)

    def getVideos(self, folder):
        videos = os.listdir(folder)
        for i in range(len(videos)):
            videos[i] = videos[i].split(".mp4")[0]
        return videos
            
    def generateTags(self, clipID, tags = ""):
        with open('./assets/tags.txt', encoding="utf8") as file:
            tags += file.read()
        tags += self.getTags(clipID)
        return tags

    def generateDescription(self, clipID = False, description = ""):
        if not clipID == False:
            description = '#{} '.format(self.getBroadcaster(clipID))
        with open("./assets/description.txt", encoding="utf8") as file:
            description += file.read()
        return description

    def generateTitle(self, clipID):
        with open("./clipData/{}.json".format(clipID), encoding="utf8") as file:
            data = json.load(file)
            return "{} ({})".format(data['title'], data['broadcaster_name'])
         

    def getUploadDate(self, hourOffset):
        return datetime.datetime.now() + datetime.timedelta(hours=hourOffset)

    def getTitle(self, clipID):
        with open("./clipData/{}.json".format(clipID), encoding="utf8") as file:
            return json.load(file)['title']

    def getTags(self, clipID):
        with open("./clipData/{}.json".format(clipID), encoding="utf8") as file:
            data = json.load(file)
            return data['broadcaster_name'] + ", " + data['title'] + ", " + data['id'] + ", "

    def getBroadcaster(self, clipID):
        with open("./clipData/{}.json".format(clipID), encoding="utf8") as file:
            data = json.load(file)
            return data['broadcaster_name']



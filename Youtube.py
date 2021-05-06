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

    def uploadClip(self, amount = 1, hourOffset = 0):
        videos = self.getVideos('./videos/clips/')
        while len(videos) < amount:
            print('Getting clips')
            self.twitch.generateClips(amount)
            videos = self.getVideos('./videos/clips/')
        for i in range(amount):
            video = './videos/clips/{}.mp4'.format(videos[i])
            title = self.generateTitle(videos[i])
            description = self.generateDescription(videos[i], "#{}".format(self.getBroadcaster(videos[i])))
            tags = self.generateTags(videos[i])
            uploadDate = self.getUploadDate(hourOffset)
            self.uploadVideo(video, title, description, tags, uploadDate)
        
    def uploadCompilation(self, hourOffset):
        videos = self.getVideos('./videos/ready_compilations/')
        while len(videos) == 0:
            print('Getting clips')
            self.twitch.generateClips(1)
            videos = self.getVideos('./videos/clips/')

        video = './videos/ready_compilations/{}.mp4'.format(videos[0])
        title = "Daily Twitch compilation"
        description = self.generateDescription(False, "#Compilation ")
        tags = self.generateTags(videos[0])
        uploadDate = self.getUploadDate(hourOffset)
        self.uploadVideo(video, title, description, tags, uploadDate)

    def uploadVideo(self, video, title, description, tags, uploadDate):
        newDir = "./videos/uploaded/{}".format(video.split("/")[-1])
        shutil.move(video, newDir)
        print("Uploading {}".format(title))
        self.API.uploadVideo(newDir, title, description, tags, uploadDate)

    def getVideos(self, folder):
        videos = os.listdir(folder)
        for i in range(len(videos)):
            videos[i] = videos[i].split(".mp4")[0]
        return videos
            
    def generateTags(self, clipID, tags = ""):
        with open('./assets/tags.txt', encoding="utf8") as file:
            tags += file.read()
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



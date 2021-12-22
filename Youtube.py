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
        while len(self.getVideos('./videos/clips/')) == 0:
            if generateWhenNoneFound:
                print('Getting clips')
                self.twitch.generateClips(1)
            else:
                print("No clips found... Use -g tag to generate anyway")
                return False
                
        videos = self.getVideos('./videos/clips/')

        vidData = self.generateVidData(videos[0])
        self.uploadVideo(
            vidData['videourl'], 
            vidData['title'], 
            vidData['description'], 
            vidData['tags']
        )
        
    def generateVidData(self, vidData):
        vidData = {
            'videourl': f'./videos/clips/{vidData}.mp4',
            'title': self.generateTitle(vidData),
            'description': self.generateDescription(vidData, f"#{self.getBroadcaster(vidData)}"),
            'tags': self.generateTags(vidData)
        }
        return vidData

    def uploadVideo(self, video, title, description, tags):
        video = self.processVideo(video)
        print(f"Uploading {title}")
        self.API.uploadVideo(video, title, description, tags)

    def processVideo(self, video):
        videoID = video.split("/")[-1]
        newDir = f"./videos/uploaded_clips/{videoID}"
        shutil.move(video, newDir)
        return newDir

    def getVideos(self, folder):
        videos = os.listdir(folder)
        for i in range(len(videos)):
            videos[i] = videos[i].split(".mp4")[0]
        return videos
            
    def generateTags(self, clipID, tags = ""):
        with open('./assets/tags.txt', encoding="utf8") as file:
            tags += file.read()
        tags += ", " + self.getTags(clipID)
        return tags

    def generateDescription(self, clipID, description = ""):
        bc = self.getBroadcaster(clipID)
        clipLink = self.getClipLink(clipID)
        description = f"Follow {bc} on https://twitch.tv/{bc} \n"
        description += f"Full VOD: {clipLink} \n"
        with open("./assets/description.txt", encoding="utf8") as file:
            description += file.read()
        description += f'#{bc} '
        return description

    def generateTitle(self, clipID):
        with open(f"./clipData/{clipID}.json", encoding="utf8") as file:
            data = json.load(file)
            return f"{data['title']} ({data['broadcaster_name']})"
         

    def getUploadDate(self, hourOffset):
        return datetime.datetime.now() + datetime.timedelta(hours=hourOffset)

    def getTitle(self, clipID):
        with open(f"./clipData/{clipID}.json", encoding="utf8") as file:
            return json.load(file)['title']

    def getTags(self, clipID):
        with open(f"./clipData/{clipID}.json", encoding="utf8") as file:
            data = json.load(file)
            return data['broadcaster_name'] + ", " + data['title'] + ", " + data['id'] + ", "

    def getBroadcaster(self, clipID):
        with open(f"./clipData/{clipID}.json", encoding="utf8") as file:
            data = json.load(file)
            return data['broadcaster_name']

            
    def getClipLink(self, clipID):
        with open(f"./clipData/{clipID}.json", encoding="utf8") as file:
            data = json.load(file)
            return data['url']



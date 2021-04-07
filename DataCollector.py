from Authorizer import Authorizer
from TwitchClip import TwitchClip
import requests
import datetime
from YoutubeAPI import YoutubeAPI
from pathlib import Path
import os

class DataCollector:
    clips = []
    headers = {}
    auth_data = {}
    parameters = {}
    authorizer = 0
    API = ""
    clipFolder = ""
    dataFolder = ""
    twitchAuthFile = ""

    def __init__(self, twitchAuthFile, youtubeSecretFile, clipFolder, dataFolder): 
        self.clipFolder = clipFolder
        self.dataFolder = dataFolder

        # Twitch API init
        self.twitchAuthFile = twitchAuthFile
        self.authorizer = Authorizer(twitchAuthFile)
        self.generateHeaders(self.authorizer.getHeaders())

        # Youtube API init
        self.API = YoutubeAPI(youtubeSecretFile)

    def collectDataFromAPI(self, url, parameters):
        self.generateParameters(parameters)
        return requests.get(url, parameters, headers=self.headers).json()

    def generateHeaders(self, headers):
        self.headers = headers

    def generateParameters(self, parameters):
        self.parameters = parameters

    def generateClipsFromData(self, url, parameters):
        data = self.collectDataFromAPI(url, parameters)['data']
        for clip in data:
            self.clips.append(TwitchClip(clip))

    def downloadClipsListToFolder(self):
        for clip in self.clips:
            if not self.doesClipDataExist(self.dataFolder, clip.getid()):
                clip.downloadMP4FromTwitchServer(self.clipFolder)
                clip.exportClipData(self.dataFolder)
            else:
                print("Clip already exists UnPOg")

    def uploadClipToYoutube(self, clipID, description, tags = ['Twitch', 'ScorchAI'], uploadDate = 0):
        uploadDate = self.getCurrentDate() - datetime.timedelta(hours=1)
        self.clips[clipID].uploadToYoutube(self.API, description, tags, uploadDate)

    def getCurrentDate(self):
        return datetime.datetime.now()
    
    def getDateWithDelta(self, date, delta):
        return date + delta

    def getDescription(self, descriptionFile = './assets/description.txt'):
        with open(descriptionFile, encoding="utf8") as file:
            return file.read()
    
    def doesClipDataExist(self, dataFolder, clipID):
        file = Path("{}{}.json".format(dataFolder,clipID))   
        return file.is_file()

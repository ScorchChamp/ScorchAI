import API.YoutubeAPI as YoutubeAPI
import os
import datetime
import json
import Twitch
import shutil

CLIPS_FOLDER = './videos/clips/'
PREP_STAGE = './videos/prepstage/'
READY_STAGE = './videos/ready_to_upload/'
UPLOADED_STAGE = './videos/uploaded_clips/'

def uploadClip(generateWhenNoneFound):
    if getVideoReadyAmount() == 0 and generateWhenNoneFound:
        Twitch.generateClips(1)

    uploadVideo(generateVidData(getNextReadyVideoID()))
    
def generateVidData(clipID):
    vidData = {
        'videourl': f'{READY_STAGE+clipID}.mp4',
        'title': generateTitle(clipID),
        'description': generateDescription(clipID),
        'tags': generateTags(clipID),
        'id': clipID
    }
    return vidData


def processVideo(videoData):
    newDir = f"{READY_STAGE+videoData['id']}"
    shutil.move(videoData['videourl'], newDir)
    return newDir

def generateDescription(clipID):
    bc = getBroadcaster(clipID)
    return f"Follow {bc} on https://twitch.tv/{bc} \nFull VOD: {getClipLink(clipID)} \n{getDescriptionTemplate()} #{bc}"


def uploadVideo(vidData):       YoutubeAPI.uploadVideo(processVideo(vidData), vidData['title'], vidData['description'], vidData['tags'])
def getVideos(folder):          return [video.split(".mp4")[0] for video in os.listdir(folder)] 

def getVideoID(video):          return video.split("/")[-1]
def getTagsTemplate():          return open("./assets/tags.txt", encoding="utf8").read()
def getDescriptionTemplate():   return open("./assets/description.txt", encoding="utf8").read()
def getUploadDate(hourOffset):  return datetime.datetime.now() + datetime.timedelta(hours=hourOffset)
def getJsonContents(file):      return json.load(open(file, encoding="utf8"))
def getClipData(clipID):        return getJsonContents(f"./clipData/{clipID}.json")

def getClipLink(clipID):        return getClipData(clipID)['url']
def getTitle(clipID):           return getClipData(clipID)['title']
def getBroadcaster(clipID):     return getClipData(clipID)['broadcaster_name']
def generateTags(clipID):       return f"{getTagsTemplate()}, {getTags(clipID)}"
def getTags(clipID):            return f"{getBroadcaster(clipID)}, {getTitle(clipID)}, {clipID}, "
def generateTitle(clipID):      return f"{getTitle(clipID)} ☀️ {getBroadcaster(clipID)}"


def getVideoName(video):    return video.split(".mp4")[0]
def getNextVideoID():       return getVideos(CLIPS_FOLDER)[0]
def getNextReadyVideoID():  return getVideos(READY_STAGE)[0]
def getVideoReadyAmount():  return len(getVideos(READY_STAGE))
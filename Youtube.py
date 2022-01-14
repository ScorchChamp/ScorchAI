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

def uploadClip(generateWhenNoneFound, channel):
    if getVideoReadyAmount() == 0 and generateWhenNoneFound:
        Twitch.generateClips(1, channel)

    uploadVideo(generateVidData(getNextReadyVideoID(), channel), channel)
    
def generateVidData(clipID, channel):
    vidData = {
        'videourl': f'{READY_STAGE+clipID}.mp4',
        'title': generateTitle(clipID, channel),
        'description': generateDescription(clipID, channel),
        'tags': generateTags(clipID, channel),
        'id': clipID
    }
    return vidData


def processVideo(videoData):
    newDir = f"{READY_STAGE+videoData['id']}"
    shutil.move(videoData['videourl'], newDir)
    return newDir

def generateDescription(clipID, channel):
    bc = getBroadcaster(clipID, channel)
    return f"Follow {bc} on https://twitch.tv/{bc} \nFull VOD: {getVodLink(clipID, channel)} \n{getDescriptionTemplate(channel)} #{bc}"


def uploadVideo(vidData, channel):       YoutubeAPI.uploadVideo(processVideo(vidData), vidData['title'], vidData['description'], vidData['tags'], channel)
def getVideos(folder):          return [video.split(".mp4")[0] for video in os.listdir(folder)] 

def getVideoID(video):          return video.split("/")[-1]
def getTagsTemplate(channel):          return open(f"./assets/Channels/{channel}/tags.txt", encoding="utf8").read()
def getDescriptionTemplate(channel):   return open(f"./assets/Channels/{channel}/description.txt", encoding="utf8").read()
def getUploadDate(hourOffset):  return datetime.datetime.now() + datetime.timedelta(hours=hourOffset)
def getJsonContents(file):      return json.load(open(file, encoding="utf8"))
def getClipData(clipID, channel):    return getJsonContents(f"./assets/Channels/{channel}/clipData/{clipID}.json")

def getVodLink(clipID, channel):         return f"https://twitch.tv/videos/{getClipData(clipID, channel)['video_id']}" 
def getClipLink(clipID, channel):        return getClipData(clipID, channel)['url']
def getTitle(clipID, channel):           return getClipData(clipID, channel)['title']
def getBroadcaster(clipID, channel):     return getClipData(clipID, channel)['broadcaster_name']
def generateTags(clipID, channel):       return f"{getTagsTemplate(channel)}, {getTags(clipID, channel)}"
def getTags(clipID, channel):            return f"{getBroadcaster(clipID, channel)}, {getTitle(clipID, channel)}, {clipID}, "
def generateTitle(clipID, channel):      return f"{getTitle(clipID, channel)} - {getBroadcaster(clipID, channel)}"


def getVideoName(video):    return video.split(".mp4")[0]
def getNextVideoID():       return getVideos(CLIPS_FOLDER)[0]
def getNextReadyVideoID():  return getVideos(READY_STAGE)[0]
def getVideoReadyAmount():  return len(getVideos(READY_STAGE))

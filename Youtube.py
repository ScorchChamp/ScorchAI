import API.YoutubeAPI as YoutubeAPI
import os
import datetime
import json
import Twitch
import shutil

def uploadClip(generateWhenNoneFound):
    while len(getVideos('./videos/clips/')) == 0:
        if generateWhenNoneFound:
            print('Getting clips')
            Twitch.generateClips(1)
        else:
            print("No clips found... Use -g tag to generate anyway")
            return False
            
    videos = getVideos('./videos/clips/')

    vidData = generateVidData(videos[0])
    uploadVideo(
        vidData['videourl'], 
        vidData['title'], 
        vidData['description'], 
        vidData['tags']
    )
    
def generateVidData(vidData):
    vidData = {
        'videourl': f'./videos/clips/{vidData}.mp4',
        'title': generateTitle(vidData),
        'description': generateDescription(vidData),
        'tags': generateTags(vidData)
    }
    return vidData

def uploadVideo(video, title, description, tags):
    YoutubeAPI.uploadVideo(processVideo(video), title, description, tags)

def processVideo(video):
    newDir = f"./videos/uploaded_clips/{getVideoID(video)}"
    shutil.move(video, newDir)
    return newDir

def getVideos(folder):
    return [video.split(".mp4")[0] for video in os.listdir(folder)]
        
def generateTags(clipID):
    return f"{getTagsTemplate()}, {getTags(clipID)}"

def generateDescription(clipID):
    bc = getBroadcaster(clipID)
    return f"Follow {bc} on https://twitch.tv/{bc} \nFull VOD: {getClipLink(clipID)} \n{getDescriptionTemplate()} #{bc}"

def getVideoID(video):          return video.split("/")[-1]
def getTagsTemplate():          return open("./assets/tags.txt", encoding="utf8").read()
def getDescriptionTemplate():   return open("./assets/description.txt", encoding="utf8").read()
def getUploadDate(hourOffset):  return datetime.datetime.now() + datetime.timedelta(hours=hourOffset)
def getJsonContents(file):      return json.load(open(file, encoding="utf8"))
def getClipData(clipID):        return getJsonContents(f"./clipData/{clipID}.json")

def getClipLink(clipID):        return getClipData(clipID)['url']
def getTitle(clipID):           return getClipData(clipID)['title']
def getBroadcaster(clipID):     return getClipData(clipID)['broadcaster_name']
def getTags(clipID):            return f"{getBroadcaster(clipID)}, {getTitle(clipID)}, {clipID}, "
def generateTitle(clipID):      return f"{getTitle(clipID)} ({getBroadcaster(clipID)})"


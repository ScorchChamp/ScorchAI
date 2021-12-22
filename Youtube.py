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
        'description': generateDescription(vidData, f"#{getBroadcaster(vidData)}"),
        'tags': generateTags(vidData)
    }
    return vidData

def uploadVideo(video, title, description, tags):
    video = processVideo(video)
    print(f"Uploading {title}")
    YoutubeAPI.uploadVideo(video, title, description, tags)

def processVideo(video):
    videoID = video.split("/")[-1]
    newDir = f"./videos/uploaded_clips/{videoID}"
    shutil.move(video, newDir)
    return newDir

def getVideos(folder):
    videos = os.listdir(folder)
    for i in range(len(videos)):
        videos[i] = videos[i].split(".mp4")[0]
    return videos
        
def generateTags(clipID, tags = ""):
    with open('./assets/tags.txt', encoding="utf8") as file:
        tags += file.read()
    tags += ", " + getTags(clipID)
    return tags

def generateDescription(clipID, description = ""):
    bc = getBroadcaster(clipID)
    clipLink = getClipLink(clipID)
    description = f"Follow {bc} on https://twitch.tv/{bc} \n"
    description += f"Full VOD: {clipLink} \n"
    with open("./assets/description.txt", encoding="utf8") as file:
        description += file.read()
    description += f' #{bc} '
    return description

def generateTitle(clipID):
    with open(f"./clipData/{clipID}.json", encoding="utf8") as file:
        data = json.load(file)
        return f"{data['title']} ({data['broadcaster_name']})"
        

def getUploadDate(hourOffset):
    return datetime.datetime.now() + datetime.timedelta(hours=hourOffset)

def getTitle(clipID):
    with open(f"./clipData/{clipID}.json", encoding="utf8") as file:
        return json.load(file)['title']

def getTags(clipID):
    with open(f"./clipData/{clipID}.json", encoding="utf8") as file:
        data = json.load(file)
        return data['broadcaster_name'] + ", " + data['title'] + ", " + data['id'] + ", "

def getBroadcaster(clipID):
    with open(f"./clipData/{clipID}.json", encoding="utf8") as file:
        data = json.load(file)
        return data['broadcaster_name']

        
def getClipLink(clipID):
    with open(f"./clipData/{clipID}.json", encoding="utf8") as file:
        data = json.load(file)
        return data['url']



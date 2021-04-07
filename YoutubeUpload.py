import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
import os
import sys
import json
from YoutubeAPI import YoutubeAPI
from DataCollector import DataCollector

API = YoutubeAPI('./assets/client_secrets.json')


# clip_folder = './clips/'
# clips = os.listdir(clip_folder)
# if (len(clips) == 1):
#     print("NO CLIPS FOUND, EXITTING...")
#     sys.exit()
# else:
#     print(clips[0])
# mp4_file = "./clips/" + clips[0]

# if not mp4_file.endswith(".mp4"):
#     mp4_file = "./clips/" + clips[1]


# title = mp4_file.split("/")[-1].split(".")[0]



def getClipNameList(folder):
    clips = os.listdir(clip_folder)
    returnClips = []
    for clip in clips:
        if clip.endswith(".mp4"):
            returnClips.append(clip.split(".")[0])
    return returnClips

clip_folder = './clips/'
clip_data_folder = './clipData/'
clips = getClipNameList(clip_folder)

if len(clips) > 0:
    clip = clips[0]
else:
    print("NO CLIPS FOUND, EXITTING...")
    sys.exit()

clipData = ""
with open('{}{}.json'.format(clip_data_folder, clip)) as f:
    clipData = json.load(f)



mp4_file = '{}{}.mp4'.format(clip_folder, clip)
title = "{} ({})".format(clipData['title'], clipData['broadcaster_name'])

description = '#{} '.format(clipData['broadcaster_name'])
with open('./assets/description.txt', encoding="utf8") as file:
    description += file.read()
description += '\n\
    VideoID: {}\n\
    Created At: {}\n\
    Created By: {}\n\
    View count on Twitch: {}\n\
    Game ID: {}\n\
    Download Clip at: {}\n'.format(
        clipData['id'],
        clipData['created_at'],
        clipData['creator_name'], 
        clipData['view_count'], 
        clipData['game_id'], 
        clipData['thumbnail_url'].split("-preview")[0] + ".mp4"
    )


tags = clipData['broadcaster_name']
with open('./assets/tags.txt', encoding="utf8") as file:
    tags += file.read()

os.rename(mp4_file, "./clips/uploaded/" + clip + ".mp4")

mp4_file = "./clips/uploaded/" + mp4_file.split("/")[-1]

uploadDate = datetime.datetime.now() + datetime.timedelta(hours=1)
API.uploadVideo(mp4_file, title, description, tags, uploadDate)
print("{} uploaded succesfully!".format(title))
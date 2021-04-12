import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
import os
import sys
import json
from YoutubeAPI import YoutubeAPI
from DataCollector import DataCollector

def getClipNameList(folder):
    CLIPS = os.listdir(CLIPS_FOLDER)
    returnClips = []
    for clip in CLIPS:
        if clip.endswith(".mp4"):
            returnClips.append(clip.split(".")[0])
    return returnClips


CLIPS_FOLDER = './clips/'
CLIP_DATA_FOLDER = './clipData/'

API = YoutubeAPI('./assets/client_secrets.json')
CLIPS = getClipNameList(CLIPS_FOLDER)

if len(CLIPS) > 0:
    clip = CLIPS[0]
else:
    print("NO CLIPS FOUND, EXITTING...")
    sys.exit()

clipData = ""
with open('{}{}.json'.format(CLIP_DATA_FOLDER, clip)) as f:
    clipData = json.load(f)



mp4_file = '{}{}.mp4'.format(CLIPS_FOLDER, clip)
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

tags = clipData['broadcaster_name'] + ", "
with open('./assets/tags.txt', encoding="utf8") as file:
    tags += file.read()

os.rename(mp4_file, "{}uploaded/{}.mp4".format(CLIPS_FOLDER, clip))
mp4_file = "{}uploaded/{}".format(CLIPS_FOLDER, mp4_file.split("/")[-1])

uploadDate = datetime.datetime.now() + datetime.timedelta(hours=1)

API.uploadVideo(mp4_file, title, description, tags, uploadDate)

print("{} uploaded succesfully!".format(title))
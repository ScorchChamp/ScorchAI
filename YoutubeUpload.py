import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
import os
import sys
import json
from YoutubeAPI import YoutubeAPI
from DataCollector import DataCollector
from assets import constants
from assets import scorchAI

def getClipNameList(folder):
    CLIPS = os.listdir(constants.CLIPS_FOLDER)
    returnClips = []
    for clip in CLIPS:
        if clip.endswith(".mp4"):
            returnClips.append(clip.split(".")[0])
    return returnClips

API = YoutubeAPI()
CLIPS = getClipNameList(constants.CLIPS_FOLDER)
if len(CLIPS) > 0:
    clip = CLIPS[0]
else:
    print("NO CLIPS FOUND, EXITTING...")
    sys.exit()

clipData = ""
with open('{}{}.json'.format(constants.CLIP_DATA_FOLDER, clip)) as f:
    clipData = json.load(f)



tags = scorchAI.generateTags(clipData)
description = scorchAI.generateDescription(clipData)
mp4_file = '{}{}.mp4'.format(constants.CLIPS_FOLDER, clip)
title = "{} ({})".format(clipData['title'], clipData['broadcaster_name'])



os.rename(mp4_file, "{}uploaded/{}.mp4".format(constants.CLIPS_FOLDER, clip))
mp4_file = "{}uploaded/{}".format(constants.CLIPS_FOLDER, mp4_file.split("/")[-1])

uploadDate = datetime.datetime.now() + datetime.timedelta(hours=1)

API.uploadVideo(mp4_file, title, description, tags, uploadDate)

print("{} uploaded succesfully!".format(title))
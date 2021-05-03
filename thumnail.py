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

thumbnail = scorchAI.generateThumbnail(clipData)
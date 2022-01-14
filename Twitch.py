import json
from datetime import datetime
import datetime
import os
import API.TwitchAPI as TwitchAPI

CATEGORIES_FILE = "categories.json"
UPLOADED_CLIPS_FOLDER = './videos/uploaded_clips/'

def getCategoriesFile(channel):                             return getJsonContents(f"./assets/Channels/{channel}/{CATEGORIES_FILE}")

def getJsonContents(file):                                  return json.load(open(file, encoding="utf8"))
def getGames(channel):                                      return getCategoriesFile(channel)['games']
def getBroadcasters(channel):                               return getCategoriesFile(channel)['broadcasters']
def getBlacklistedCreators(channel):                        return getCategoriesFile(channel)['blacklisted_broadcasters']

def clipIsInRightLanguage(clip, language = 'en'):           return 'en' in clip['language']
def clipHasEnoughViews(clip, min_views):                    return clip['view_count'] > min_views
def clipBroadcasterIsBlacklisted(clip, channel):            return clip['broadcaster_id'] in getBlacklistedCreators(channel)
def clipAlreadyUploaded(clip, channel):                     return os.path.isfile(f"./assets/Channels/{channel}/clipData/{clip['id']}.json")
def daysTooHigh(days):                                      return days > 7

def isClipViable(clip, category, channel):
    if     clipAlreadyUploaded(clip, channel):              return False
    if not clipHasEnoughViews(clip, category['min_views']): return False
    if not clipIsInRightLanguage(clip, channel):            return False
    if     clipBroadcasterIsBlacklisted(clip, channel):     return False
    return True


def generateClips(amount, channel):
    emptyFolder(UPLOADED_CLIPS_FOLDER)
    [generateClip(channel) for i in range(amount)]

def generateClip(channel):
    current_priority = 1
    current_day = 1
    gotten_clip = False
    while not gotten_clip:
        current_category = getNextcategory(current_priority, channel)
        print(f"prio: {current_priority}, day: {current_day}")
        if not current_category:
            current_priority = 1
            current_day += 1
            if daysTooHigh(current_day): 
                print("Days too high without a clip! Quitting :( ...")
                exit()
        else:
            clip = getNextViableClip(current_category, channel, current_day)
            if clip:
                dumpClipData(clip, channel)
                TwitchAPI.downloadClip(clip)
                gotten_clip = True
            current_priority += 1

    
def getNextViableClip(category, channel, days = 1):
    parameters = category['parameters']
    parameters["started_at"] = getTimeWithDelay(days)
    if not "first" in parameters: parameters['first'] = 10
    clip_list = TwitchAPI.getClipsList(parameters)

    for clip in clip_list:
        if isClipViable(clip, category, channel): return clip
    return False

def getNextcategory(priority, channel):
    for category in getBroadcasters(channel):
        category = getBroadcasters(channel)[category]
        if category['priority'] == priority: return category
    for category in getGames(channel):
        category = getGames(channel)[category]
        if category['priority'] == priority: return category

    return False

def dumpClipData(clip, channel):
    file = f"./assets/Channels/{channel}/clipData/{clip['id']}.json"
    with open(file, 'w') as fp:
        json.dump(clip, fp)

def emptyFolder(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

def getTimeWithDelay(days = 1):
    YESTERDAY_DATE_ISO = datetime.datetime.now() - datetime.timedelta(days=days)
    YESTERDAY_DATE_FORMATTED = YESTERDAY_DATE_ISO.strftime("%Y-%m-%dT%H:%M:%SZ")
    return YESTERDAY_DATE_FORMATTED


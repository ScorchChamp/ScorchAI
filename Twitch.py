import json
from datetime import datetime
import datetime
import os
import API.TwitchAPI as TwitchAPI

CATEGORIES_FILE = "assets/categories.json"
UPLOADED_CLIPS_FOLDER = './videos/uploaded_clips/'

def getJsonContents(file):                                  return json.load(open(file, encoding="utf8"))
def getGames():                                             return getJsonContents(CATEGORIES_FILE)['games']
def getBroadcasters():                                      return getJsonContents(CATEGORIES_FILE)['broadcasters']
def getBlacklistedCreators():                               return getJsonContents(CATEGORIES_FILE)['blacklisted_broadcasters']

def clipIsInRightLanguage(clip, language = 'en'):           return 'en' in clip['language']
def clipHasEnoughViews(clip, min_views):                    return clip['view_count'] > min_views
def clipBroadcasterIsBlacklisted(clip):                     return clip['broadcaster_id'] in getBlacklistedCreators()
def clipAlreadyUploaded(clip):                              return os.path.isfile(f"./clipData/{clip['id']}.json")
def daysTooHigh(days):                                      return days > 5

def isClipViable(clip, category):
    if     clipAlreadyUploaded(clip):                       return False
    if     clipAlreadyUploaded(clip):                       return False
    if not clipHasEnoughViews(clip, category['min_views']): return False
    if not clipIsInRightLanguage(clip):                     return False
    if     clipBroadcasterIsBlacklisted(clip):              return False
    return True


def generateClips(amount):
    emptyFolder(UPLOADED_CLIPS_FOLDER)
    [generateClip() for i in range(amount)]

def generateClip():
    current_priority = 1
    current_day = 1
    gotten_clip = False
    while not gotten_clip:
        current_category = getNextcategory(current_priority)
        print(f"prio: {current_priority}, day: {current_day}")
        if not current_category:
            current_priority = 1
            current_day += 1
            if daysTooHigh(current_day): return False
        else:
            clip = getNextViableClip(current_category, current_day)
            if clip:
                dumpClipData(clip)
                TwitchAPI.downloadClip(clip)
                gotten_clip = True
            current_priority += 1

    
def getNextViableClip(category, days = 1):
    parameters = category['parameters']
    parameters["started_at"] = getTimeWithDelay(days)
    if not "first" in parameters: parameters['first'] = 10
    clip_list = TwitchAPI.getClipsList(parameters)

    for clip in clip_list:
        if isClipViable(clip, category): return clip
    return False

def getNextcategory(priority):
    for category in getBroadcasters():
        category = getBroadcasters()[category]
        if category['priority'] == priority: return category
    for category in getGames():
        category = getGames()[category]
        if category['priority'] == priority: return category

    return False

def dumpClipData(clip):
    file = f"./clipData/{clip['id']}.json"
    with open(file, 'w') as fp:
        json.dump(clip, fp)

def emptyFolder(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

def getTimeWithDelay(days = 1):
    YESTERDAY_DATE_ISO = datetime.datetime.now() - datetime.timedelta(days=days)
    YESTERDAY_DATE_FORMATTED = YESTERDAY_DATE_ISO.strftime("%Y-%m-%dT%H:%M:%SZ")
    return YESTERDAY_DATE_FORMATTED


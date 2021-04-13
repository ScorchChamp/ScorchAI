from assets import constants
import sys
import urllib.request
from tqdm import tqdm

def generateDescription(clipData):
    description = '#{} '.format(clipData['broadcaster_name'])
    with open(constants.DESCRIPTION_FILE, encoding="utf8") as file:
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

def generateTags(clipData):
    tags = clipData['broadcaster_name'] + ", "
    with open('./assets/tags.txt', encoding="utf8") as file:
        tags += file.read()
    return tags
    
def generatorFileNameFromFolderAndName(folder, name):
    return '{}{}.mp4'.format(folder, name)

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_url(url, output_path, title):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=title) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)
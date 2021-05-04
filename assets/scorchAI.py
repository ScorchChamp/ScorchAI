from assets import constants
import sys
import urllib
from tqdm import tqdm
# from PIL import Image
# from PIL import ImageFont
# from PIL import ImageDraw

# def generateThumbnail(clipData):
#     # NOT YET USED

#     download_url(clipData['thumbnail_url'], "./images/thumbnails/{}.jpg".format(clipData['id']), clipData['id'])

#     text = clipData['broadcaster_name']


#     img = Image.open("./images/thumbnails/{}.jpg".format(clipData['id']))
#     draw = ImageDraw.Draw(img)
#     font = ImageFont.truetype("./assets/ostrich-regular.ttf", 64)
    
#     x,y = font.getsize(text)
#     width, height = img.size
#     draw.rectangle((0, height-y, x, height), fill=(0,0,0,128))
#     draw.text((0, height-y), text , (255,255,255), font=font)
    
#     img.save("./images/thumbnails/{}-thumb.jpg".format(clipData['id']))
#     return "./images/thumbnails/{}-thumb.jpg".format(clipData['id'])


def generateDescription(clipData):
    brc = clipData['broadcaster_name']
    description = "FOLLOW {} ON: https://twitch.tv/{}".format(brc, brc)
    description += '\n#{} '.format(brc)
    with open(constants.DESCRIPTION_FILE, encoding="utf8") as file:
        description += file.read()
    return description

def generateTags(clipData):
    tags = clipData['broadcaster_name'] + ", " + clipData['id'] + ","
    with open('./assets/tags.txt', encoding="utf8") as file:
        tags += file.read()
    return tags
    
def generatorFileNameFromFolderAndName(folder, name):
    return '{}{}.mp4'.format(folder, name)

def generateTitle(title, brc_name):
    title = "{} ({})".format(title, brc_name)
    return title

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_url(url, output_path, title):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=title) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


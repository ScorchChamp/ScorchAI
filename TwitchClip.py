import sys
import urllib
import json

class TwitchClip:
    data = []
    clipFile = ''
    def __init__(self, data): 
        self.data = data

    def downloadMP4FromTwitchServer(self, output_folder):
        self.title = self.data['title']
        self.mp4Name = self.data['id']
        self.thumbnailURL = self.data['thumbnail_url']
        try:    
            self.clipFile = generatorFileNameFromFolderAndName(output_folder, self.mp4Name)
            urllib.request.urlretrieve(self.getdownload_url(), self.clipFile, reporthook=self.dl_progress) 
            print()
        except: 
            print("download failed, yikes")
            sys.stdout.write(sys.exc_info()[0])

    def uploadToYoutube(self, API, description, tags, uploadDate):
        API.uploadVideo(self.clipFile, self.title, description, tags, uploadDate)

    def exportClipData(self, folder):
        file = "{}{}.json".format(folder, self.getid())
        with open(file, 'w') as fp:
            json.dump(self.data, fp)





    def getDownloadURLFromThumbnailURL(self):   
        return "{}.mp4".format(self.thumbnailURL.split('-preview')[0])

    def geturl(self):               return self.data['url']
    def getid(self):                return self.data['id']
    def gettitle(self):             return self.title
    def getview_count(self):        return self.data['view_count']
    def getCreatedAt(self):        return self.data['created_at']
    def getthumbnail_url(self):     return self.data['thumbnail_url']
    def getdownload_url(self):      return self.data['thumbnail_url'].split("-preview")[0] + ".mp4"
    def getClipFile(self):          return self.clipFile
    def getLanguage(self):          return self.data['language']
    def getCreatorName(self):       return self.data['creator_name']
    def getGameID(self):            return self.data['game_id']

    def dl_progress(self, count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write(self.gettitle()+" ["+"-"*percent+"_"*(100-percent)+"]" + "\r")

def generatorFileNameFromFolderAndName(folder, name):
    return '{}{}.mp4'.format(folder, name)

from Youtube import Youtube
from Twitch import Twitch
import argparse
import os
from pathlib import Path

VERSION = 3.1
FOLDERS = ["/videos/", "/auth/", "/assets/", "/videos/assets", "/videos/clips", "/videos/prepstage", "/videos/uploaded_clips", "/clipData/"]
FILES = ["/auth/auth.json", "/auth/client_secrets.json", "/assets/categories.json", "/assets/descripton.txt"]
CLIPS_FOLDER = './videos/clips/'
PREP_STAGE = './videos/prepstage/'

parser = argparse.ArgumentParser(prog='scorchai', description='Uses scorchai to process videos')

parser.add_argument('-g', '--generate', action='store_true', help='Generate when no clip is found, doesnt do anything on its own')
parser.add_argument('-u', '--upload', action='store_true', help='Upload clip')
parser.add_argument('-c', '--compile', type=int, help='Compile clips', default=0)
parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(VERSION))

args = parser.parse_args()

class ScorchAI:
    def __init__(self, args): 
        self.youtube = Youtube()
        self.twitch = Twitch()

    def runAI(self):
        self.compile(args.compile)
        if args.upload:  
            self.youtube.uploadClip(args.generate)
    
    def compile(self, compileAmount):
        if compileAmount > 0:
            self.setupCompile(compileAmount)
            os.system("ffmpeg -y -f concat -safe 0 -i ./videos/prepstage/input.txt -c copy ./videos/uploaded_clips/output.mp4")
            self.uploadCompilation()
            self.afterCompile()
            
    def afterCompile(self):
        self.twitch.cleanFolder(CLIPS_FOLDER)
        self.twitch.cleanFolder(PREP_STAGE)
    
    def uploadCompilation(self):
        video = "./videos/uploaded_clips/output.mp4"
        title = self.generateCompilationTitle()
        tags = ""
        description = "ScorchAI Compilation! \n\nEXPAND ME\n\n "
        bcs = []
        for path, subdirs, files in os.walk(PREP_STAGE):
            for filename in files:
                if filename.endswith(".mp4"):
                    clipID = filename.split(".mp4")[0]
                    bcs.append(self.youtube.getBroadcaster(clipID))
        bcs = list(dict.fromkeys(bcs))
        for bc in bcs:
            description += "Watch {} on https://www.twitch.tv/{} \n".format(bc, bc)
        with open("./assets/description.txt", encoding="utf8") as file:
            description += file.read()
        self.youtube.uploadVideo(video, title, description, tags)

    def generateCompilationTitle(self):
        bcs = []
        for path, subdirs, files in os.walk(PREP_STAGE):
            for filename in files:
                if filename.endswith(".mp4"):
                    clipID = filename.split(".mp4")[0]
                    bcs.append(self.youtube.getBroadcaster(clipID))
        bcs = list(dict.fromkeys(bcs))
        return "{}, {} and {} (ScorchAI Compilation)".format(bcs[0],bcs[1],bcs[2])
    
    def setupCompile(self, amount):
        vidAmount = len(self.getVideos(CLIPS_FOLDER))
        self.twitch.generateClips(amount - vidAmount)

        a = open("./videos/prepstage/input.txt", "w")
        for path, subdirs, files in os.walk(CLIPS_FOLDER):
            for filename in files:
                if filename.endswith(".mp4"):
                    os.system("ffmpeg -y -i ./videos/clips/{} -filter:v fps=60 -vcodec libx264 -ar 44100 -preset ultrafast ./videos/prepstage/{}".format(filename, filename))
                    a.write("file {}\n".format(filename)) 
        a.close()

    def getVideos(self, folder):
        videos = os.listdir(folder)
        for i in range(len(videos)):
            videos[i] = videos[i].split(".mp4")[0]
        return videos




scai = ScorchAI(args)
scai.runAI()
 

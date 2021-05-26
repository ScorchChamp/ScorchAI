from Youtube import Youtube
from Twitch import Twitch
import argparse
import os

VERSION = 2.2

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
        if args.compile > 0:
            self.compile(args.compile)
        if args.upload:  
            self.youtube.uploadClip(args.generate)
    
    def compile(self, compileAmount):
        self.setupCompile(compileAmount)
        os.system("ffmpeg -y -f concat -safe 0 -i ./videos/prepstage/input.txt -c copy ./videos/uploaded_clips/output.mp4")
        self.postCompile()


    def postCompile(self):
        self.twitch.cleanFolder('./videos/clips/')
        self.twitch.cleanFolder('./videos/prepstage/')
        self.uploadCompilation()
    
    def uploadCompilation(self):
        video = "./videos/uploaded_clips/output.mp4"
        title = "AUTOMATED COMPILATION TEST"
        tags = ""
        with open("./assets/description.txt", encoding="utf8") as file:
            description = file.read()
        self.youtube.uploadVideo(video, title, description, tags)

    
    def setupCompile(self, amount):
        vidAmount = len(self.getVideos('./videos/clips/'))
        self.twitch.generateClips(amount - vidAmount)

        a = open("./videos/prepstage/input.txt", "w")
        for path, subdirs, files in os.walk('./videos/clips/'):
            for filename in files:
                if filename.endswith(".mp4"):
                    os.system("ffmpeg -y -i ./videos/clips/{} -filter:v fps=60 -vcodec libx264 -c:a aac -preset ultrafast ./videos/prepstage/{}".format(filename, filename))
                    a.write("file {}\n".format(filename)) 
        a.close()

    def getVideos(self, folder):
        videos = os.listdir(folder)
        for i in range(len(videos)):
            videos[i] = videos[i].split(".mp4")[0]
        return videos




scai = ScorchAI(args)
scai.runAI()
 

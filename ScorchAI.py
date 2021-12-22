import Youtube
import Twitch
import argparse
import os
import shutil

VERSION = 3.1
prog = "scorchai"

FOLDERS = ["/videos/", "/auth/", "/assets/", "/videos/assets", "/videos/clips", "/videos/prepstage", "/videos/uploaded_clips", "/clipData/"]
FILES = ["/auth/auth.json", "/auth/client_secrets.json", "/assets/categories.json", "/assets/descripton.txt"]
CLIPS_FOLDER = './videos/clips/'
PREP_STAGE = './videos/prepstage/'

parser = argparse.ArgumentParser(prog=prog, description='Uses scorchai to process videos')
parser.add_argument('-g', '--generate', action='store_true', help='Generate when no clip is found, doesnt do anything on its own')
parser.add_argument('-u', '--upload', action='store_true', help='Upload clip')
parser.add_argument('-s', '--short', action='store_true', help='Make shorts')
parser.add_argument('-c', '--compile', type=int, help='Compile clips', default=0)
parser.add_argument('-v', '--version', action='version', version=f'{prog} {VERSION}')

args = parser.parse_args()

def runAI():
    compile(args.compile)
    if args.short:
        vidAmount = len(getVideos(CLIPS_FOLDER))
        if vidAmount < 1:
            Twitch.generateClips(1)
        vid = getVideos(CLIPS_FOLDER)[0] + ".mp4"
        newDir = PREP_STAGE+vid
        shutil.move(CLIPS_FOLDER+vid, newDir)
        os.system(f'ffmpeg -i {PREP_STAGE+vid} -vf "pad=iw:2*trunc(iw*16/18):(ow-iw)/2:(oh-ih)/2,setsar=1" -c:a copy {CLIPS_FOLDER+vid}')

    if args.upload:  
        Youtube.uploadClip(args.generate)

def compile(compileAmount):
    if compileAmount > 0:
        setupCompile(compileAmount)
        os.system("ffmpeg -y -f concat -safe 0 -i ./videos/prepstage/input.txt -c copy ./videos/uploaded_clips/output.mp4")
        uploadCompilation()
        afterCompile()
        
def afterCompile():
    Twitch.cleanFolder(CLIPS_FOLDER)
    Twitch.cleanFolder(PREP_STAGE)

def uploadCompilation():
    video = "./videos/uploaded_clips/output.mp4"
    title = generateCompilationTitle()
    tags = ""
    description = "ScorchAI Compilation! \n\nEXPAND ME\n\n "
    bcs = []
    for path, subdirs, files in os.walk(PREP_STAGE):
        for filename in files:
            if filename.endswith(".mp4"):
                clipID = filename.split(".mp4")[0]
                bcs.append(Youtube.getBroadcaster(clipID))
    bcs = list(dict.fromkeys(bcs))
    for bc in bcs:
        description += f"Watch {bc} on https://www.twitch.tv/{bc} \n"
    with open("./assets/description.txt", encoding="utf8") as file:
        description += file.read()
    Youtube.uploadVideo(video, title, description, tags)

def generateCompilationTitle():
    bcs = []
    for path, subdirs, files in os.walk(PREP_STAGE):
        for filename in files:
            if filename.endswith(".mp4"):
                clipID = filename.split(".mp4")[0]
                bcs.append(Youtube.getBroadcaster(clipID))
    bcs = list(dict.fromkeys(bcs))
    return f"{bcs[0]}, {bcs[1]} and {bcs[2]} (ScorchAI Compilation)"

def setupCompile(amount):
    vidAmount = len(getVideos(CLIPS_FOLDER))
    Twitch.generateClips(amount - vidAmount)

    a = open("./videos/prepstage/input.txt", "w")
    for path, subdirs, files in os.walk(CLIPS_FOLDER):
        for filename in files:
            if filename.endswith(".mp4"):
                os.system(f"ffmpeg -y -i ./videos/clips/{filename} -filter:v fps=60 -vcodec libx264 -ar 44100 -preset ultrafast ./videos/prepstage/{filename}")
                a.write(f"file {filename}\n") 
    a.close()

def getVideos(folder):
    videos = os.listdir(folder)
    for i in range(len(videos)):
        videos[i] = videos[i].split(".mp4")[0]
    return videos




runAI()
 

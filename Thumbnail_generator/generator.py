import os
from PIL import Image


GENERATED_FOLDER = "./generated/"

def getBestFrame(file):
    name = file.split(".mp4")[0]
    os.system(f"ffmpeg -y -i {file} -vf 'thumbnail' -frames:v 1 {GENERATED_FOLDER}{name}.png")

def putOverlayOverImage(file, overlay_file):
    background = Image.open(file)
    foreground = Image.open(overlay_file)

    background.paste(foreground, (0, 0), foreground)
    background.save(file)

def putMinecraftSkinsOverImage(file, skins):
    background = Image.open(file)
    for skin in skins:
        foreground = Image.open(skin)
        background.paste(foreground, (0, 0), foreground)
    background.save(file)



def generateThumbnail(file):
    name = file.split(".mp4")[0]
    getBestFrame(file)
    putOverlayOverImage(f"{GENERATED_FOLDER}{name}.png", "./overlays/overlay.png")
    putMinecraftSkinsOverImage(f"{GENERATED_FOLDER}{name}.png", ["./overlays/Tubbo.png"])







generateThumbnail("BadSuaveWrenRlyTho-cOvMsUZRdkXNQnYf.mp4")
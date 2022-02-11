import os
from PIL import Image, ImageFont, ImageDraw
import json

GENERATED_FOLDER = "./generated/"


    


def putMinecraftSkinsOverImage(file, skins):
    background = Image.open(file)
    for skin in skins:
        foreground = Image.open(skin)
        background.paste(foreground, (0, 0), foreground)
    background.save(file)



def generateThumbnail(file):
    with open("data.json", "r") as f:
        data = json.load(f)['channel1']
        overlay = data['overlay']
        name = file.split(".mp4")[0]
        font = data['font']
        font_size = data['font_size']
        font_color = data['font_color']
        getBestFrame(file)

        putOverlayOverImage(f"{GENERATED_FOLDER}{name}.png", f"./overlays/{overlay}.png")
        putTextOverImage(f"{GENERATED_FOLDER}{name}.png", "This is a test!", font, font_size, font_color)
        # putMinecraftSkinsOverImage(f"{GENERATED_FOLDER}{name}.png", ["./overlays/Tubbo.png"])







generateThumbnail("FuriousMistyMousePartyTime.mp4")
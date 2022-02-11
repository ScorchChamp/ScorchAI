import os
from PIL import Image, ImageFont, ImageDraw



class ThumbnailGenerator:

    def generateBackground(self, file: str = None, *, output_folder: str = "./generated_frames/"):
        os.mkdir(output_folder)
        name = file.split(".mp4")[0]
        os.system(f"ffmpeg -y -i {file} -vf 'thumbnail' -frames:v 1 {output_folder}{name}.png")

    def layerImages(self, background: str, **layers):
        image = Image.open(background)
        for layer in layers:
            foreground = Image.open(layer)
            background.paste(foreground, (0, 0), foreground)
        image.save(background)

    def putTextOverImage(self, file, text, font, font_size, font_color):
        image = Image.open(file)
        w, h = image.size
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font, font_size)
        fw, fh = font.getsize(text)        
        draw.text(((w-fw)/2, 50),text, font_color,font=font, align="center")
        image.save(file)



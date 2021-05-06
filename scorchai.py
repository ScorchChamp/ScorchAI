from Youtube import Youtube
from Twitch import Twitch
import argparse

VERSION = 2.2

parser = argparse.ArgumentParser(prog='scorchai', description='Uses scorchai to process videos')

parser.add_argument('-g', '--generate', action='store_true', help='Generate when no clip is found')
parser.add_argument('-u', '--upload', action='store_true', help='Upload clip')
parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(VERSION))

args = parser.parse_args()

youtube = Youtube()
twitch = Twitch()

if args.upload > 0:   
    print("Started uploading clips")
    youtube.uploadClip(args.generate)

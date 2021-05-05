from Youtube import Youtube
from Twitch import Twitch
import argparse

VERSION = 2.0

parser = argparse.ArgumentParser(prog='scorchai', description='Uses scorchai to process videos')

parser.add_argument('-g', '--generate', type=int, help='Amount of clips to be generated', default = 0)
parser.add_argument('-c', '--compile', action='store_true', help='Compile all clips in clips folder')
parser.add_argument('-d', '--delay',  type=int, help='Hours of delay until upload', default=0)
parser.add_argument('-ua', '--uploadamount', type=int, help='Amount of clips to upload', default=0)
parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(VERSION))
parser.add_argument('-uco', '--uploadcompilation', action='store_true', help='Whether or not to upload compilation')

args = parser.parse_args()

youtube = Youtube()
twitch = Twitch()

if args.generate > 0:
    print("Started generating clips")
    twitch.generateClips(args.generate)

if args.compile == True:
    print("Started compiling clips")
    twitch.compileClips()

if args.uploadamount > 0:   
    print("Started uploading clips")
    youtube.uploadClip(args.uploadamount, args.delay)

if args.uploadcompilation:
    youtube.uploadCompilation(args.delay)
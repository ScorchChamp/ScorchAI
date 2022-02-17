import argparse
from sqlite3 import paramstyle
import APIConnector

VERSION = 3.1
PROGRAM_NAME = "ScorchAI"

parser = argparse.ArgumentParser(prog=PROGRAM_NAME, description='Uses scorchai to process videos')
parser.add_argument('-s', '--short', action='store_true', help='Make shorts')
parser.add_argument('-c', '--compile', type=int, help='Compile clips', default=0)
parser.add_argument('-ch', '--channel', type=str)
parser.add_argument('-v', '--version', action='version', version=f'{PROGRAM_NAME}v{VERSION}')

args = parser.parse_args()
short = args.short
compile = args.compile

channel = args.channel
if not channel: raise Exception("No channel ID given!")

channel_data = APIConnector.getChannelData(Channel_ID=channel)
categories = APIConnector.getCategories(Channel_ID=channel)

index = 0
next_clip = None
while not next_clip and index < len(categories):
    category = categories[index]
    valid_clips = APIConnector.getNextClip(Channel_ID=channel, game_id=category['game_id'], broadcaster_id=category['Broadcaster_id'])
    if valid_clips: 
        for clip in valid_clips:
            if clip['Viewcount'] < category['Minimum_views']: continue
            next_clip = clip
    index += 1


print(next_clip)

APIConnector.insertUpload(next_clip['Clip_ID'], channel)
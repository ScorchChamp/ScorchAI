import os.path
import DatabaseConnector as db
import Twitch
import YoutubeAPI

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class ScorchAI:
    version = "1.5.2"
    name = "ScorchAI"

    def __init__(self):
        self.database_file = os.path.join(BASE_DIR, "database.db")
        self.twitch = Twitch.Twitch()
        self.twitch.refreshAllCategories()


    def uploadClip(self, channelID: str, *, amount: int = 1):
        for i in range(0, amount):
            data = self.twitch.getFirstValidClip(channelID)
            id = data[0]
            title = data[1]
            tags = self.twitch.db.selectTags(channelID=channelID)
            description = self.twitch.db.selectChannels(channelID=channelID)[0][2]
            tags.append([title, id, channelID])
            clip_file = self.twitch.downloadClip(channelID=channelID, clipID=id)
            YoutubeAPI.uploadVideo(file=clip_file, title=title, description=description, tags=tags, channel=channelID)

                

scai = ScorchAI()

scai.uploadClip(channelID='UC37Fy80jwUvBQVDya-xcNZQ', amount=1)
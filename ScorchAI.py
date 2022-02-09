import os.path
import DatabaseConnector as db
import Twitch

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class ScorchAI:
    version = "1.5.2"
    name = "ScorchAI"

    def __init__(self):
        self.database_file = os.path.join(BASE_DIR, "database.db")
        self.twitch = Twitch.Twitch()
        self.twitch.refreshAllCategories()


    def uploadClip(self, channelID: str, *, amount: int = 1, clipID: str = None):
        if clipID: 
            id = self.twitch.db.selectClips(clipID=clipID)[0]
            self.twitch.downloadClip(channelID=channelID, clipID=id)
        else:
            for i in range(0, amount):
                id = self.twitch.getFirstValidClip(channelID)[0]
                self.twitch.downloadClip(channelID=channelID, clipID=id)

                

scai = ScorchAI()

scai.uploadClip(channelID='UC37Fy80jwUvBQVDya-xcNZQ')
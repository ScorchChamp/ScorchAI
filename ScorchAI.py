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

    # print(db.selectNotUploadedClip(channelID='3rfsdf45y5gd'))

scai = ScorchAI()
from numpy import clip
import DatabaseConnector as db
import os
from TwitchAPI import TwitchAPI

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Twitch:
    database_file = os.path.join(BASE_DIR, "database.db")
    twitch_api = None

    def __init__(self):
        self.db = db.DatabaseConnector(self.database_file)
        self.twitch_api = TwitchAPI()

    def refreshAllCategories(self):
        for category in self.db.selectCategories():
            self.refreshClipData(game_id = category[3], broadcaster_id = category[4])


    def refreshClipData(self, *, broadcaster_id: int = None, game_id: str = None):
        if game_id is not None: self.refreshGameClips(game_id)
        if broadcaster_id is not None: self.refreshBroadcasterClips(broadcaster_id)

    def refreshGameClips(self, game_id: str):
        data = self.twitch_api.getClipsList({"game_id": game_id})
        if data:
            for clip in data:
                self.saveClipData(clip)

    def refreshBroadcasterClips(self, broadcaster_id: int):
        data = self.twitch_api.getClipsList({"broadcaster_id": broadcaster_id})
        for clip in data: self.saveClipData(clip)

    def saveUserData(self, user_id: int):
        if len(self.db.selectUsers(userID=user_id)) == 0:
            user_data = self.twitch_api.getUserData(user_id=user_id)
            for user in user_data:
                if 'email' in user: email = user['email']
                else: email = ''
                self.db.insertNewUser(user['id'], user['login'], user['display_name'], user['type'], user['broadcaster_type'], user['description'], user['profile_image_url'], user['offline_image_url'], user['view_count'], email, user['created_at'])

    def saveGameData(self, game_id: int):
        if len(self.db.selectGames(gameID=game_id)) == 0:
            game_data = self.twitch_api.getGameData(game_id=game_id)
            for game in game_data:
                self.db.insertNewGame(game['id'], game['name'], game['box_art_url'])

    def saveClipData(self, data: dict):
        if len(self.db.selectClips(clipID=data['id'])) == 0:
            self.saveUserData(data['broadcaster_id'])
            self.saveUserData(data['creator_id'])
            self.saveGameData(data['game_id'])
            self.db.insertNewBroadcaster(data['broadcaster_id'], data['broadcaster_name'])
            self.db.insertNewClip(
                data['id'],
                data['title'],
                data['broadcaster_id'],
                data['url'],
                data['embed_url'],
                data['creator_id'],
                data['video_id'],
                data['game_id'],
                data['language'],
                data['view_count'],
                data['created_at'],
                data['thumbnail_url'],
                data['duration'],
                data['thumbnail_url'].split("-preview")[0] + ".mp4"
            )

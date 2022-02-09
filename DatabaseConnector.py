import sqlite3 as sql

class DatabaseConnector:
    db_file = '%'
    connection = '%'
    query_folder = "./queries/"

    def __init__(self, db_file: str):
        self.db_file = db_file
        self.setupDatabase()

    def setupDatabase(self):
        with open(self.query_folder + 'Setup.sql','r') as setup: query = setup.read()
        for q in query.split(";"): self.executeQuery(q)

    def executeQuery(self, query: str, values: dict = []):
        try:
            with sql.connect(self.db_file) as db:
                cursor = db.cursor()
                cursor.execute(query, values)
                db.commit()
            return cursor.fetchall()
        except Exception as e:
            # print(e)
            pass

    def getQuery(self, queryName):
        with open(self.query_folder + queryName + '.sql','r') as setup: 
            query = setup.read()
        return query



    # INSERTS/SELECTS:
        
    def insertNewUser(self, userID: int, login: str, display_name: str, type: str, broadcaster_type: str, description: str, profile_image_url: str, offline_image_url: str, view_count: str, email: str, created_at: str):
        self.executeQuery(self.getQuery("insertNewUser"), (userID, login, display_name, type, broadcaster_type, description, profile_image_url, offline_image_url, view_count, email, created_at))

    def insertNewChannel(self, channelID: int, channelDisplayName: str, channelDescription: str):
        self.executeQuery(self.getQuery("insertNewChannel"), (channelID, channelDisplayName, channelDescription))

    def insertNewTag(self, channelID: int, tag: str):
        self.executeQuery(self.getQuery("insertNewTag"), (channelID, tag))

    def insertNewGame(self, gameID: int, gameName: str, box_art_url: str):
        self.executeQuery(self.getQuery("insertNewGame"), (gameID, gameName, box_art_url))

    def insertNewClip(self, clipID, Title, Broadcaster_id, Url, Embed_url, Creator_id, Video_id, Game_id, Language, Viewcount, Created_at, Thumbnail_url, Duration, Download_URL):
        self.executeQuery(self.getQuery("insertNewClip"), (clipID, Title, Broadcaster_id, Url, Embed_url, Creator_id, Video_id, Game_id, Language, Viewcount, Created_at, Thumbnail_url, Duration, Download_URL))

    def insertNewCategory(self, channelID, priority, minimum_views, gameID, broadcasterID):
        self.executeQuery(self.getQuery("insertNewCategory"), (channelID, priority, minimum_views, gameID, broadcasterID))

    def insertNewClipUploadedToChannel(self, clipID, channelID, upload_date):
        self.executeQuery(self.getQuery("insertNewClipUploadedToChannel"), (clipID, channelID, upload_date))

    def insertNewBroadcaster(self, broadcasterID, broadcasterName):
        self.executeQuery(self.getQuery("insertNewBroadcaster"), (broadcasterID, broadcasterName))


    def selectUsers(self, *, userID: int = '%', username: str = "%"):
        return self.executeQuery(self.getQuery("selectUsers"), (userID, username))

    def selectBroadcasters(self, *, broadcasterID: int = '%', broadcaster_name: str = "%"):
        return self.executeQuery(self.getQuery("selectBroadcasters"), (broadcasterID, broadcaster_name))

    def selectChannels(self, ID: int = '%', *, displayname: str = "%", description: str = "%") -> list:
        return self.executeQuery(self.getQuery("selectChannels"), (ID, displayname, description))

    def selectTags(self, *, channelID: str = "%", tag: str = "%") -> list:
        return self.executeQuery(self.getQuery("selectTags"), (channelID, tag))

    def selectGames(self, *, gameID: str = "%", gameName: str = "%") -> list:
        return self.executeQuery(self.getQuery("selectGames"), (gameName,gameID))

    def selectClips(self, *, clipID: str = "%", Title: str = "%", Broadcaster_id: int = '%', Url: str = "%", Embed_url: str = "%", Creator_id: int = '%', Video_id: int = '%', Game_id: int = '%', Language: str = "%", Viewcount: int = '%', Created_at: str = "%", Thumbnail_url: str = "%", Duration: int = '%') -> list:
        return self.executeQuery(self.getQuery("selectClips"), (clipID, Broadcaster_id, Creator_id, Video_id, Game_id, Language))

    def selectCategories(self, *, channelID: str = "%", priority: int = '%') -> list:
        return self.executeQuery(self.getQuery("selectCategories"), (channelID, priority))

    def selectClipsUploadedToChannel(self, *, clipID: str = "%", channelID: str = "%") -> list:
        return self.executeQuery(self.getQuery("selectClipsUploadedToChannel"), (clipID, channelID))

    def selectNotUploadedClip(self, *, channelID: str = "%") -> list:
        return self.executeQuery(self.getQuery("selectNotUploadedClip"), (channelID, channelID))

    def getClipDownloadURL(self, ClipID: str):
        return self.executeQuery("SELECT Download_URL FROM clips WHERE Clip_ID LIKE ?", (ClipID,))[0][0]

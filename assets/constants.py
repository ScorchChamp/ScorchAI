#GENERAL FOLDER CONSTANTS
CLIPS_LINK = "https://api.twitch.tv/helix/clips"

CLIPS_FOLDER =       "./clips/"
UPLOADED_FOLDER =    "./clips/uploaded/"
CLIP_DATA_FOLDER =   "./clipData/"

TAGS_FILE =          "./assets/tags.txt"
AUTH_FILE =          "./assets/auth.json"
CATEGORIES_FILE =    "./assets/categories.json"
DESCRIPTION_FILE =   "./assets/description.txt"
CLIENTSECRETS_FILE = './assets/client_secrets.json'

#API CONSTANTS
API_NAME =    'youtube'
API_VERSION = 'v3'
SCOPES =     ['https://www.googleapis.com/auth/youtube.upload']

#VIDEO STATUS
VIDEO_STATUS = {
    'privacyStatus': 'private',
    'publishAt': "THIS SHOULD NOT BE PRINTED",
    'selfDeclaredMadeForKids': False
}


#ERROR MESSAGES
CLIP_DOWNLOAD_FAILED_MESSAGE = "Download failed, yikes"


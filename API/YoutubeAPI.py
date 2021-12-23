import API.Google
import shutil

CLIPS_FOLDER = './videos/clips/'
PREP_STAGE = './videos/prepstage/'
READY_STAGE = './videos/ready_to_upload/'
UPLOADED_STAGE = './videos/uploaded_clips/'

def uploadVideo(file, title, description, tags):
    new_dir = UPLOADED_STAGE + file.split("/")[-1] + ".mp4"
    shutil.move(file, new_dir)
    API.Google.Upload_Video(getRequestBody(title, description, tags), new_dir)    
            
def upload_thumbnails(thumbnail = False):
    if not thumbnail:
        print("No thumbnail specified, skipping upload")

def getRequestBody(title, description, tags):
    return {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': 24 
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        },
        'notifySubscribers': True
    }
import Google
import shutil

CLIPS_FOLDER = './videos/clips/'
PREP_STAGE = './videos/prepstage/'
READY_STAGE = './videos/ready_to_upload/'
UPLOADED_STAGE = './videos/uploaded_clips/'

def uploadVideo(file, title, description, tags, channel):
    request_body = getRequestBody(title=title, description=description, tags=tags)
    video_id = Google.Upload_Video(request_body, file, channel)
    upload_thumbnails()    
            
def upload_thumbnails(*, video_id: str = ""):
    if not video_id:
        print("No thumbnail specified, skipping upload")

def getRequestBody(*, title: str = "", description: str = "", tags: dict = []):
    return {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': 24 
        },
        'status': {
            'privacyStatus': 'private',
            'selfDeclaredMadeForKids': False
        },
        'notifySubscribers': True
    }
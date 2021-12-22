import API.Google

def uploadVideo(file, title, description, tags):
    API.Google.Upload_Video(getRequestBody(title, description, tags), file)    
            
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
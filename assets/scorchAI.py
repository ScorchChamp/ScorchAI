from assets import constants

def generateDescription(clipData):
    description = '#{} '.format(clipData['broadcaster_name'])
    with open(constants.DESCRIPTION_FILE, encoding="utf8") as file:
        description += file.read()
    description += '\n\
        VideoID: {}\n\
        Created At: {}\n\
        Created By: {}\n\
        View count on Twitch: {}\n\
        Game ID: {}\n\
        Download Clip at: {}\n'.format(
            clipData['id'],
            clipData['created_at'],
            clipData['creator_name'], 
            clipData['view_count'], 
            clipData['game_id'], 
            clipData['thumbnail_url'].split("-preview")[0] + ".mp4"
        )

def generateTags(clipData):
    tags = clipData['broadcaster_name'] + ", "
    with open('./assets/tags.txt', encoding="utf8") as file:
        tags += file.read()
    return tags

def dl_progress(self, count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write(self.gettitle()+" ["+"-"*percent+"_"*(100-percent)+"]" + "\r")

    
def generatorFileNameFromFolderAndName(folder, name):
    return '{}{}.mp4'.format(folder, name)

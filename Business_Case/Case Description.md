
## Brief description
ScorchLLC wants to have an application that makes it able to automatically upload Twitch clips to Youtube.

## Specifications
### API connections
The owner should be able to log into multiple different youtube channels where clips should be uploaded. The owner can decide how often per hour it should upload, and which games/broadcasters should be uploaded. Every category of games/broadcasters should include a minimum amount of views and language which the owner can pick.


### Thumbnail
Every youtube-channel should have a thumbnail-overlay which can be changed by the owner. The thumbnail should include the clip-title with a max of 10 characters. The thumbnail should include a custom overlay depending on the broadcaster whom the clip is from.

### AI
The priority of broadcasters/games the application uploads should dynamically changed based on the views on youtube. 
Likewise, the thumbnail could change dynamically based on click-through-rate.

### Database
Whenever a clip is uploaded, the data should be uploaded to the database. This data should be connected to which youtube-channel it has been uploaded.

### API
The database should have an API which makes it easier to insert and get data.
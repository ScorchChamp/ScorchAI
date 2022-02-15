

CREATE TABLE users (
    User_ID int,
    login varchar(100),
    display_name varchar(100),
    type varchar(100),
    broadcaster_type varchar(100),
    Description varchar(150),
    profile_image_url varchar(150),
    offline_image_url varchar(150),
    view_count varchar(100),
    email varchar(100),
    created_at datetime,

    PRIMARY KEY (User_ID)
);

CREATE TABLE Channels (
    Channel_ID varchar(100),
    Channel_Displayname varchar(100),
    Description varchar(1000),

    PRIMARY KEY (Channel_ID)
);

CREATE TABLE Tags (
    Channel_ID varchar(100),
    Tag varchar(20),

    PRIMARY KEY (Channel_ID, Tag),
    FOREIGN KEY (Channel_ID) REFERENCES Channels(Channel_ID)
);

CREATE TABLE Games (
    Game_ID varchar(50),
    name varchar(50),
    box_art_url varchar(100),

    PRIMARY KEY (Game_ID)
);

CREATE TABLE Categories (
    Channel_ID varchar(100),
    Priority int,
    Minimum_views int,
    game_id varchar(50),
    Broadcaster_id int,

    PRIMARY KEY (Channel_ID, Priority),
    FOREIGN KEY (game_id) REFERENCES Games(Game_ID),
    FOREIGN KEY (Broadcaster_id) REFERENCES users(User_ID),
    CHECK (
        (game_id IS NOT NULL OR Broadcaster_id IS NOT NULL)
        AND NOT (game_id IS NOT NULL AND Broadcaster_id IS NOT NULL)
    )
);

CREATE TABLE Clips_Uploaded_To_Channel (
    Clip_ID varchar(100),
    Channel_ID varchar(100),
    upload_date datetime,

    PRIMARY KEY (Clip_ID, Channel_ID),
    FOREIGN KEY (Clip_ID) REFERENCES Clips(Clip_ID),
    FOREIGN KEY (Channel_ID) REFERENCES Channels(Channel_ID)
);

CREATE TABLE Clips (
    Clip_ID varchar(100),
    Title varchar(100),
    Broadcaster_id int,
    Url varchar(100),
    Embed_url varchar(100),
    Creator_id int,
    Video_id int,
    Game_id varchar(50),
    Language varchar(10),
    Viewcount int,
    Created_at datetime,
    Thumbnail_url varchar(150),
    Duration int,
    Download_URL varchar(200),

    PRIMARY KEY (Clip_ID)
    FOREIGN KEY (Game_id) REFERENCES Games(Game_ID),
    FOREIGN KEY (Creator_id) REFERENCES users(User_ID),
    FOREIGN KEY (Broadcaster_id) REFERENCES users(User_ID)
);
INSERT INTO Channels VALUES 
    ('UC37Fy80jwUvBQVDya-xcNZQ', 'Bedrock' , 'Test Description!'),
    ('abcdefg', 'tester' , 'Test 22222222222222!');
INSERT INTO Games VALUES 
    (743, 'Chess', 'some-url');
INSERT INTO Users VALUES 
    (40934651, 'testuser', 'Test User', 'Tester', 'Partner', 'I am a test account!', NULL, NULL, 100, 'test@scorchchamp.com', '15-02-2022');
INSERT INTO Categories VALUES 
    ('UC37Fy80jwUvBQVDya-xcNZQ', 1, 10, NULL, 40934651),
    ('UC37Fy80jwUvBQVDya-xcNZQ', 2, 10, 743, NULL),
    ('abcdefg', 1, 10, 743, NULL),
    ('abcdefg', 2, 10, NULL, 40934651);
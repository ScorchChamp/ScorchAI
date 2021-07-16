CREATE TABLE youtube_channel (
	channel_id varchar,
	channel_name varchar,
	pickle_file varchar,
	PRIMARY KEY(channel_id)
);
CREATE TABLE twitch_channel (
	channel_id int,
	channel_name varchar UNIQUE,
	PRIMARY KEY(channel_id)
);
CREATE TABLE twitch_game (
	game_id int,
	game_name varchar UNIQUE,
	PRIMARY KEY(game_id)
);
CREATE TABLE API_SECRET (
	channel_id int UNIQUE,
	client_id varchar UNIQUE,
	client_secret varchar,
	redirect_uri varchar,
	OAUTH varchar UNIQUE,
	refresh_token varchar UNIQUE,
	PRIMARY KEY(channel_id)
);
CREATE TABLE descriptions (
	channel_id varchar,
	desc_tag varchar, -- Identifier for description (able to switch between descriptions)
	description varchar, 
	PRIMARY KEY(channel_id, desc_tag),
	FOREIGN KEY (channel_id) REFERENCES youtube_channel(channel_id)
);
CREATE TABLE categories (
	youtube_channel_id varchar,
	prio int,
	min_views int,
	game_id int,
	twitch_channel_id int, 
	primary key(youtube_channel_id, prio),
	FOREIGN KEY (youtube_channel_ID) REFERENCES youtube_channel(channel_id),
	FOREIGN KEY (game_id) REFERENCES twitch_game(game_id),
	FOREIGN KEY (twitch_channel_id) REFERENCES twitch_channel(channel_id),
	CHECK (game_id IS NOT NULL OR twitch_channel_id IS NOT NULL)
);

INSERT INTO twitch_channel VALUES (1, "test")
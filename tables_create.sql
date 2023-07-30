create table if not exists request_data (
	id serial primary key,
	telegram_id varchar(40) UNIQUE,
	latitude float DEFAULT 32.086944,
	longitude float DEFAULT 34.801483,
	radius int DEFAULT 500,
	balcony bool  DEFAULT TRUE,
	min_square int DEFAULT 30,
    max_square int DEFAULT 200
	);



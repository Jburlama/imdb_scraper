CREATE TABLE IF NOT EXISTS "movies" (
	"title" TEXT UNIQUE,
	"release_date" TEXT
) strict;


CREATE TABLE IF NOT EXISTS "genres" (
	"genre" TEXT UNIQUE
) strict;


CREATE TABLE IF NOT EXISTS "stars" (
	"name" TEXT UNIQUE
) strict;


CREATE TABLE IF NOT EXISTS "movie_genres" (
	"movie_title" TEXT,
	"genre" TEXT,
	PRIMARY KEY("movie_title", "genre"),
	FOREIGN KEY("movie_title")
		REFERENCES "movies"("title")
			ON DELETE CASCADE
			ON UPDATE NO ACTION,
	FOREIGN KEY("genre")
		REFERENCES "genres"("genre")
			ON DELETE CASCADE
			ON UPDATE NO ACTION
) strict;


CREATE TABLE IF NOT EXISTS "movie_stars" (
	"movie_title" TEXT,
	"star_name" TEXT,
	PRIMARY KEY("movie_title", "star_name"),
	FOREIGN KEY("movie_title")
		REFERENCES "movies"("title")
			ON DELETE CASCADE
			ON UPDATE NO ACTION,
	FOREIGN KEY("star_name")
		REFERENCES "stars"("name")
			ON DELETE CASCADE
			ON UPDATE NO ACTION
) strict;

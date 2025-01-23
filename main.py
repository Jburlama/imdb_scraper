from curl_cffi import requests
from bs4 import BeautifulSoup, SoupStrainer
from tqdm import tqdm
import sqlite3


def main():
	movies = scrapemovies()
	add_to_db(movies)


def add_to_db(movies):
	conn = sqlite3.connect("imdb.db")
	
	pbar = tqdm(total=len(movies), desc="Adding to db")
	for movie in movies:
		try:
			conn.execute("INSERT INTO movies('title', 'release_date') VALUES (?, ?)",
						(movie["title"], movie["date"]))
		except sqlite3.IntegrityError:
			pass

		for genre in movie["genres"]:
			try:
				conn.execute("INSERT INTO movie_genres('movie_title', 'genre') VALUES (?, ?)",
							(movie["title"], genre))
			except sqlite3.IntegrityError:
				pass

		for star in movie["stars"]:
			try:
				conn.execute("INSERT INTO stars('name') VALUES (?)",
							 (star,))
			except sqlite3.IntegrityError:
				pass
			try:
				conn.execute("INSERT INTO movie_stars('movie_title', 'star_name') VALUES (?, ?)",
							(movie["title"], star))
			except sqlite3.IntegrityError:
				pass
		pbar.update(1)

	conn.commit()
	conn.close()
	pbar.close()
	print("Added to imdb.db")


def scrapemovies():
	url = "https://www.imdb.com/calendar/?region=US&type=MOVIE&ref_=rlm"
	r = requests.get(url, impersonate="chrome")
	soup = BeautifulSoup(r.text, "lxml", parse_only=SoupStrainer("section", {"class":"ipc-page-section ipc-page-section--base"}))
	
	film_genres = [
		"Action",
		"Adventure",
		"Animation",
		"Biography",
		"Comedy",
		"Crime",
		"Documentary",
		"Drama",
		"Family",
		"Fantasy",
		"History",
		"Horror",
		"Music",
		"Musical",
		"Mystery",
		"Romance",
		"Sci-Fi",
		"Sport",
		"Thriller",
		"War"
	]
	
	items = []
	articles = soup.find_all("article", {"class": "sc-54f5ef07-1 EOMYO"})
	
	pbar = tqdm(total=len(articles), desc="Scraping ...")
	for article in articles:
		date = article.find("h3", {"class": "ipc-title__text"}).get_text(strip=True)
		movies = article.find_all("li", {"class": "ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click sc-48869e4f-0 dJwARK"})
		for movie in movies:
			title = movie.find("a", {"class": "ipc-metadata-list-summary-item__t"}).get_text(strip=True)
			title = title[:len(title) - 7]
			genres = []
			stars = []
			genresli = movie.find_all("li", {"class": "ipc-inline-list__item"})
			for genre in genresli:
				g = genre.get_text(strip=True)
				if g in film_genres:
					genres.append(g)
				else:
					stars.append(g)
			items.append({
				"title": title,
				"genres": genres,
				"stars": stars,
				"date": format_date(date)
			})
		pbar.update(1)
	pbar.close()
	print("Scrape done")
	return items


def format_date(date):
	months = {
		"Jan": 1,
		"Feb": 2,
		"Mar": 3,
		"Apr": 4,
		"May": 5,
		"Jun": 6,
		"Jul": 7,
		"Aug": 8,
		"Sep": 9,
		"Oct": 10,
		"Nov": 11,
		"Dec": 12
	}
	day, year = date.split(",")
	month = str(months[date.split(" ")[0]])
	if len(month) == 1:
		month = "0" + month
	day = day.split(" ")[-1]

	new_format = f"{year}-{month}-{day}".strip()
	return (new_format)
	

if __name__=="__main__":
	main()

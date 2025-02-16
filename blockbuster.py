#TODO: Get Showing Movies
#TODO: Get Upcoming Movies
#TODO: Get Studio
#TODO: Get Director
import requests

API_KEY = '84d9e59d25c552dc703b703442e9f457'


def acceptable_genres(genre_ids):
    acceptable_genre_ids = [28, 12, 16, 35, 14, 878]
    if any(genre_id in acceptable_genre_ids for genre_id in genre_ids):
        return True
    else:
        return False

 
def genre_from_id(genre_id):
    genres = {
        28: "Action",
        12: "Adventure",
        16: "Animation",
        35: "Comedy",
        80: "Crime",
        99: "Documentary",
        18: "Drama",
        10751: "Family",
        14: "Fantasy",
        36: "History",
        27: "Horror",
        10402: "Music",
        9648: "Mystery",
        10749: "Romance",
        878: "Science Fiction",
        10770: "TV Movie",
        53: "Thriller",
        10752: "War",
        37: "Western"
    }

    return genres[genre_id]

def get_poster_url(poster_path, size="w500"):
    base_url = "https://image.tmdb.org/t/p"
    return f"{base_url}/{size}{poster_path}"

def dict_of_movies(data):
    movies = {}
    for movie in data['results']:
        acceptable_genre = acceptable_genres(movie['genre_ids'])

        if movie['original_language'] == 'en' and acceptable_genre:
            main_genre = genre_from_id(movie['genre_ids'][0])
            thumbnail = get_poster_url(movie["poster_path"])

            try:
                secondary_genre = genre_from_id(movie['genre_ids'][1])
            except IndexError:
                secondary_genre = "N/A"

            movies[movie['title']] = {
                'title': movie['title'],
                'release_date': movie['release_date'],
                'main_genre': main_genre,
                'secondary_genre': secondary_genre,
                'overview': movie['overview'],
                'thumbnail': thumbnail
            }

    return movies

def get_upcoming_movies(date, future_date):
    params = {
        'api_key': API_KEY,
        'primary_release_date.gte': date,
        'primary_release_date.lte': future_date,
        'region': 'ZA'
    }

    url = f"https://api.themoviedb.org/3/movie/upcoming?api_key={API_KEY}"
    response = requests.get(url, params=params)
    data = response.json()

    return dict_of_movies(data)

# #CURRENTLY SHOWING
def now_showing():
    params = {
        'api_key': API_KEY,
        'region': 'ZA'
    }

    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={API_KEY}"
    response = requests.get(url, params=params)
    data = response.json()

    return dict_of_movies(data)


if __name__ == "__main__":
    import date
    full_date = date.get_today_date()[0]
    day = date.get_today_date()[2]

    if day == 6:
        print("Sunday") #CHANGE THIS!!!
        print(get_upcoming_movies(full_date, date.get_future_date(30)))
        print("Now Showing")
        print(now_showing())
import http.client
import json

import date

def get_songs(week) -> list:
    conn = http.client.HTTPSConnection("billboard2.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "api",
        'x-rapidapi-host': "billboard2.p.rapidapi.com"
    }

    conn.request("GET", f"/hot_100?date={week}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    chart_data = json.loads(data.decode("utf-8"))

    sorted_songs = sorted(chart_data, key=lambda x: int(x['rank']))
    top_ten_songs = sorted_songs[:10]

    return top_ten_songs


# import json
# with open('songs.json') as file:
#     data = json.load(file)
#     # print(data)

# chart_data = json.loads(data.decode("utf-8"))

# sorted_songs = sorted(chart_data, key=lambda x: int(x['rank']))
# top_ten_songs = sorted_songs[:10]

def dict_of_songs(data) -> dict:
    songs = {}
    for song in data:
        songs[song['title']] = {
            'title': song['title'],
            'artist': song['artist'],
            'rank': song['rank'],
            'thumbnail': song['image']
        }

    return songs


if __name__ == "__main__":
    week = date.get_future_date(-2)
    top_ten_songs = get_songs(week)
    print(dict_of_songs(top_ten_songs))
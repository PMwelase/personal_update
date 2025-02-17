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


def dict_of_songs(data) -> dict:
    songs = {}
    if len(data) == 10:
        for song in data:
            songs[song['title']] = {
                'title': song['title'],
                'artist': song['artist'],
                'rank': song['rank'],
                'thumbnail': song['image']
            }

        return songs
    return None


def main():
    week = date.get_future_date(-2)
    top_songs = {}
    
    songs = get_songs(week)
    top_songs = dict_of_songs(songs)

    if top_songs != None:
        return top_songs
    else:
        songs = {}
        with open('songs.json') as file:
            data = json.load(file)
            print(data)
        
        sorted_songs = sorted(data, key=lambda x: int(x['rank']))
        top_ten_songs = sorted_songs[:10]

        songs = dict_of_songs(top_ten_songs)
    
    return songs


    

if __name__ == "__main__":
    print(main())
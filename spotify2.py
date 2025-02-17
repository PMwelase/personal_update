import html
import json
import urllib.parse

def clean_text(text):
    """Clean text by unescaping HTML entities and removing featuring artists."""
    text = html.unescape(text)
    if ' Featuring ' in text:
        text = text.split(' Featuring ')[0]
    if ' & ' in text:
        text = text.split(' & ')[0]
    return text.strip()

def generate_spotify_search_url(title, artist):
    """Generate a Spotify search URL for a track."""
    query = f"{clean_text(title)} {clean_text(artist)}"
    encoded_query = urllib.parse.quote(query)
    return f"spotify:search:{encoded_query}"

def create_playlist_link(songs_data, playlist_name="Billboard Top Tracks"):
    """
    Create a Spotify playlist creation link with pre-filled search queries.
    
    Args:
        songs_data (dict): Dictionary of songs with title and artist
        playlist_name (str): Name for the playlist
    
    Returns:
        str: Spotify URL that will open the playlist creation page
    """
    # Encode playlist name
    encoded_name = urllib.parse.quote(playlist_name)
    
    # Generate search URIs for each track
    search_uris = []
    for song in songs_data.values():
        search_uri = generate_spotify_search_url(song['title'], song['artist'])
        search_uris.append(search_uri)
    
    # Join URIs with commas
    uri_list = ','.join(search_uris)
    
    # Create the full URL
    base_url = "https://open.spotify.com/search/"
    playlist_url = f"{base_url}{encoded_name}?go=1&uri={urllib.parse.quote(uri_list)}"
    
    return playlist_url

def main():
    try:
        # Load and process the songs
        print("Loading JSON file...")
        with open('songs.json') as file:
            data = json.load(file)
        
        sorted_songs = sorted(data, key=lambda x: int(x['rank']))
        top_ten_songs = sorted_songs[:10]
        
        # Convert to dictionary format
        songs = {}
        for song in top_ten_songs:
            songs[song['title']] = {
                'title': song['title'],
                'artist': song['artist'],
                'rank': song['rank']
            }
        
        # Generate the playlist link
        playlist_url = create_playlist_link(
            songs,
            playlist_name="Billboard Top Tracks 2025"
        )
        
        print("\nShare this link to create the playlist:")
        print(playlist_url)
        print("\nWhen users click this link:")
        print("1. It will open Spotify in their browser")
        print("2. They'll see all the songs ready to be added")
        print("3. They can click 'Add to Playlist' to create a new playlist or add to existing one")
        
    except FileNotFoundError:
        print("Error: songs.json file not found")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in songs.json: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

    return playlist_url

if __name__ == "__main__":
    main()
    